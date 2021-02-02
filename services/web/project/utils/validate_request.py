import datetime
from project import app


class ValidateRequest:

    def __init__(self):
        self.success = True
        self.format = "%Y-%m-%d"

    def validator(self, form_data):
        self.is_exist_form_data_key(form_data)
        if not self.success:
            return self.success
        self.is_validate_date_format(form_data["start_date"], form_data["end_date"])
        if not self.success:
            return self.success
        self.is_not_in_future(form_data["start_date"], form_data["end_date"])
        if not self.success:
            return self.success

        return self.success

    def is_exist_form_data_key(self, form_data):
        if "league" not in form_data or "start_date" not in form_data or "end_date" not in form_data:
            app.logger.info("The request didn't contain valid key")
            self.success = False

    def is_validate_date_format(self, start_date, end_date):
        try:
            datetime.datetime.strptime(start_date, self.format)
            datetime.datetime.strptime(end_date, self.format)
        except ValueError:
            app.logger.info("Incorrect date string format. It should be YYYY-MM-DD")
            self.success = False

    def is_not_in_future(self, start_date, end_date):
        start_date = datetime.datetime.strptime(start_date, self.format)
        end_date = datetime.datetime.strptime(end_date, self.format)

        if start_date > end_date:
            app.logger.info("start date date is bigger than end date")
            self.success = False
