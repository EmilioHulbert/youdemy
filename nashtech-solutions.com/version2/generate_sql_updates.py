import os

MEDIA_DIR = "media"
SQL_LOG = "update_media_refs.sql"
SUPPORTED_EXTS = [".png", ".jpg", ".jpeg"]

def generate_sql_updates():
    with open(SQL_LOG, "w") as sql:
        for root, _, files in os.walk(MEDIA_DIR):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in SUPPORTED_EXTS:
                    original = os.path.join(root, file)
                    new = original.rsplit(ext, 1)[0] + ".webp"
                    if os.path.exists(new):
                        sql.write(
                            "UPDATE django_db_table SET image_field = REPLACE(image_field, '{}', '{}');\n"
                            .format(file, file.replace(ext, ".webp"))
                        )

    print(f"✅ SQL rewrite file generated: {SQL_LOG}")
    print("⚠️ You MUST manually review & adjust table + field names.")

if __name__ == "__main__":
    generate_sql_updates()

