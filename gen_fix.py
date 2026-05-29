import os, base64, json
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request, urllib.error

ROOT = r"c:\Users\kanat\Desktop\dec-athlete"
ASSETS = os.path.join(ROOT, "reproduction", "heroinepilates-mens", "assets")

with open(os.path.join(ROOT, ".env"), "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"): continue
        k, _, v = line.partition("=")
        os.environ[k.strip()] = v.strip().strip('"').strip("'")
API_KEY = os.environ["GEMINI_API_KEY"]

JOBS = [
    ("intro1", "05_s-372x548_16825a38-d654-45eb-9f6c-57d6200faa99.webp",
     "Photorealistic back view of a lean Japanese MALE businessman in his 30s wearing a crisp white dress shirt, "
     "standing straight. Only his back and shoulders are visible, short black hair, no tie visible. "
     "Clean bright studio portrait, soft white background with subtle natural shadows. Focus on the straight spine and broad square male shoulders. "
     "Absolutely a man, adult male. Professional, refined and masculine mood. No text, no logos.",
     "3:4"),
    ("flow4", "16_s-7008x4672_v-frms_webp_2481bae7-1d12-4b02-8aed-19ad02a7d0bb_small.webp",
     "Photorealistic adult Japanese MALE man in his 30s, short black hair, lean athletic build, "
     "sitting on a pilates reformer performing a core stability exercise, both arms extended forward holding the straps. "
     "Wearing a white t-shirt and grey athletic shorts. Behind him stands a male Japanese trainer in his 30s in a black athletic t-shirt, gently supporting his back with one hand. "
     "Both are men. Bright minimalist pilates studio, soft white curtains glowing with window light, wooden floor, minimal interior. "
     "Focused, calm, professional atmosphere. No text, no logos, no food, no bread.",
     "4:3"),
]

URL = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={API_KEY}"

def gen(job):
    name, filename, prompt, aspect = job
    body = {"instances":[{"prompt": prompt}], "parameters":{"sampleCount":1,"aspectRatio":aspect,"personGeneration":"allow_adult"}}
    req = urllib.request.Request(URL, data=json.dumps(body).encode("utf-8"), headers={"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.loads(r.read().decode("utf-8"))
        b64 = data["predictions"][0]["bytesBase64Encoded"]
        raw = base64.b64decode(b64)
        with open(os.path.join(ASSETS, "gen_"+name+".png"), "wb") as f: f.write(raw)
        with open(os.path.join(ASSETS, filename), "wb") as f: f.write(raw)
        return name, True, f"{len(raw)}B"
    except urllib.error.HTTPError as e:
        return name, False, f"HTTP {e.code}: {e.read().decode('utf-8', errors='ignore')[:200]}"
    except Exception as e:
        return name, False, str(e)

with ThreadPoolExecutor(max_workers=2) as ex:
    for f in as_completed({ex.submit(gen, j): j[0] for j in JOBS}):
        print(f.result())
