# Mevami

**Mevami** is an automated system designed to scan your Clone Hero song library and generate a hosted web interface to showcase your setlist. Make it easier for you, your friends or anyone to see what songs they could play in your collection.

Mevami changes how you manage your Clone Hero library. It makes it easier to:

* **Access your library online**: Look through your songs even when you aren't at your PC.

* **Save time**: No more manual scrolling through thousands of songs on the Clone Hero menu.

* **Keep the party going!**: Your friends can browse the setlist simultaneously, so there's no downtime between songs.


<center>
<img src="https://imgur.com/J08k67f.png" width="90%">
</center>

## Features

* **Filtering**: Search by song title, artist, or album.

* **Instrument Difficulty Sorting**: Sort your entire library based on specific instrument difficulties or intensity.

* **Guitar Hero Live support**: Guitar-Live, Bass-Live, Rhythm-Live, and Guitar Co-op-Live instruments are fully recognized and displayed alongside standard instruments.

<center>
<img src="https://imgur.com/WYYGZiv.png" width="90%">
</center>

* **Difficulty badges on each of the instruments**: Get the difficulties available for each of the available instruments for a song simply by clicking on the instrument icon.







<center>
<img src="https://imgur.com/tnKXgfB.png" width="50%">
</center>

* **Randomizer**: A "Random Song" button that helps pick the next track.


<center>
<img src="https://imgur.com/42VAuUF.png" width="50%">
</center>

* **External Links**: Spotify and YouTube search buttons for every song in your catalog.

* **Video badge** Identify which songs have video background.

<center>
<img src="https://imgur.com/KKGuB1e.png" width="30%">
</center>

## How does it work?
Mevami uses the Python script `generate_list.py` to scan your clone hero songs folder, then creates two files: `data.json` (Contains all the info from the songs) and `genres.json` (A list of the genres from all your songs).

`index.html` has the code to build and display your searchable website using the generated files and the resources folder.

Theres an executable called **publish** (`publish.sh` for MacOS/Linux and `publish.bat` for Windows), what it does it runs `generate_list.py` script that creates the json files and also publish them on github, updating your website data, so each time you added new songs you just have to run this executable.

## Setup Guide

### Step 1 — Install Python

Python is a free program the scanner needs to run.
[More info](https://wiki.python.org/moin/BeginnersGuide/Download) on how to install it.

<details>
<summary><strong>Windows</strong></summary>

1. Go to [python.org/downloads](https://www.python.org/downloads/) and click the big **Download** button.
2. Run the installer. **Important:** Before clicking Install, check the box that says **"Add Python to PATH"** — this is easy to miss!
3. To confirm it worked, open the **Start Menu**, search for **Command Prompt**, open it, and type:
   ```
   python --version
   ```
   You should see something like `Python 3.x.x`. If you do, you're good!

</details>

<details>
<summary><strong>macOS</strong></summary>

1. Before downloading anything, check if your Mac already has Python 3.

   * Open Terminal (Press Command (⌘) + Space and type "Terminal").

   * Type the following command and hit Enter:

   ```bash
   python3 --version
   ```

Note: If it displays a version number (e.g., Python 3.12.x), you’re all set! If you get a "command not found" error, proceed to the next step.

2. Go to [python.org/downloads](https://www.python.org/downloads/) and download the macOS installer.
3. Open the downloaded file and follow the steps.
4. To confirm it worked, open **Terminal** (search for it in Spotlight with `⌘ + Space`) and type:
   ```bash
   python3 --version
   ```

</details>

<details>
<summary><strong>Linux</strong></summary>

Python is usually already installed. Check by opening a terminal and running:
```bash
python3 --version
```

If it's not installed:
```bash
# Debian / Ubuntu
sudo apt update && sudo apt install python3

# Fedora
sudo dnf install python3

# Arch
sudo pacman -S python
```

</details>

---

### Step 2 — Install the Required Python Libraries

Once Python is installed, you need to install the two libraries Mevami depends on. Open a terminal in the Mevami folder and run:

**Windows:**
```
pip install -r requirements.txt
```

**Mac / Linux:**
```bash
pip3 install -r requirements.txt
```

This installs `mido` (for reading MIDI chart files) and `tqdm` (for the progress bar during scanning). You only need to do this once.

> 💡 **Tip:** If you get a "pip not found" error on Mac/Linux, try `python3 -m pip install -r requirements.txt` instead.

---

### Step 3 — Decide How You Want to Host It

Before installing anything else, think about how you want to share your setlist:

| Option | Best for | What you need |
|--------|----------|---------------|
| **GitHub Pages** ⭐ Recommended | Sharing with friends, accessible from any device, hosted on the web, accessible from anywhere. | A free GitHub account. |
| **Local server** | Showing your setlist to friends at home on their phones connected to your Wi-Fi. | Python installed (you need it anyway). |
| **Custom domain/server** | If you already have a hosting set up. | You probably already know what to do. 😄 |


⚠️ Note on the local server option: While it works great in many cases, some mobile devices can be finicky about connecting to local network servers depending on their settings. I recommend the GitHub Pages, to skip more configuration.



### Step 4 — Installing Git

You have two ways to go here — pick whichever feels more comfortable:

| Option | Best for | Pros | Cons |
|--------|----------|------|------|
| **GitHub Desktop** ⭐ Recommended for beginners | If you've never used Git before, or prefer clicking buttons over typing commands. | No terminal needed, easy to set up, handles authentication automatically. | Updating your setlist requires a few manual steps in the app instead of just running the publish script. |
| **Git (command line)** | If you're comfortable with terminals or want full control. | Updating is as simple as running the publish executable — fully automated. | Initial config (authentication, tokens) can be tricky for beginners. |
---

#### 🖥️ Option A — GitHub Desktop (Beginner Friendly)

GitHub Desktop is a free app that lets you manage your Git repos with a simple visual interface — no terminal required for most tasks.

1. Download it from [desktop.github.com](https://desktop.github.com/) and install it.
2. Open GitHub Desktop and click **Sign in to GitHub.com**. Log in with your GitHub account (or create a free one at [github.com](https://github.com)).
3. That's it! GitHub Desktop handles authentication for you automatically — no tokens, no SSH keys. 🎉

> **Note for Linux users:** GitHub Desktop doesn't officially support Linux. You'll want to use the command line option below instead.

---

#### ⌨️ Option B — Git (Command Line)

Click on your OS to see how to install it. You can also check the [official guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

<details>
<summary><strong>Windows</strong></summary>

1. Download the installer from [git-scm.com/download/win](https://git-scm.com/download/win).
2. Run it and click **Next** through all the steps — the default options are fine.
3. After installing, you'll have a program called **Git Bash**. Use that whenever a step below asks you to open a terminal.

</details>

<details>
<summary><strong>macOS</strong></summary>

Open **Terminal** and run:
```bash
git --version
```
If Git isn't installed, macOS will offer to install it automatically. Just click through the prompts.

**⚠️ Heads up:** If Git was already installed on your Mac (which is common), it may have saved your Mac's system name and email as your Git identity instead of your GitHub info. This means your commits might not be linked to your GitHub account correctly.
To fix it, open Terminal and run these two commands, replacing the values with the name and email you use on GitHub:

```bash
git config --global user.name "YourGitHubUsername"
git config --global user.email "you@example.com"
```

</details>

<details>
<summary><strong>Linux</strong></summary>

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install git

# Fedora
sudo dnf install git

# Arch
sudo pacman -S git
```

</details>

#### **Setting up Git (command line only)**

Check [Github docs-Set up Git](https://docs.github.com/en/get-started/git-basics/set-up-git) for more info on how to do this.
The trickiest part is Git Authentication. I recommend using GitHub Classic Access Tokens — just be careful, because those are like passwords. Here's a video on how to do it.


[![Watch the video](https://img.youtube.com/vi/iLrywUfs7yU/0.jpg)](https://www.youtube.com/watch?v=iLrywUfs7yU)

---

### Step 5 — Clone the Mevami Repo

You need your own personal copy of Mevami on GitHub so you can host your setlist. Pick the path that matches how you set up Git in the previous step:

---

#### 🖥️ Using GitHub Desktop

1. Go to the [Mevami repository page](https://github.com/s3vro-h1/mevami) on GitHub and click the green **Code** button, then select **Open with GitHub Desktop**. This will download the project to your computer.

2. Once it's open in GitHub Desktop, go to **Repository → Show in Explorer** (Windows) or **Repository → Show in Finder** (Mac) to open the folder.

3. Delete the hidden `.git` folder inside it — this cuts the connection to the original project:
   * **Windows:** You may need to enable "Show hidden items" in File Explorer first. Then simply delete the `.git` folder.
   * **Mac:** Press `⌘ + Shift + .` in Finder to show hidden files, then delete the `.git` folder.

4. Back in GitHub Desktop, go to **File → Add Local Repository** and select the folder. It will warn you that it's not a Git repository — click **Create a Repository** to start a fresh one.

5. Give it a name (like `mevami` or `my-setlist`), then click **Create Repository**.

6. Go to [GitHub.com/new](https://github.com/new) and create a new **empty** repository with the same name. **Do not check any boxes like "Initialize with a README."**

7. Back in GitHub Desktop, click **Publish repository** (top right). Make sure the name matches what you created on GitHub, then click **Publish**.

---

#### ⌨️ Using the Command Line

1. **Clone the project to your computer:**
```bash
git clone https://github.com/s3vro-h1/mevami.git
cd mevami
```

2. **Unrelate it from the original:** Delete the hidden .git folder (this wipes the connection to the original project):

* Windows (Command Prompt): `rmdir /s /q .git`

* Windows (PowerShell): `Remove-Item -Recurse -Force .git`

* Mac/Linux: `rm -rf .git`

3. Start your own history:

```bash
git init
git branch -M main
git add .
git commit -m "Initial commit"
```

4. **Connect to your own GitHub:** Go to [GitHub.com/new](https://github.com/new) and create a new empty repository. You can name it mevami or anything else you like (e.g., my-setlist, but for that you would have to rename also the older mevami to the new name of your repo). **Do not check any boxes like "Initialize with a README."**
Once created, run these commands in your terminal:

```bash
# Connect your local folder to your new GitHub repo
# Replace <your-username> and <repo-name> with your actual details!
git remote add origin https://github.com/<your-username>/<repo-name>.git

# Upload your files
git push -u origin main
```

---

### Step 6 — Point Mevami to Your Songs

Open the file called `config.py` in a text editor (Notepad works fine on Windows). You'll see this:

```python
SONGS_PATH = ""
OS = "LINUX"
```

Change it to match your setup:

- **`SONGS_PATH`** — the folder where your Clone Hero songs are stored. Examples:

  | System | Example |
  |--------|---------|
  | Windows | `C:/Users/YourName/Clone Hero/Songs` |
  | macOS | `/Users/YourName/Clone Hero/Songs` |
  | Linux | `/home/yourname/Clone Hero/Songs` |

  > **⚠️ Windows users:** Use forward slashes (`/`) in the path, not backslashes (`\`). Python can misread backslashes as special characters.

- **`OS`** — set it to `"LINUX"` if you're on Linux. For Windows or macOS, use `"WINDOWS"` or `"MAC"`.

Your finished `config.py` should look something like this:
```python
SONGS_PATH = "C:/Users/YourName/Clone Hero/Songs"
OS = "WINDOWS"
```

Save the file when you're done.

#### ✅ Test it!

Before moving on, let's make sure the scanner can actually find your songs. Open a terminal in the Mevami folder and run:

**Windows (Command Prompt):**
```
python generate_list.py
```

**Mac / Linux:**
```bash
python3 generate_list.py
```

If it works, you'll see it scanning your library and two files will be created: `data.json` and `genres.json`. If you get an error, double-check your `SONGS_PATH` — a typo there is the most common culprit.

---

### Step 7 — Enable Your Website

### 🌎 RECOMMENDED: GitHub Pages Setup
*Make your setlist accessible to anyone, anywhere.*
1. Go to your repository on GitHub.
2. Click **Settings** (the tab near the top of the page).
3. In the left sidebar, click **Pages**.
4. Under **Source**, select the `main` branch and the `/ (root)` folder.
5. Click **Save**.

Your website will be live at:
```
https://<your-username>.github.io/<name-of-your-repo>
```



> Note: It may take a minute or two the first time. After that, updates are much faster.

> 💡 **Tip:** Once your URL is live, you can generate a QR code at a site like [qr-code-generator.com](https://www.qr-code-generator.com/) so friends can scan their way straight to your setlist — no typing needed!


(This is how your github pages section should look like after a few minutes).
![Github Pages example](https://imgur.com/nhW1RAv.png)


### 🏠 Alternative: Local Hosting
*(Use this only if you don't want to use GitHub)*
 
> ⚠️ **I don't recommend this method.** Managing your local IP address is not ideal — it can change, it's easy to mistype, and some mobile devices can be finicky about connecting to local servers. If you want to reliably share your setlist with others, go with the GitHub Pages option instead.
 
That said, here's how it works if you still want to use it:
 
This option lets you browse your setlist locally on any device connected to your WiFi — no internet or GitHub needed.
 
1. Open a terminal in the Mevami folder and run:
   ```bash
   python -m http.server 8000
   ```
   This starts a simple local web server that serves the files in that folder. Leave the terminal open while you use it.
 
2. On the **same device**, you can open the setlist at:
   ```
   http://localhost:8000
   ```
 
3. To access it from **another device on the same WiFi** (like a friend's phone), you'll need your local IP address first. Find it with:
 
   | System | Command |
   |--------|---------|
   | Windows | `ipconfig` (look for "IPv4 Address") |
   | macOS / Linux | `ip a` or `ifconfig` |
 
   Then have them open:
   ```
   http://<your-local-ip>:8000
   ```
   For example: `http://192.168.1.42:8000`
 
4. When you're done, stop the server by pressing `Ctrl+C` in the terminal.
 
> 🔒 **Privacy note:** This is only accessible to devices on the same WiFi network and is not reachable from the internet. Still, be mindful that anyone on your network could access it while the server is running.

### 🌐 Advanced: Custom Domain

As I said before, If you already have a domain for your own website, I'm guessing you already know how to do it!

---

## Updating Your Setlist

### If you are using Git
Every time you add new songs to Clone Hero, just run the publish script. It will scan your library and update your website automatically.

#### On Mac or Linux

The first time only, you need to give the script permission to run. Open a terminal in the mevami folder and type:
```bash
chmod +x publish.sh
```

Then, every time you want to update:
```bash
./publish.sh
```

#### On Windows

Just double-click `publish.bat`. A window will open, do its thing, and close. Your site will update in about a minute.

### If you are using GitHub Desktop

1. **Run the scanner.** Open a terminal in the Mevami folder and run:

   **Windows:**
   ```
   python generate_list.py
   ```
   **Mac / Linux:**
   ```bash
   python3 generate_list.py
   ```
   This will regenerate `data.json` and `genres.json` with your new songs.

2. **Open GitHub Desktop.** You'll see the two updated files listed under "Changes".

3. At the bottom-left, type a short summary (e.g., `Update setlist`) and click **Commit to main**.

4. Click **Push origin** (top right) to upload the changes. Your website will update in about a minute.

---

## Customize your website!!

You can personalize your setlist page in two ways: directly from the website itself, or by editing the `config.json` file.

### 🎨 Using the Theme Panel (easiest way)

The website has a built-in **Theme panel** — no file editing needed. Just click the **🎨 Theme** button in the top bar of your setlist page. A side panel will open where you can pick colors for every part of the UI using color pickers, and see your changes live as you make them.

When you're happy with the result, click **⬇ Export config.json** to download a ready-to-use `config.json` with your chosen colors baked in. Replace the existing `config.json` in your Mevami folder with that file, then push the update so your hosted site reflects the new theme permanently.

> 💡 Colors are also saved in your browser automatically, so your customizations persist locally even before you export.

### ✏️ Editing `config.json` directly

You can also personalize your setlist page by editing the `config.json` file — no coding required. Open it with any text editor (Notepad, TextEdit, VS Code, anything works).

Here are some examples:
<center>
<img src="https://imgur.com/9mmGOiw.png" width="100%">
</center>


<center>
<img src="https://imgur.com/L153V5H.png" width="100%">
</center>

<center>
<img src="https://imgur.com/vb6WajS.png" width="100%">
</center>

Note: I no longer have the color codes for these examples, I've lost them, sorry.

You'll find three things you can change:

| Field | What it does |
|-------|--------------|
| `tabTitle` | The text shown on the browser tab |
| `appName` | The big title displayed at the top of the page. Wrap the part you want highlighted in `<span>…</span>` and it'll automatically pick up your primary color |
| `colors` | The full color palette of the site |

### 🎨 Colors

Inside the `colors` section you'll find these tokens:

| Token | What it controls |
|-------|-----------------|
| `primary` | Accent color — artist names, headings, active buttons, links |
| `song-name` | color of the name of the songs |
| `primaryDim` | A slightly darker accent, used for button borders and hovers |
| `primaryDark` | Dark tint of the accent, used for active button backgrounds |
| `bg` | Main page background |
| `surface` | Card and input backgrounds |
| `surface2` | Slightly lighter surface, used for hovers and the sort bar |
| `border` | Lines and outlines throughout the UI |
| `text` | Main readable text |
| `muted` | Secondary/subtle text — album names, stats, placeholders |

All values are standard **hex color codes** (e.g. `"#22d3ee"`). You can pick colors from any color picker online — [coolors.co](https://coolors.co) or [htmlcolorcodes.com](https://htmlcolorcodes.com/color-picker/) are great options.

> 💡 **Tip:** `primary`, `primaryDim`, and `primaryDark` should be three shades of the same color — light, medium, and dark — for the best look.

After saving `config.json`, how you apply the changes depends on how you're hosting:

- **Locally** — just refresh your browser, changes are instant.
- **GitHub Pages** — run the publish script or commit & push via GitHub Desktop. Your site will update in about a minute.
- **Custom domain/server** — upload the updated `config.json` to your server the same way you normally deploy files.
---

## QR code

Make it even easier for your friends to access your setlist! Just paste your website URL into this [QR code generator](https://www.qr-code-generator.com/) and it will create a QR code you can print out or pull up on your phone.

<center>
<img src="https://imgur.com/W4FL6zm.png" width="100%">
</center>

---

## Just one last thing & AI Agents Disclosure
I apologize if the setup guide is a bit long or has many options! I know many people visiting this page might not know anything about coding, Git, or GitHub, so I wanted to make sure everyone could get it to work. I hope the guide was clear enough.

I'm no professional web developer — I mainly know Python and like to experiment with code. The front-end was built with Claude's help, and the back-end had a few stubborn bugs I also leaned on it to sort out. This project started as something just for me, so I didn't stress too much about polish, so if you found some weird code or beahivour that coulod explain it.

I'm sure any front-end developer could build a much better interface with smarter ways to sort and display everything — and honestly, I'd love to see it. I'm planning to study a bit more about web development and improve things over time, without using the AI agents for this.

Contributions are very welcome! If you want to improve the front-end, add features, or fix bugs, feel free to open a pull request. No contribution is too small — whether it's a design improvement, a new sorting option, or just cleaning up something that bothered you.
If you're not sure where to start, the front-end is probably the area that could use the most love.

Have fun!!

-[S3VRO](https://github.com/s3vro-h1)

---

## License
This project is open-source and licensed under the GNU GPLv3. This is a copyleft license that requires anyone who distributes a modified version of this software to also make their source code available under the same license. See the LICENSE file for full details.