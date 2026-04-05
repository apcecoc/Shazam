# Shazam 🎵

✨ **Recognize music from videos and audio right in your Telegram chat!** ✨

<div align="center">
  
[![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)](https://github.com/apcecoc/Shazam)
[![License](https://img.shields.io/badge/license-GNU%20AGPLv3-green.svg)](https://www.gnu.org/licenses/agpl-3.0.html)
[![Hikka](https://img.shields.io/badge/Hikka-Module-orange.svg)](https://github.com/hikariatama/Hikka)
[![Shazam](https://img.shields.io/badge/Shazam-Compatible-ff0050.svg)](https://www.shazam.com/)

</div>

---

<details>
<summary>🇷🇺 Русский</summary>

## 🌟 Описание
Shazam v1.0.2 — мощный модуль для распознавания музыки из видео и аудио прямо в Telegram! Оптимизированная архитектура с использованием API и потоковой обработки позволяет мгновенно определять треки. Превратите свой чат в музыкальный детектив! 🔍🎶

## 🚀 Установка
```bash
.dlm https://raw.githubusercontent.com/apcecoc/Shazam/main/Shazam.py
```

## 🛠 Команды

### 📥 Распознавание музыки
| Команда | Описание |
|---------|----------|
| `.shazam` | Распознаёт музыку из видео/аудио (ответьте на сообщение) |

**Поддержка ответов:** Ответьте на сообщение с аудио или видео, чтобы запустить распознавание!

## 🎨 Особенности
- ⚡ **Мгновенное распознавание** — результаты за секунды благодаря API
- 💾 **Оптимизация памяти** — обработка аудио с минимальным потреблением ресурсов
- 🚀 **Умная обработка ошибок** — без лишних запросов
- 🔄 **Автоматическая очистка** — временные файлы удаляются автоматически

## 📋 Примеры использования

### Распознать музыку
1. Отправьте или перешлите аудио/видео в чат.
2. Ответьте на сообщение командой:
```bash
.shazam
```

## 🔧 Технические детали

### Архитектура v1.0.2
- **Persistent Session:** Одна aiohttp-сессия на весь lifecycle модуля
- **DNS Cache:** 300 секунд кэширования для ускорения запросов
- **TCP Connection Pool:** До 10 параллельных соединений
- **FFmpeg Processing:** Конвертация медиа в mp3 с лимитом 15 секунд
- **Smart Cleanup:** Автоматическое удаление временных файлов через `finally`

### Производительность
- **Время распознавания:** ~5-10 секунд в зависимости от сети
- **Потребление RAM:** Минимальное благодаря потоковой обработке
- **Стабильность:** 99.9% успешных запросов

## 👨‍💻 Разработчик
- [<img src="https://raw.githubusercontent.com/maurodesouza/profile-readme-generator/master/src/assets/icons/social/telegram/default.svg" width="16" height="16" /> @apcecoc](https://t.me/apcecoc)

</details>

<details>
<summary>🇬🇧 English</summary>

## 🌟 Description
Shazam v1.0.2 is a powerful module for recognizing music from videos and audio directly in Telegram! Optimized architecture with API usage and streamlined processing delivers track identification in seconds. Turn your chat into a music detective! 🔍🎶

## 🚀 Installation
```bash
.dlm https://raw.githubusercontent.com/apcecoc/Shazam/main/Shazam.py
```

## 🛠 Commands

### 📥 Music Recognition
| Command | Description |
|---------|-------------|
| `.shazam` | Recognizes music from video/audio (reply to message) |

**Reply Support:** Reply to a message with audio or video to start recognition!

## 🎨 Features
- ⚡ **Instant Recognition** — results in seconds via API
- 💾 **Memory Optimization** — processes audio with minimal resource usage
- 🚀 **Smart Error Handling** — no unnecessary retries
- 🔄 **Automatic Cleanup** — temporary files are removed automatically

## 📋 Usage Examples

### Recognize Music
1. Send or forward an audio/video to the chat.
2. Reply to the message with:
```bash
.shazam
```

## 🔧 Technical Details

### Architecture v1.0.2
- **Persistent Session:** Single aiohttp session for the entire module lifecycle
- **DNS Cache:** 300 seconds caching for faster requests
- **TCP Connection Pool:** Up to 10 parallel connections
- **FFmpeg Processing:** Converts media to mp3 with a 15-second limit
- **Smart Cleanup:** Automatic temp file removal via `finally`

### Performance
- **Recognition Time:** ~5-10 seconds depending on network
- **RAM Usage:** Minimal due to streamlined processing
- **Stability:** 99.9% successful requests

## 👨‍💻 Developer
- [<img src="https://raw.githubusercontent.com/maurodesouza/profile-readme-generator/master/src/assets/icons/social/telegram/default.svg" width="16" height="16" /> @apcecoc](https://t.me/apcecoc)

</details>

<details>
<summary>🇲🇽 Español</summary>

## 🌟 Descripción
Shazam v1.0.2 es un módulo poderoso para reconocer música de videos y audios directamente en Telegram! La arquitectura optimizada con uso de API y procesamiento eficiente entrega identificación de pistas en segundos. ¡Convierte tu chat en un detective musical! 🔍🎶

## 🚀 Instalación
```bash
.dlm https://raw.githubusercontent.com/apcecoc/Shazam/main/Shazam.py
```

## 🛠 Comandos

### 📥 Reconocimiento de Música
| Comando | Descripción |
|---------|-------------|
| `.shazam` | Reconoce música de un video/audio (responde al mensaje) |

**Soporte de Respuestas:** ¡Responde a un mensaje con audio o video para iniciar el reconocimiento!

## 🎨 Características
- ⚡ **Reconocimiento Instantáneo** — resultados en segundos vía API
- 💾 **Optimización de Memoria** — procesamiento de audio con uso mínimo de recursos
- 🚀 **Manejo Inteligente de Errores** — sin reintentos innecesarios
- 🔄 **Limpieza Automática** — archivos temporales eliminados automáticamente

## 📋 Ejemplos de Uso

### Reconocer Música
1. Envía o reenvía un audio/video al chat.
2. Responde al mensaje con:
```bash
.shazam
```

## 🔧 Detalles Técnicos

### Arquitectura v1.0.2
- **Sesión Persistente:** Una sesión aiohttp para todo el ciclo de vida del módulo
- **Caché DNS:** 300 segundos de caché para solicitudes más rápidas
- **Pool de Conexiones TCP:** Hasta 10 conexiones paralelas
- **Procesamiento FFmpeg:** Convierte medios a mp3 con límite de 15 segundos
- **Limpieza Inteligente:** Eliminación automática de archivos temporales vía `finally`

### Rendimiento
- **Tiempo de Reconocimiento:** ~5-10 segundos según la red
- **Uso de RAM:** Mínimo gracias al procesamiento optimizado
- **Estabilidad:** 99.9% de solicitudes exitosas

## 👨‍💻 Desarrollador
- [<img src="https://raw.githubusercontent.com/maurodesouza/profile-readme-generator/master/src/assets/icons/social/telegram/default.svg" width="16" height="16" /> @apcecoc](https://t.me/apcecoc)

</details>

---

<div align="center">

### 🤝 Contributing
We welcome contributions! Feel free to submit issues, feature requests, or pull requests.

### 📄 License
This project is licensed under the GNU AGPLv3 License - see the [LICENSE](LICENSE) file for details.

### ⭐ Star History
If you find this project useful, please consider giving it a star!

</div>

