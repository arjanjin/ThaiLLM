# ThaiLLM Pathumma Chat

Web chat interface and CLI for the [ThaiLLM Pathumma API](https://thaillm.or.th).

## Features

- **Streaming responses** — text streams in real-time like ChatGPT
- **Markdown rendering** — code blocks with syntax highlighting and copy button
- **System prompt** — customize the AI's role (e.g. HR assistant, language tutor)
- **Dark / Light mode** — toggle with preference saved in browser
- **Chat history** — save, load, and delete conversations (stored as JSON)
- **Export** — download chat as `.txt` or print to PDF

## Setup

### 1. Clone and create virtual environment

```bash
git clone https://github.com/arjanjin/ThaiLLM.git
cd ThaiLLM
python -m venv venv
```

### 2. Activate virtual environment

```bash
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API credentials

Create a `.env` file in the project root:

```env
THAILLM_API_KEY=your_api_key_here
THAILLM_CONSUMER_ID=your_consumer_id_here
```

## Usage

### Web UI

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### CLI Chatbot

```bash
python main.py
```

## Project Structure

```
ThaiLLM/
├── app.py               # Flask web server
├── main.py              # CLI chatbot
├── thaillm_client.py    # API client (chat + streaming)
├── templates/
│   └── index.html       # Web UI
├── chats/               # Saved conversations (gitignored)
├── requirements.txt
└── .env                 # API credentials (gitignored)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat/stream` | Stream a chat response (SSE) |
| `GET`  | `/api/history` | List saved chats |
| `POST` | `/api/history/save` | Save current conversation |
| `GET`  | `/api/history/<id>` | Load a saved conversation |
| `DELETE` | `/api/history/<id>` | Delete a saved conversation |

## Requirements

- Python 3.8+
- ThaiLLM API key and Consumer ID from [thaillm.or.th](https://thaillm.or.th)
