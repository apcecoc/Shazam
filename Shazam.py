__version__ = (1, 0, 0)

#        █████  ██████   ██████ ███████  ██████  ██████   ██████ 
#       ██   ██ ██   ██ ██      ██      ██      ██    ██ ██      
#       ███████ ██████  ██      █████   ██      ██    ██ ██      
#       ██   ██ ██      ██      ██      ██      ██    ██ ██      
#       ██   ██ ██       ██████ ███████  ██████  ██████   ██████

#              © Copyright 2025
#           https://t.me/apcecoc
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @apcecoc
# requires: aiohttp

from telethon.types import Message
from telethon.errors.rpcerrorlist import DocumentInvalidError
from .. import loader, utils
import tempfile
import os
import subprocess
import aiohttp
import random
import string
import urllib.parse
import asyncio

@loader.tds
class Shazam(loader.Module):
    strings = {
        "name": "Shazam",
        "_cls_doc": "Recognize music from video/audio messages",
        "no_reply": "Reply to a video or audio message! 📹🔊",
        "invalid_media": "This is not audio or video! ❌",
        "audio_too_large": "Audio clip exceeds 4MB limit! 📏",
        "upload_error": "Error during upload: {}",
        "no_url": "Could not extract upload URL! 🔗",
        "api_error": "API request failed: {} (Status: {}, Response: {})",
        "no_match": "No music match found! 🎵❌",
        "result_header": "Title: {} 🎵\nArtist: {} 👤\nShazam URL: <a href='{}'>Link</a> 🔗\n🔗Listen on:\n<emoji document_id=5233578612665375810>🎵</emoji> {}\n<emoji document_id=5321505140199418151>🎥</emoji> {}",
        "processing": "Processing your audio with Shazam <emoji document_id=5346259862814734771>📱</emoji>{}",
        "processing_fallback": "Processing your audio with Shazam 📱{}",
    }

    strings_ru = {
        "_cls_doc": "Распознавание музыки из видео/аудио сообщений",
        "no_reply": "Ответьте на видео или аудио сообщение! 📹🔊",
        "invalid_media": "Это не аудио или видео! ❌",
        "audio_too_large": "Аудио клип превышает лимит 4MB! 📏",
        "upload_error": "Ошибка при загрузке: {}",
        "no_url": "Не удалось извлечь URL загрузки! 🔗",
        "api_error": "Ошибка запроса API: {} (Статус: {}, Ответ: {})",
        "no_match": "Музыка не распознана! 🎵❌",
        "result_header": "Название: {} 🎵\nИсполнитель: {} 👤\nURL Shazam: <a href='{}'>Ссылка</a> 🔗\n🔗Слушать на:\n<emoji document_id=5233578612665375810>🎵</emoji> {}\n<emoji document_id=5321505140199418151>🎥</emoji> {}",
        "processing": "Обработка аудио с Shazam <emoji document_id=5346259862814734771>📱</emoji>{}",
        "processing_fallback": "Обработка аудио с Shazam 📱{}",
    }

    strings_mx = {
        "_cls_doc": "Reconocimiento de música de mensajes de video/audio",
        "no_reply": "¡Responde a un mensaje de video o audio! 📹🔊",
        "invalid_media": "¡Esto no es audio ni video! ❌",
        "audio_too_large": "¡El clip de audio excede el límite de 4MB! 📏",
        "upload_error": "Error al subir: {}",
        "no_url": "¡No se pudo extraer la URL de carga! 🔗",
        "api_error": "Error en la solicitud de API: {} (Estado: {}, Respuesta: {})",
        "no_match": "¡No se encontró coincidencia de música! 🎵❌",
        "result_header": "Título: {} 🎵\nArtista: {} 👤\nURL de Shazam: <a href='{}'>Enlace</a> 🔗\n🔗Escuchar en:\n<emoji document_id=5233578612665375810>🎵</emoji> {}\n<emoji document_id=5321505140199418151>🎥</emoji> {}",
        "processing": "Procesando tu audio con Shazam <emoji document_id=5346259862814734771>📱</emoji>{}",
        "processing_fallback": "Procesando tu audio con Shazam 📱{}",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "upload_api",
                "https://api.apcecoc.pp.ua/music-to-url",
                lambda: "API endpoint for audio upload"
            )
        )
        self._session = None
        self._timeout = aiohttp.ClientTimeout(total=60, connect=10)

    async def client_ready(self):
        self._session = aiohttp.ClientSession(
            timeout=self._timeout,
            connector=aiohttp.TCPConnector(limit=10, ttl_dns_cache=300)
        )

    async def on_unload(self):
        if self._session and not self._session.closed:
            await self._session.close()

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

        def rand_str(length):
            return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

        file_path = None
        try:
            if not self._session or self._session.closed:
                self._session = aiohttp.ClientSession(
                    timeout=self._timeout,
                    connector=aiohttp.TCPConnector(limit=10, ttl_dns_cache=300)
                )

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

                form = aiohttp.FormData()
                form.add_field('file', open(mp3_path, 'rb'))
                async with self._session.post(self.config["upload_api"], data=form) as response:
                    response.raise_for_status()
                    upload_data = await response.json()
                    audio_url = upload_data.get("url")
                    if not audio_url:
                        raise ValueError(self.strings("no_url"))
                    audio_url = urllib.parse.urljoin(audio_url, urllib.parse.urlparse(audio_url).path.replace('//', '/'))

                headers = {
                    "Content-Type": "application/json"
                }
                async with self._session.get("https://api.paxsenix.org/tools/shazam", params={"url": audio_url}, headers=headers) as resp:
                    resp.raise_for_status()
                    data = await resp.json()

                if not data.get("ok") or "track" not in data:
                    raise ValueError(self.strings("no_match"))

                track = data["track"]
                title = track.get("title", "Unknown")
                artist = track.get("artist", "Unknown")
                shazam_url = track.get("url", "")

                hub = data.get("hub", [])
                spotify_link = ""
                youtube_link = ""
                query = urllib.parse.quote(f"{title} {artist}")

                if hub:
                    for h in hub:
                        if "actions" in h and h["actions"] and "type" in h:
                            uri = h["actions"][0]["uri"]
                            caption = h["caption"]
                            if h["type"] == "SPOTIFY" and uri.startswith("spotify:search:"):
                                spotify_query = uri.split("spotify:search:")[1]
                                uri = f"https://open.spotify.com/search/{spotify_query}"
                                spotify_link = f"<a href='{uri}'>{caption}</a>"
                            elif h["type"] == "YOUTUBEMUSIC":
                                youtube_link = f"<a href='{uri}'>{caption}</a>"

                if not spotify_link:
                    spotify_link = f"<a href='https://open.spotify.com/search/{query}'>Open in Spotify</a>"
                if not youtube_link:
                    youtube_link = f"<a href='https://music.youtube.com/search?q={query}&feature=shazam'>Open in YouTube Music</a>"

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
        except aiohttp.ClientError as e:
            progress_task.cancel()
            await utils.answer(status_message, self.strings("upload_error").format(str(e)), parse_mode="html")
        except ValueError as e:
            progress_task.cancel()
            await utils.answer(status_message, str(e), parse_mode="html")
        except Exception as e:
            progress_task.cancel()
            await utils.answer(status_message, self.strings("api_error").format(str(e), resp.status if 'resp' in locals() else 'N/A', await resp.text() if 'resp' in locals() else 'N/A'), parse_mode="html")
        finally:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError:
                    pass