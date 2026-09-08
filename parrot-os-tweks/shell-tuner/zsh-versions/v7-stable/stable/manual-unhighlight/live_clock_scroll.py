import os

from gi.repository import GLib
import terminatorlib.plugin as plugin


AVAILABLE = ['LiveClockScroll']


class LiveClockScroll(plugin.Plugin):
    capabilities = []

    def __init__(self):
        self.poll_id = GLib.timeout_add(50, self._poll)

        # PTY -> paused state
        self.paused = {}

        # VTE -> connected signal handlers
        self.connected = set()

        # VTE -> mouse button currently held
        self.mouse_pressed = set()

    # =========================================================
    # UNLOAD
    # =========================================================

    def unload(self):
        if self.poll_id:
            GLib.source_remove(self.poll_id)
            self.poll_id = None

    # =========================================================
    # PROC HELPERS
    # =========================================================

    def _read_file(self, path):
        try:
            with open(path, "r") as f:
                return f.read().strip()
        except Exception:
            return None

    def _stat_info(self, pid):
        """
        Read Linux /proc/<pid>/stat.

        Returns:
            {
                "pid": pid,
                "ppid": ppid,
                "pgid": pgid,
                "sid": sid,
                "tty_nr": tty_nr,
                "tpgid": tpgid,
            }

        We deliberately use /proc/<pid>/stat rather than
        /proc/<pid>/fd/0 because the Terminator process runs
        as the normal user while nested sudo/su processes may
        belong to root.
        """

        data = self._read_file(
            f"/proc/{pid}/stat"
        )

        if not data:
            return None

        try:
            # comm is enclosed in parentheses and may itself
            # contain spaces, so locate the final ')' first.
            close = data.rfind(")")

            if close == -1:
                return None

            rest = data[close + 2:].split()

            # After "(comm)", field numbering begins:
            #
            # field 3  = state       -> rest[0]
            # field 4  = ppid        -> rest[1]
            # field 5  = pgrp        -> rest[2]
            # field 6  = session     -> rest[3]
            # field 7  = tty_nr      -> rest[4]
            # field 8  = tpgid       -> rest[5]

            return {
                "pid": int(pid),
                "ppid": int(rest[1]),
                "pgid": int(rest[2]),
                "sid": int(rest[3]),
                "tty_nr": int(rest[4]),
                "tpgid": int(rest[5]),
            }

        except (ValueError, IndexError):
            return None

    def _children(self, pid):
        """
        Read children directly from the kernel's process tree.

        This intentionally avoids scanning every process on the
        machine, which prevents unrelated stale root sessions
        from being mistaken for the current terminal.
        """

        data = self._read_file(
            f"/proc/{pid}/task/{pid}/children"
        )

        if not data:
            return []

        result = []

        for item in data.split():
            try:
                result.append(int(item))
            except ValueError:
                pass

        return result

    # =========================================================
    # PTY NUMBER
    # =========================================================

    def _tty_nr_to_pts(self, tty_nr):
        """
        Convert Linux tty_nr to a /dev/pts/N number.

        For devpts, the device number is encoded as:

            major = tty_nr >> 8
            minor = tty_nr & 0xff

        PTYs use major 136-143.

        The exact minor is enough for the /dev/pts/N naming
        used by the Zsh state files.
        """

        try:
            tty_nr = int(tty_nr)
        except (TypeError, ValueError):
            return None

        if tty_nr == 0:
            return None

        major = (tty_nr >> 8) & 0xff
        minor = tty_nr & 0xff

        # Linux Unix98 PTY slave majors are 136 through 143.
        if 136 <= major <= 143:
            return str((major - 136) * 256 + minor)

        return None

    # =========================================================
    # PROCESS TREE
    # =========================================================

    def _collect_descendants(self, root_pid):
        """
        Return every living descendant of root_pid.

        We follow the actual kernel parent/child relationship,
        so unrelated old root shells elsewhere on the system
        are never included.
        """

        result = []

        queue = [root_pid]
        visited = set()

        while queue:

            pid = queue.pop(0)

            if pid in visited:
                continue

            visited.add(pid)

            info = self._stat_info(pid)

            if info is not None:
                result.append(info)

            for child in self._children(pid):

                if child not in visited:
                    queue.append(child)

        return result

    # =========================================================
    # ACTIVE PTY / SESSION DETECTION
    # =========================================================

    def _terminal_pts(self, terminal):
        """
        Determine which PTY currently contains the active shell.

        Normal shell:

            remac zsh
                |
                +-- pts/8

        Nested sudo/su:

            remac zsh              pts/8
                |
                +-- sudo           pts/8
                    |
                    +-- sudo       pts/12
                        |
                        +-- su     pts/12
                            |
                            +-- root bash pts/12

        The important distinction is the SESSION.

        The original Terminator shell belongs to one session.
        sudo/su can establish a new controlling-terminal session.
        We therefore:

          1. collect only descendants of terminal.pid
          2. group them by session ID
          3. determine which sessions have a real PTY
          4. prefer the deepest/newest descendant session
          5. otherwise fall back to the original PTY

        This avoids reading root-owned /proc/<pid>/fd/0.
        """

        try:
            root_pid = getattr(
                terminal,
                "pid",
                None
            )

            if not root_pid:
                return None

            root_pid = int(root_pid)

        except Exception:
            return None

        processes = self._collect_descendants(
            root_pid
        )

        if not processes:
            return None

        # -----------------------------------------------------
        # Build session information.
        # -----------------------------------------------------

        sessions = {}

        for info in processes:

            sid = info["sid"]

            if sid not in sessions:
                sessions[sid] = {
                    "sid": sid,
                    "depth": -1,
                    "pts": None,
                    "members": [],
                }

            sessions[sid]["members"].append(
                info
            )

        # -----------------------------------------------------
        # Calculate depth from the original terminal PID.
        #
        # We use PPID relationships among the descendants.
        # -----------------------------------------------------

        by_pid = {
            info["pid"]: info
            for info in processes
        }

        depth = {
            root_pid: 0
        }

        changed = True

        while changed:

            changed = False

            for info in processes:

                pid = info["pid"]

                if pid in depth:
                    continue

                parent = info["ppid"]

                if parent in depth:

                    depth[pid] = (
                        depth[parent] + 1
                    )

                    changed = True

        # -----------------------------------------------------
        # Assign each session its deepest descendant and PTY.
        # -----------------------------------------------------

        for sid, session in sessions.items():

            best_depth = -1
            best_pts = None

            for info in session["members"]:

                pid = info["pid"]

                d = depth.get(
                    pid,
                    0
                )

                if d > best_depth:

                    pts = self._tty_nr_to_pts(
                        info["tty_nr"]
                    )

                    if pts is not None:

                        best_depth = d
                        best_pts = pts

            session["depth"] = best_depth
            session["pts"] = best_pts

        # -----------------------------------------------------
        # Determine the original session.
        # -----------------------------------------------------

        root_info = by_pid.get(root_pid)

        if root_info is None:
            return None

        root_sid = root_info["sid"]

        # -----------------------------------------------------
        # Candidate sessions.
        #
        # A nested sudo/su session will normally have a different
        # SID and will be deeper in the descendant tree.
        # -----------------------------------------------------

        candidates = []

        for sid, session in sessions.items():

            if session["pts"] is None:
                continue

            candidates.append(
                session
            )

        if not candidates:
            return None

        # -----------------------------------------------------
        # Prefer the deepest session.
        #
        # If two sessions have the same depth, prefer the one
        # whose session leader appears deeper in the tree.
        #
        # The original session remains the fallback.
        # -----------------------------------------------------

        nested = [
            s
            for s in candidates
            if s["sid"] != root_sid
        ]

        if nested:

            nested.sort(
                key=lambda s: (
                    s["depth"],
                    s["sid"]
                ),
                reverse=True
            )

            return nested[0]["pts"]

        # Normal remac shell.
        root_session = sessions.get(
            root_sid
        )

        if root_session:

            return root_session["pts"]

        # Last-resort fallback.
        return candidates[0]["pts"]

    # =========================================================
    # DEBUG
    # =========================================================

    def _debug(self, message):
        try:
            with open(
                "/tmp/live-clock-debug",
                "a"
            ) as f:
                f.write(
                    message + "\n"
                )

        except Exception:
            pass

    # =========================================================
    # STATE FILE
    # =========================================================

    def _write_state(self, pts, state):

        if not pts:
            return

        state_file = (
            f"/tmp/zsh-live-clock-{pts}"
        )

        tmp_file = (
            state_file + ".tmp"
        )

        try:

            with open(
                tmp_file,
                "w"
            ) as f:

                f.write(state)

            os.replace(
                tmp_file,
                state_file
            )

        except OSError:
            pass

    # =========================================================
    # PAUSE
    # =========================================================

    def _pause_terminal(self, terminal):

        pts = self._terminal_pts(
            terminal
        )

        if not pts:
            return

        self.paused[pts] = True

        self._write_state(
            pts,
            "paused"
        )

        self._debug(
            f"MOUSE PAUSE: pts={pts}"
        )

    # =========================================================
    # MOUSE PRESS
    # =========================================================

    def _mouse_press(
        self,
        vte,
        event,
        terminal
    ):

        self.mouse_pressed.add(
            id(vte)
        )

        self._pause_terminal(
            terminal
        )

        return False

    # =========================================================
    # MOUSE RELEASE
    # =========================================================

    def _mouse_release(
        self,
        vte,
        event,
        terminal
    ):

        vte_id = id(vte)

        self.mouse_pressed.discard(
            vte_id
        )

        self._debug(
            "MOUSE RELEASE"
        )

        return False

    # =========================================================
    # CONNECT MOUSE SIGNALS
    # =========================================================

    def _connect_mouse_handlers(
        self,
        terminal,
        vte
    ):

        key = id(vte)

        if key in self.connected:
            return

        try:

            vte.connect(
                "button-press-event",
                self._mouse_press,
                terminal
            )

            vte.connect(
                "button-release-event",
                self._mouse_release,
                terminal
            )

            self.connected.add(
                key
            )

            self._debug(
                f"MOUSE CONNECTED: vte={key}"
            )

        except Exception as e:

            self._debug(
                "MOUSE CONNECT ERROR: "
                f"{type(e).__name__}: {e}"
            )

    # =========================================================
    # SCROLL / SELECTION STATE
    # =========================================================

    def _get_vte_state(self, vte):

        # -----------------------------------------------------
        # Scroll position
        # -----------------------------------------------------

        try:

            adjustment = (
                vte.get_vadjustment()
            )

            upper = (
                adjustment.get_upper()
            )

            page = (
                adjustment.get_page_size()
            )

            value = (
                adjustment.get_value()
            )

            bottom = max(
                0,
                upper - page
            )

            scrolled = (
                value < bottom - 0.5
            )

        except Exception as e:

            self._debug(
                "SCROLL ERROR: "
                f"{type(e).__name__}: {e}"
            )

            scrolled = False

        # -----------------------------------------------------
        # Text selection
        # -----------------------------------------------------

        try:

            selected = (
                vte.get_has_selection()
            )

        except Exception:

            selected = False

        return (
            scrolled,
            selected
        )

    # =========================================================
    # MAIN POLL
    # =========================================================

    def _poll(self):

        try:

            import terminatorlib.terminator as terminatorlib

            terminator = (
                terminatorlib.Terminator()
            )

            for terminal in terminator.terminals:

                vte = terminal.get_vte()

                pts = self._terminal_pts(
                    terminal
                )

                self._debug(
                    "VTE DEBUG: "
                    f"terminal.id={id(terminal)} "
                    f"terminal.pid="
                    f"{getattr(terminal, 'pid', None)} "
                    f"active_pts={pts} "
                    f"vte_type={type(vte).__name__}"
                )

                self._connect_mouse_handlers(
                    terminal,
                    vte
                )

                if not pts:
                    continue

                vte_id = id(vte)

                scrolled, selected = (
                    self._get_vte_state(
                        vte
                    )
                )

                pressed = (
                    vte_id
                    in self.mouse_pressed
                )

                self._debug(
                    "STATE: "
                    f"pts={pts} "
                    f"scrolled={scrolled} "
                    f"selected={selected} "
                    f"pressed={pressed}"
                )

                should_pause = (
                    scrolled
                    or selected
                    or pressed
                )

                # -------------------------------------------------
                # PAUSE
                # -------------------------------------------------

                if should_pause:

                    if (
                        self.paused.get(pts)
                        is not True
                    ):

                        self.paused[pts] = True

                        self._write_state(
                            pts,
                            "paused"
                        )

                        self._debug(
                            f"PAUSE: pts={pts}"
                        )

                # -------------------------------------------------
                # RESUME
                # -------------------------------------------------

                else:

                    if (
                        self.paused.get(pts)
                        is not False
                    ):

                        self.paused[pts] = False

                        self._write_state(
                            pts,
                            "live"
                        )

                        self._debug(
                            f"RESUME: pts={pts}"
                        )

        except Exception as e:

            self._debug(
                "POLL ERROR: "
                f"{type(e).__name__}: {e}"
            )

        return True