import json
from day05 import summarize_by_topic
from day06 import load_records

def main():
  input_path = 'records.json'
  output_path = 'summary.json'

  try:
    records = load_records(input_path)
  except FileNotFoundError:
    print(f'文件不存在：{input_path}')
    raise SystemExit(1)
  except json.JSONDecodeError:
    print(f'JSON 格式错误：{input_path}')
    raise SystemExit(1)

  summary = summarize_by_topic(records)
  with open('summary.json', 'w', encoding='utf-8') as file:
    json.dump(summary, file, ensure_ascii=False, indent=2)

  print(f"汇总已保存到 {output_path}。")

if __name__ == '__main__':
  main()


