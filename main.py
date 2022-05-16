import datetime as dt


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        return sum([rec.amount for rec in self.records if rec.date == dt.datetime.now().date()])

    def get_week_stats(self):
        return sum([rec.amount for rec in self.records if rec.date > dt.datetime.now().date() - dt.timedelta.days(7)])


class CaloriesCalculator(Calculator):


    def get_calories_remained(self):
        current = self.get_today_stats()
        if current >= self.limit:
            return 'Хватит есть!'
        else:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {self.limit - current} кКал'


class CashCalculator(Calculator):


    USD_RATE = 63.3
    EURO_RATE = 65.7

    def get_today_cash_remained(self, currency):
        current = self.get_today_stats()
        dic_currency = {'rub': [1, 'руб'],
                        'usd': [self.USD_RATE, 'USD'],
                        'eur': [self.EURO_RATE, 'Euro']}
        if current >= self.limit:
            return f'Денег нет, держись'
        else:
            return f'''На сегодня осталось {round((self.limit - current) / 
                                                  dic_currency[currency][0], 2)} {dic_currency[currency][1]}'''


class Record:


    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.date = self._get_date(date)
        self.comment = comment

    def _get_date(self, date):
        if date == None:
            return dt.datetime.now().date()
        date_format = '%d.%m.%Y'
        return dt.datetime.strptime(date, date_format).date()


if __name__ == '__main__':
    # для CashCalculator
    r1 = Record(amount=3000, comment='Кофе')
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
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

