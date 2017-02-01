import unittest

from temp import fahrenheit_to_celsius
from investment import compound_value_sixth_months as investment

class TestCohortAnswers(unittest.TestCase):
    def test_temp(self):
        self.assertEqual(fahrenheit_to_celsius(32), 0.0)
        self.assertEqual(fahrenheit_to_celsius(-40), -40.0)
        self.assertEqual(fahrenheit_to_celsius(212), 100)

    def test_investment(self):
        truncated_tester = lambda amt, int: round(investment(amt, int), 9)
        self.assertEqual(truncated_tester(100, 0.05), 608.811017706)
        self.assertEqual(truncated_tester(200, 0.03), 1210.54385954)

if __name__ == '__main__':
    unittest.main()
