import unittest
from sprint3 import sprint3


class sprint3_test(unittest.TestCase):
    def setUp(self):
        self.validator = sprint3()
    
    def test_siblings_marrying(self):
        gedcom_data_1 = [
            "0 @I1@ INDI",
            "1 FAMC @F1@",
            "1 FAMS @F2@",
            "0 @I2@ INDI",
            "1 FAMC @F1@",
            "1 FAMS @F3@",
            "0 @I3@ INDI",
            "1 FAMC @F1@",
            "0 @F1@ FAM",
            "1 CHIL @I1@",
            "1 CHIL @I2@",
            "1 CHIL @I3@",
            "0 @F2@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I4@",
            "0 @F3@ FAM",
            "1 HUSB @I5@",
            "1 WIFE @I2@"
        ]

        gedcom_data_2 = [
            "0 @I1@ INDI",
            "1 FAMC @F1@",
            "1 FAMS @F2@",
            "0 @I2@ INDI",
            "1 FAMC @F1@",
            "1 FAMS @F2@",
            "0 @I3@ INDI",
            "1 FAMC @F1@",
            "1 FAMS @F3@",
            "0 @F1@ FAM",
            "1 CHIL @I1@",
            "1 CHIL @I2@",
            "1 CHIL @I3@",
            "0 @F2@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@",
            "0 @F3@ FAM",
            "1 HUSB @I4@",
            "1 WIFE @I3@"
        ]


        gedcom_data_3 = [
            "0 @I1@ INDI",
            "1 FAMC @F1@",
            "1 FAMS @F2@",
            "0 @I2@ INDI",
            "1 FAMC @F1@",
            "1 FAMS @F3@",
            "0 @I3@ INDI",
            "1 FAMC @F1@",
            "0 @I4@ INDI",
            "1 FAMC @F4@",
            "0 @I5@ INDI",
            "1 FAMC @F4@",
            "0 @F1@ FAM",
            "1 CHIL @I1@",
            "1 CHIL @I2@",
            "1 CHIL @I3@",
            "0 @F2@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I6@",
            "0 @F3@ FAM",
            "1 HUSB @I7@",
            "1 WIFE @I2@",
            "0 @F4@ FAM",
            "1 CHIL @I4@",
            "1 CHIL @I5@",
            "0 @F5@ FAM",
            "1 HUSB @I8@",
            "1 WIFE @I9@"
        ]


        gedcom_data_4 = [
            "0 @I1@ INDI",
            "1 FAMC @F1@",
            "1 FAMS @F2@",
            "0 @I2@ INDI",
            "1 FAMC @F1@",
            "1 FAMS @F2@",
            "0 @I3@ INDI",
            "1 FAMC @F1@",
            "1 FAMS @F3@",
            "0 @I4@ INDI",
            "1 FAMC @F1@",
            "1 FAMS @F3@",
            "0 @F1@ FAM",
            "1 CHIL @I1@",
            "1 CHIL @I2@",
            "1 CHIL @I3@",
            "1 CHIL @I4@",
            "0 @F2@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@",
            "0 @F3@ FAM",
            "1 HUSB @I3@",
            "1 WIFE @I4@"
        ]

        gedcom_data_5 = [
            "0 @I1@ INDI",
            "1 FAMC @F1@",
            "1 FAMS @F2@",
            "0 @I2@ INDI",
            "1 FAMC @F1@",
            "1 FAMS @F2@",
            "0 @I3@ INDI",
            "1 FAMC @F1@",
            "0 @F1@ FAM",
            "1 CHIL @I1@",
            "1 CHIL @I2@",
            "1 CHIL @I3@",
            "0 @F2@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@"
        ]

        expected_1 = {}
        invalid_1 = self.validator.siblings_marrying(gedcom_data_1)
        self.assertEqual(invalid_1, expected_1)

        expected_2 = {'@F2@': ('@I2@', '@I1@')}
        invalid_2 = self.validator.siblings_marrying(gedcom_data_2)
        self.assertEqual(invalid_2, expected_2)

        expected_3 = {}
        invalid_3 = self.validator.siblings_marrying(gedcom_data_3)
        self.assertEqual(invalid_3, expected_3)

        expected_4 = {'@F2@': ('@I2@', '@I1@'), '@F3@': ('@I4@', '@I3@')}
        invalid_4 = self.validator.siblings_marrying(gedcom_data_4)
        self.assertEqual(invalid_4, expected_4)

        expected_5 = {'@F2@': ('@I2@', '@I1@')}
        invalid_5 = self.validator.siblings_marrying(gedcom_data_5)
        self.assertEqual(invalid_5, expected_5)

    def test_invalid_dates(self):
        gedcom_data_1 = [
            "0 @I1@ INDI",
            "1 BIRT",
            "2 DATE 32 DEC 2025",
            "1 DEAT",
            "2 DATE 1 JAN 2010",
            "0 @F1@ FAM",
            "1 MARR",
            "2 DATE 15 JUL 2020",
            "1 DIV",
            "2 DATE 1 JAN 2023"
        ]

        gedcom_data_2 = [
            "0 @I1@ INDI",
            "1 BIRT",
            "2 DATE 30 DEC 2025",
            "1 DEAT",
            "2 DATE 1 JAN 2010",
            "0 @F1@ FAM",
            "1 MARR",
            "2 DATE 15 JUL 2020",
            "1 DIV",
            "2 DATE 1 JAN 2023"
        ]
       
        expected_1 = {'2 DATE 32': '32 DEC 2025'}
        invalid_1 = self.validator.invalid_dates(gedcom_data_1)
        self.assertEqual(invalid_1, expected_1)

        expected_2 = {}
        invalid_2 = self.validator.invalid_dates(gedcom_data_2)
        self.assertEqual(invalid_2, expected_2)


    """
    def test_gender_role(self):
        gedcom_data_1 = [
            "0 @I1@ INDI",
            "1 NAME John /Doe/",
            "1 SEX M",
            "0 @I2@ INDI",
            "1 NAME Jane /Smith/",
            "1 SEX F",
            "0 @F1@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@",
            "0 @F2@ FAM",
            "1 HUSB @I2@",
            "1 WIFE @I1@"
        ]

        expected_1 = []
        invalid_1 = self.validator.find_gender_violations(gedcom_data_1)
        self.assertEqual(invalid_1, expected_1)
    """


"""
def test_upcoming_anniversaries(self):

        gedcom_data_1 = [
            "0 @I1@ INDI",
            "1 NAME John /Doe/",
            "1 BIRT",
            "2 DATE 30 DEC 1990",
            "1 DEAT",
            "2 DATE 1 JAN 2010",
            "0 @F1@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@",
            "1 MARR",
            "2 DATE 15 JUL 2024",
            "1 DIV",
            "2 DATE 1 JAN 2023"
        ]

        expected_1 = {}
        invalid_1 = self.validator.find_marriages_in_next_30_days(gedcom_data_1)
        self.assertEqual(invalid_1, expected_1)
    """

    