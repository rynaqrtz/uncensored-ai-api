<div align="center">
  <img src="https://i.postimg.cc/Cx7RNJsQ/rynaqrtz.gif" alt="Uncensored AI API Banner" width="600">

  <h1>🔮 Uncensored AI API</h1>

  <p>
    <strong>Unofficial REST API & CLI wrapper</strong> untuk <a href="https://uncensored.ai">uncensored.ai</a><br>
    Akses model <strong>Anubis 70B</strong> via reverse-engineered Supabase Edge Function.<br>
    Auto auth · Multi-turn context · Real-time streaming · CLI-first
  </p>

  <p>
    <a href="https://github.com/rynaqrtz/uncensored-ai-api/stargazers">
      <img src="https://img.shields.io/github/stars/rynaqrtz/uncensored-ai-api?style=for-the-badge&color=FFD700&logo=github&logoColor=white" alt="Stars">
    </a>
    <a href="https://github.com/rynaqrtz/uncensored-ai-api/network/members">
      <img src="https://img.shields.io/github/forks/rynaqrtz/uncensored-ai-api?style=for-the-badge&color=4A90E2&logo=git&logoColor=white" alt="Forks">
    </a>
    <a href="https://github.com/rynaqrtz/uncensored-ai-api/issues">
      <img src="https://img.shields.io/github/issues/rynaqrtz/uncensored-ai-api?style=for-the-badge&color=E74C3C" alt="Issues">
    </a>
    <a href="https://github.com/rynaqrtz/uncensored-ai-api/commits/main">
      <img src="https://img.shields.io/github/last-commit/rynaqrtz/uncensored-ai-api?style=for-the-badge&color=2ECC71" alt="Last Commit">
    </a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/version-1.0.0-0969da?style=flat-square" alt="Version">
    <img src="https://img.shields.io/badge/node-%3E%3D18.x-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node">
    <img src="https://img.shields.io/badge/model-Anubis%2070B-7C3AED?style=flat-square" alt="Model">
    <img src="https://img.shields.io/badge/auth-Supabase%20JWT-3ECF8E?style=flat-square&logo=supabase&logoColor=white" alt="Auth">
    <img src="https://img.shields.io/badge/stream-SSE%20✓-F97316?style=flat-square" alt="Streaming">
  </p>
</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Fitur Unggulan](#-fitur-unggulan)
- [Tech Stack](#-tech-stack)
- [Statistik & Spesifikasi](#-statistik--spesifikasi)
- [Quick Start](#-quick-start)
- [Instalasi](#-instalasi)
- [CLI Usage](#-cli-usage)
- [Response Format](#-response-format)
- [Deploy ke Vercel](#️-deploy-ke-vercel)
- [Deploy ke VPS (Express)](#-deploy-ke-vps-expressjs)
- [Arsitektur & Reverse Engineering](#-arsitektur--reverse-engineering)
- [Struktur Proyek](#-struktur-proyek)
- [Error Handling](#-error-handling)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [Disclaimer](#️-disclaimer)

---

## 🌟 Overview

**Uncensored AI API** adalah wrapper CLI dan REST API yang membungkus endpoint internal [uncensored.ai](https://uncensored.ai) — sebuah platform yang menyediakan model **Anubis 70B** tanpa system prompt restrictif. Dibangun dengan hasil reverse engineering React SPA + Supabase Edge Function.

> 💡 **Use case:** Integrasi model AI ke project Node.js, bot, atau aplikasi web tanpa perlu urus autentikasi Supabase manual — semua dihandle otomatis.

**Kenapa pakai ini?**

- ✅ Zero konfigurasi — langsung jalan dengan satu command
- ✅ Auto signup + token refresh tanpa intervensi manual
- ✅ Multi-turn context memory otomatis tersimpan lokal
- ✅ Streaming output real-time ala ChatGPT
- ✅ Siap deploy serverless di Vercel dalam hitungan menit

---

## ✨ Fitur Unggulan

| Fitur | Deskripsi |
|-------|-----------|
| 🔄 **Auto Signup + Token Refresh** | Jika token expired, sistem otomatis signup akun baru. Token dipersist di `.unces_token.json` |
| 🧠 **Context Memory** | Percakapan multi-turn disimpan di `.unces_context.json`. Gunakan `--new` untuk reset sesi |
| ⚡ **Real-time Streaming** | Output muncul saat AI "mengetik" via Server-Sent Events (SSE). Gunakan `--json` untuk output batch |
| 🧹 **Clean Output** | Auto-strip mojibake, control characters, dan whitespace berlebih dari response raw SSE |
| 📦 **Modular Export** | Fungsi `chat()` bisa di-import langsung ke project Express/Vercel/Next.js lain |
| 💻 **CLI First-class** | Semua opsi (temp, max tokens, reset context) tersedia langsung dari terminal |

---

## 🛠 Tech Stack

| Teknologi | Versi | Kegunaan |
|-----------|-------|----------|
| **Node.js** | `≥ 18.x` | Runtime |
| **node-fetch** | `^2.7.0` | HTTP client — SSE streaming + Supabase calls |
| **Supabase Auth** | — | JWT access token + auto refresh |
| **Vercel** | — | Serverless deployment |

---

## 📊 Statistik & Spesifikasi

| Parameter | Nilai |
|-----------|-------|
| **Model** | Anubis 70B (`uaia18lqf6dn-drummer-anubis-70b-1-1-copy`) |
| **Provider** | Supabase Edge Function |
| **Max Tokens** | 100,000 (kustomisasi via `--max`) |
| **Temperature Range** | 0.0 – 2.0 (default `1.2`) |
| **Auth Mechanism** | Supabase JWT — expire 1 jam, auto-refresh |
| **Streaming Protocol** | Server-Sent Events (SSE) |
| **Context Storage** | Local JSON (`.unces_context.json`) |
| **Token Storage** | Local JSON (`.unces_token.json`) |
| **Fallback Endpoint** | `chat-backup` (non-streaming) jika SSE gagal |

---

## ⚡ Quick Start

```bash
git clone https://github.com/rynaqrtz/uncensored-ai-api.git
cd uncensored-ai-api
npm install
node unces.js "Halo, siapa kamu?"
```

Pertama kali jalan, sistem auto-signup akun Supabase dan simpan token. Request berikutnya langsung pakai token tersimpan.

---

## 📦 Instalasi

**Requirements:** Node.js `≥ 18.x`, npm atau yarn

```bash
# 1. Clone
git clone https://github.com/rynaqrtz/uncensored-ai-api.git
cd uncensored-ai-api

# 2. Install dependencies
npm install

# 3. Test
node unces.js "Jelaskan cara kerja neural network"
```

---

## 💻 CLI Usage

```bash
node unces.js [options] "prompt"
```

### Options

| Option | Alias | Tipe | Default | Keterangan |
|--------|-------|------|---------|------------|
| `--new` | `-n` | flag | `false` | Reset context, mulai sesi baru |
| `--json` | `-j` | flag | `false` | Output JSON terstruktur (non-streaming) |
| `--temp <n>` | — | float | `1.2` | Temperature: 0.0 (deterministik) – 2.0 (kreatif) |
| `--max <n>` | — | int | `100000` | Batas maksimum token output |

### Contoh Penggunaan

```bash
# Basic prompt
node unces.js "Jelaskan sejarah internet secara detail"

# Mulai sesi baru (reset context)
node unces.js --new "Halo, nama saya Andi"

# Lanjut sesi — AI ingat nama kamu
node unces.js "Siapa nama saya tadi?"

# JSON output + temperature tinggi
node unces.js --json --temp 1.8 "Tulis cerita fiksi sci-fi"

# Batasi panjang output
node unces.js --max 5000 "Rangkum teori relativitas Einstein"

# Kombinasi flags
node unces.js --new --json --temp 0.5 --max 20000 "Analisis algoritma quicksort"
```

### Alur Context Memory

```
Sesi baru: node unces.js --new "Nama saya Budi"
           └─ Simpan ke .unces_context.json
           
Lanjut:    node unces.js "Siapa saya?"
           └─ Load .unces_context.json → AI ingat "Budi"

Reset:     node unces.js --new "Kita mulai ulang"
           └─ Hapus .unces_context.json lama
```

---

## 📄 Response Format

### Streaming Mode (default)

Output muncul karakter per karakter langsung di terminal saat AI merespons.

### JSON Mode (`--json`)

```json
{
  "success": true,
  "model": "anubis-70b",
  "content": "Jawaban lengkap dari AI ada di sini...",
  "creator": "rynaqrtz",
  "max_tokens_sent": 100000,
  "output_length": 15234,
  "word_count": 2105
}
```

### Error Response

```json
{
  "success": false,
  "creator": "rynaqrtz",
  "error": "Token expired and signup failed: 429 Too Many Requests"
}
```

---

## ☁️ Deploy ke Vercel

### 1. Clone & Install

```bash
git clone https://github.com/rynaqrtz/uncensored-ai-api.git
cd uncensored-ai-api
npm install
```

### 2. Buat `api/chat.js`

```javascript
const { chat } = require('../unces');

module.exports = async (req, res) => {
  const { prompt, new: newChat, temp, max } = req.query;

  if (!prompt) {
    return res.status(400).json({ success: false, error: 'Parameter "prompt" diperlukan' });
  }

  try {
    const result = await chat(prompt, {
      newChat: newChat === 'true',
      temperature: parseFloat(temp) || 1.2,
      maxTokens: parseInt(max) || 100000,
      stream: false,
    });
    res.status(200).json(result);
  } catch (e) {
    res.status(500).json({ success: false, error: e.message, creator: 'rynaqrtz' });
  }
};
```

### 3. `vercel.json`

```json
{
  "version": 2,
  "functions": {
    "api/chat.js": {
      "runtime": "nodejs18.x",
      "memory": 512,
      "maxDuration": 30
    }
  },
  "rewrites": [
    { "source": "/api/chat", "destination": "/api/chat" }
  ]
}
```

### 4. Deploy

```bash
npm i -g vercel
vercel --prod
```

### 5. Gunakan API

```bash
curl "https://your-project.vercel.app/api/chat?prompt=Halo+siapa+kamu"
curl "https://your-project.vercel.app/api/chat?prompt=Analisis+data+ini&new=true&temp=0.7"
curl "https://your-project.vercel.app/api/chat?prompt=Cerita+pendek&max=5000&temp=1.8"
```

> ⚠️ **Vercel Free Tier:** Execution limit **30 detik** (dengan konfigurasi `maxDuration` di atas). Untuk prompt yang menghasilkan output sangat panjang (>50k token), pertimbangkan Railway atau VPS.

---

## 🖥 Deploy ke VPS (Express.js)

```bash
npm install express
```

Buat `server.js`:

```javascript
const express = require('express');
const { chat } = require('./unces');

const app = express();

app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET');
  next();
});

app.get('/api/chat', async (req, res) => {
  const { prompt, new: newChat, temp, max } = req.query;

  if (!prompt) {
    return res.status(400).json({ success: false, error: 'prompt required' });
  }

  try {
    const result = await chat(prompt, {
      newChat: newChat === 'true',
      temperature: parseFloat(temp) || 1.2,
      maxTokens: parseInt(max) || 100000,
      stream: false,
    });
    res.json(result);
  } catch (e) {
    res.status(500).json({ success: false, error: e.message, creator: 'rynaqrtz' });
  }
});

app.listen(3000, () => console.log('🚀 Uncensored AI API running at http://localhost:3000'));
```

### Production dengan PM2

```bash
npm install -g pm2
pm2 start server.js --name uncensored-ai-api
pm2 save && pm2 startup
```

---

## 🔬 Arsitektur & Reverse Engineering

### Alur Request

```
Client (CLI / HTTP GET)
       │
       ▼
  unces.js
       │
       ├─ Cek .unces_token.json
       │     ├─ Tidak ada / Expired → POST /auth/v1/signup (auto)
       │     └─ Ada → gunakan existing token
       │
       ├─ Load .unces_context.json (multi-turn history)
       │
       ▼
  POST https://mkstqjtsujvcaobdksxs.supabase.co/functions/v1/chat-streaming
       Headers: Authorization: Bearer <jwt_access_token>
                apikey: <supabase_anon_key>
       Body: {
         messages: [...context, { role: "user", content: prompt }],
         systemPrompt: "...",
         stream: true,
         temperature: 1.2,
         max_tokens: 100000
       }
       │
       ▼
  SSE Stream: data: {"choices":[{"delta":{"content":"token"}}]}
       │
       ├─ Streaming mode → print langsung ke stdout
       └─ JSON mode → buffer semua token → return JSON
       │
       ▼
  Simpan context ke .unces_context.json
```

### Komponen Internal

| Komponen | Detail |
|----------|--------|
| **Auth Endpoint** | `POST /auth/v1/signup` dengan email acak |
| **Token Type** | JWT access token + refresh token |
| **Token Expire** | 1 jam — auto-refresh via signup baru |
| **Chat Endpoint** | `supabase.co/functions/v1/chat-streaming` |
| **Model ID** | `uaia18lqf6dn-drummer-anubis-70b-1-1-copy` |
| **Stream Protocol** | Server-Sent Events — `data: {...}\n\n` |
| **Fallback** | `chat-backup` endpoint (non-streaming) |
| **Token Storage** | `.unces_token.json` di direktori kerja |
| **Context Storage** | `.unces_context.json` di direktori kerja |

### Headers yang Diperlukan

```http
POST /functions/v1/chat-streaming HTTP/1.1
Host: mkstqjtsujvcaobdksxs.supabase.co
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

---

## ⚠️ Error Handling

| HTTP Code | Situasi |
|:---------:|---------|
| `200` | Sukses |
| `400` | Parameter `prompt` tidak ada |
| `401` | Token expired dan signup gagal |
| `429` | Rate limit dari Supabase — terlalu banyak signup |
| `500` | Error internal scraper / network issue |
| `504` | Timeout di Vercel |

---

## ❓ FAQ

**Q: Apakah perlu akun uncensored.ai?**

Tidak. Sistem auto-signup akun baru setiap kali diperlukan. Kamu tidak perlu punya akun manual.

---

**Q: Token saya expired, apa yang terjadi?**

Sistem otomatis signup akun baru dan simpan token fresh ke `.unces_token.json`. Proses ini transparan.

---

**Q: Apa itu `.unces_token.json` dan `.unces_context.json`?**

Dua file lokal yang disimpan di direktori kerja:
- `.unces_token.json` — JWT access token dari Supabase
- `.unces_context.json` — History percakapan multi-turn

Keduanya otomatis dikelola oleh scraper. Tidak perlu diedit manual. Jangan di-commit ke git (sudah ada di `.gitignore`).

---

**Q: Kenapa temperature default-nya 1.2?**

Model Anubis 70B merespons lebih baik di temperature sedikit di atas 1.0. Di bawah 0.5 cenderung terlalu deterministik, di atas 1.8 mulai inkoheren. Range sweet spot: `0.7 – 1.5`.

---

**Q: Bisa dipakai di production dengan traffic tinggi?**

Tidak disarankan. Ini bukan API resmi — tidak ada SLA, rate limit bisa berubah sewaktu-waktu, dan bergantung pada ketersediaan endpoint Supabase milik pihak ketiga.

---

**Q: Kenapa `node-fetch` versi 2 dan bukan 3?**

node-fetch v3 adalah ESM-only. Karena proyek ini menggunakan CommonJS (`require`), versi 2 lebih kompatibel tanpa perlu ubah ke `import`.

---

## 🤝 Contributing

Pull request sangat welcome. Untuk perubahan besar, buka issue dulu.

```bash
# 1. Fork repo
# 2. Buat branch baru
git checkout -b feat/nama-fitur

# 3. Commit dengan pesan yang jelas
git commit -m "feat: tambah support streaming di Vercel via chunked response"

# 4. Push
git push origin feat/nama-fitur

# 5. Buat Pull Request
```

---

## ⚠️ Disclaimer

Proyek ini dibuat murni untuk **tujuan edukasi dan penelitian reverse engineering**. Bukan produk resmi dari uncensored.ai atau Supabase. Tidak ada jaminan ketersediaan layanan. Segala risiko penggunaan menjadi tanggung jawab pengguna sepenuhnya.

---

<div align="center">
  <br>
  <p>
    <strong>Made with ❤️ by <a href="https://github.com/rynaqrtz">rynaqrtz</a></strong>
  </p>
  <p>
    <sub>⭐ Star repo ini kalau berguna buat kamu!</sub>
  </p>
</div>
