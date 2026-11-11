from day03 import WEEKLY_TARGET_HOURS, calculate_remaining_hours

def parse_daily_records(raw):
  parts = raw.split()
  if len(parts) != 7:
    raise ValueError('请输入7个数字，用空格分隔')
  
  try:
    daily_records = list(map(float, parts))
  except ValueError:
    raise ValueError('每个输入都必须是数字，例如：1.5 2.0 3.5 4.0 5.5 6.0 7.5')

  for record in daily_records:
    if not (0 <= record <= 24):
      raise ValueError("每天的时长必须在 0 到 24 小时之间。")
  
  return daily_records

def calculate_weekly_summary(daily_records):
  total_hours = 0
  study_days = 0

  for record in daily_records:
    total_hours += record

    if record > 0:
      study_days += 1
  
  remaining_hours = calculate_remaining_hours(total_hours, WEEKLY_TARGET_HOURS)
  return total_hours, study_days, remaining_hours


def main():
  raw = input('请输入7个数字，用空格分隔：')
  try:
    daily_hours = parse_daily_records(raw)
  except ValueError as error:
    print(error)
    raise SystemExit(1)

  total_hours, study_days, remaining_hours = calculate_weekly_summary(daily_hours)
  
  print(f'本周学习总时长：{total_hours}')
  print(f'本周学习天数：{study_days}')
  print(f'距离 15 小时还差 {remaining_hours} 小时')

if __name__ == '__main__':
  main()