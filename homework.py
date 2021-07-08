import datetime as dt
from datetime import date
from typing import Union


class Calculator:
    """Класс Calculator родительский.
       В нем содержатся и суммируются записи
       о потраченных суммах и съеденных калориях
       за конкретные даты, класс также содержит
       дневной лимит калорий и денег."""
    delta_time = dt.timedelta(days=7)

    def __init__(self, limit: Union[int, float]) -> None:
        """Конструктор класса Calculator."""

        self.limit = limit
        self.records = []

    def add_record(self, record) -> None:
        """Добавляет записи в родительский класс.В качестве аргумента принимает
           объект класса Record и сохраняет его в списке records"""

        self.records.append(record)

    def get_today_stats(self) -> int:
        """Суммирует записи о калориях и деньгах за сегодняшнюю дату."""

        return sum([record.amount for record
                    in self.records if record.date == date.today()])

    def get_week_stats(self) -> int:
        """Суммирует записи о калориях и деньгах за последние 7 дней."""

        today = date.today()
        date_week = today - Calculator.delta_time

        return sum([record.amount for record
                    in self.records if today >= record.date > date_week])

    def get_remained(self) -> int:
        
        difference = self.limit - self.get_today_stats()
        return difference


class Record:
    """Класс Record. Отдельный класс для удобства создания записей."""

    def __init__(self, amount: Union[int, float],
                 comment: str, date=None) -> None:
        """Конструктор класса Record. Содержит условия для даты."""

        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CaloriesCalculator(Calculator):
    """Класс CaloriesCalculator унаследован от родительского класса Calculator.
       В нем содержатся функции
       для подсчета калорий за день и за последние 7 дней."""

    def get_calories_remained(self) -> str:
        """Считает количество съеденных калорий за день,
           сравнивает с лимитом калорий."""

        calorie_difference = self.get_remained()
        if calorie_difference > 0:
            return (f'Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью'
                    f' не более {calorie_difference} кКал')

        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Класс CashCalculator унаследован от родительского класса Calculator.
       В нем содержатся функции
       для подсчета денег, потраченных за день и за последние 7 дней.
       Содержит курсы валют и словарь для них."""

    USD_RATE = 60.00
    EURO_RATE = 70.00

    cur_t = ({'usd': [USD_RATE, 'USD'],
              'eur': [EURO_RATE, 'Euro'],
              'rub': [1, 'руб']})

    def get_today_cash_remained(self, val: Union[float, str]) -> str:
        """Считает сколько потраченно денег за день,
           сравнивает с лимитом на день."""

        name, rate = CashCalculator.cur_t[val][1], CashCalculator.cur_t[val][0]

        if self.get_remained() == 0:
            return 'Денег нет, держись'
        else:
            get_today_rate = self.get_remained() / rate
            cash_balance = round(get_today_rate, 2)
            module_cash_balance = abs(cash_balance)
            if cash_balance > 0:
                return f'На сегодня осталось {cash_balance} {name}'
            else:
                return (f'Денег нет, держись: '
                        f'твой долг - {module_cash_balance} {name}')


if __name__ == "__main__":
    # Проверка
    # создадим калькулятор денег с дневным лимитом 1000

    cash_calculator = CashCalculator(1000)
# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(Record(amount=3000,
                               comment='бар в Танин др',
                               date='08.11.2019'))

    print(cash_calculator.get_today_cash_remained('rub'))
# должно напечататься
# На сегодня осталось 555 руб

    print(cash_calculator.get_week_stats())
# должно напечататься 455

# Проверка
# создадим калькулятор денег с дневным лимитом 2000

    calorie_calculator = CaloriesCalculator(2000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
    calorie_calculator.add_record(Record(amount=1186,
                                  comment='Кусок тортика. И ещё один.'))
# и к этой записи тоже дата должна добавиться автоматически
    calorie_calculator.add_record(Record(amount=84, comment='Йогурт.'))
# а тут пользователь указал дату, сохраняем её
    calorie_calculator.add_record(Record(amount=1140,
                                  comment='Баночка чипсов.',
                                  date='24.02.2019'))

    print(calorie_calculator.get_calories_remained())
# должно напечататься
# Сегодня можно сьесть что-нибудь ещё,
# но с общей калорийностью не более 730 кКал
    print(calorie_calculator.get_week_stats())
# должно напечататься
# 1270
