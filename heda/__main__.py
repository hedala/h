
import asyncio
from pyrogram import idle

from heda import heda, log
from heda.config import LogConfig
from heda.utils.heroku import heroku, git

async def main():
    log(__name__).info("Bot starting...")
    await git()
    heroku()
    await heda.start()
    log(__name__).info("Bot started.")
    await heda.send_message(LogConfig.LOG_CHAT_ID, "`Bot başlatıldı.`")
    await idle()
    log(__name__).info("Bot stopping...")
    await heda.stop()
    log(__name__).info("Bot stopped.")


if __name__ == "__main__":
    heda.run(main())
