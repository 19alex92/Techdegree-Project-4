import datetime
import os

from peewee import *

db = SqliteDatabase('data_work_log.db')

class WorkLog(Model):

    employee_name = CharField(max_length=255)
    task = CharField(max_length=255)
    time = IntegerField()
    date = DateTimeField()
    notes = TextField(default=None)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


class Search:

    def __init__(self, initial_file):
        self.initial_file = initial_file

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def initialize(self):
        """Creates the database and the table if they don't exist."""
        db.connect()
        db.create_tables([WorkLog], safe=True)

    def add_to_file(self, employee_name, date, task, time, notes):
        WorkLog.create(employee_name=employee_name, date=date, task=task, time=time, notes=notes)

    def search_string(self, input_user):
        search_file = self.initial_file.where(WorkLog.employee_name.contains(input_user) |
                                              WorkLog.task.contains(input_user) |
                                              WorkLog.notes.contains(input_user))
        return search_file

    def search_employee(self, input_user):
        search_file = self.initial_file.where(WorkLog.employee_name.contains(input_user))
        return search_file

    def search_time(self, input_user):
        search_file = self.initial_file.where(WorkLog.time == (input_user))
        return search_file

    def search_date(self, input_user):
        search_file = self.initial_file.where(WorkLog.date.contains(input_user))
        return search_file

    def search_between_date(self, date1, date2):
        search_file = self.initial_file.where(WorkLog.date.between(date1,
                                                                   date2))
        return search_file

    def show_all_employees(self):
        employees = self.initial_file.select(WorkLog.employee_name).distinct().order_by(WorkLog.employee_name)
        for data in employees:
            print(data.employee_name)

    def show_all_dates(self):
        dates = self.initial_file.select(WorkLog.date).distinct().order_by(WorkLog.date)
        for date in dates:
            date = date.date.strftime('%d/%m/%Y')
            print(date)

    def edit_entry(self, value, input_key, input_user):
        if input_key == 1:
            value.employee_name = input_user
        elif input_key == 2:
            value.date = input_user
        elif input_key == 3:
            value.task = input_user
        elif input_key == 4:
            value.time = input_user
        elif input_key == 5:
            value.notes = input_user
        value.save()

    def delete_entry(self, value):
        value.delete_instance()
