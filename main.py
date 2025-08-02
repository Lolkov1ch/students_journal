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

# soon 

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
            # placeholder
            pass
        elif choice == '2':
            # placeholder
            pass
        elif choice == '3':
            # placeholder
            pass
        elif choice == '4':
            # placeholder
            pass
        elif choice == '5':
            # placeholder
            pass
        elif choice == '6':
            # placeholder
            pass
        elif choice == '7':
            # placeholder
            pass
        elif choice == '8':
            # placeholder
            pass
        elif choice == '0':
            # placeholder
            break
        else:
            print("Невірна команда. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
