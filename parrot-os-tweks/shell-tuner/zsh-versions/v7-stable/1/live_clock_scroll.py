import os
from gi.repository import GLib
import terminatorlib.plugin as plugin


AVAILABLE = ['LiveClockScroll']


class LiveClockScroll(plugin.Plugin):
    capabilities = []

    def __init__(self):
        self.poll_id = GLib.timeout_add(100, self._poll)
        self.connected = set()
        self.selecting = set()

    def unload(self):
        if self.poll_id:
            GLib.source_remove(self.poll_id)
            self.poll_id = None

        self.connected.clear()
        self.selecting.clear()

    # ------------------------------------------------------------------
    # VTE SIGNAL CONNECTION
    # ------------------------------------------------------------------

    def _connect(self, vte):
        ident = id(vte)

        if ident in self.connected:
            return

        vte.connect('button-press-event', self._press)
        vte.connect('button-release-event', self._release)

        self.connected.add(ident)

    # ------------------------------------------------------------------
    # MOUSE PRESS
    # ------------------------------------------------------------------

    def _press(self, vte, event):
        if event.button == 1:
            self.selecting.add(id(vte))

        return False

    # ------------------------------------------------------------------
    # MOUSE RELEASE
    # ------------------------------------------------------------------

    def _release(self, vte, event):
        if event.button == 1:
            ident = id(vte)

            # Keep the clock paused through the actual mouse release.
            # Remove the latch on the next GTK idle cycle.
            GLib.idle_add(self._finish_selection, ident)

        return False

    def _finish_selection(self, ident):
        self.selecting.discard(ident)
        return False

    # ------------------------------------------------------------------
    # WRITE STATE FOR ZSH
    # ------------------------------------------------------------------

    def _write_state(self, terminal, vte, position):
        pid = getattr(terminal, "pid", 0)

        if not pid:
            return

        try:
            tty = os.path.realpath(
                f"/proc/{pid}/fd/0"
            )
        except Exception:
            return

        if not tty.startswith("/dev/pts/"):
            return

        pts = tty.rsplit("/", 1)[-1]

        # --------------------------------------------------------------
        # PAUSE CLOCK IF:
        #
        #   1. terminal is scrolled away from bottom
        #   2. LMB selection is active
        #   3. VTE still reports an active selection
        #
        # --------------------------------------------------------------

        selecting = id(vte) in self.selecting
        has_selection = vte.get_has_selection()

        if position == "BOTTOM" and not selecting and not has_selection:
            state = "live"
        else:
            state = "paused"

        state_file = f"/tmp/zsh-live-clock-{pts}"
        tmp_file = state_file + ".tmp"

        try:
            with open(tmp_file, "w") as f:
                f.write(state)

            os.replace(tmp_file, state_file)

        except Exception:
            pass

    # ------------------------------------------------------------------
    # MAIN POLLER
    # ------------------------------------------------------------------

    def _poll(self):
        try:
            import terminatorlib.terminator as terminatorlib

            terminator = terminatorlib.Terminator()

            for terminal in terminator.terminals:

                vte = terminal.get_vte()

                self._connect(vte)

                adjustment = vte.get_vadjustment()

                upper = adjustment.get_upper()
                page = adjustment.get_page_size()
                value = adjustment.get_value()

                bottom = max(0, upper - page)

                if value >= bottom - 0.5:
                    position = "BOTTOM"
                else:
                    position = "SCROLLED"

                self._write_state(
                    terminal,
                    vte,
                    position
                )

        except Exception:
            pass

        return True