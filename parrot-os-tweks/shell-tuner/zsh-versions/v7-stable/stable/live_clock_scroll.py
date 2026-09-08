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
    # LEFT MOUSE BUTTON PRESS
    # ------------------------------------------------------------------

    def _press(self, vte, event):
        if event.button == 1:
            self.selecting.add(id(vte))

        return False

    # ------------------------------------------------------------------
    # LEFT MOUSE BUTTON RELEASE
    # ------------------------------------------------------------------

    def _release(self, vte, event):
        if event.button != 1:
            return False

        ident = id(vte)

        # Do NOT clear the selection immediately.
        #
        # VTE/Terminator must first finish processing the mouse release.
        # We then copy the selection explicitly and remove the visual
        # highlight from an idle callback.
        GLib.idle_add(
            self._finish_selection,
            vte,
            ident
        )

        return False

    # ------------------------------------------------------------------
    # COPY THEN REMOVE HIGHLIGHT
    # ------------------------------------------------------------------

    def _finish_selection(self, vte, ident):

        try:
            # Keep the selected text in the clipboard.
            #
            # Terminator's copy_on_selection normally already did this,
            # but copying here guarantees that the clipboard is populated
            # before we remove the VTE selection.
            if vte.get_has_selection():
                vte.copy_clipboard()

                # Remove ONLY the visual selection.
                #
                # This does NOT clear the clipboard.
                vte.unselect_all()

        except Exception:
            pass

        # Mouse interaction is completely finished.
        self.selecting.discard(ident)

        return False

    # ------------------------------------------------------------------
    # WRITE CLOCK STATE
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
        # CLOCK IS LIVE ONLY WHEN:
        #
        #   1. terminal is at the bottom
        #   2. no mouse selection is active
        #   3. VTE has no selection
        #
        # Otherwise the clock is paused.
        # --------------------------------------------------------------

        selecting = id(vte) in self.selecting
        has_selection = vte.get_has_selection()

        if (
            position == "BOTTOM"
            and not selecting
            and not has_selection
        ):
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

                bottom = max(
                    0,
                    upper - page
                )

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