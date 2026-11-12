def summarize_by_topic(records):
  hours_by_topic = {}

  for record in records:
    topic = record['topic']
    hours = record['hours']
    hours_by_topic[topic] = hours_by_topic.get(topic, 0) + hours

  return hours_by_topic


if __name__ == '__main__':

  records = [
    {'topic': 'Python', 'hours': 2.5},
    {'topic': '后端', 'hours': 2},
    {'topic': 'Python', 'hours': 1.5},
  ]

  assert summarize_by_topic(records) == {'Python': 4.0, '后端': 2}
  assert summarize_by_topic([{'topic': 'Python', 'hours': 2.5}]) == {'Python': 2.5}
  assert summarize_by_topic([]) == {}
  print("3 条测试通过。")



