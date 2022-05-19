import datetime as dt


class Calculator:

    def __init__(self, limit):
        """Сохраняем лимит и записи."""
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Добавление новой записи."""
        self.records.append(record)

    def get_today_stats(self):
        """Суммируем сумму за сегодня."""
        fix_date = dt.datetime.now().date()
        return sum(rec.amount for rec in self.records if rec.date == fix_date)

    def get_balance(self) -> int:
        """Получение остатка от лимита."""
        return self.limit - self.get_today_stats()

    def get_week_stats(self):
        fix_date = dt.datetime.now().date()
        """Суммируем сумму за последние 7 дней."""
        return sum(rec.amount for rec in self.records if rec.date > fix_date - dt.timedelta.days(7))


class CaloriesCalculator(Calculator):

    LIMIT_UP = 'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {balance} кКал'
    LIMIT_DOWN = 'Хватит есть!'

    def get_calories_remained(self):
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

    def get_today_cash_remained(self, currency):
        """Проверям превышение лимита затрат и выдаем результат в необходимой валюте."""
        try:
            currency_balance = round(self.get_balance() / self.DIC_CURRENCY[currency][0], 2)
        except:
            raise KeyError(self.ERROR_CURRENCY.format(current = currency, reception = ', '.join(self.DIC_CURRENCY.keys())))
        if self.get_today_stats() >= self.limit:
            return self.LIMIT_DOWN
        return self.LIMIT_UP.format(balance = currency_balance, currency = self.DIC_CURRENCY[currency][1])


class Record:

    RUS_DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        """Сохраняем артибуты записи."""
        self.amount = amount
        self.date = self._get_date(date)
        self.comment = comment

    def _get_date(self, date):
        """Проверка наличия и приведение даты."""
        if date == None:
            return dt.datetime.now().date()
        return dt.datetime.strptime(date, self.RUS_DATE_FORMAT).date()


if __name__ == '__main__':
    # для CashCalculator
    r1 = Record(amount=3000, comment='Кофе')
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    cash_calculator.add_record(Record(amount=400, comment='Серёге за обед'))
    cash_calculator.add_record(Record(amount=3000,
                                      comment='бар в Танин др',
                                      date='08.11.2019'))
    print(cash_calculator.get_today_cash_remained('ru'))
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



