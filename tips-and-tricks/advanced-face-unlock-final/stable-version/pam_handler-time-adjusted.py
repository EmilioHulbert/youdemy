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

def get_parallel_input(prompt_text):
    global face_matched
    sys.stdout.write(prompt_text)
    sys.stdout.flush()

    fd = sys.stdin.fileno()
    try:
        old_settings = termios.tcgetattr(fd)
    except Exception:
        return None

    try:
        new_settings = termios.tcgetattr(fd)
        new_settings[3] = new_settings[3] & ~termios.ECHO & ~termios.ICANON
        termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)

        typed_password = ""
        while True:
            if face_matched:
                try:
                    termios.tcflush(fd, termios.TCIFLUSH)
                except Exception:
                    pass
                return None

            ready, _, _ = select.select([sys.stdin], [], [], 0.05)
            if ready:
                char = sys.stdin.read(1)
                if char in ('\n', '\r'):
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    try:
                        termios.tcflush(fd, termios.TCIFLUSH)
                    except Exception:
                        pass
                    break
                elif char == '\x7f':  # Handle backspace
                    typed_password = typed_password[:-1]
                elif char:
                    typed_password += char
                    
        return typed_password
    finally:
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

        # if is_tty:
        #     # TERMINAL MODE: Run your flawless parallel input engine
        #     prompt = f"[sudo] password for {user} (or scanning face...): "
        #     password_attempt = get_parallel_input(prompt)
        # else:
        #     # GUI/LOCKSCREEN MODE: Let the camera scan concurrently without blocking input
        #     start_scan = time.time()
        #     while (time.time() - start_scan) < 2.5:
        #         if face_matched:
        #             break
        #         time.sleep(0.1)

        #     # If the face didn't match immediately, bring up the graphical prompt box safely
        #     if not face_matched:
        #         try:
        #             resp = pamh.conversation(pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "Password (or scanning face...): "))
        #             password_attempt = resp.resp
        #         except Exception:
        #             return 11  # Return PAM_IGNORE on prompt breakage
        if is_tty:
            # TERMINAL MODE: Run your flawless parallel input engine
            prompt = f"[sudo] password for {user} (or scanning face...): "
            password_attempt = get_parallel_input(prompt)
        else:
            # GUI/LOCKSCREEN MODE: Let the camera scan concurrently without blocking input
            # INCREASED: Give the camera a full 15-second window to authenticate you hands-free
            gui_timeout = 15.0  
            start_scan = time.time()
            while (time.time() - start_scan) < gui_timeout:
                if face_matched:
                    break
                time.sleep(0.1)

            # If the face didn't match after 15 seconds, bring up the graphical prompt box safely
            if not face_matched:
                try:
                    resp = pamh.conversation(pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "Password: "))
                    password_attempt = resp.resp
                except Exception:
                    return 11  # Return PAM_IGNORE on prompt breakage


                    
        # Signal the background camera processes to wrap up execution
        input_done = True
        if camera_process and camera_process.poll() is None:
            camera_process.terminate()

        # 3. Handle Successful Face Match Authentication Path
        if face_matched:
            return 0  # PAM_SUCCESS (Face unlocked it natively!)

        # 4. Handle Password Pass-through / Verification Matrix
        if password_attempt:
            if is_tty:
                # Terminal authentication has Root privileges; check local shadow securely
                try:
                    shadow_hash = spwd.getspnam(user).sp_pwdp
                    if crypt.crypt(password_attempt, shadow_hash) == shadow_hash:
                        return 0  # PAM_SUCCESS
                except Exception:
                    pass
                return 7  # PAM_AUTH_ERR (Wrong password in terminal)
            else:
                # Graphical Lockscreen: forward the token and pass verification responsibilities
                # down the stack seamlessly to pam_unix.so
                try:
                    pamh.authtok = password_attempt
                except Exception:
                    pass
                return 11  # PAM_IGNORE (Tells PAM stack to verify our token via standard modules)

        return 7  # PAM_AUTH_ERR if no face matched and no password entered
    except Exception:
        if camera_process and camera_process.poll() is None:
            camera_process.terminate()
        return 7

def pam_sm_setcred(pamh, flags, argv): return 0
def pam_sm_acct_mgmt(pamh, flags, argv): return 0
def pam_sm_open_session(pamh, flags, argv): return 0
def pam_sm_close_session(pamh, flags, argv): return 0
