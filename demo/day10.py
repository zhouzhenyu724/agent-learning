import json

from day05 import summarize_by_topic
from day06 import load_records


def validate_records(records):
    if not isinstance(records, list):
        raise ValueError("学习记录必须是列表。")

    for record in records:
        if not isinstance(record, dict):
            raise ValueError("每条学习记录必须是字典。")
        if "topic" not in record:
            raise ValueError("缺少 topic 字段。")
        if "hours" not in record:
            raise ValueError("缺少 hours 字段。")

        hours = record["hours"]
        if isinstance(hours, bool) or not isinstance(hours, (int, float)):
            raise ValueError("hours 必须是数字。")
        if not (0 <= hours <= 24):
            raise ValueError("hours 必须在 0 到 24 之间。")


def main():
    records_path = "records.json"
    summary_path = "summary.json"

    try:
        records = load_records(records_path)
        validate_records(records)
    except FileNotFoundError:
        print(f"文件不存在：{records_path}")
        raise SystemExit(1)
    except json.JSONDecodeError:
        print(f"JSON 格式错误：{records_path}")
        raise SystemExit(1)
    except ValueError as error:
        print(error)
        raise SystemExit(1)

    summary = summarize_by_topic(records)
    with open(summary_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, ensure_ascii=False, indent=2)

    print(f"汇总已保存到 {summary_path}。")


if __name__ == "__main__":
    main()