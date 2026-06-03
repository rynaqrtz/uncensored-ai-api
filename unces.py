import requests
import json
import os
import sys
import time
import codecs
import argparse

SUPA_URL = "https://mkstqjtsujvcaobdksxs.supabase.co"
SUPA_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1rc3RxanRzdWp2Y2FvYmRrc3hzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI3NzQyNjksImV4cCI6MjA2ODM1MDI2OX0.suu2A2fAcdJfAG0dOjOjWLfU6BXxNSn5GrbiSSmUiw0"
TOKENS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".unces_tokens.json")
CONTEXT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".unces_context.json")
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

def signup():
    email = f"r_{int(time.time())}_{os.urandom(3).hex()}@mail.com"
    pwd = "Ryn4Qrtz!2024"
    r = requests.post(f"{SUPA_URL}/auth/v1/signup", headers={
        "apikey": SUPA_KEY, "Content-Type": "application/json"
    }, json={"email": email, "password": pwd}, timeout=15)
    data = r.json()
    if r.status_code != 200 or not data.get("access_token"):
        raise Exception(data.get("msg", "Signup failed"))
    return {
        "email": email,
        "password": pwd,
        "refresh_token": data["refresh_token"],
        "access_token": data["access_token"],
        "expires_at": data.get("expires_at", 0),
        "created_at": int(time.time()),
        "usage_count": 0,
    }

def load_tokens():
    tokens = load_json(TOKENS_FILE) or []
    if isinstance(tokens, dict):
        tokens = [tokens]
    return tokens

def save_tokens(tokens):
    save_json(TOKENS_FILE, tokens)

def get_active_token(tokens):
    for td in tokens:
        if time.time() < td.get("expires_at", 0) - 60:
            return td, tokens
    new_td = signup()
    tokens.append(new_td)
    save_tokens(tokens)
    return new_td, tokens

def rotate_account(tokens, old_token):
    print("\n[!] Quota habis — beralih ke akun baru...", file=sys.stderr)
    tokens = [t for t in tokens if t.get("access_token") != old_token.get("access_token")]
    new_td = signup()
    tokens.append(new_td)
    save_tokens(tokens)
    return new_td, tokens

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

    endpoint = f"{SUPA_URL}/functions/v1/chat-streaming"

    for attempt in range(3):
        r = requests.post(endpoint, headers=headers, json=payload, stream=True, timeout=180)

        if r.status_code == 200:
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
        else:
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
    args = parser.parse_args()

    if args.list_accounts:
        tokens = load_tokens()
        print(f"Jumlah akun tersimpan: {len(tokens)}")
        for i, td in enumerate(tokens):
            print(f"  [{i}] {td.get('email')} — {td.get('usage_count', 0)} usage")
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