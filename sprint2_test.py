import unittest
from sprint2 import sprint2


class sprint2_test(unittest.TestCase):
    def setUp(self):
        self.validator = sprint2()
    
    def test_divorce_before_marriage(self):
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
            "2 DATE 15 JAN 1999"
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

        expected_invalid_dates_1 = {}
        invalid_dates_1 = self.validator.divorce_before_marriage(gedcom_lines_1)
        self.assertEqual(invalid_dates_1, expected_invalid_dates_1)

        expected_invalid_dates_2 = {"@F2@": ("20 JUL 2000", "15 JAN 1999")}
        invalid_dates_2 = self.validator.divorce_before_marriage(gedcom_lines_2)
        self.assertEqual(invalid_dates_2, expected_invalid_dates_2)

        expected_invalid_dates_3 = {}
        invalid_dates_3 = self.validator.divorce_before_marriage(gedcom_lines_3)
        self.assertEqual(invalid_dates_3, expected_invalid_dates_3)

        expected_invalid_dates_4 = {"@F4@": ("25 DEC 2026", "30 NOV 2021")}
        invalid_dates_4 = self.validator.divorce_before_marriage(gedcom_lines_4)
        self.assertEqual(invalid_dates_4, expected_invalid_dates_4)

        expected_invalid_dates_5 = {}
        invalid_dates_5 = self.validator.divorce_before_marriage(gedcom_lines_5)
        self.assertEqual(invalid_dates_5, expected_invalid_dates_5)

    def test_death_before_marraige(self):
        gedcom_lines_1 = [
            "0 @F1@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@",
            "1 MARR",
            "2 DATE 15 APR 2010",
            "0 @I1@ INDI",
            "1 BIRT",
            "2 DATE 20 JAN 1950",
            "1 DEAT",
            "2 DATE 15 APR 2005",
            "0 @I2@ INDI",
            "1 BIRT",
            "2 DATE 22 FEB 1955",
            "1 DEAT",
            "2 DATE 01 MAR 2008"
        ]
        gedcom_lines_2 = [
            "0 @F2@ FAM",
            "1 HUSB @I3@",
            "1 WIFE @I4@",
            "1 MARR",
            "2 DATE 10 JUN 2000",
            "0 @I3@ INDI",
            "1 BIRT",
            "2 DATE 10 OCT 1960",
            "1 DEAT",
            "2 DATE 05 MAY 1999",
            "0 @I4@ INDI",
            "1 BIRT",
            "2 DATE 15 DEC 1965"
        ]

        gedcom_lines_3 = [
            "0 @F3@ FAM",
            "1 HUSB @I5@",
            "1 WIFE @I6@",
            "1 MARR",
            "2 DATE 05 MAY 1990",
            "0 @I5@ INDI",
            "1 BIRT",
            "2 DATE 14 JUL 1955",
            "0 @I6@ INDI",
            "1 BIRT",
            "2 DATE 19 NOV 1960",
            "1 DEAT",
            "2 DATE 01 JAN 1989"
        ]

        gedcom_lines_4 = [
            "0 @F4@ FAM",
            "1 HUSB @I7@",
            "1 WIFE @I8@",
            "1 MARR",
            "2 DATE 11 SEP 1975",
            "0 @I7@ INDI",
            "1 BIRT",
            "2 DATE 01 JAN 1945",
            "1 DEAT",
            "2 DATE 01 JAN 2005",
            "0 @I8@ INDI",
            "1 BIRT",
            "2 DATE 05 MAY 1950",
            "1 DEAT",
            "2 DATE 01 JAN 2010"
        ]

        gedcom_lines_5 = [
            "0 @F5@ FAM",
            "1 HUSB @I9@",
            "1 WIFE @I10@",
            "1 MARR",
            "2 DATE 23 MAR 1980",
            "0 @I9@ INDI",
            "1 BIRT",
            "2 DATE 14 FEB 1950",
            "1 DEAT",
            "2 DATE 01 JAN 1990",
            "0 @I10@ INDI",
            "1 BIRT",
            "2 DATE 10 JUN 1955",
            "1 DEAT",
            "2 DATE 01 JAN 1979"
        ] 

        expected_invalid_dates_1 = {'@F1@': ('15 APR 2010', '15 APR 2005', '01 MAR 2008')}
        invalid_dates_1 = self.validator.death_before_marriage(gedcom_lines_1)
        self.assertEqual(invalid_dates_1, expected_invalid_dates_1)

        expected_invalid_dates_2 = {'@F2@': ('10 JUN 2000', '05 MAY 1999', None)}
        invalid_dates_2 = self.validator.death_before_marriage(gedcom_lines_2)
        self.assertEqual(invalid_dates_2, expected_invalid_dates_2)

        expected_invalid_dates_3 = {'@F3@': ('05 MAY 1990', None, '01 JAN 1989')}
        invalid_dates_3 = self.validator.death_before_marriage(gedcom_lines_3)
        self.assertEqual(invalid_dates_3, expected_invalid_dates_3)

        expected_invalid_dates_4 = {}
        invalid_dates_4 = self.validator.death_before_marriage(gedcom_lines_4)
        self.assertEqual(invalid_dates_4, expected_invalid_dates_4)

        expected_invalid_dates_5 = {'@F5@': ('23 MAR 1980', '01 JAN 1990', '01 JAN 1979')}
        invalid_dates_5 = self.validator.death_before_marriage(gedcom_lines_5)
        self.assertEqual(invalid_dates_5, expected_invalid_dates_5)


    def test_death_before_divorce(self):
        gedcom_lines_1 = [
            "0 @F1@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@",
            "1 DIV",
            "2 DATE 15 APR 2010",
            "0 @I1@ INDI",
            "1 BIRT",
            "2 DATE 20 JAN 1950",
            "1 DEAT",
            "2 DATE 15 APR 2005",
            "0 @I2@ INDI",
            "1 BIRT",
            "2 DATE 22 FEB 1955",
            "1 DEAT",
            "2 DATE 01 MAR 2008"
        ]

        gedcom_lines_2 = [
            "0 @F2@ FAM",
            "1 HUSB @I3@",
            "1 WIFE @I4@",
            "1 DIV",
            "2 DATE 10 JUN 2000",
            "0 @I3@ INDI",
            "1 BIRT",
            "2 DATE 10 OCT 1960",
            "1 DEAT",
            "2 DATE 05 MAY 1999",
            "0 @I4@ INDI",
            "1 BIRT",
            "2 DATE 15 DEC 1965"
        ]

        gedcom_lines_3 = [
            "0 @F3@ FAM",
            "1 HUSB @I5@",
            "1 WIFE @I6@",
            "1 DIV",
            "2 DATE 05 MAY 1990",
            "0 @I5@ INDI",
            "1 BIRT",
            "2 DATE 14 JUL 1955",
            "0 @I6@ INDI",
            "1 BIRT",
            "2 DATE 19 NOV 1960",
            "1 DEAT",
            "2 DATE 01 JAN 1991"
        ]

        gedcom_lines_4 = [
            "0 @F4@ FAM",
            "1 HUSB @I7@",
            "1 WIFE @I8@",
            "1 DIV",
            "2 DATE 11 SEP 1975",
            "0 @I7@ INDI",
            "1 BIRT",
            "2 DATE 01 JAN 1945",
            "1 DEAT",
            "2 DATE 01 JAN 2005",
            "0 @I8@ INDI",
            "1 BIRT",
            "2 DATE 05 MAY 1950",
            "1 DEAT",
            "2 DATE 01 JAN 2010"
        ]

        gedcom_lines_5 = [
            "0 @F5@ FAM",
            "1 HUSB @I9@",
            "1 WIFE @I10@",
            "1 DIV",
            "2 DATE 23 MAR 1980",
            "0 @I9@ INDI",
            "1 BIRT",
            "2 DATE 14 FEB 1950",
            "1 DEAT",
            "2 DATE 01 JAN 1990",
            "0 @I10@ INDI",
            "1 BIRT",
            "2 DATE 10 JUN 1955",
            "1 DEAT",
            "2 DATE 01 JAN 1979"
        ]

        expected_invalid_dates_1 =  {'@F1@': ('15 APR 2010', '15 APR 2005', '01 MAR 2008')}
        invalid_dates_1 = self.validator.divorce_before_death(gedcom_lines_1)
        self.assertEqual(invalid_dates_1, expected_invalid_dates_1)

        expected_invalid_dates_2 = {'@F2@': ('10 JUN 2000', '05 MAY 1999', None)}
        invalid_dates_2 = self.validator.divorce_before_death(gedcom_lines_2)
        self.assertEqual(invalid_dates_2, expected_invalid_dates_2)

        expected_invalid_dates_3 = {}
        invalid_dates_3 = self.validator.divorce_before_death(gedcom_lines_3)
        self.assertEqual(invalid_dates_3, expected_invalid_dates_3)

        expected_invalid_dates_4 = {}
        invalid_dates_4 = self.validator.divorce_before_death(gedcom_lines_4)
        self.assertEqual(invalid_dates_4, expected_invalid_dates_4)

        expected_invalid_dates_5 = {'@F5@': ('23 MAR 1980', '01 JAN 1990', '01 JAN 1979')}
        invalid_dates_5 = self.validator.divorce_before_death(gedcom_lines_5)
        self.assertEqual(invalid_dates_5, expected_invalid_dates_5)

    def test_over_150(self):
        gedcom_lines_1 = [
            "0 @F1@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@",
            "1 DIV",
            "2 DATE 15 APR 2010",
            "0 @I1@ INDI",
            "1 BIRT",
            "2 DATE 20 JAN 1850", 
            "1 DEAT",
            "2 DATE 15 APR 2005",
            "0 @I2@ INDI",
            "1 BIRT",
            "2 DATE 22 FEB 1955",
            "1 DEAT",
            "2 DATE 01 MAR 2008"
        ]

        gedcom_lines_2 = [
            "0 @F1@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@",
            "1 DIV",
            "2 DATE 15 APR 2010",
            "0 @I1@ INDI",
            "1 BIRT",
            "2 DATE 20 JAN 1940",
            "1 DEAT",
            "2 DATE 15 APR 1995",
            "0 @I2@ INDI",
            "1 BIRT",
            "2 DATE 22 FEB 1955",
            "1 DEAT",
            "2 DATE 01 MAR 2008"
        ]

        gedcom_lines_3 = [
            "0 @F1@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@",
            "1 DIV",
            "2 DATE 15 APR 2010",
            "0 @I1@ INDI",
            "1 BIRT",
            "2 DATE 20 JAN 1840",
            "1 DEAT",
            "2 DATE 15 APR 1995",
            "0 @I2@ INDI",
            "1 BIRT",
            "2 DATE 22 FEB 1855",
            "1 DEAT",
            "2 DATE 01 MAR 2008"
        ]

        gedcom_lines_4 = [
            "0 @F1@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@",
            "1 DIV",
            "2 DATE 15 APR 2010",
            "0 @I1@ INDI",
            "1 BIRT",
            "2 DATE 20 JAN 1870",
            "1 DEAT",
            "2 DATE 15 APR 2025",
            "0 @I2@ INDI",
            "1 BIRT",
            "2 DATE 22 FEB 1855",
            "1 DEAT",
            "2 DATE 01 MAR 2008"
        ]

        gedcom_lines_5 = [
            "0 @F1@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@",
            "1 DIV",
            "2 DATE 15 APR 2010",
            "0 @I1@ INDI",
            "1 BIRT",
            "2 DATE 20 JAN 1965",
            "1 DEAT",
            "2 DATE 15 APR 2016",
            "0 @I2@ INDI",
            "1 BIRT",
            "2 DATE 22 FEB 1955",
            "1 DEAT",
            "2 DATE 01 MAR 2008"
        ]

        expected_invalid_dates_1 =  {'@I1@': ('20 Jan 1850', '15 Apr 2005')}
        invalid_dates_1 = self.validator.over_150(gedcom_lines_1)
        self.assertEqual(invalid_dates_1, expected_invalid_dates_1)

        expected_invalid_dates_2 = {}
        invalid_dates_2 = self.validator.over_150(gedcom_lines_2)
        self.assertEqual(invalid_dates_2, expected_invalid_dates_2)

        expected_invalid_dates_3 = {'@I1@': ('20 Jan 1840', '15 Apr 1995'), '@I2@': ('22 Feb 1855', '01 Mar 2008')}
        invalid_dates_3 = self.validator.over_150(gedcom_lines_3)
        self.assertEqual(invalid_dates_3, expected_invalid_dates_3)

        expected_invalid_dates_4 = {'@I1@': ('20 Jan 1870', '15 Apr 2025'), '@I2@': ('22 Feb 1855', '01 Mar 2008')}
        invalid_dates_4 = self.validator.over_150(gedcom_lines_4)
        self.assertEqual(invalid_dates_4, expected_invalid_dates_4)

        expected_invalid_dates_5 = {}
        invalid_dates_5 = self.validator.over_150(gedcom_lines_5)
        self.assertEqual(invalid_dates_5, expected_invalid_dates_5)
