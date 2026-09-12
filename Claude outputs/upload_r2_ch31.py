# -*- coding: utf-8 -*-
# upload_r2_ch31.py — upload audio/slide-NN.mp3 to Cloudflare R2
# bucket urantia-media, key audiobook/kr/ch31/slide-NN.mp3  →  https://audio.urantiareaders.com/audiobook/kr/ch31/slide-NN.mp3
# Files already in the bucket are skipped. Run:  python upload_r2_ch31.py
import os, sys, json, subprocess

def need(mod, pip=None):
    try:
        __import__(mod)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip or mod])
need("boto3")
import boto3
from botocore.exceptions import ClientError

ACCOUNT_ID = "f84ed041969c71e367f50d6f9d99e839"
BUCKET     = "urantia-media"
PREFIX     = "audiobook/kr/ch31"
HERE       = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR  = os.path.join(HERE, "audio")
KEY_FILE   = os.path.join(HERE, "r2_keys.json")

def get_keys():
    for p in (KEY_FILE, os.path.join(os.path.dirname(HERE), "r2_keys.json")):
        if os.path.exists(p):
            d = json.load(open(p, encoding="utf-8"))
            ak = d.get("access_key") or d.get("access_key_id") or d.get("aws_access_key_id") or d.get("ACCESS_KEY")
            sk = d.get("secret_key") or d.get("secret_access_key") or d.get("aws_secret_access_key") or d.get("SECRET_KEY")
            if ak and sk:
                return ak, sk
    ak = input("R2 Access Key ID: ").strip()
    sk = input("R2 Secret Access Key: ").strip()
    json.dump({"access_key": ak, "secret_key": sk}, open(KEY_FILE, "w", encoding="utf-8"))
    print("Saved to r2_keys.json (never commit this file to GitHub)")
    return ak, sk

def main():
    ak, sk = get_keys()
    s3 = boto3.client("s3", endpoint_url=f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com",
                      aws_access_key_id=ak, aws_secret_access_key=sk, region_name="auto")
    files = sorted(f for f in os.listdir(AUDIO_DIR) if f.lower().endswith(".mp3"))
    if not files:
        print("No mp3 in audio/. Run generate_audio_ch31.py first."); return
    up = skip = 0
    for f in files:
        key = f"{PREFIX}/{f}"
        try:
            s3.head_object(Bucket=BUCKET, Key=key); skip += 1; continue
        except ClientError:
            pass
        s3.upload_file(os.path.join(AUDIO_DIR, f), BUCKET, key,
                       ExtraArgs={"ContentType": "audio/mpeg", "CacheControl": "public, max-age=31536000"})
        up += 1
        print(f"uploaded: https://audio.urantiareaders.com/{key}")
    print(f"\nDone — uploaded {up}, already there {skip}  (total {len(files)})")

if __name__ == "__main__":
    main()
