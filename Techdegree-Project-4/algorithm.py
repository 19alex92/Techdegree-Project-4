import csv
import datetime
import os
import re

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

    def edit_entry(self, initial_file, delete_index, input_key, input_user):
        if input_key == 1:
            input_key = 'Date'
        elif input_key == 2:
            input_key = 'Task name'
        elif input_key == 3:
            input_key = 'Time spent'
        elif input_key == 4:
            input_key = 'Notes'
        initial_file[delete_index].update({input_key: input_user})

    def delete_entry(self, value):
        value.delete_instance()
