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

# 失敗した横長6枚だけ再生成（4:3）
JOBS = [
    ("reason", "13_s-6865x4577_v-frms_webp_8fa17114-4274-44b9-bdfa-04b239b97817_small.webp",
     "Photorealistic Japanese man in his 30s wearing a white t-shirt and grey athletic pants, "
     "training on a pilates reformer machine in a bright private studio. A male Japanese instructor in his 30s in black athletic wear is coaching him with a gentle hand on his shoulder. "
     "Natural window light, wooden floor, curtains softly glowing white, minimal Japanese interior. "
     "Cinematic, calm, professional wellness mood. No text, no logos."),
    ("flow1", "19_s-7008x4672_v-frms_webp_a556ccb9-a858-4d7f-a2b2-8106fb2b9c70_small.webp",
     "Photorealistic Japanese businessman in his 40s in a casual grey hoodie sitting across a small round white table from a male Japanese trainer in a black polo shirt. "
     "Between them is a tablet showing posture analysis lines. A small plant decorates the table. "
     "Bright minimalist studio interior, white walls and curtains, warm natural light. Both look engaged and professional. No text, no logos."),
    ("flow2", "14_s-6980x4653_v-frms_webp_6c4a53aa-e497-4999-b2b6-0490f9893bfc_small.webp",
     "Photorealistic Japanese man in his 30s lying on a pilates reformer machine, "
     "wearing a white t-shirt and navy shorts, while a male Japanese trainer in a black tank top gently adjusts his knee position. "
     "Both are calm and focused. Bright private studio with wooden floor, white curtains glowing with natural light. "
     "Minimal clean interior. No text, no logos."),
    ("flow3", "20_s-7008x4672_v-frms_webp_bc3784a5-d32f-4575-8788-272b8a0eb906_small.webp",
     "Photorealistic Japanese man in his 30s doing a chest opening stretch with arms raised wide, "
     "wearing a white t-shirt and black athletic shorts. A male Japanese trainer in black sports top stands behind him gently guiding his shoulder posture. "
     "Pilates studio with wooden floor, equipment and plant in soft background, bright natural white light. No text, no logos."),
    ("flow4", "16_s-7008x4672_v-frms_webp_2481bae7-1d12-4b02-8aed-19ad02a7d0bb_small.webp",
     "Photorealistic Japanese man in his 30s sitting on a pilates reformer performing a core stability exercise, arms forward holding the straps, "
     "wearing a white t-shirt and grey shorts, male Japanese trainer in black shirt supporting his back. "
     "Soft white curtains behind, natural window light, focused athletic atmosphere. Minimal Japanese studio interior. No text, no logos."),
    ("flow5", "18_s-7008x4672_v-frms_webp_a4c4df2c-31d7-4a02-93e8-431c82421a1f_small.webp",
     "Photorealistic Japanese businessman in his 40s in a white dress shirt doing a seated desk stretch, "
     "one arm across the chest, looking slightly relaxed. A male Japanese trainer sits opposite him explaining with a tablet. "
     "Clean bright studio with wooden floor, white cabinets and curtain. Warm natural light. No text, no logos."),
]

URL = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={API_KEY}"

def generate(job):
    name, filename, prompt = job
    body = {"instances": [{"prompt": prompt}], "parameters": {"sampleCount": 1, "aspectRatio": "4:3", "personGeneration": "allow_adult"}}
    req = urllib.request.Request(URL, data=json.dumps(body).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.loads(r.read().decode("utf-8"))
        preds = data.get("predictions", [])
        if not preds:
            return name, False, f"no predictions"
        b64 = preds[0].get("bytesBase64Encoded")
        if not b64:
            return name, False, "no b64"
        raw = base64.b64decode(b64)
        with open(os.path.join(ASSETS, "gen_" + name + ".png"), "wb") as f:
            f.write(raw)
        with open(os.path.join(ASSETS, filename), "wb") as f:
            f.write(raw)
        return name, True, f"{len(raw)}B"
    except urllib.error.HTTPError as e:
        return name, False, f"HTTP {e.code}: {e.read().decode('utf-8', errors='ignore')[:300]}"
    except Exception as e:
        return name, False, f"ERR: {e}"

def main():
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(generate, j): j[0] for j in JOBS}
        ok = 0
        for f in as_completed(futs):
            name, o, msg = f.result()
            print(("OK  " if o else "FAIL"), name, "-", msg[:200])
            if o: ok += 1
    print(f"\nDone: {ok}/{len(JOBS)}")

if __name__ == "__main__":
    main()
