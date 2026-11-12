import json
from day05 import summarize_by_topic
from day06 import load_records

def main():
  records_path = 'records.json'
  summary_path = 'summary.json'

  try:
    records = load_records(records_path)
  except FileNotFoundError:
    print(f'文件不存在：{records_path}')
    raise SystemExit(1)
  except json.JSONDecodeError:
    print(f'JSON 格式错误：{records_path}')
    raise SystemExit(1)

  if not isinstance(records, list):
    print('学习记录必须是列表。')
    raise SystemExit(1)
  
  for record in records:
    if not isinstance(record, dict):
      print('学习记录必须是字典。')
      raise SystemExit(1)
  
  summary = summarize_by_topic(records)
  with open(summary_path, 'w', encoding='utf-8') as file:
    json.dump(summary, file, ensure_ascii=False, indent=2)

  print(f"汇总已保存到 {summary_path}。")

if __name__ == '__main__':
  main()

