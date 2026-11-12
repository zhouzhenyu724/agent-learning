import json
from day05 import summarize_by_topic

def load_records(path):
  with open(path, encoding='utf-8') as file:
    return json.load(file)


def main():
  path = 'records.json'
  try:
    records = load_records(path)
  except FileNotFoundError:
    print(f'文件不存在：{path}')
    raise SystemExit(1)
  except json.JSONDecodeError:
    print(f'JSON 格式错误：{path}')
    raise SystemExit(1)

  
  hours_by_topic = summarize_by_topic(records)

  for topic, hours in hours_by_topic.items():
    print(f'{topic}：{hours}小时')

if __name__ == '__main__':
  main()