import unittest
from sprint4 import sprint4


class sprint4_test(unittest.TestCase):
    def setUp(self):
        self.validator = sprint4()
    
    def test_gender_roles(self):
        gedcom_data_1 = [
            "0 @I1@ INDI",
            "1 SEX M",
            "1 FAMC @F1@",
            "1 FAMS @F2@",
            "0 @I2@ INDI",
            "1 SEX F",
            "1 FAMC @F1@",
            "1 FAMS @F3@",
            "0 @I3@ INDI",
            "1 SEX M",
            "1 FAMC @F4@",
            "1 FAMS @F5@",
            "0 @I4@ INDI",
            "1 SEX F",
            "1 FAMC @F4@",
            "0 @F1@ FAM",
            "1 HUSB @I5@",
            "1 WIFE @I6@",
            "1 CHIL @I1@",
            "1 CHIL @I2@",
            "0 @F2@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I7@",
            "0 @F3@ FAM",
            "1 HUSB @I8@",
            "1 WIFE @I2@",
            "0 @F4@ FAM",
            "1 HUSB @I9@",
            "1 WIFE @I10@",
            "1 CHIL @I3@",
            "1 CHIL @I4@",
            "0 @F5@ FAM",
            "1 HUSB @I11@",
            "1 WIFE @I3@"
        ]

        gedcom_data_2 = [
            "0 @I1@ INDI",
            "1 SEX M",
            "1 FAMC @F1@",
            "1 FAMS @F2@",
            "0 @I2@ INDI",
            "1 SEX F",
            "1 FAMC @F1@",
            "1 FAMS @F3@",
            "0 @I3@ INDI",
            "1 SEX M",
            "1 FAMC @F4@",
            "1 FAMS @F5@",
            "0 @I4@ INDI",
            "1 SEX F",
            "1 FAMC @F4@",
            "0 @F1@ FAM",
            "1 HUSB @I5@",
            "1 WIFE @I6@",
            "1 CHIL @I1@",
            "1 CHIL @I2@",
            "0 @F2@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I7@",
            "0 @F3@ FAM",
            "1 HUSB @I8@",
            "1 WIFE @I2@",
            "0 @F4@ FAM",
            "1 HUSB @I9@",
            "1 WIFE @I10@",
            "1 CHIL @I3@",
            "1 CHIL @I4@"
        ]

        gedcom_data_3 = [
            "0 @I1@ INDI",
            "1 SEX F",
            "1 FAMC @F1@",
            "1 FAMS @F2@",
            "0 @I2@ INDI",
            "1 SEX F",
            "1 FAMC @F1@",
            "1 FAMS @F3@",
            "0 @I3@ INDI",
            "1 SEX M",
            "1 FAMC @F4@",
            "1 FAMS @F5@",
            "0 @I4@ INDI",
            "1 SEX F",
            "1 FAMC @F4@",
            "0 @F1@ FAM",
            "1 HUSB @I5@",
            "1 WIFE @I6@",
            "1 CHIL @I1@",
            "1 CHIL @I2@",
            "0 @F2@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I7@",
            "0 @F3@ FAM",
            "1 HUSB @I8@",
            "1 WIFE @I2@",
            "0 @F4@ FAM",
            "1 HUSB @I9@",
            "1 WIFE @I10@",
            "1 CHIL @I3@",
            "1 CHIL @I4@",
            "0 @F5@ FAM",
            "1 HUSB @I11@",
            "1 WIFE @I3@"
        ]


        
        expected_1 = ['Family @F5@: Wife @I3@ is not female']
        invalid_1 = self.validator.check_gender_roles(gedcom_data_1)
        self.assertEqual(invalid_1, expected_1)

        expected_2 = []
        invalid_2 = self.validator.check_gender_roles(gedcom_data_2)
        self.assertEqual(invalid_2, expected_2)

        expected_3 = ['Family @F2@: Husband @I1@ is not male', 'Family @F5@: Wife @I3@ is not female']
        invalid_3 = self.validator.check_gender_roles(gedcom_data_3)
        self.assertEqual(invalid_3, expected_3)

    def test_list_upcoming_anniversaries(self):

        gedcom_data_1 = [
            "0 @I1@ INDI",
            "1 NAME John /Doe/",
            "1 BIRT",
            "2 DATE 1 JAN 1950",
            "0 @I2@ INDI",
            "1 NAME Jane /Doe/",
            "1 BIRT",
            "2 DATE 5 FEB 1950",
            "0 @I3@ INDI",
            "1 NAME Jack /Doe/",
            "1 BIRT",
            "2 DATE 15 MAR 1955",
            "1 DEAT",
            "2 DATE 10 APR 2020",
            "0 @I4@ INDI",
            "1 NAME Jill /Doe/",
            "1 BIRT",
            "2 DATE 25 DEC 1960",
            "0 @F1@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@",
            "1 MARR",
            "2 DATE 14 AUG 1980",
            "0 @F2@ FAM",
            "1 HUSB @I3@",
            "1 WIFE @I4@",
            "1 MARR",
            "2 DATE 25 DEC 1990"
        ]

        gedcom_data_2 = [
            "0 @I1@ INDI",
            "1 NAME Michael /Smith/",
            "1 BIRT",
            "2 DATE 10 JAN 1960",
            "0 @I2@ INDI",
            "1 NAME Sarah /Smith/",
            "1 BIRT",
            "2 DATE 20 FEB 1965",
            "0 @I3@ INDI",
            "1 NAME David /Smith/",
            "1 BIRT",
            "2 DATE 30 MAR 1970",
            "1 DEAT",
            "2 DATE 15 APR 2021",
            "0 @I4@ INDI",
            "1 NAME Laura /Smith/",
            "1 BIRT",
            "2 DATE 12 DEC 1975",
            "0 @F1@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@",
            "1 MARR",
            "2 DATE 5 JUL 1985",
            "0 @F2@ FAM",
            "1 HUSB @I3@",
            "1 WIFE @I4@",
            "1 MARR",
            "2 DATE 18 DEC 1995"
        ]

        gedcom_data_3 = [
            "0 @I1@ INDI",
            "1 NAME Thomas /Davis/",
            "1 BIRT",
            "2 DATE 15 FEB 1930",
            "0 @I2@ INDI",
            "1 NAME Susan /Davis/",
            "1 BIRT",
            "2 DATE 10 MAR 1935",
            "0 @I3@ INDI",
            "1 NAME Mark /Davis/",
            "1 BIRT",
            "2 DATE 5 APR 1940",
            "1 DEAT",
            "2 DATE 30 MAY 2018",
            "0 @I4@ INDI",
            "1 NAME Nancy /Davis/",
            "1 BIRT",
            "2 DATE 20 JUN 1945",
            "0 @F1@ FAM",
            "1 HUSB @I1@",
            "1 WIFE @I2@",
            "1 MARR",
            "2 DATE 1 AUG 1950",
            "0 @F2@ FAM",
            "1 HUSB @I3@",
            "1 WIFE @I4@",
            "1 MARR",
            "2 DATE 10 SEP 1965"
        ]


        expected_1 = ['John /Doe/ and Jane /Doe/ have an anniversary on 14 AUG 1980']
        invalid_1 = self.validator.list_upcoming_anniversaries(gedcom_data_1)
        self.assertEqual(invalid_1, expected_1)

        expected_2 = []
        invalid_2 = self.validator.list_upcoming_anniversaries(gedcom_data_2)
        self.assertEqual(invalid_2, expected_2)

        expected_3 = ['Thomas /Davis/ and Susan /Davis/ have an anniversary on 1 AUG 1950']
        invalid_3 = self.validator.list_upcoming_anniversaries(gedcom_data_3)
        self.assertEqual(invalid_3, expected_3)


