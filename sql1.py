#SQL1

import os
import re
import math
import sqlite3
from sqlite3 import Error

db = 'test.db'

# делаем простой запрос в бд, возвращаем среднее время в минутах
def time_avg(group_pref): 
    data = ('Open', group_pref)
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        query = """
        SELECT AVG(minutes_in_status) 
        FROM 'history'
        WHERE (status = ?) AND (issue_key LIKE ?)
        """
        cursor.execute(query, data)
        items = cursor.fetchall()
    except Error:
        print(Error)
    finally:
        conn.close()
    return items

# приводим значения из бд к int и форматируем в часы и минуты
def show_ave_time(group_name):
    ave_time = float(re.findall(r'-[0-9.]+|[0-9.]+', str(time_avg('%' + group_name + '-%')[0]))[0])
    ave_time = math.modf(ave_time)
    minutes = int(ave_time[0] * 100)
    hours = int(ave_time[1] / 60)
    if minutes >= 60:
        hours += 1
        minutes -= 60
    print('Среднее время задачи в статусе "Open" для группы {0} составляет: {1}:{2} (часы:минуты)'.format(group_name, hours, minutes))


# при бОльшем количестве групп можно дописать функцию, 
# которая будет считать количество уникальных групп
groups_name = ['A', 'B', 'C', 'D', 'E']
# выводим значения всех групп
for i in groups_name:
    show_ave_time(i)
