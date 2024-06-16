import unittest
from sprint1 import sprint1


class sprint1_test(unittest.TestCase):
    def setUp(self):
        self.validator = sprint1()
    
    def test_dates_before_current_date(self):
        gedcom_lines_1 = [
            "0 @I1@ INDI",
            "1 BIRT",
            "2 DATE 30 DEC 2025",
            "1 DEAT",
            "2 DATE 1 JAN 2010",
            "0 @F1@ FAM",
            "1 MARR",
            "2 DATE 15 JUN 2020",
            "1 DIV",
            "2 DATE 1 JAN 2023"
        ]

        gedcom_lines_2 = [
            "0 @I2@ INDI",
            "1 BIRT",
            "2 DATE 25 DEC 1980",
            "1 DEAT",
            "2 DATE 1 JAN 2022",
            "0 @F2@ FAM",
            "1 MARR",
            "2 DATE 20 JUL 2000",
            "1 DIV",
            "2 DATE 15 JAN 2015"
        ]

        gedcom_lines_3 = [
            "0 @I3@ INDI",
            "1 BIRT",
            "2 DATE 15 MAR 1995",
            "1 DEAT",
            "2 DATE 1 JAN 2018",
            "0 @F3@ FAM",
            "1 MARR",
            "2 DATE 10 APR 2010",
            "1 DIV",
            "2 DATE 5 FEB 2019"
        ]

        gedcom_lines_4 = [
            "0 @I4@ INDI",
            "1 BIRT",
            "2 DATE 5 MAY 2005",
            "1 DEAT",
            "2 DATE 1 JAN 2020",
            "0 @F4@ FAM",
            "1 MARR",
            "2 DATE 25 DEC 2026",
            "1 DIV",
            "2 DATE 30 NOV 2021"
        ]

        gedcom_lines_5 = [
            "0 @I5@ INDI",
            "1 BIRT",
            "2 DATE 20 JUN 1975",
            "1 DEAT",
            "2 DATE 1 JAN 2019",
            "0 @F5@ FAM",
            "1 MARR",
            "2 DATE 11 SEP 1999",
            "1 DIV",
            "2 DATE 12 DEC 2018"
        ]

        expected_invalid_dates_1 = [("1 BIRT", "2 DATE 30 DEC 2025")]
        invalid_dates_1 = self.validator.dates_before_current_date(gedcom_lines_1)
        self.assertEqual(invalid_dates_1, expected_invalid_dates_1)

        expected_invalid_dates_2 = []
        invalid_dates_2 = self.validator.dates_before_current_date(gedcom_lines_2)
        self.assertEqual(invalid_dates_2, expected_invalid_dates_2)

        expected_invalid_dates_3 = []
        invalid_dates_3 = self.validator.dates_before_current_date(gedcom_lines_3)
        self.assertEqual(invalid_dates_3, expected_invalid_dates_3)

        expected_invalid_dates_4 = [("1 MARR", "2 DATE 25 DEC 2026")]
        invalid_dates_4 = self.validator.dates_before_current_date(gedcom_lines_4)
        self.assertEqual(invalid_dates_4, expected_invalid_dates_4)

        expected_invalid_dates_5 = []
        invalid_dates_5 = self.validator.dates_before_current_date(gedcom_lines_5)
        self.assertEqual(invalid_dates_5, expected_invalid_dates_5)
        
    def test_birth_before_marriage(self):
        gedcom_lines_1 = [
           "0 @I1@ INDI",
            "1 BIRT",
            "2 DATE 1 JAN 1980",
            "1 MARR",
            "2 DATE 1 JAN 2000",
            "0 @I2@ INDI",
            "1 BIRT",
            "2 DATE 25 DEC 1985",
            "1 MARR",
            "2 DATE 15 JUN 2010",
            "0 @I3@ INDI",
            "1 BIRT",
            "2 DATE 15 MAR 1975",
            "1 MARR",
            "2 DATE 20 APR 1995",
            "0 @I4@ INDI",
            "1 BIRT",
            "2 DATE 10 MAY 1990",
            "1 MARR",
            "2 DATE 11 MAY 1989",  
            "0 @I5@ INDI",
            "1 BIRT",
            "2 DATE 20 JUN 1975",
            "1 MARR",
            "2 DATE 20 JUN 2025"
        ]

        gedcom_lines_2 = [
            "0 @I2@ INDI",
            "1 BIRT",
            "2 DATE 25 DEC 1985",
            "1 MARR",
            "2 DATE 15 JUN 2010"
        ]

        gedcom_lines_3 = [
            "0 @I3@ INDI",
            "1 BIRT",
            "2 DATE 20 MAR 1975",
            "1 MARR",
            "2 DATE 20 MAR 1975" #same day 
        ]

        gedcom_lines_4 = [
            "0 @I4@ INDI",
            "1 BIRT",
            "2 DATE 10 MAY 1990",
            "1 MARR",
            "2 DATE 5 MAY 1989"  #invalid case
        ]

        gedcom_lines_5 = [
            "0 @I5@ INDI",
            "1 BIRT",
            "2 DATE 20 JUN 1975",
            "1 MARR",
            "2 DATE 20 JUN 2025"
        ]

        expected_results_1 = {
            "@I1@": True,
            "@I2@": True,
            "@I3@": True,
            "@I4@": False,
            "@I5@": True
        }
        expected_results_2 = {
            "@I2@": True
        }
        expected_results_3 = {
            "@I3@": False
        }
        expected_results_4 = {
            "@I4@": False
        }
        expected_results_5 = {
            "@I5@": True
        }



        self.assertEqual(self.validator.birth_before_marriage(gedcom_lines_1), expected_results_1)
        self.assertEqual(self.validator.birth_before_marriage(gedcom_lines_2), expected_results_2)
        self.assertEqual(self.validator.birth_before_marriage(gedcom_lines_3), expected_results_3)
        self.assertEqual(self.validator.birth_before_marriage(gedcom_lines_4), expected_results_4)
        self.assertEqual(self.validator.birth_before_marriage(gedcom_lines_5), expected_results_5)

    def test_birth_before_death(self):
        gedcom_lines_1 = [
           "0 @I1@ INDI",
            "1 BIRT",
            "2 DATE 1 JAN 1980",
            "1 DEAT",
            "2 DATE 1 JAN 2000",
            "0 @I2@ INDI",
            "1 BIRT",
            "2 DATE 25 DEC 1985",
            "1 DEAT",
            "2 DATE 15 JUN 2010",
            "0 @I3@ INDI",
            "1 BIRT",
            "2 DATE 15 MAR 1975",
            "1 DEAT",
            "2 DATE 20 APR 1995",
            "0 @I4@ INDI",
            "1 BIRT",
            "2 DATE 10 MAY 1990",
            "1 DEAT",
            "2 DATE 11 MAY 1989",  
            "0 @I5@ INDI",
            "1 BIRT",
            "2 DATE 20 JUN 1975",
            "1 DEAT",
            "2 DATE 20 JUN 2025"
        ]

        gedcom_lines_2 = [
            "0 @I2@ INDI",
            "1 BIRT",
            "2 DATE 25 DEC 1985",
            "1 DEAT",
            "2 DATE 15 JUN 2010"
        ]

        gedcom_lines_3 = [
            "0 @I3@ INDI",
            "1 BIRT",
            "2 DATE 20 MAR 1975",
            "1 DEAT",
            "2 DATE 20 MAR 1975" #same day 
        ]

        gedcom_lines_4 = [
            "0 @I4@ INDI",
            "1 BIRT",
            "2 DATE 10 MAY 1990",
            "1 DEAT",
            "2 DATE 5 MAY 1989"  #invalid case
        ]

        gedcom_lines_5 = [
            "0 @I5@ INDI",
            "1 BIRT",
            "2 DATE 20 JUN 1975",
            "1 DEAT",
            "2 DATE 20 JUN 2025"
        ]

        expected_results_1 = {
            "@I1@": True,
            "@I2@": True,
            "@I3@": True,
            "@I4@": False,
            "@I5@": True
        }
        expected_results_2 = {
            "@I2@": True
        }
        expected_results_3 = {
            "@I3@": False
        }
        expected_results_4 = {
            "@I4@": False
        }
        expected_results_5 = {
            "@I5@": True
        }



        self.assertEqual(self.validator.birth_before_death(gedcom_lines_1), expected_results_1)
        self.assertEqual(self.validator.birth_before_death(gedcom_lines_2), expected_results_2)
        self.assertEqual(self.validator.birth_before_death(gedcom_lines_3), expected_results_3)
        self.assertEqual(self.validator.birth_before_death(gedcom_lines_4), expected_results_4)
        self.assertEqual(self.validator.birth_before_death(gedcom_lines_5), expected_results_5)

if __name__ == "__main__":
    unittest.main()