import subprocess
import os
import threading
import time
import sys
import select
import termios
import crypt
import spwd

face_matched = False
input_done = False
camera_process = None  # Track the active subprocess globally to terminate it cleanly

def camera_thread_loop(user):
    global face_matched, input_done, camera_process
    start_time = time.time()
    timeout_limit = 15  # 15 seconds is plenty for a face scan

    while (time.time() - start_time) < timeout_limit and not input_done and not face_matched:
        # Run verify.py cleanly out-of-process
        # camera_process = subprocess.Popen(
        #     ["/usr/bin/python3", "/lib/security/howdy/verify.py", user],
        #     stdout=subprocess.DEVNULL,
        #     stderr=subprocess.DEVNULL,
        #     env={"PYTHONPATH": "/lib/security/howdy"}
        # )
        # Run verify.py cleanly out-of-process with the copied base environment
        camera_process = subprocess.Popen(
            ["/usr/bin/python3", "/lib/security/howdy/verify.py", user],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=os.environ.copy() if "PYTHONPATH" in os.environ else {"PYTHONPATH": "/lib/security/howdy", "PATH": "/usr/bin:/bin:/usr/sbin:/sbin"}
        )
        
        # Wait for the individual scan to finish or see if input finished
        while camera_process.poll() is None:
            if input_done:
                camera_process.terminate()
                return
            time.sleep(0.05)

        if camera_process.returncode == 0:
            face_matched = True
            break
            
        time.sleep(0.1)

# def get_parallel_input(prompt_text):
#     global face_matched
#     sys.stdout.write(prompt_text)
#     sys.stdout.flush()

#     fd = sys.stdin.fileno()
#     try:
#         old_settings = termios.tcgetattr(fd)
#     except Exception:
#         # If we are in a GUI (LightDM/MATE lockscreen), tcgetattr fails.
#         # Return None immediately so we can route cleanly to standard PAM conversations.
#         return None

#     try:
#         # Secure the terminal by disabling echo
#         new_settings = termios.tcgetattr(fd)
#         new_settings[3] = new_settings[3] & ~termios.ECHO
#         termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)

#         typed_password = ""
#         while True:
#             if face_matched:
#                 # Flush the TTY input buffer before exiting to kill the double-Enter bug!
#                 termios.tcflush(fd, termios.TCIFLUSH)
#                 return None

#             ready, _, _ = select.select([sys.stdin], [], [], 0.05)
#             if ready:
#                 char = sys.stdin.read(1)
#                 if char in ('\n', '\r'):
#                     sys.stdout.write("\n")
#                     break
#                 elif char == '\x7f':  # Handle backspace
#                     typed_password = typed_password[:-1]
#                 else:
#                     typed_password += char
                    
#         return typed_password
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def get_parallel_input(prompt_text):
    global face_matched
    sys.stdout.write(prompt_text)
    sys.stdout.flush()

    fd = sys.stdin.fileno()
    try:
        old_settings = termios.tcgetattr(fd)
    except Exception:
        # If we are in a GUI (LightDM/MATE lockscreen), tcgetattr fails.
        # Return None immediately so we can route cleanly to standard PAM conversations.
        return None

    try:
        # Secure the terminal by disabling echo and enabling non-canonical (raw) input mode
        new_settings = termios.tcgetattr(fd)
        # ~ECHO turns off character printing, ~ICANON processes keystrokes instantly without waiting for Enter
        new_settings[3] = new_settings[3] & ~termios.ECHO & ~termios.ICANON
        termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)

        typed_password = ""
        while True:
            if face_matched:
                try:
                    # Flush the input buffer to kill any pending trailing keys on face match exit
                    termios.tcflush(fd, termios.TCIFLUSH)
                except Exception:
                    pass
                return None

            # Poll stdin for typing every 50ms without stalling the CPU
            ready, _, _ = select.select([sys.stdin], [], [], 0.05)
            if ready:
                char = sys.stdin.read(1)
                if char in ('\n', '\r'):
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    try:
                        # Flush right after user hits Enter to kill the double-prompt ghost sequence
                        termios.tcflush(fd, termios.TCIFLUSH)
                    except Exception:
                        pass
                    break
                elif char == '\x7f':  # Handle backspace
                    typed_password = typed_password[:-1]
                elif char:  # Append valid characters
                    typed_password += char
                    
        return typed_password
    finally:
        # Crucial: Always restore the terminal configuration back to standard functional state
        try:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception:
            pass
            
def pam_sm_authenticate(pamh, flags, argv):
    global face_matched, input_done, camera_process
    try:
        user = pamh.get_user(None)
        face_matched = False
        input_done = False
        camera_process = None

        # 1. Fire up the camera loop asynchronously immediately
        bg_thread = threading.Thread(target=camera_thread_loop, args=(user,))
        bg_thread.daemon = True
        bg_thread.start()

        # 2. Check if we are running in a terminal TTY or a Graphical Screen Lock
        fd = sys.stdin.fileno()
        is_tty = True
        try:
            termios.tcgetattr(fd)
        except Exception:
            is_tty = False

        password_attempt = None

        if is_tty:
            # TERMINAL MODE: Run your flawless parallel input engine
            prompt = f"[sudo] password for {user} (or scanning face...): "
            password_attempt = get_parallel_input(prompt)
        else:
            # GUI/LOCKSCREEN MODE: Let the camera scan concurrently without blocking input
            # Give the camera a brief 2.5-second head start to authenticate you instantly
            start_scan = time.time()
            while (time.time() - start_scan) < 2.5:
                if face_matched:
                    break
                time.sleep(0.1)

            # If the face didn't match immediately, bring up the graphical prompt box safely
            if not face_matched:
                try:
                    resp = pamh.conversation(pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "Password (or scanning face...): "))
                    password_attempt = resp.resp
                except Exception:
                    return 7

        # Signal the background camera processes to wrap up execution
        input_done = True
        if camera_process and camera_process.poll() is None:
            camera_process.terminate()

        # 3. Final Win-Condition Matrix Valuation
        if face_matched:
            return 0  # PAM_SUCCESS (Face unlocked it natively!)

        # 4. Local password hash mapping fallback validation
        if password_attempt:
            try:
                shadow_hash = spwd.getspnam(user).sp_pwdp
                if crypt.crypt(password_attempt, shadow_hash) == shadow_hash:
                    return 0  # PAM_SUCCESS (Password matched local shadow keys)
            except Exception:
                pass

        return 7  # PAM_AUTH_ERR
    except Exception:
        if camera_process and camera_process.poll() is None:
            camera_process.terminate()
        return 7
        
def pam_sm_setcred(pamh, flags, argv): return 0
def pam_sm_acct_mgmt(pamh, flags, argv): return 0
def pam_sm_open_session(pamh, flags, argv): return 0
def pam_sm_close_session(pamh, flags, argv): return 0
