__version__ = (1, 0, 2)

#        █████  ██████   ██████ ███████  ██████  ██████   ██████ 
#       ██   ██ ██   ██ ██      ██      ██      ██    ██ ██      
#       ███████ ██████  ██      █████   ██      ██    ██ ██      
#       ██   ██ ██      ██      ██      ██      ██    ██ ██      
#       ██   ██ ██       ██████ ███████  ██████  ██████   ██████

#              © Copyright 2026
#           https://t.me/apcecoc
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @apcecoc
# requires: aiohttp shazamio ffmpeg

from telethon.types import Message
from telethon.errors.rpcerrorlist import DocumentInvalidError
from .. import loader, utils
import tempfile
import os
import subprocess
import urllib.parse
import asyncio
from shazamio import Shazam as ShazamIO

@loader.tds
class Shazam(loader.Module):
    strings = {
        "name": "Shazam",
        "_cls_doc": "Recognize music from video/audio messages",
        "no_reply": "Reply to a video or audio message! 📹🔊",
        "invalid_media": "This is not audio or video! ❌",
        "audio_too_large": "Audio clip exceeds 4MB limit! 📏",
        "no_match": "No music match found! 🎵❌",
        "result_header": "Title: {} 🎵\nArtist: {} 👤\nShazam URL: <a href='{}'>Link</a> 🔗\n🔗Listen on:\n<emoji document_id=5233578612665375810>🎵</emoji> {}\n<emoji document_id=5321505140199418151>🎥</emoji> {}",
        "processing": "Processing your audio with Shazam <emoji document_id=5346259862814734771>📱</emoji>{}",
        "processing_fallback": "Processing your audio with Shazam 📱{}",
        "api_error": "Processing error: {}",
    }

    strings_ru = {
        "_cls_doc": "Распознавание музыки из видео/аудио сообщений",
        "no_reply": "Ответьте на видео или аудио сообщение! 📹🔊",
        "invalid_media": "Это не аудио или видео! ❌",
        "audio_too_large": "Аудио клип превышает лимит 4MB! 📏",
        "no_match": "Музыка не распознана! 🎵❌",
        "result_header": "Название: {} 🎵\nИсполнитель: {} 👤\nURL Shazam: <a href='{}'>Ссылка</a> 🔗\n🔗Слушать на:\n<emoji document_id=5233578612665375810>🎵</emoji> {}\n<emoji document_id=5321505140199418151>🎥</emoji> {}",
        "processing": "Обработка аудио с Shazam <emoji document_id=5346259862814734771>📱</emoji>{}",
        "processing_fallback": "Обработка аудио с Shazam 📱{}",
        "api_error": "Ошибка обработки: {}",
    }

    strings_mx = {
        "_cls_doc": "Reconocimiento de música de mensajes de video/audio",
        "no_reply": "¡Responde a un mensaje de video o audio! 📹🔊",
        "invalid_media": "¡Esto no es audio ni video! ❌",
        "audio_too_large": "¡El clip de audio excede el límite de 4MB! 📏",
        "no_match": "¡No se encontró coincidencia de música! 🎵❌",
        "result_header": "Título: {} 🎵\nArtista: {} 👤\nURL de Shazam: <a href='{}'>Enlace</a> 🔗\n🔗Escuchar en:\n<emoji document_id=5233578612665375810>🎵</emoji> {}\n<emoji document_id=5321505140199418151>🎥</emoji> {}",
        "processing": "Procesando tu audio con Shazam <emoji document_id=5346259862814734771>📱</emoji>{}",
        "processing_fallback": "Procesando tu audio con Shazam 📱{}",
        "api_error": "Error de procesamiento: {}",
    }

    @loader.command(
        ru_doc="Распознать музыку из видео/аудио (ответьте на сообщение)",
        mx_doc="Reconocer música de un video/audio (responde al mensaje)",
        en_doc="Recognize music from video/audio (reply to message)"
    )
    async def shazam(self, message: Message):
        if not message.reply_to_msg_id:
            await utils.answer(message, self.strings("no_reply"), parse_mode="html")
            return

        reply = await message.get_reply_message()
        if not (reply.audio or reply.video or reply.voice or reply.document and "audio" in reply.document.mime_type):
            await utils.answer(message, self.strings("invalid_media"), parse_mode="html")
            return

        try:
            status_message = await utils.answer(message, self.strings("processing").format("..."), parse_mode="html")
        except DocumentInvalidError:
            status_message = await utils.answer(message, self.strings("processing_fallback").format("..."), parse_mode="html")

        async def update_progress():
            dots = ["...", "....", "....."]
            for i in range(30):
                await asyncio.sleep(1)
                try:
                    await utils.answer(status_message, self.strings("processing").format(dots[i % 3]), parse_mode="html")
                except DocumentInvalidError:
                    await utils.answer(status_message, self.strings("processing_fallback").format(dots[i % 3]), parse_mode="html")

        progress_task = asyncio.create_task(update_progress())
        file_path = None

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                ext = ''
                if reply.video:
                    ext = '.mp4'
                elif reply.audio:
                    ext = '.mp3'
                elif reply.voice:
                    ext = '.ogg'
                elif reply.document:
                    mime = reply.document.mime_type.lower()
                    if 'video' in mime:
                        ext = '.mp4'
                    elif 'mp3' in mime or 'mpeg' in mime:
                        ext = '.mp3'
                    elif 'ogg' in mime:
                        ext = '.ogg'

                input_path = os.path.join(temp_dir, "input" + ext)
                await self._client.download_media(reply, input_path)

                if not os.path.exists(input_path):
                    raise ValueError("Failed to download media! 🚫")

                mp3_path = os.path.join(temp_dir, "audio.mp3")
                duration = 15

                subprocess.run(
                    [
                        "ffmpeg",
                        "-i", input_path,
                        "-ss", "0",
                        "-t", str(duration),
                        "-b:a", "256k",
                        "-f", "mp3",
                        mp3_path
                    ],
                    check=True,
                    capture_output=True
                )

                if os.path.getsize(mp3_path) > 4 * 1024 * 1024:
                    raise ValueError(self.strings("audio_too_large"))

                # Распознавание через локальную библиотеку ShazamIO
                shazam_client = ShazamIO()
                out = await shazam_client.recognize(mp3_path)

                if not out or "track" not in out:
                    raise ValueError(self.strings("no_match"))

                track = out["track"]
                title = track.get("title", "Unknown")
                artist = track.get("subtitle", "Unknown") # В shazamio артист обычно находится в subtitle
                shazam_url = track.get("url", "")

                query = urllib.parse.quote(f"{title} {artist}")
                
                # Дефолтные ссылки, как в вашем старом коде
                spotify_link = f"<a href='https://open.spotify.com/search/{query}'>Open in Spotify</a>"
                youtube_link = f"<a href='https://music.youtube.com/search?q={query}&feature=shazam'>Open in YouTube Music</a>"

                # Пытаемся вытянуть оригинальный Spotify URI, если он есть
                providers = track.get("hub", {}).get("providers", [])
                for provider in providers:
                    if provider.get("type") == "SPOTIFY":
                        uri = provider.get("actions", [{}])[0].get("uri", "")
                        if uri.startswith("spotify:search:"):
                            spotify_query = uri.split("spotify:search:")[1]
                            spotify_link = f"<a href='https://open.spotify.com/search/{spotify_query}'>Open in Spotify</a>"
                        break

                result = self.strings("result_header").format(
                    title,
                    artist,
                    shazam_url,
                    spotify_link,
                    youtube_link
                )

                progress_task.cancel()
                await utils.answer(status_message, result, parse_mode="html")

        except subprocess.CalledProcessError as e:
            progress_task.cancel()
            await utils.answer(status_message, f"Error processing audio with ffmpeg: {e.stderr.decode()}", parse_mode="html")
        except FileNotFoundError:
            progress_task.cancel()
            await utils.answer(status_message, "ffmpeg not found! Install it in your environment. ⚠️", parse_mode="html")
        except ValueError as e:
            progress_task.cancel()
            await utils.answer(status_message, str(e), parse_mode="html")
        except Exception as e:
            progress_task.cancel()
            await utils.answer(status_message, self.strings("api_error").format(str(e)), parse_mode="html")