import os
import time
import wget
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(
    filters.command(["yt"])
)
async def youtube_downloader(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a YouTube link.")
        return
    link = message.command[1]
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(link, download=False)
        title = info["title"]
        formats = info["formats"]

    qualities = [2160, 1440, 1080, 720, 480, 360]
    available_qualities = []
    for q in qualities:
        for f in formats:
            if f.get("height") == q:
                available_qualities.append(q)
                break
    
    if not available_qualities:
        await message.reply_text("No suitable video formats found.")
        return
    
    buttons = []
    for q in available_qualities:
        buttons.append([InlineKeyboardButton(f"{q}p", callback_data=f"download_{q}")])
    await message.reply_text(
        f"Video: {title}\nSelect the desired quality:",
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True
    )


@Client.on_callback_query(
    filters.regex("download_(360|480|720|1080|1440|2160)")
)
async def callback_query_handler(client, callback_query):
    quality = int(callback_query.data.split("_")[1])
    link = callback_query.message.reply_to_message.text.split(" ", maxsplit=1)[1]
    
    download_message = await callback_query.message.edit_text("Download started. Please wait...")
    start_time = time.time()
    
    ydl_opts = {
        "format": f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]",
        "merge_output_format": "mp4",
        "outtmpl": "downloads/%(title)s.%(ext)s",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)
        output_file = ydl.prepare_filename(info_dict)
        duration = info_dict.get("duration")
        thumbnails = info_dict.get("thumbnails", [])
        jpg_thumbnails = [t for t in thumbnails if t["url"].endswith(".jpg")][-1]["url"]
        print(jpg_thumbnails)
    thumb = wget.download(jpg_thumbnails)
    await download_message.edit_text("Download completed. Video is being sent...")
    await callback_query.message.reply_video(
        video=output_file,
        caption=f"Video downloaded in {quality}p quality.",
        duration=duration,
        thumb=thumb
    )

    await download_message.delete()
    if os.path.exists(output_file):
        os.remove(output_file)
    if os.path.exists(thumb):
        os.remove(thumb)
