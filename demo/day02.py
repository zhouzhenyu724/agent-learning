WEEKS = 16
WEEKLY_TARGET_HOURS = 15

try:
  daily_hours = float(input('每天学习时间（允许小数）：'))
except ValueError:
  print('每天学习时间必须是数字')
  exit()

if not (0 < daily_hours <= 24):
  print('每天学习时间必须在0到24小时之间')
  raise SystemExit(1)

try:
  week_days = int(input('每周学习天数：'))
except ValueError:
  print('每周学习天数必须是整数')
  raise SystemExit(1)

if not(1 <= week_days <=7):
  print('每周学习天数必须在1到7天之间')
  raise SystemExit(1)

name = input('请输入你的姓名：').strip()
occupation = input('请输入你的职业：').strip()
goal = input('请输入你的目标：').strip()

weekly_hours = daily_hours * week_days
total_hours = weekly_hours * WEEKS

print('\n=========学习信息卡===========')
print(f'姓名：{name}')
print(f'职业：{occupation}')
print(f'目标：{goal}')
print(f'每周学习时间：{weekly_hours}小时')
print(f'16周学习总时间：{total_hours}小时')


print(f'\n每周学习总时长：{weekly_hours}小时')
print(f'{WEEKS}周学习总时长：{total_hours}小时')

if total_hours >= WEEKLY_TARGET_HOURS:
  print('你已经完成了每周目标')
else:
  print(f'你还需要{WEEKLY_TARGET_HOURS - total_hours}小时才能完成每周目标')
