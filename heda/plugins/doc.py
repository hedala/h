import os
import aiohttp
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from heda import paste

supported_extensions = [
    ".txt", ".py", ".js", ".html", ".css", ".json", ".xml", ".csv", ".tsv",
    ".md", ".rst", ".ini", ".cfg", ".yaml", ".yml", ".toml", ".log", ".sql",
    ".php", ".rb", ".java", ".cpp", ".c", ".h", ".sh", ".bat", ".ps1", ".vb",
    ".swift", ".kt", ".go", ".rs", ".scala", ".pl", ".lua", ".r", ".m", ".vba",
    ".cs", ".fs", ".coffee", ".ts", ".dart", ".tex", ".hs", ".lhs", ".agda",
    ".asm", ".clj", ".erl", ".ex", ".exs", ".hrl", ".lisp", ".rkt", ".ss", ".scm"
]

@Client.on_message(filters.command("open"))
async def open_file(client, message: Message):
    if message.reply_to_message and message.reply_to_message.document:
        doc = message.reply_to_message.document
        file_name = doc.file_name
        file_extension = os.path.splitext(file_name)[1].lower()

        if file_extension in supported_extensions:
            file_path = await client.download_media(message.reply_to_message)
            with open(file_path, "r") as file:
                content = file.read()
            
            if len(content) <= 4090:
                await message.reply(f"```\n{content}```", parse_mode=enums.ParseMode.MARKDOWN)
            else:
                paste_url = await paste.dpaste(content)
                if paste_url:
                    await message.reply(f"Dosya içeriği çok uzun. İçeriğe şu adresten ulaşabilirsiniz: {paste_url}")
                else:
                    await message.reply("Dosya içeriği yüklenirken bir hata oluştu.")
            
            os.remove(file_path)
        else:
            await message.reply("Desteklenmeyen dosya türü.")
    else:
        await message.reply("Lütfen bir dosyayı yanıtlayın.")

@Client.on_message(filters.command("doc"))
async def create_document(client, message: Message):
    if message.reply_to_message:
        text = message.reply_to_message.text
        file_name = message.text.split(" ", maxsplit=1)[1]
        if text and file_name:
        with open(file_name, "w") as file:
            file.write(text)
        
        await message.reply_document(file_name)
        os.remove(file_name)
    else:
        await message.reply("Lütfen bir metni yanıtlayın.")
        
