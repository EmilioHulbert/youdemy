import os
import re

LOG_FILE = "webp_references.log"
TEMPLATE_DIRS = ["templates", "static"]  # HTML + CSS locations

FILE_EXTS = [".html", ".htm", ".css"]

# Regex handles: /static/img/logo.png or {% static 'img/logo.jpg' %}
PATTERN = re.compile(r"(?P<path>[\w/.-]+\.(png|jpg|jpeg))")

def update_refs():
    with open(LOG_FILE, "w") as log:
        for directory in TEMPLATE_DIRS:
            for root, _, files in os.walk(directory):
                for file in files:
                    if os.path.splitext(file)[1].lower() in FILE_EXTS:
                        full_path = os.path.join(root, file)
                        with open(full_path, "r") as f:
                            content = f.read()

                        updated = content
                        matches = PATTERN.findall(content)

                        for match in matches:
                            orig = match[0]
                            new = orig.rsplit(".", 1)[0] + ".webp"
                            updated = updated.replace(orig, new)
                            log.write(f"{full_path}: {orig} -> {new}\n")

                        if updated != content:
                            with open(full_path, "w") as f:
                                f.write(updated)
                            print(f"UPDATED: {full_path}")

if __name__ == "__main__":
    update_refs()

