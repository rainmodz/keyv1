from flask import Flask, render_template, request
import time, random, string, json, os

app = Flask(__name__)
KEY_FILE = "keys.json"

# Auto-create keys.json if missing
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "w") as f:
        json.dump({}, f)

def load_keys():
    with open(KEY_FILE, "r") as f:
        return json.load(f)

def save_keys(keys):
    with open(KEY_FILE, "w") as f:
        json.dump(keys, f)

def generate_key(length=16):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generatekey")
def gen_key():
    key = generate_key()
    keys = load_keys()
    keys[key] = int(time.time())
    save_keys(keys)
    return render_template("generatekey.html", key=key)

@app.route("/validate")
def validate():
    key = request.args.get("key")
    if not key:
        return "NO_KEY"
    keys = load_keys()
    if key in keys:
        if time.time() - keys[key] < 86400:
            return "VALID"
        else:
            return "EXPIRED"
    return "INVALID"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
