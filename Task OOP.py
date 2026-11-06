class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecture(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and
                course in lecturer.courses_attached and
                course in self.courses_in_progress):

            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def _get_average_grade(self):
        if not self.grades:
            return 0.0
        all_grades = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0.0

    def __str__(self):
        courses_in_progress_str = ", ".join(self.courses_in_progress)
        finished_courses_str = ", ".join(self.finished_courses)
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {self._get_average_grade()}\n"
                f"Курсы в процессе изучения: {courses_in_progress_str}\n"
                f"Завершенные курсы: {finished_courses_str}")

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._get_average_grade() < other._get_average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _get_average_grade(self):
        if not self.grades:
            return 0.0
        all_grades = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0.0

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {self._get_average_grade()}")

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._get_average_grade() < other._get_average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student) and
                course in self.courses_attached and
                course in student.courses_in_progress):

            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


# =====================================================================
# ЗАДАНИЕ №4: НОВЫЕ ФУНКЦИИ
# =====================================================================

# 1. Функция для подсчета средней оценки за ДЗ по всем студентам в рамках курса
def get_avg_student_grade(students_list, course_name):
    all_grades = []
    for student in students_list:
        if course_name in student.grades:
            all_grades.extend(student.grades[course_name])

    if not all_grades:
        return 0.0
    return round(sum(all_grades) / len(all_grades), 1)


# 2. Функция для подсчета средней оценки за лекции всех лекторов в рамках курса
def get_avg_lecturer_grade(lecturers_list, course_name):
    all_grades = []
    for lecturer in lecturers_list:
        if course_name in lecturer.grades:
            all_grades.extend(lecturer.grades[course_name])

    if not all_grades:
        return 0.0
    return round(sum(all_grades) / len(all_grades), 1)


# =====================================================================
# ПОЛЕВЫЕ ИСПЫТАНИЯ (ПРИМЕРЫ С ДВУМЯ ЭКЗЕМПЛЯРАМИ)
# =====================================================================
if __name__ == '__main__':
    # Создаем по 2 экземпляра каждого класса
    student1 = Student('Иван', 'Петров', 'М')
    student2 = Student('Анна', 'Сидорова', 'Ж')

    lecturer1 = Lecturer('Сергей', 'Дмитриев')
    lecturer2 = Lecturer('Елена', 'Васильева')

    reviewer1 = Reviewer('Олег', 'Иванов')
    reviewer2 = Reviewer('Мария', 'Кузнецова')

    # Настраиваем курсы
    student1.courses_in_progress += ['Python', 'Git']
    student2.courses_in_progress += ['Python']
    student1.add_courses('Введение в программирование')

    lecturer1.courses_attached += ['Python', 'Git']
    lecturer2.courses_attached += ['Python']

    reviewer1.courses_attached += ['Python', 'Git']
    reviewer2.courses_attached += ['Python']

    # Вызываем методы взаимодействия
    # 1. Проверяющие ставят оценки студентам за ДЗ
    reviewer1.rate_hw(student1, 'Python', 9)
    reviewer1.rate_hw(student1, 'Python', 10)
    reviewer2.rate_hw(student2, 'Python', 8)
    reviewer2.rate_hw(student2, 'Python', 10)

    # 2. Студенты ставят оценки лекторам за лекции
    student1.rate_lecture(lecturer1, 'Python', 10)
    student1.rate_lecture(lecturer1, 'Git', 9)
    student2.rate_lecture(lecturer2, 'Python', 8)
    student2.rate_lecture(lecturer2, 'Python', 10)

    # Выводим информацию по каждому объекту (проверка __str__)
    print("--- СТУДЕНТЫ ---")
    print(student1)
    print()
    print(student2)
    print("\n--- ЛЕКТОРЫ ---")
    print(lecturer1)
    print()
    print(lecturer2)
    print("\n--- ПРОВЕРЯЮЩИЕ ---")
    print(reviewer1)

    # Проверяем работу новых функций подсчета средних по курсу
    students = [student1, student2]
    lecturers = [lecturer1, lecturer2]

    print("\n--- СРЕДНИЕ БАЛЛЫ ПО КУРСУ 'Python' ---")
    print(f"Средняя оценка за ДЗ у всех студентов: {get_avg_student_grade(students, 'Python')}")
    print(f"Средняя оценка за лекции у всех лекторов: {get_avg_lecturer_grade(lecturers, 'Python')}")
