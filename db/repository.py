import calendar
import datetime
import time

from sqlalchemy import select

from db.engineer import DbEngine
from db.model import People, Help


class Repository:
    def __init__(self):
        self.db = DbEngine()

    def get_people_for_month(self, dt:datetime.date) -> list[People]:
        with self.db.get_session() as session:
            first_day=self.get_first_day_of_month(dt)
            last_day = self.get_last_day_of_month(dt)

            help_in_range = select(1).where(
                    Help.people_id==People.people_id,  # Correlate with the main query's table
                    Help.help_time >=first_day,
                    Help.help_time<=last_day
            )
            people = session.query(People).where(help_in_range.exists()).all()

            return people

    @staticmethod
    def get_last_day_of_month(dt:datetime.date):
        last_day_num = calendar.monthrange(dt.year, dt.month)[1]
        last_day_date = dt.replace(day=last_day_num)

        return time.mktime(last_day_date.timetuple())

    @staticmethod
    def get_first_day_of_month(dt:datetime.date):
        last_day_date = dt.replace(day=1)

        return time.mktime(last_day_date.timetuple())