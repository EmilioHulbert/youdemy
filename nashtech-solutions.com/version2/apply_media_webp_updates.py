#!/usr/bin/env python3
"""
apply_media_webp_updates.py

Safe updater for media file references -> .webp

Usage:
  1) Review output in DRY-RUN mode:
     python3 apply_media_webp_updates.py --dry-run

  2) When satisfied, run actual updates:
     python3 apply_media_webp_updates.py --apply

Requirements:
  pip install psycopg2-binary

This script assumes PostgreSQL.
It logs operations to db_webp_changes.log and db_webp_preview.log
"""

import os
import re
import argparse
import psycopg2
from psycopg2 import sql

# CONFIG: adjust DB connection details
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "yourdbname")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "")

MAPPING_LOG = "webp_conversion_static_media.log"
DRYRUN_LOG = "db_webp_preview.log"
APPLY_LOG = "db_webp_changes.log"

# Only these SQL types will be considered for textual replacements
TEXT_TYPES = ("text", "character varying", "varchar")

def read_mappings(mapping_file):
    """
    Read mapping file lines of form:
      media/ProductImage/hp_pavilion.jpg -> media/ProductImage/hp_pavilion.webp
    Returns list of tuples: (basename_old, basename_new, old_relpath, new_relpath)
    """
    mappings = []
    line_re = re.compile(r"^\s*(?P<old>.+\.\w+)\s*->\s*(?P<new>.+\.\w+)\s*$")
    with open(mapping_file, "r", encoding="utf-8") as f:
        for ln in f:
            m = line_re.match(ln.strip())
            if not m:
                continue
            oldp = m.group("old").strip()
            newp = m.group("new").strip()
            oldname = os.path.basename(oldp)
            newname = os.path.basename(newp)
            # sanity: only operate on png/jpg/jpeg -> webp
            if not oldname.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            if not newname.lower().endswith(".webp"):
                continue
            # verify .webp actually exists on disk (safety)
            if not os.path.exists(newp):
                print(f"[WARN] new file missing, skipping mapping: {newp}")
                continue
            mappings.append((oldname, newname, oldp, newp))
    return mappings

def find_text_columns(conn):
    """
    Return list of (schema, table, column) for columns with text-like types
    """
    q = """
    SELECT table_schema, table_name, column_name, data_type
      FROM information_schema.columns
     WHERE data_type IN %s
       AND table_schema NOT IN ('pg_catalog', 'information_schema')
    """
    with conn.cursor() as cur:
        cur.execute(q, (TEXT_TYPES,))
        return cur.fetchall()

def count_occurrences(conn, schema, table, column, needle):
    with conn.cursor() as cur:
        query = sql.SQL("SELECT count(*) FROM {}.{} WHERE {} LIKE %s").format(
            sql.Identifier(schema),
            sql.Identifier(table),
            sql.Identifier(column)
        )
        cur.execute(query, (f"%{needle}%",))
        return cur.fetchone()[0]

def do_update(conn, schema, table, column, old_str, new_str):
    """
    Perform UPDATE: replace occurrences of old_str with new_str in the specified column.
    Returns number of rows affected.
    """
    with conn.cursor() as cur:
        upd = sql.SQL("UPDATE {}.{} SET {} = replace({}, %s, %s) WHERE {} LIKE %s").format(
            sql.Identifier(schema),
            sql.Identifier(table),
            sql.Identifier(column),
            sql.Identifier(column),
            sql.Identifier(column)
        )
        cur.execute(upd, (old_str, new_str, f"%{old_str}%"))
        return cur.rowcount

def main(dry_run=True):
    mappings = read_mappings(MAPPING_LOG)
    if not mappings:
        print("No valid mappings found in", MAPPING_LOG)
        return

    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )
    conn.autocommit = False

    cols = find_text_columns(conn)
    print(f"Found {len(cols)} text-like columns to inspect.")

    preview_lines = []
    apply_lines = []

    try:
        for oldname, newname, oldp, newp in mappings:
            print(f"\n=== Mapping: {oldname} -> {newname} ===")
            for schema, table, column, dtype in cols:
                # check quickly whether this column contains the filename
                cnt = count_occurrences(conn, schema, table, column, oldname)
                if cnt and cnt > 0:
                    msg = f"WOULD CHANGE: {schema}.{table}.{column} -- rows: {cnt} -- replace '{oldname}' -> '{newname}'"
                    print(msg)
                    preview_lines.append(msg + "\n")
                    if not dry_run:
                        # run update inside a SAVEPOINT so failures on one update don't abort the whole run
                        with conn.cursor() as cur:
                            cur.execute("SAVEPOINT sp_before_update;")
                        try:
                            affected = do_update(conn, schema, table, column, oldname, newname)
                            conn.commit()
                            apl = f"UPDATED: {schema}.{table}.{column} -- affected: {affected} -- '{oldname}' -> '{newname}'"
                            print(apl)
                            apply_lines.append(apl + "\n")
                        except Exception as e:
                            conn.rollback()
                            with conn.cursor() as cur:
                                cur.execute("ROLLBACK TO SAVEPOINT sp_before_update;")
                            err = f"ERROR updating {schema}.{table}.{column}: {e}"
                            print(err)
                            apply_lines.append(err + "\n")
        # write logs
        with open(DRYRUN_LOG, "w", encoding="utf-8") as f:
            f.writelines(preview_lines)
        with open(APPLY_LOG, "w", encoding="utf-8") as f:
            f.writelines(apply_lines)

    finally:
        conn.close()
    print("\nDone. Preview:", DRYRUN_LOG, "Apply log:", APPLY_LOG)
    if dry_run:
        print("Run with --apply to execute updates (after manual review).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply webp media updates to Postgres DB safely.")
    parser.add_argument("--apply", action="store_true", help="actually apply the updates (default: dry-run)")
    args = parser.parse_args()
    main(dry_run=not args.apply)

