from dataclasses import dataclass


@dataclass
class StudyRecord:
    topic: str
    hours: int | float


def validate_records(raw: object) -> list[StudyRecord]:
    if not isinstance(raw, list):
        raise ValueError("学习记录必须是列表。")

    records: list[StudyRecord] = []
    for index, item in enumerate(raw, start=1):
        prefix = f"第 {index} 条记录"

        if not isinstance(item, dict):
            raise ValueError(f"{prefix}必须是字典。")
        if "topic" not in item or "hours" not in item:
            raise ValueError(f"{prefix}必须包含 topic 和 hours。")

        topic = item["topic"]
        hours = item["hours"]

        if not isinstance(topic, str):
            raise ValueError(f"{prefix}的 topic 必须是字符串。")
        if isinstance(hours, bool) or not isinstance(hours, (int, float)):
            raise ValueError(f"{prefix}的 hours 必须是数字。")
        if not 0 <= hours <= 24:
            raise ValueError(f"{prefix}的 hours 必须在 0 到 24 之间。")

        records.append(StudyRecord(topic=topic, hours=hours))

    return records


def summarize_by_topic(records: list[StudyRecord]) -> dict[str, int | float]:
    totals: dict[str, int | float] = {}
    for record in records:
        totals[record.topic] = totals.get(record.topic, 0) + record.hours
    return totals