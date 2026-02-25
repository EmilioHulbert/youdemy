#location /lib/security/howdy/pam/pam_handler.py
import subprocess
import os

def pam_sm_authenticate(pamh, flags, argv):
    try:
        user = pamh.get_user(None)
        
        # Run our new headless script
        process = subprocess.run(
            ["/usr/bin/python3", "/lib/security/howdy/verify.py", user],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env={"PYTHONPATH": "/lib/security/howdy"},
            timeout=3
        )

        if process.returncode == 0:
            return 0  # PAM_SUCCESS
        return 7      # PAM_AUTH_ERR
    except:
        return 7

def pam_sm_setcred(pamh, flags, argv): return 0
def pam_sm_acct_mgmt(pamh, flags, argv): return 0
def pam_sm_open_session(pamh, flags, argv): return 0
def pam_sm_close_session(pamh, flags, argv): return 0
