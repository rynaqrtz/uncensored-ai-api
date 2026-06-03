<div align="center">
  <img src="https://i.postimg.cc/Cx7RNJsQ/rynaqrtz.gif" alt="Uncensored AI API Banner" width="600">

  <h1>🔮 Uncensored AI API</h1>

  <p>
    <strong>Unofficial REST API & CLI wrapper</strong> untuk <a href="https://uncensored.ai">uncensored.ai</a><br>
    Akses model <strong>Anubis 70B</strong> via reverse-engineered Supabase Edge Function.<br>
    <strong>No limits. No filters. No restrictions.</strong>
  </p>

  <p>
    <a href="https://github.com/rynaqrtz/uncensored-ai-api/stargazers">
      <img src="https://img.shields.io/github/stars/rynaqrtz/uncensored-ai-api?style=for-the-badge&color=FFD700&logo=github&logoColor=white" alt="Stars">
    </a>
    <a href="https://github.com/rynaqrtz/uncensored-ai-api/network/members">
      <img src="https://img.shields.io/github/forks/rynaqrtz/uncensored-ai-api?style=for-the-badge&color=4A90E2" alt="Forks">
    </a>
    <a href="https://github.com/rynaqrtz/uncensored-ai-api/issues">
      <img src="https://img.shields.io/github/issues/rynaqrtz/uncensored-ai-api?style=for-the-badge&color=E74C3C" alt="Issues">
    </a>
    <img src="https://img.shields.io/badge/version-2.0.0-blue?style=flat-square" alt="Version">
    <img src="https://img.shields.io/badge/model-Anubis%2070B-7C3AED?style=flat-square" alt="Model">
    <img src="https://img.shields.io/badge/auth-Supabase%20JWT-3ECF8E?style=flat-square&logo=supabase&logoColor=white" alt="Auth">
    <img src="https://img.shields.io/badge/stream-SSE%20✓-F97316?style=flat-square" alt="Streaming">
    <img src="https://img.shields.io/badge/creator-rynaqrtz-orange?style=flat-square" alt="Creator">
  </p>
</div>

---

## 🌟 Overview

**Uncensored AI API** adalah wrapper CLI dan REST API yang membungkus endpoint internal [uncensored.ai](https://uncensored.ai) — platform yang menyediakan model **Anubis 70B** tanpa system prompt restrictif. Dibangun dari hasil reverse engineering React SPA + Supabase Edge Function.

> 💡 **Use case:** Integrasi model AI ke project Python, bot, atau aplikasi web tanpa perlu urus autentikasi Supabase manual.

**Kenapa pakai ini?**

- ✅ **Zero konfigurasi** — langsung jalan dengan satu command
- ✅ **Auto signup + token refresh** — tidak perlu daftar manual
- ✅ **Multi-account pool** — rotasi akun otomatis saat quota habis
- ✅ **Circuit breaker** — mencegah ban dengan backoff otomatis
- ✅ **Multi-turn context memory** — percakapan tersimpan otomatis
- ✅ **Streaming output real-time** — ala ChatGPT
- ✅ **Siap deploy serverless** — Vercel, VPS, Termux
- ✅ **Prompt uncensored penuh** — tidak ada filter moral/etika/hukum

---

## ✨ Fitur Unggulan

| Fitur | Deskripsi |
|-------|-----------|
| 🔄 **Auto Signup + Token Refresh** | Token expired? Sistem otomatis signup akun baru. Token dipersist di `.unces_tokens.json` |
| 🧠 **Context Memory** | Percakapan multi-turn disimpan di `.unces_context.json`. Gunakan `--new` untuk reset sesi |
| 👥 **Multi-Account Pool** | Kumpulan akun disimpan & dirotasi otomatis. `--list` untuk lihat, `--prewarm N` untuk isi ulang |
| ⚡ **Circuit Breaker** | Jika gagal 5x berturut-turut, sistem pause 30 detik sebelum coba lagi — mencegah ban |
| 🌐 **Proxy Support** | Baca file `.unces_proxies.txt`, satu proxy per baris. Otomatis dipakai saat signup |
| ⚡ **Real-time Streaming** | Output muncul saat AI "mengetik" via Server-Sent Events |
| 📦 **Modular** | Fungsi `chat()` bisa di-import langsung ke project lain |
| 💻 **CLI First-class** | Semua opsi (temp, max tokens, reset context, force new account) langsung dari terminal |

---

## 🛠 Tech Stack

| Teknologi | Kegunaan |
|-----------|----------|
| **Python 3.8+** | Runtime utama |
| **requests** | HTTP client — SSE streaming + Supabase calls |
| **Supabase Auth** | JWT access token + auto refresh |
| **Vercel** | Serverless deployment |

---

## 📊 Spesifikasi

| Parameter | Nilai |
|-----------|-------|
| **Model** | Anubis 70B (`uaia18lqf6dn-drummer-anubis-70b-1-1-copy`) |
| **Provider** | Supabase Edge Function |
| **Max Tokens** | 100,000 (kustomisasi via `--max`) |
| **Temperature** | 0.0 – 2.0 (default `0.9`) |
| **Auth** | Supabase JWT — expire 1 jam, auto-refresh |
| **Streaming** | Server-Sent Events (SSE) |
| **Context** | Local JSON (`.unces_context.json`) |
| **Token Storage** | Local JSON (`.unces_tokens.json`) |

---

## ⚡ Quick Start

```bash
git clone https://github.com/rynaqrtz/uncensored-ai-api.git
cd uncensored-ai-api
pip install -r requirements.txt
python unces.py "Halo, siapa kamu?"
```

Pertama kali jalan, sistem auto-signup akun Supabase dan simpan token. Request berikutnya langsung pakai token tersimpan.

---

📦 Instalasi

Requirements: Python ≥ 3.8

```bash
git clone https://github.com/rynaqrtz/uncensored-ai-api.git
cd uncensored-ai-api
pip install -r requirements.txt
python unces.py "Jelaskan cara kerja neural network"
```

---

💻 CLI Usage

```bash
python unces.py [options] "prompt"
```

Options

Option Alias Default Keterangan
--new -n false Reset context, mulai sesi baru
--json -j false Output JSON terstruktur
--temp <n> — 0.9 Temperature: 0.0 – 2.0
--max <n> — 100000 Batas maksimum token output
--force-new — false Paksa buat akun baru
--list — — Lihat daftar akun tersimpan
--prewarm <n> — — Isi ulang pool akun (N akun baru)

Contoh

```bash
python unces.py "Jelaskan sejarah internet"

python unces.py --new "Halo, nama saya Andi"
python unces.py "Siapa nama saya tadi?"

python unces.py --json --temp 1.8 "Tulis cerita fiksi sci-fi"

python unces.py --max 5000 "Rangkum teori relativitas Einstein"

python unces.py --list
python unces.py --prewarm 10
python unces.py --force-new "Prompt dengan akun baru"
```

---

🌐 Proxy Support

Buat file .unces_proxies.txt di direktori yang sama dengan unces.py. Isi satu proxy per baris:

```
http://user:pass@proxy1.com:8080
http://user:pass@proxy2.com:8080
socks5://127.0.0.1:9050
```

Proxy akan dipakai secara acak saat signup akun baru.

---

📄 Response Format

Streaming Mode (default)

Output muncul langsung di terminal saat AI merespons.

JSON Mode (--json)

```json
{
  "success": true,
  "model": "anubis-70b",
  "content": "Jawaban lengkap dari AI...",
  "creator": "rynaqrtz",
  "output_length": 15234,
  "word_count": 2105,
  "account": "r_1748917200_a1b2c3@mail.com"
}
```

---

☁️ Deploy ke Vercel

1. Clone & Install

```bash
git clone https://github.com/rynaqrtz/uncensored-ai-api.git
cd uncensored-ai-api
```

2. Deploy

```bash
vercel --prod
```

3. Gunakan API

```
GET https://your-project.vercel.app/api/chat?prompt=Halo+siapa+kamu
GET https://your-project.vercel.app/api/chat?prompt=Cerita+pendek&new=true&temp=1.5&max=5000
```

---

🖥 Deploy ke VPS (Flask)

```python
from flask import Flask, request, jsonify
from unces import chat

app = Flask(__name__)

@app.route('/api/chat')
def api_chat():
    prompt = request.args.get('prompt', '')
    if not prompt:
        return jsonify({"error": "prompt required"}), 400
    new_chat = request.args.get('new', 'false') == 'true'
    temp = float(request.args.get('temp', 0.9))
    max_tokens = int(request.args.get('max', 100000))
    result = chat(prompt, temperature=temp, max_tokens=max_tokens, new_chat=new_chat, stream=False)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=3000)
```

---

🔬 Arsitektur & Reverse Engineering

```
Client (CLI / HTTP GET)
       │
       ▼
  unces.py
       │
       ├─ Cek .unces_tokens.json
       │     ├─ Tidak ada / Expired → POST /auth/v1/signup (auto)
       │     └─ Ada → gunakan existing token
       │
       ├─ Load .unces_context.json (multi-turn history)
       │
       ▼
  POST https://mkstqjtsujvcaobdksxs.supabase.co/functions/v1/chat-streaming
       Body: {
         messages: [...],
         systemPrompt: "...",
         stream: true,
         temperature: 0.9,
         max_tokens: 100000
       }
       │
       ▼
  SSE Stream: data: {"choices":[{"delta":{"content":"token"}}]}
       │
       ├─ Streaming mode → print langsung
       └─ JSON mode → buffer semua token → return JSON
```

---

🗂️ Struktur Proyek

```
uncensored-ai-api/
├── unces.py                 # Module utama + CLI
├── api/
│   └── chat.py              # Handler Vercel
├── requirements.txt         # requests
├── vercel.json              # Konfigurasi deploy
├── .unces_tokens.json       # Pool akun (auto-generated)
├── .unces_context.json      # History percakapan (auto-generated)
├── .unces_proxies.txt       # Daftar proxy (opsional)
├── README.md
```

---

<div align="center">
  <br>
  <p>
    <strong>Made with ❤️ by <a href="https://github.com/rynaqrtz">rynaqrtz:p</a></strong>
  </p>
  <p>
    <sub>⭐ Star repo ini kalau berguna buat kamu^^!</sub>
  </p>
</div>
