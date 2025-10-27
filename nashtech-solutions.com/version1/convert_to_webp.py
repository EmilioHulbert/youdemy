import os
from PIL import Image

STATIC_DIR = "static"
LOG_FILE = "webp_conversion.log"

SUPPORTED_EXTS = [".jpg", ".jpeg", ".png"]

def convert_to_webp():
    with open(LOG_FILE, "w") as log:
        for root, _, files in os.walk(STATIC_DIR):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in SUPPORTED_EXTS:
                    original_path = os.path.join(root, file)
                    webp_path = original_path.rsplit(ext, 1)[0] + ".webp"

                    try:
                        img = Image.open(original_path)
                        if ext == ".png":
                            img.save(webp_path, "webp", lossless=True)
                        else:
                            img.save(webp_path, "webp")
                        log.write(f"CONVERTED: {original_path} -> {webp_path}\n")
                        print(f"OK: {original_path}")
                    except Exception as e:
                        log.write(f"ERROR: {original_path}: {e}\n")
                        print(f"FAILED: {original_path}: {e}")

if __name__ == "__main__":
    convert_to_webp()

