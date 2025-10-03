import discord
from discord.ext import commands
from flask import Flask, request
import threading
import asyncio
import config
from datetime import datetime

# === CONFIGURATION ===
CHANNEL_ID = 1423608926955372594  # Discord channel ID
EVENT_COLORS = {
    "push": discord.Color.green(),
    "pull_request": discord.Color.blue(),
    "issues": discord.Color.orange()
}
FOOTER_TEXT = "GitHub Event • Open Source Bot"

# === discord bot ===
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# === flask webserver ===
app = Flask(__name__)

@app.route("/github", methods=["POST"])
def github_webhook():
    payload = request.json

    # handle push events
    if "commits" in payload:
        repo = payload["repository"]["full_name"]
        repo_url = payload["repository"]["html_url"]
        pusher = payload["pusher"]["name"]
        branch = payload.get("ref", "").split("/")[-1] if "ref" in payload else "unknown"
        commits = payload["commits"]

        # create embed
        embed = discord.Embed(
            title=f"📦 Push in {repo}:{branch}",
            url=repo_url,
            description=f"**{pusher}** pushed {len(commits)} commit(s)",
            color=EVENT_COLORS.get("push", discord.Color.default()),
            timestamp=datetime.utcnow()
        )

        # add commit list with changed files
        for c in commits:
            msg = c["message"]
            url = c["url"]
            author = c["author"]["name"]

            # collect file changes
            files = []
            if "added" in c and c["added"]:
                files.extend([f"+ {f}" for f in c["added"]])
            if "modified" in c and c["modified"]:
                files.extend([f"~ {f}" for f in c["modified"]])
            if "removed" in c and c["removed"]:
                files.extend([f"- {f}" for f in c["removed"]])

            # limit to 5 entries
            file_preview = "\n".join(files[:5])
            if len(files) > 5:
                file_preview += f"\n… and {len(files) - 5} more"

            value = f"[{msg}]({url})\n```diff\n{file_preview or 'No file changes'}\n```"

            embed.add_field(
                name=f"✏️ {author}",
                value=value,
                inline=False
            )

        # author avatar if available
        if "sender" in payload and "avatar_url" in payload["sender"]:
            embed.set_thumbnail(url=payload["sender"]["avatar_url"])

        embed.set_footer(text=FOOTER_TEXT)

        # send embed to channel
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            asyncio.run_coroutine_threadsafe(channel.send(embed=embed), bot.loop)

    return "OK", 200

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# === start ===
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(config.TOKEN)