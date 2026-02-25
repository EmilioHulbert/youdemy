#location /lib/security/howdy/verify.py
import sys

import os

# Hide the Qt/GUI errors
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["OPENCV_LOG_LEVEL"] = "OFF"

sys.path.append("/lib/security/howdy")
from compare import Compare

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
        
    user = sys.argv[1]
    try:
        # Use the internal engine directly
        c = Compare("/lib/security/howdy/config.ini")
        identified_user = c.identify()
        
        if identified_user == user:
            sys.exit(0) # Match
    except Exception:
        pass
    
    sys.exit(1) # No match or error

if __name__ == "__main__":
    main()
