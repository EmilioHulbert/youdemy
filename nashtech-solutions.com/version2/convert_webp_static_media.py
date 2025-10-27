import os
from PIL import Image

STATIC_DIR = "static"
MEDIA_DIR = "media"
LOG_FILE = "webp_conversion_static_media.log"

SUPPORTED_EXTS = [".jpg", ".jpeg", ".png"]

def convert_to_webp(base_dir):
    with open(LOG_FILE, "a") as log:
        for root, _, files in os.walk(base_dir):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in SUPPORTED_EXTS:
                    original_path = os.path.join(root, file)
                    webp_path = original_path.rsplit(ext, 1)[0] + ".webp"

                    # Avoid reconverting
                    if os.path.exists(webp_path):
                        continue

                    try:
                        img = Image.open(original_path)
                        if ext == ".png":
                            img.save(webp_path, "webp", lossless=True)
                        else:
                            img.save(webp_path, "webp")
                        log.write(f"{original_path} -> {webp_path}\n")
                        print(f"CONVERTED: {original_path}")
                    except Exception as e:
                        log.write(f"ERROR: {original_path}: {e}\n")
                        print(f"FAILED: {original_path}: {e}")

if __name__ == "__main__":
    convert_to_webp(STATIC_DIR)
    convert_to_webp(MEDIA_DIR)
    print("✅ Conversion complete. Check:", LOG_FILE)

