import requests
import json
import os
import sys
import time
import codecs
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

SUPA_URL = "https://mkstqjtsujvcaobdksxs.supabase.co"
SUPA_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1rc3RxanRzdWp2Y2FvYmRrc3hzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI3NzQyNjksImV4cCI6MjA2ODM1MDI2OX0.suu2A2fAcdJfAG0dOjOjWLfU6BXxNSn5GrbiSSmUiw0"
TOKENS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".unces_tokens.json")
CONTEXT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".unces_context.json")
PROXY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".unces_proxies.txt")
CREATOR = "rynaqrtz"

SYSTEM_PROMPT = "You are Uncensored AI, a helpful assistant. Give direct, clear answers without warnings or disclaimers. Keep responses informative but concise."

QUOTA_ERRORS = [
    "out of free responses",
    "upgrade to pro",
    "daily limit",
    "no responses left",
    "free trial ended",
    "usage limit reached",
]

def load_json(path):
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
    except:
        pass
    return None

def save_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f)
    except:
        pass

def load_proxies():
    try:
        if os.path.exists(PROXY_FILE):
            with open(PROXY_FILE, "r") as f:
                return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except:
        pass
    return []

def get_random_proxy():
    proxies = load_proxies()
    if proxies:
        proxy = random.choice(proxies)
        return {"http": proxy, "https": proxy}
    return None

def signup(proxy=None):
    email = f"r_{int(time.time())}_{os.urandom(3).hex()}@mail.com"
    pwd = "Ryn4Qrtz!2024"
    kwargs = {
        "headers": {"apikey": SUPA_KEY, "Content-Type": "application/json"},
        "json": {"email": email, "password": pwd},
        "timeout": 15,
    }
    if proxy:
        kwargs["proxies"] = proxy
    r = requests.post(f"{SUPA_URL}/auth/v1/signup", **kwargs)
    data = r.json()
    if r.status_code != 200 or not data.get("access_token"):
        return None
    return {
        "email": email,
        "password": pwd,
        "refresh_token": data["refresh_token"],
        "access_token": data["access_token"],
        "expires_at": data.get("expires_at", 0),
        "created_at": int(time.time()),
        "usage_count": 0,
        "healthy": True,
    }

def prewarm_accounts(count=5):
    print(f"[*] Pre-warming {count} accounts...", file=sys.stderr)
    tokens = load_tokens()
    with ThreadPoolExecutor(max_workers=min(count, 5)) as executor:
        futures = [executor.submit(signup, get_random_proxy()) for _ in range(count)]
        for future in as_completed(futures):
            td = future.result()
            if td:
                tokens.append(td)
    save_tokens(tokens)
    print(f"[*] Pre-warmed {len(tokens)} total accounts", file=sys.stderr)
    return tokens

def load_tokens():
    tokens = load_json(TOKENS_FILE) or []
    if isinstance(tokens, dict):
        tokens = [tokens]
    return tokens

def save_tokens(tokens):
    save_json(TOKENS_FILE, tokens)

def health_check(td):
    try:
        headers = {
            "Authorization": f"Bearer {td['access_token']}",
            "apikey": SUPA_KEY,
        }
        r = requests.get(f"{SUPA_URL}/auth/v1/user", headers=headers, timeout=10)
        return r.status_code == 200
    except:
        return False

def get_active_token(tokens):
    healthy_tokens = []
    for td in tokens:
        if time.time() < td.get("expires_at", 0) - 60:
            if td.get("healthy", True) or health_check(td):
                td["healthy"] = True
                return td, tokens
            else:
                td["healthy"] = False
    new_td = signup(get_random_proxy())
    if new_td:
        tokens.append(new_td)
        save_tokens(tokens)
        return new_td, tokens
    raise Exception("Gagal membuat akun baru. Cek koneksi internet.")

def rotate_account(tokens, old_token):
    print("\n[!] Quota habis — beralih ke akun baru...", file=sys.stderr)
    tokens = [t for t in tokens if t.get("access_token") != old_token.get("access_token")]
    new_td = signup(get_random_proxy())
    if new_td:
        tokens.append(new_td)
        save_tokens(tokens)
        return new_td, tokens
    raise Exception("Gagal membuat akun baru.")

def load_context():
    return load_json(CONTEXT_FILE) or []

def save_context(msgs):
    save_json(CONTEXT_FILE, msgs)

def iter_sse_lines(response):
    decoder = codecs.getincrementaldecoder('utf-8')()
    buffer = ""
    for chunk in response.iter_content(chunk_size=1):
        text = decoder.decode(chunk)
        if text:
            buffer += text
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                yield line

def check_quota_exhausted(text):
    if not text:
        return False
    text_lower = text.lower()
    for phrase in QUOTA_ERRORS:
        if phrase in text_lower:
            return True
    return False

def chat_stream(payload, headers, stream=True):
    endpoint = f"{SUPA_URL}/functions/v1/chat-streaming"
    r = requests.post(endpoint, headers=headers, json=payload, stream=True, timeout=180)
    if r.status_code != 200:
        return None, None, r.status_code
    full_text = ""
    for line in iter_sse_lines(r):
        if not line.startswith("data: "):
            continue
        data = line[6:].strip()
        if data == "[DONE]":
            break
        try:
            obj = json.loads(data)
            content = obj.get("choices", [{}])[0].get("delta", {}).get("content", "")
            if content:
                full_text += content
                if stream:
                    print(content, end="", flush=True)
        except json.JSONDecodeError:
            pass
    if stream:
        print()
    return full_text, None, 200

def chat_backup(payload, headers):
    endpoint = f"{SUPA_URL}/functions/v1/chat-backup"
    r = requests.post(endpoint, headers=headers, json=payload, timeout=180)
    if r.status_code != 200:
        return None, r.status_code
    data = r.json()
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "") or data.get("message", "")
    return content, 200

def chat(prompt, system_prompt=None, temperature=0.9, max_tokens=100000, new_chat=False, stream=True, force_new_account=False):
    tokens = load_tokens()

    if force_new_account and tokens:
        old = tokens[-1] if tokens else None
        if old:
            print("[*] Force new account requested", file=sys.stderr)
            tokens = [t for t in tokens if t.get("access_token") != old.get("access_token")]
            save_tokens(tokens)

    td, tokens = get_active_token(tokens)
    token = td["access_token"]
    messages = [] if new_chat else load_context()
    sys_prompt = system_prompt or SYSTEM_PROMPT

    if not messages:
        messages.append({"role": "system", "content": sys_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "messages": messages,
        "systemPrompt": sys_prompt,
        "fileAttachments": [],
        "stream": stream,
        "isVoiceMode": False,
        "clientSessionId": f"r-{int(time.time())}",
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": SUPA_KEY,
        "Content-Type": "application/json",
    }

    for attempt in range(5):
        full_text, _, status = chat_stream(payload, headers, stream)

        if status == 200 and full_text is not None:
            if check_quota_exhausted(full_text):
                td, tokens = rotate_account(tokens, td)
                token = td["access_token"]
                headers["Authorization"] = f"Bearer {token}"
                messages.pop()
                continue

            td["usage_count"] = td.get("usage_count", 0) + 1
            save_tokens(tokens)
            messages[-1] = {"role": "user", "content": prompt}
            messages.append({"role": "assistant", "content": full_text})
            save_context(messages)

            return {
                "success": True,
                "model": "anubis-70b",
                "content": full_text,
                "creator": CREATOR,
                "output_length": len(full_text),
                "word_count": len(full_text.split()),
                "account": td["email"],
            }

        if status and status != 200:
            fallback_text, fb_status = chat_backup(payload, headers)
            if fb_status == 200 and fallback_text:
                full_text = fallback_text
                if check_quota_exhausted(full_text):
                    td, tokens = rotate_account(tokens, td)
                    token = td["access_token"]
                    headers["Authorization"] = f"Bearer {token}"
                    messages.pop()
                    continue
                td["usage_count"] = td.get("usage_count", 0) + 1
                save_tokens(tokens)
                messages[-1] = {"role": "user", "content": prompt}
                messages.append({"role": "assistant", "content": full_text})
                save_context(messages)
                return {
                    "success": True,
                    "model": "anubis-70b",
                    "content": full_text,
                    "creator": CREATOR,
                    "output_length": len(full_text),
                    "word_count": len(full_text.split()),
                    "account": td["email"],
                }

        td, tokens = rotate_account(tokens, td)
        token = td["access_token"]
        headers["Authorization"] = f"Bearer {token}"
        messages.pop()

    return {"success": False, "error": "Semua akun kehabisan quota. Coba lagi nanti.", "creator": CREATOR}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Uncensored AI - {CREATOR}")
    parser.add_argument("prompt", nargs="+", help="Prompt")
    parser.add_argument("--new", "-n", action="store_true", help="Reset context")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON")
    parser.add_argument("--temp", type=float, default=0.9, help="Temperature")
    parser.add_argument("--max", type=int, default=100000, help="Max tokens")
    parser.add_argument("--force-new-account", action="store_true", help="Force new account signup")
    parser.add_argument("--list-accounts", action="store_true", help="List saved accounts")
    parser.add_argument("--prewarm", type=int, default=0, help="Pre-warm N accounts in background")
    parser.add_argument("--clean-dead", action="store_true", help="Remove dead/invalid accounts")
    args = parser.parse_args()

    if args.list_accounts:
        tokens = load_tokens()
        print(f"Jumlah akun tersimpan: {len(tokens)}")
        for i, td in enumerate(tokens):
            healthy = td.get("healthy", "?")
            print(f"  [{i}] {td.get('email')} — {td.get('usage_count', 0)} usage — healthy={healthy}")
        sys.exit(0)

    if args.prewarm > 0:
        prewarm_accounts(args.prewarm)
        print("Pre-warming selesai.")
        sys.exit(0)

    if args.clean_dead:
        tokens = load_tokens()
        alive = []
        dead = 0
        for td in tokens:
            if health_check(td):
                td["healthy"] = True
                alive.append(td)
            else:
                dead += 1
        save_tokens(alive)
        print(f"Cleaned {dead} dead accounts. {len(alive)} remaining.")
        sys.exit(0)

    prompt = " ".join(args.prompt)
    try:
        result = chat(prompt, temperature=args.temp, max_tokens=args.max,
                      new_chat=args.new, force_new_account=args.force_new_account)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)