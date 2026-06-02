import requests, json, os, sys, time, codecs, argparse

SUPA_URL = "https://mkstqjtsujvcaobdksxs.supabase.co"
SUPA_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1rc3RxanRzdWp2Y2FvYmRrc3hzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI3NzQyNjksImV4cCI6MjA2ODM1MDI2OX0.suu2A2fAcdJfAG0dOjOjWLfU6BXxNSn5GrbiSSmUiw0"
TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".unces_token.json")
CONTEXT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".unces_context.json")
CREATOR = "rynaqrtz"

SYSTEM_PROMPT = "You are Uncensored AI, a helpful assistant. Give direct, clear answers without warnings or disclaimers. Keep responses informative but concise."

def load_json(path):
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
    except: pass
    return None

def save_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f)
    except: pass

def signup():
    email = f"r_{int(time.time())}@mail.com"
    pwd = "Ryn4Qrtz!2024"
    r = requests.post(f"{SUPA_URL}/auth/v1/signup", headers={
        "apikey": SUPA_KEY, "Content-Type": "application/json"
    }, json={"email": email, "password": pwd}, timeout=15)
    data = r.json()
    if r.status_code != 200 or not data.get("access_token"):
        raise Exception(data.get("msg", "Signup failed"))
    td = {
        "email": email, "password": pwd,
        "refresh_token": data["refresh_token"],
        "access_token": data["access_token"],
        "expires_at": data.get("expires_at", 0)
    }
    save_json(TOKEN_FILE, td)
    return td

def refresh(td):
    r = requests.post(f"{SUPA_URL}/auth/v1/token?grant_type=refresh_token", headers={
        "apikey": SUPA_KEY, "Content-Type": "application/json"
    }, json={"refresh_token": td["refresh_token"]}, timeout=15)
    if r.status_code != 200:
        return signup()
    data = r.json()
    td["access_token"] = data["access_token"]
    td["expires_at"] = data.get("expires_at", 0)
    td["refresh_token"] = data.get("refresh_token", td["refresh_token"])
    save_json(TOKEN_FILE, td)
    return td

def get_token():
    td = load_json(TOKEN_FILE)
    if not td: td = signup()
    if time.time() > td.get("expires_at", 0) - 60: td = refresh(td)
    return td["access_token"]

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

def chat(prompt, system_prompt=None, temperature=0.9, max_tokens=100000, new_chat=False, stream=True):
    token = get_token()
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

    r = requests.post(f"{SUPA_URL}/functions/v1/chat-streaming", headers=headers, json=payload, stream=True, timeout=180)

    if r.status_code != 200:
        raise Exception(f"HTTP {r.status_code}")

    full_text = ""
    for line in iter_sse_lines(r):
        if not line.startswith("data: "): continue
        data = line[6:].strip()
        if data == "[DONE]": break
        try:
            obj = json.loads(data)
            content = obj.get("choices", [{}])[0].get("delta", {}).get("content", "")
            if content:
                full_text += content
                if stream: print(content, end="", flush=True)
        except json.JSONDecodeError: pass

    if stream: print()

    messages[-1] = {"role": "user", "content": prompt}
    messages.append({"role": "assistant", "content": full_text})
    save_context(messages)

    return {
        "success": True, "model": "anubis-70b", "content": full_text,
        "creator": CREATOR, "output_length": len(full_text),
        "word_count": len(full_text.split()),
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Uncensored AI - {CREATOR}")
    parser.add_argument("prompt", nargs="+", help="Prompt")
    parser.add_argument("--new", "-n", action="store_true", help="Reset context")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON")
    parser.add_argument("--temp", type=float, default=0.9, help="Temperature")
    parser.add_argument("--max", type=int, default=100000, help="Max tokens")
    args = parser.parse_args()

    prompt = " ".join(args.prompt)
    try:
        result = chat(prompt, temperature=args.temp, max_tokens=args.max, new_chat=args.new)
        if args.json: print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)
