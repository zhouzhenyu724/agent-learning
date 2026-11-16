import argparse
import json
import sqlite3
from contextlib import closing
from pathlib import Path


def validate_records(records):
    if not isinstance(records, list):
        raise ValueError("学习记录必须是列表。")

    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"第 {index} 条记录必须是字典。")
        if "topic" not in record or "hours" not in record:
            raise ValueError(f"第 {index} 条记录缺少 topic 或 hours。")

        topic = record["topic"]
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError(f"第 {index} 条记录的 topic 必须是非空字符串。")

        hours = record["hours"]
        if isinstance(hours, bool) or not isinstance(hours, (int, float)):
            raise ValueError(f"第 {index} 条记录的 hours 必须是数字。")
        if not 0 <= hours <= 24:
            raise ValueError(f"第 {index} 条记录的 hours 必须在 0 到 24 之间。")


def init_db(db_path):
    with closing(sqlite3.connect(db_path)) as conn, conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS learning_records (
                id INTEGER PRIMARY KEY,
                topic TEXT NOT NULL,
                hours REAL NOT NULL CHECK (hours BETWEEN 0 AND 24)
            )
        """)


def save_records(db_path, records):
    validate_records(records)
    rows = [(record["topic"], record["hours"]) for record in records]
    print('Saving records to database:', rows)

    with closing(sqlite3.connect(db_path)) as conn, conn:
        conn.executemany(
            "INSERT INTO learning_records (topic, hours) VALUES (?, ?)",
            rows,
        )


def summarize_by_topic(db_path):
    with closing(sqlite3.connect(db_path)) as conn:
        rows = conn.execute("""
            SELECT topic, SUM(hours)
            FROM learning_records
            GROUP BY topic
            ORDER BY topic
        """)
        return dict(rows)


def main():
    parser = argparse.ArgumentParser(description="导入学习记录并按主题汇总。")
    parser.add_argument("records", type=Path)
    parser.add_argument("--db", type=Path, default=Path("learning.db"))
    args = parser.parse_args()

    try:
        records = json.loads(args.records.read_text(encoding="utf-8"))
        init_db(args.db)
        save_records(args.db, records)
        summary = summarize_by_topic(args.db)
    except (OSError, ValueError, sqlite3.Error) as error:
        parser.exit(1, f"处理失败：{error}\n")

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()