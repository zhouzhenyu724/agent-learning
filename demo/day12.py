import json
from pathlib import Path

from study_records import summarize_by_topic, validate_records


def main() -> int:
    directory = Path(__file__).resolve().parent
    source = directory / "records.json"
    target = directory / "summary.json"

    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
        records = validate_records(raw)
    except FileNotFoundError:
        print(f"文件不存在：{source.name}")
        return 1
    except json.JSONDecodeError:
        print(f"JSON 格式错误：{source.name}")
        return 1
    except ValueError as error:
        print(error)
        return 1

    summary = summarize_by_topic(records)
    target.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"汇总已保存到 {target.name}。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())