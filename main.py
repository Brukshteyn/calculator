import datetime as dt
from dataclasses import dataclass


@dataclass
class Record:

    RUS_DATE_FORMAT = '%d.%m.%Y'

    amount: int
    comment: str
    date: str = None
    date = (dt.datetime.now().date() if not date
        else dt.datetime.strptime(date, self.RUS_DATE_FORMAT).date()
            )


class Calculator:

    def __init__(self, limit : int) -> None:
        """Сохраняем лимит и записи."""
        self.limit = limit
        self.records = []

    def add_record(self, record : Record) -> None:
        """Добавление новой записи."""
        self.records.append(record)

    def get_today_stats(self) -> int:
        """Суммируем сумму за сегодня."""
        fix_date = dt.datetime.now().date()
        return sum(rec.amount for rec in self.records if rec.date == fix_date)

    def get_balance(self) -> int:
        """Получение остатка от лимита."""
        return self.limit - self.get_today_stats()

    def get_week_stats(self) -> int:
        fix_date = dt.datetime.now().date()
        """Суммируем сумму за последние 7 дней."""
        return sum(rec.amount for rec in self.records if rec.date > fix_date - dt.timedelta.days(7))


class CaloriesCalculator(Calculator):

    LIMIT_UP = 'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {balance} кКал'
    LIMIT_DOWN = 'Хватит есть!'

    def get_calories_remained(self) -> str:
        """Проверяем превышение лимита по каллориям."""
        if self.get_today_stats() >= self.limit:
            return self.LIMIT_DOWN
        return self.LIMIT_UP.format(balance = self.get_balance())


class CashCalculator(Calculator):

    DIC_CURRENCY = {'rub': (1, 'руб'),
                    'usd': (63.3, 'USD'),
                    'eur': (65.7, 'Euro')}
    LIMIT_UP = 'На сегодня осталось {balance} {currency}'
    LIMIT_DOWN = 'Денег нет, держись'
    ERROR_CURRENCY = 'currency, ожидали - {reception}; пришло - {current}'

    def get_today_cash_remained(self, currency : str) -> str:
        """Проверям превышение лимита затрат и выдаем результат в необходимой валюте."""
        try:
            currency_balance = round(self.get_balance() / self.DIC_CURRENCY[currency][0], 2)
        except:
            raise KeyError(self.ERROR_CURRENCY.format(current = currency, reception = ', '.join(self.DIC_CURRENCY.keys())))
        if self.get_today_stats() >= self.limit:
            return self.LIMIT_DOWN
        return self.LIMIT_UP.format(balance = currency_balance, currency = self.DIC_CURRENCY[currency][1])


if __name__ == '__main__':
    # для CashCalculator
    r1 = Record(amount=3000, comment='Кофе')
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    cash_calculator.add_record(Record(amount=400, comment='Серёге за обед'))
    cash_calculator.add_record(Record(amount=3000,
                                      comment='бар в Танин др',
                                      date='08.11.2019'))
    print(cash_calculator.get_today_cash_remained('rub'))
    # для CaloriesCalculator
    r2 = Record(amount=1186,
                comment='Кусок тортика. И ещё один.',
                date='24.02.2019')
    cal_calculator = CaloriesCalculator(400)
    cal_calculator.add_record(Record(amount=145, comment='кофе'))
    cal_calculator.add_record(Record(amount=300, comment='обед'))
    cal_calculator.add_record(Record(amount=3000,
                                     comment='бар',
                                     date='08.11.2019'))
    print(cal_calculator.get_calories_remained())



