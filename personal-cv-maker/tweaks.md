The terminal message `Opening in existing browser session.` is the smoking gun here.

Even though you closed your student profile window, **Chrome runs a background process framework.** If *any* instance of Chrome is still running on your system (like your main `emiliohulbert2017` profile), launching a new Chrome command won't actually start a fresh, independent process. Instead, the existing background process intercepts your command, opens a new window under your main session, and completely ignores your debugging flags (`--remote-debugging-port=9222`).

Because the command was hijacked by the existing session, the debugging port **9222** never actually opened—which is why your `netstat` command returned absolutely nothing.

To Chrome, all profiles share the same binary executable pool, so your main profile absolutely *does* have something to do with it.

---

### How to fix it (2 Options)

#### Option 1: The `--user-data-dir` trick (Recommended for Devs)

The easiest way to force Chrome to completely isolate your debugging session from your currently open main browser is to pass a temporary or completely separate user data directory *just* for your automated cv-maker work.

You can copy your Profile 4 folder to a dedicated workspace or let Chrome spin up a clean isolated environment like this:

```bash
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.config/google-chrome-debug" --no-first-run --new-window

```

Because the `--user-data-dir` is completely different from your main browser's path (`~/.config/google-chrome`), Chrome is forced to spawn a brand-new, independent process pool, and port 9222 *will* open.

#### Option 2: Kill all existing Chrome processes

If you absolutely *must* use Profile 4 from your standard configuration directory right now, you have to kill your main browser session entirely so that no Chrome processes are running in the background.

1. Close your main Chrome browser window manually.
2. In your terminal, completely nuke any lingering background Chrome processes:
```bash
pkill -f chrome

```


3. Verify nothing is left running:
```bash
ps aux | grep chrome

```


4. Now, run your original debugging command again:
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.config/google-chrome" --profile-directory="Profile 4" --no-first-run --new-window

```



Check `netstat -tuln | grep 922` after doing either of those, and you'll see port 9222 sitting wide open and ready for your Puppeteer/automation scripts.
Copying the contents of `Profile 4` into a separate user data directory is actually a brilliant workaround. It gives you the best of both worlds: it completely bypasses the open Chrome session conflict, keeps your main browser alive, and retains all your saved auto-logins.

However, because of how Chrome structures its configuration folders, you can't just dump the files straight into `google-chrome-debug`. You have to place them inside a folder named `Default` within that new directory.

When Chrome launches, it always looks for a folder named `Default` as its primary profile unless told otherwise.

Here is exactly how to set this up:

---

### Step 1: Create the new directory structure

Open your terminal and create the debug directory along with its internal `Default` profile folder:

```bash
mkdir -p "$HOME/.config/google-chrome-debug/Default"

```

### Step 2: Copy your Student Profile contents

Copy everything from your original `Profile 4` into this new `Default` folder. We will use `cp -r` to make sure all session data, cookies, and login states transfer over:

```bash
cp -r "$HOME/.config/google-chrome/Profile 4/"* "$HOME/.config/google-chrome-debug/Default/"

```

### Step 3: Launch the isolated Debug session

Now, run your command pointing to the new isolated directory. Because Chrome sees this as a completely different user data root, it will spawn a brand new process without touching your main open browser:

```bash
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.config/google-chrome-debug" --no-first-run --new-window

```

---

### Why this works perfectly for your goal

1. **Zero interference:** Your main `emiliohulbert2017` profile stays open and untouched.
2. **Port 9222 opens instantly:** `netstat -tuln | grep 922` will now show the port listening because Chrome was forced to start a separate process pool.
3. **Persistent Logins:** Because you copied the underlying database files (`Cookies`, `Login Data`, etc.), your student portal and Google account sessions will remain actively logged in.
