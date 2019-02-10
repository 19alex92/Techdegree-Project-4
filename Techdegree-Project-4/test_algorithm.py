import datetime
import unittest
from unittest import mock

from peewee import *

from algorithm import WorkLog, Search
import work_log as log

test_db = SqliteDatabase('test_database.db')


class TestData(Model):

    employee_name = CharField(max_length=255)
    task = CharField(max_length=255)
    time = IntegerField()
    date = DateTimeField()
    notes = TextField(default=None)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = test_db


data = TestData.select()
start_testing = Search(data)


def initialize():
        """Creates the database and the table if they don't exist."""
        test_db.connect()
        test_db.create_tables([TestData], safe=True)


def add_to_file():
    exist = TestData.select()
    if exist.exists():
        pass
    else:
        TestData.create(employee_name='Test Person', date=datetime.datetime(2019, 1, 1, 0, 0, 0, 0),
                        task='Test Task', time=55, notes='Test note')


class AlgorithmTests(unittest.TestCase):

    def setUp(self):
        # This mimics the user input
        self.employee_name = 'Test Person'
        self.date = datetime.datetime(2019, 1, 1, 0, 0, 0, 0)
        self.task = 'Test Task'
        self.time = 55
        self.notes = 'Test note'

    def test_search_string(self):
        method = start_testing.search_string(self.employee_name, TestData)
        self.assertEqual(method, data)

    def test_search_employee(self):
        method = start_testing.search_employee(self.employee_name, TestData)
        self.assertEqual(method, data)

    def test_search_time(self):
        method = start_testing.search_time(self.time, TestData)
        self.assertEqual(method, data)

    def test_search_date(self):
        method = start_testing.search_date(self.date, TestData)
        self.assertEqual(method, data)

    def test_search_between_date(self):
        method = start_testing.search_between_date(self.date, self.date, TestData)
        self.assertEqual(method, data)

    def test_show_all_employees(self):
        method = start_testing.show_all_employees(TestData)
        self.assertEqual([data for data in method], [self.employee_name])

    def test_show_all_dates(self):
        method = start_testing.show_all_dates(TestData)
        self.assertEqual([data for data in method], ['01/01/2019'])

    def test_edit_entry(self):
        method = start_testing.edit_entry(TestData.get(), 1, self.employee_name)
        self.assertEqual(method, TestData.get())
        method = start_testing.edit_entry(TestData.get(), 2, self.date)
        self.assertEqual(method, TestData.get())
        method = start_testing.edit_entry(TestData.get(), 3, self.task)
        self.assertEqual(method, TestData.get())
        method = start_testing.edit_entry(TestData.get(), 4, self.time)
        self.assertEqual(method, TestData.get())
        method = start_testing.edit_entry(TestData.get(), 5, self.notes)
        self.assertEqual(method, TestData.get())

    def test_add_entry(self):
        pass

    def test_search_entry(self):
        pass

    def test_result_menue(self):
        pass

    def test_main_menu(self):
        mock.builtins.input = lambda _: "A"
        assert log.main_menu == log.add_entry()



if __name__ == "__main__":
    initialize()
    add_to_file()
    unittest.main()
