# discord-github-notifier 
*A lightweight GitHub → Discord bridge bot.*

`discord-github-notifier` is an simple open-source **Discord bot** that listens to GitHub webhooks and posts them as rich Discord embeds.  
Perfect for keeping your team up-to-date with **commits, file changes, pull requests, and issues** – directly inside your Discord server.

---

## ✨ Features
- 📦 **Push events** → show commits with author, message, and changed files
- 🔀 **Pull requests** → (planned) title, author, status, and PR link
- 📝 **Issues** → (planned) new issues, comments, and updates
- 🎨 **Customizable** embed colors, footer text, and formatting
- 🖼️ **Rich embeds** with commit previews and GitHub avatars
- ⚡ Built with **Flask** + **discord.py**

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/lul-v3/discord-github-notifier.git
cd discord-github-notifier
```

### 2. Install dependencies
```Bash
pip install discord.py flask
```

### 3. Configuration
A ``config.py`` file is already included.
Simply open it and add your Discord bot token:
```Bash
TOKEN = "YOUR_DISCORD_BOT_TOKEN"
```
Make sure to also set the **Discord Channel ID** in ``main.py``.

### 4. Run the bot
```Bash
python main.py
```

### 5. Setup ngrok (for local testing)
```Bash
ngrok http 5000
```
Use the generated HTTPS URL in your GitHub repo webhook settings:
``https://<your-ngrok-id>.ngrok-free.app/github``

## 🔧 GitHub Webhook Setup
1. Go to your GitHub repository → **Settings** → **Webhooks** → **Add webhook**
2. **Payload URL** → ``https://<your-ngrok-id>.ngrok-free.app/github``
3. **Content type** → ``application/json``
4. **Events** → `Just the push event` (or `Send me everything`)

## 📸 Preview
Here’s an example of how a push event looks inside Discord:<br>
![preview](https://raw.githubusercontent.com/lul-v3/discord-github-notifier/refs/heads/main/_github/img/preview.png?token=GHSAT0AAAAAADI5KTXIBJMOIELSFUMIZPX42G7UWEQ)

## ⚙️ Customization
You can easily change:
- Event colors (``EVENT_COLORS`` in ``main.py``)
- Footer text (``FOOTER_TEXT``)
- Discord Channel ID
- Extend with more GitHub event handlers
