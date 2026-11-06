#Usage commands
google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug" --no-first-run --new-window
or
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.config/chrome-debug" --no-first-run --new-window
npm install -g puppeteer-cli
3. In this newly opened window, navigate back to your Zety builder dashboard if it doesn't open automatically: `[https://builder.zety.com/resume/final-resume](https://builder.zety.com/resume/final-resume)`. Keep this window open.

---

# 1. Create a fake, non-default data directory structure pointing to your real profile folder
mkdir -p "$HOME/chrome-dev-profile"
ln -s "$HOME/.config/google-chrome/Profile 4" "$HOME/chrome-dev-profile/Default"

# 2. Launch Chrome using the new fake data directory path
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/chrome-dev-profile" --no-first-run --new-window


## Step 2: Set Up the Compilation Project Directory
Let's assemble a dedicated workspace folder on your desktop to prevent any script execution path conflicts. Run these commands in your terminal:

```bash
mkdir -p ~/Desktop/try && cd ~/Desktop/try
npm install puppeteer

nano export_resume.js
#already created the above

node export_resume.js


