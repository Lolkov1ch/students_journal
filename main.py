import sqlite3

DB_NAME = 'university.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            major TEXT
        );
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            instructor TEXT
        );
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_courses (
            student_id INTEGER,
            course_id INTEGER,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
        );
        ''')
        conn.commit()

def execute(query, params=(), fetch=False):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        conn.commit()

def input_int(prompt):
    while True:
        val = input(prompt)
        if val.isdigit():
            return int(val)
        else:
            print("Будь ласка, введіть число.")

def list_table(table, columns):
    rows = execute(f"SELECT {', '.join(columns)} FROM {table}", fetch=True)
    if not rows:
        print(f"Записів у таблиці {table} немає.")
        return []
    for row in rows:
        print(", ".join(f"{col}: {val}" for col, val in zip(columns, row)))
    return rows

def add_student():
    name = input("Ім'я студента: ")
    age = input_int("Вік: ")
    major = input("Спеціальність: ")
    execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)", (name, age, major))
    print(f"Студент {name} доданий!")

def add_course():
    course_name = input("Назва курсу: ")
    instructor = input("Ім'я викладача: ")
    execute("INSERT INTO courses (course_name, instructor) VALUES (?, ?)", (course_name, instructor))
    print(f"Курс {course_name} доданий!")

def update_student():
    list_table('students', ['id', 'name', 'age', 'major'])
    student_id = input_int("Введіть ID студента, якого хочете оновити: ")

    name = input("Нове ім'я (залиште порожнім, щоб не змінювати): ")
    age_str = input("Новий вік (залиште порожнім, щоб не змінювати): ")
    major = input("Нова спеціальність (залиште порожнім, щоб не змінювати): ")

    if name:
        execute("UPDATE students SET name = ? WHERE id = ?", (name, student_id))
    if age_str.isdigit():
        execute("UPDATE students SET age = ? WHERE id = ?", (int(age_str), student_id))
    if major:
        execute("UPDATE students SET major = ? WHERE id = ?", (major, student_id))
    print("Дані студента оновлені.")

def update_course():
    list_table('courses', ['course_id', 'course_name', 'instructor'])
    course_id = input_int("Введіть ID курсу, який хочете оновити: ")

    course_name = input("Нова назва курсу (залиште порожнім, щоб не змінювати): ")
    instructor = input("Новий викладач (залиште порожнім, щоб не змінювати): ")

    if course_name:
        execute("UPDATE courses SET course_name = ? WHERE course_id = ?", (course_name, course_id))
    if instructor:
        execute("UPDATE courses SET instructor = ? WHERE course_id = ?", (instructor, course_id))
    print("Дані курсу оновлені.")

def add_student_course():
    print("Студенти:")
    list_table('students', ['id', 'name'])
    student_id = input_int("Введіть ID студента: ")

    print("Курси:")
    list_table('courses', ['course_id', 'course_name'])
    course_id = input_int("Введіть ID курсу: ")

    try:
        execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
        print("Курс додано студенту!")
    except sqlite3.IntegrityError:
        print("Цей студент вже записаний на цей курс або ID неправильні.")

def list_students_by_course():
    print("Курси:")
    list_table('courses', ['course_id', 'course_name'])
    course_id = input_int("Введіть ID курсу для перегляду студентів: ")

    students = execute('''
        SELECT students.id, students.name, students.age, students.major
        FROM students
        JOIN student_courses ON students.id = student_courses.student_id
        WHERE student_courses.course_id = ?
    ''', (course_id,), fetch=True)

    if not students:
        print("На цей курс ніхто не записаний.")
        return

    print(f"Студенти на курсі ID {course_id}:")
    for s in students:
        print(f"ID: {s[0]}, Ім'я: {s[1]}, Вік: {s[2]}, Спеціальність: {s[3]}")

def main():
    init_db()
    while True:
        print("\nМеню:")
        print("1. Додати студента")
        print("2. Додати курс")
        print("3. Переглянути студентів")
        print("4. Переглянути курси")
        print("5. Оновити студента")
        print("6. Оновити курс")
        print("7. Записати студента на курс")
        print("8. Переглянути студентів за курсом")
        print("0. Вийти")

        choice = input("Оберіть дію: ")
        if choice == '1':
            add_student()
        elif choice == '2':
            add_course()
        elif choice == '3':
            list_table('students', ['id', 'name', 'age', 'major'])
        elif choice == '4':
            list_table('courses', ['course_id', 'course_name', 'instructor'])
        elif choice == '5':
            update_student()
        elif choice == '6':
            update_course()
        elif choice == '7':
            add_student_course()
        elif choice == '8':
            list_students_by_course()
        elif choice == '0':
            print("Вихід...")
            break
        else:
            print("Невірна команда. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
