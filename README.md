<div align="center">
  <img src="https://i.postimg.cc/Cx7RNJsQ/rynaqrtz.gif" alt="Uncensored AI API Banner" width="600">

  <h1>🔮 Uncensored AI API</h1>

  <p>
    <strong>Unofficial REST API & CLI wrapper</strong> untuk <a href="https://uncensored.ai">uncensored.ai</a><br>
    Akses model <strong>Anubis 70B</strong> via reverse-engineered Supabase Edge Function.<br>
    Auto auth · Multi-turn context · Real-time streaming · CLI-first
  </p>

  <p>
    <a href="https://github.com/rynaqrtz/ai-collection/stargazers">
      <img src="https://img.shields.io/github/stars/rynaqrtz/ai-collection?style=for-the-badge&color=FFD700" alt="Stars">
    </a>
    <a href="https://github.com/rynaqrtz/ai-collection/network/members">
      <img src="https://img.shields.io/github/forks/rynaqrtz/ai-collection?style=for-the-badge&color=4A90E2" alt="Forks">
    </a>
    <img src="https://img.shields.io/badge/version-1.0.0-blue?style=flat-square" alt="Version">
    <img src="https://img.shields.io/badge/model-Anubis%2070B-7C3AED?style=flat-square" alt="Model">
    <img src="https://img.shields.io/badge/creator-rynaqrtz-orange?style=flat-square" alt="Creator">
  </p>
</div>

---

## 🌟 Overview

**Uncensored AI API** membungkus endpoint internal uncensored.ai — model **Anubis 70B** tanpa filter. Hasil reverse engineering React SPA + Supabase Edge Function.

- ✅ Zero konfigurasi
- ✅ Auto signup + token refresh
- ✅ Multi-turn context memory
- ✅ Streaming output real-time
- ✅ Siap deploy Vercel

---

## ⚡ Quick Start

```bash
git clone https://github.com/rynaqrtz/ai-collection.git
cd ai-collection/uncensored-ai
pip install -r requirements.txt
python unces.py "Halo, siapa kamu?"
```

---

💻 CLI Usage

```bash
python unces.py [options] "prompt"
```

Option Default Keterangan
--new, -n false Reset context
--json, -j false Output JSON
--temp <n> 0.9 Temperature (0-2)
--max <n> 100000 Max tokens

---

☁️ Deploy Vercel

```bash
vercel --prod
```

```
GET /api/chat?prompt=Halo+siapa+kamu
GET /api/chat?prompt=Cerita+pendek&new=true&temp=1.5
```

---

📄 Response Format

```json
{
  "success": true,
  "model": "anubis-70b",
  "content": "Jawaban dari AI...",
  "creator": "rynaqrtz"
}
```

---

<div align="center">
  <strong>Made with ❤️ by <a href="https://github.com/rynaqrtz">rynaqrtz</a></strong>
</div>