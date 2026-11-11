name = input('请输入你的姓名：')
position = input('请输入你的职业：')
time = input('请输入你的工作时间：')
goal = input('请输入你的目标：')

print(f'姓名：{name} \n职业：{position} \n工作时间：{time} \n目标：{goal}')


day_time = input('每天学习时间（允许小数）：')
week_day = input('每周学习天数：')

week_tolal_time = float(day_time) * int(week_day)

week16_total_time = week_tolal_time * 16

print(f'每周学习总时间：{week_tolal_time}小时')

print(f'16周学习总时间：{week16_total_time}小时')