import unittest
from project.utils.validate_request import ValidateRequest

class TestRequestValidator(unittest.TestCase):

    def setUp(self):
        self.validator = ValidateRequest()

    def test_key_validator_with_valid_form_data(self):
        res = self.validator.validator(
            {
                "league": "test",
                "start_date": "2020-09-09",
                "end_date": "2020-09-12"
            }
        )

        self.assertTrue(res)

    def test_key_validator_with_invalid_form_data(self):
        res = self.validator.validator(
            {
                "league": "test",
                "invalid": "2020-09-09",
                "end_date": "2020-09-12"
            }
        )

        self.assertFalse(res)

    def test_date_format_with_valid_format(self):
        res = self.validator.validator(
            {
                "league": "test",
                "start_date": "2020-09-09",
                "end_date": "2020-09-12"
            }
        )

        self.assertTrue(res)

    def test_date_format_with_invalid_format(self):
        res = self.validator.validator(
            {
                "league": "test",
                "start_date": "2020-90-2",
                "end_date": "2020-09-12"
            }
        )

        self.assertFalse(res)

    def test_date_not_in_future(self):
        res = self.validator.validator(
            {
                "league": "test",
                "start_date": "2020-09-10",
                "end_date": "2020-09-12"
            }
        )

        self.assertTrue(res)

    def test_date_in_future(self):
        res = self.validator.validator(
            {
                "league": "test",
                "start_date": "2020-09-20",
                "end_date": "2020-09-12"
            }
        )

        self.assertFalse(res)
