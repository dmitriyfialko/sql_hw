from datetime import datetime, timedelta
from faker import Faker
from random import randint, choice
import sqlite3


disciplines = [
    'Вища математика',
    'Дискретна математика',
    'Лінійна алгебра',
    'Історія Укрвїни',
    'Програмування',
    'Креслення',
    'Теорія емовірності',
    'Англійська',
]

groups = ['ПЦБ-01', 'ПЦБ-02', 'ПЦБ-03', 'ПЦБ-04']
NUMBER_TEACHER = 5
NUMBER_STUDENT = 50
fake = Faker('uk_UA')
connect = sqlite3.connect('hw.db')
cur = connect.cursor()


def create_tables():
    with open('create_tables.sql', 'r') as f:
        sql = f.read()
        cur.executescript(sql)


def seed_teachers():
    teachers = [fake.name() for _ in range(NUMBER_TEACHER)]
    sql = 'INSERT INTO teachers(fullname) VALUES (?);'
    cur.executemany(sql, zip(teachers, ))


def seed_disciplines():
    sql = 'INSERT INTO disciplines(name, teacher_id) VALUES (?, ?);'
    cur.executemany(sql, zip(disciplines, iter(randint(1, NUMBER_TEACHER) for _ in range(1, len(disciplines)))))


def seed_groups():
    sql = 'INSERT INTO groups(name) VALUES (?);'
    cur.executemany(sql, zip(groups, ))


def seed_students():
    students = [fake.name() for _ in range(NUMBER_STUDENT)]
    sql = 'INSERT INTO students(fullname, group_id) VALUES (?, ?);'
    cur.executemany(sql, zip(students, iter(randint(1, len(groups)) for _ in range(1, len(students)))))


def seed_grade():
    start_date = datetime.strptime('2022-09-01', '%Y-%m-%d')
    end_date = datetime.strptime('2023-06-15', '%Y-%m-%d')
    sql = 'INSERT INTO grades(discipline_id, student_id, grade, date_of) VALUES (?, ?, ?, ?);'

    def get_list_date(start: datetime, end: datetime):
        result = []
        while start <= end:
            if start.isoweekday() < 6:
                result.append(start)
            start += timedelta(days=1)
        return result

    list_date = get_list_date(start_date, end_date)
    grades = []
    for day in list_date:
        random_disciplines = [randint(1, len(disciplines)) for _ in range(3)]
        for discipline_id in random_disciplines:
            random_students = [randint(1, NUMBER_STUDENT) for _ in range(5)]
            for student_id in random_students:
                grades.append((discipline_id, student_id, randint(1, 100), day.date()))

    cur.executemany(sql, grades)


if __name__ == '__main__':
    try:
        create_tables()
        seed_teachers()
        seed_disciplines()
        seed_groups()
        seed_students()
        seed_grade()

        connect.commit()
    except sqlite3.Error as error:
        print(error)
    finally:
        connect.close()


