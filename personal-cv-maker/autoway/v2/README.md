#Usage commands
google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug" --no-first-run --new-window
or
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.config/chrome-debug" --no-first-run --new-window
npm install -g puppeteer-cli
3. In this newly opened window, navigate back to your Zety builder dashboard if it doesn't open automatically: `[https://builder.zety.com/resume/final-resume](https://builder.zety.com/resume/final-resume)`. Keep this window open.

---

## Step 2: Set Up the Compilation Project Directory
Let's assemble a dedicated workspace folder on your desktop to prevent any script execution path conflicts. Run these commands in your terminal:

```bash
mkdir -p ~/Desktop/try && cd ~/Desktop/try
npm install puppeteer

nano export_resume.js
#already created the above

node export_resume.js


