from datetime import date

def days_to_birthday(birthday):
    today = date.today()
    # Получаем дату следующего дня рождения в этом году
    current_year_birthday = date(today.year, birthday.month, birthday.day)
    if current_year_birthday < today:
        # Если день рождения уже прошел в этом году, берем дату следующего года
        current_year_birthday = date(today.year + 1, birthday.month, birthday.day)
    # Вычисляем количество дней между сегодняшней датой и днем рождения
    days_until_birthday = current_year_birthday - today
    print (days_until_birthday.days)

days_to_birthday(date(1990, 5, 25))

