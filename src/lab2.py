# Лабораторна робота №2. Створення та використання функцій, реалізація рекурсії
# Варіант: 1
# ПІБ: Ковальчук Діана

from functools import reduce
from typing import List, Callable, Dict, Tuple
from datetime import datetime, timedelta
import random

# Звичайні функції
def get_grade_description(score: float) -> str:
    """Визначає текстовий статус за 100-бальною шкалою."""
    if score >= 90:
        return "Відмінно (A)"
    elif score >= 75:
        return "Добре (B, C)"
    elif score >= 60:
        return "Задовільно (D, E)"
    else:
        return "Незадовільно (FX, F)"

def calculate_weighted_score(score: float, weight: float) -> float:
    return round(score * weight, 2)

# Функція з параметрами за замовчуванням
def calculate_final_grade(current_score: float, exam_score: float = 0.0, exam_weight: float = 0.4) -> float:
    if exam_score == 0.0:
        return current_score
    final = (current_score * (1 - exam_weight)) + (exam_score * exam_weight)
    return round(final, 1)

# Функція зі змінною кількістю аргументів
def average_score(*scores: float) -> float:
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 1)

# Лямбда-функція (перевірка чи складено екзамен за 100-бальною шкалою)
is_passed = lambda score: score >= 60.0

# Рекурсивна функція
def find_grade_range(data: List[Dict[str, float]], start: int, end: int) -> Tuple[float, float]:
    if start == end:
        score = data[start]['score']
        return (score, score)
    
    mid = (start + end) // 2
    left_min, left_max = find_grade_range(data, start, mid)
    right_min, right_max = find_grade_range(data, mid + 1, end)
    
    return (min(left_min, right_min), max(left_max, right_max))

# Функція вищого порядку
def apply_to_grades_data(data: List[Dict[str, float]], func: Callable[[float], float]) -> List[Dict[str, float]]:
    return [
        {**item, 'score': func(item['score'])}
        for item in data
    ]

# Генерація тестових даних 
def generate_student_data(records_count: int) -> List[Dict[str, float]]:
    base_date = datetime(2026, 9, 1)
    data = []
    subjects = ["Програмування", "Вища математика", "Бази даних", "Алгоритми", "Комп'ютерні мережі"]
    
    for i in range(records_count):
        date = base_date + timedelta(days=i * 2)
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'subject': subjects[i % len(subjects)],
            'score': round(random.uniform(35.0, 100.0), 1), # Бали від 35 до 100
            'weight': round(random.uniform(1.0, 3.0), 1)
        })
    return data


def main():
    print("Система аналізу успішності студентів ")
    student_data = generate_student_data(25)
    
    while True:
        print("\nОберіть операцію:")
        print("1. Показати журнал успішності ")
        print("2. Додати бонусні +5 балів усім ")
        print("3. Розрахувати підсумковий бал")
        print("4. Фільтрація успішних складань ")
        print("5. Знайти діапазон оцінок ")
        print("6. Розрахувати середню оцінку групи ")
        print("7. Вийти")
        
        try:
            choice = int(input("Ваш вибір: "))
            
            if choice == 1:
                print("\n--- Журнал оцінок ---")
                for record in student_data[:5]:
                    status = get_grade_description(record['score'])
                    print(f"Дата: {record['date']} | Предмет: {record['subject']} | Бал: {record['score']} | Статус: {status}")
                    
            elif choice == 2:
                # Додаємо 5 балів, але не більше 100 за допомогою лямбди та ФВП
                add_bonus = lambda s: min(100.0, round(s + 5.0, 1))
                converted_data = apply_to_grades_data(student_data, add_bonus)
                print("\n--- Оцінки з урахуванням бонусів (+5 балів) ---")
                for record in converted_data[:5]:
                    print(f"Предмет: {record['subject']} | Новий бал: {record['score']}/100")
                    
            elif choice == 3:
                print("\n--- Розрахунок підсумкової оцінки ---")
                for record in student_data[:5]:
                    final = calculate_final_grade(record['score'], exam_score=85.0, exam_weight=0.4)
                    print(f"Предмет: {record['subject']} | Поточний: {record['score']} | Підсумковий (іспит 85): {final}")
                    
            elif choice == 4:
                passed_records = list(filter(lambda x: is_passed(x['score']), student_data))
                print(f"\nУспішно складених (>= 60 балів): {len(passed_records)} із {len(student_data)}")
                for record in passed_records[:5]:
                    print(f"Предмет: {record['subject']} — Бал: {record['score']}")
                    
            elif choice == 5:
                min_s, max_s = find_grade_range(student_data, 0, len(student_data) - 1)
                print(f"\nМінімальний бал у групі: {min_s}")
                print(f"Максимальний бал у групі: {max_s}")
                
            elif choice == 6:
                all_scores = [record['score'] for record in student_data]
                avg = average_score(*all_scores)
                print(f"\nСередня оцінка за всіма записів: {avg} / 100")
                
            elif choice == 7:
                print("\nВихід з програми...")
                break
            else:
                print("Невірний вибір. Спробуйте від 1 до 7.")
                
        except ValueError:
            print("Будь ласка, введіть число.")

if __name__ == "__main__":
    main()
