import main as test
import datetime as dt
import re


class TestOutput:

	def start_test(self) -> None:
		"""Запуск последовательных тестов."""
		self.test_record()
		self.test_calculator()
		self.test_calories_calc()
		self.test_cash_calories()

	def test_record(self) -> AssertionError:
		"""Проверка правильности введения даты."""
		record = test.Record('test', 2)
		assert record.date == dt.datetime.now().date(), 'Не задали сегодняшнюю дату по умолчанию в классе Record'

	def test_calculator(self, limit : int = 1000) -> AssertionError:
		"""Тест на правильность расчётов в классе."""
		calculator = test.Calculator(limit)
		calculator.add_record(test.Record(200, 'one', dt.datetime.now().date().strftime('%d.%m.%Y')))
		calculator.add_record(test.Record(500, 'two', (dt.datetime.now().date() - dt.timedelta(days = 6)).strftime('%d.%m.%Y')))
		calculator.add_record(test.Record(400, 'three', (dt.datetime.now().date() - dt.timedelta(days = 9)).strftime('%d.%m.%Y')))
		assert calculator.get_today_stats() == 200, 'Неверно вычислена сумма за сегодня'
		assert calculator.get_balance() == 800, 'Неверно вычислен остаток лимита на сегодня'
		assert calculator.get_week_stats() == 700, 'Неверно вычислена сумма за последние 7 дней'

	def test_calories_calc(self, limit : int = 1000) -> AssertionError:
		"""Тест на правильность расчётов в классе."""
		calc_calories = test.CaloriesCalculator(limit)
		past = self.exclude_digit_from_text(calc_calories.get_calories_remained())
		calc_calories.add_record(test.Record(limit, 'one', dt.datetime.now().date().strftime('%d.%m.%Y')))
		future = self.exclude_digit_from_text(calc_calories.get_calories_remained())
		assert past != future, 'Неверное сравнение лимита и текущих калорий'

	def test_cash_calories(self, limit : int = 1000) -> AssertionError:
		"""Тест на правильность расчётов в классе."""
		calc_cash = test.CashCalculator(limit)
		past = self.exclude_digit_from_text(calc_cash.get_today_cash_remained('rub'))
		calc_cash.add_record(test.Record(limit / 2, 'one', dt.datetime.now().date().strftime('%d.%m.%Y')))
		assert abs(self.get_digit_from_text(calc_cash.get_today_cash_remained('usd')) / (limit / 2 // 60) - 1) < 0.25, 'Не правильная конвертация в USD'
		assert abs(self.get_digit_from_text(calc_cash.get_today_cash_remained('eur')) / (limit / 2 // 60) - 1) < 0.25, 'Не правильная конвертация в Euro'
		calc_cash.add_record(test.Record(limit / 2, 'two', dt.datetime.now().date().strftime('%d.%m.%Y')))
		future = self.exclude_digit_from_text(calc_cash.get_today_cash_remained('rub'))
		assert past != future, 'Неверное сравнение лимита и текущих затрат'

	def exclude_digit_from_text(self, text : str) -> str:
		return re.sub(r'[0-9]', '', text)

	def get_digit_from_text(self, text : str) -> float:
		return float(re.sub(r'([а-яА-ЯёЁa-zA-Z ])', '', text))


	

if __name__ == '__main__':
	TestOutput().start_test()