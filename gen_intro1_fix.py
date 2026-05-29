import os, base64, json, urllib.request, urllib.error
ROOT = r"c:\Users\kanat\Desktop\dec-athlete"
ASSETS = os.path.join(ROOT, "reproduction", "heroinepilates-mens", "assets")
with open(os.path.join(ROOT, ".env"), "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"): continue
        k, _, v = line.partition("=")
        os.environ[k.strip()] = v.strip().strip('"').strip("'")
API_KEY = os.environ["GEMINI_API_KEY"]

prompt = (
    "Photorealistic portrait of a strong handsome adult Japanese businessman, male, 35 years old, "
    "short black hair, wearing a white dress shirt with sleeves rolled up, gazing confidently to the side. "
    "Broad muscular shoulders visible, strong jawline, clean shaven. "
    "Only a man in frame, absolutely masculine, not a woman. "
    "Clean bright studio portrait on pale beige background. Dignified, sophisticated mood. No text, no logos."
)
body = {"instances":[{"prompt": prompt}], "parameters":{"sampleCount":1,"aspectRatio":"3:4","personGeneration":"allow_adult"}}
URL = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={API_KEY}"
req = urllib.request.Request(URL, data=json.dumps(body).encode("utf-8"), headers={"Content-Type":"application/json"}, method="POST")
with urllib.request.urlopen(req, timeout=180) as r:
    data = json.loads(r.read().decode("utf-8"))
raw = base64.b64decode(data["predictions"][0]["bytesBase64Encoded"])
with open(os.path.join(ASSETS, "gen_intro1.png"), "wb") as f: f.write(raw)
with open(os.path.join(ASSETS, "05_s-372x548_16825a38-d654-45eb-9f6c-57d6200faa99.webp"), "wb") as f: f.write(raw)
print("OK", len(raw))
