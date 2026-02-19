import csv
import dataclasses
import datetime
import io

from db.repository import Repository
from service.model import Gender


@dataclasses.dataclass
class PeopleService:
    repo: Repository=Repository()

    def get_people_for_month(self, dt:datetime.date)->str:
        list_people=self.repo.get_people_for_month(dt=dt)
        si = io.StringIO()
        writer = csv.writer(si, delimiter=';')
        writer.writerow(['Имя', 'Отчество','Фамилия', 'Пол', 'Место откуда прибыл(а)', 'Комментарии'])
        for p in list_people:
            writer.writerow([p.people_name.capitalize(), p.people_patronymic.capitalize(), p.people_family.capitalize(), Gender.from_int(p.people_gender), p.people_came_from.capitalize(), p.people_comment.capitalize()])

        output_string = si.getvalue()
        si.close()

        return output_string

