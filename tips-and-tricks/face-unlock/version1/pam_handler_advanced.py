import subprocess
import os
import time

def pam_sm_authenticate(pamh, flags, argv):
    try:
        user = pamh.get_user(None)
        start_time = time.time()
        timeout_limit = 30  # Total time to keep trying in seconds

        # Loop until 30 seconds have passed
        while (time.time() - start_time) < timeout_limit:
            # Calculate remaining time for this specific run
            remaining_time = timeout_limit - (time.time() - start_time)
            
            process = subprocess.run(
                ["/usr/bin/python3", "/lib/security/howdy/verify.py", user],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env={"PYTHONPATH": "/lib/security/howdy"},
                timeout=remaining_time
            )

            # If it found you, succeed immediately!
            if process.returncode == 0:
                return 0  # PAM_SUCCESS
            
            # Optional: Add a tiny sleep so it doesn't slam the CPU 
            time.sleep(0.5)

        return 7  # PAM_AUTH_ERR (Timed out after 30s without a match)
    except:
        return 7

def pam_sm_setcred(pamh, flags, argv): return 0
def pam_sm_acct_mgmt(pamh, flags, argv): return 0
def pam_sm_open_session(pamh, flags, argv): return 0
def pam_sm_close_session(pamh, flags, argv): return 0