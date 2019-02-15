import datetime
import unittest
from unittest import mock
import unittest.mock


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

        data = WorkLog()
        data = data.select()
        self.search_solution = data.where(WorkLog.notes.contains("agtzuiklmnbew"))

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

    def test_texts(self):
        text = str(log.enter)
        self.assertEqual(log.enter, text)

        text = str(log.try_again)
        self.assertEqual(log.try_again, text)

        text = str(log.no_entry)
        self.assertEqual(log.no_entry, text)

        text = str(log.not_valid)
        self.assertEqual(log.not_valid, text)

        text = str(log.text_search_entry)
        self.assertEqual(log.text_search_entry, text)

        text = str(log.edit_entry_text)
        self.assertEqual(log.edit_entry_text, text)

        text = str(log.text_main_menu)
        self.assertEqual(log.text_main_menu, text)

    def test_add_entry(self):
        employee_name = "TestPerson"
        raw_date = "12/12/2019"
        task = "TestTask"
        time = 45
        notes = "agtzuiklmnbew"
        decision = "Y"
        log.add_entry(employee_name, raw_date, task, time, notes, decision)
        self.assertEqual([value.notes for value in self.search_solution], [notes])
        for value in self.search_solution:
            value.delete_instance()

        self.assertEqual(log.add_entry(employee_name, raw_date, task, time, notes, decision='N'), 'test_successful')

        with self.assertRaises(ValueError):
            log.add_entry(employee_name=employee_name, raw_date='45', task=task, time=time, notes=notes, decision='N')

        with self.assertRaises(ValueError):
            log.add_entry(employee_name=None, raw_date=raw_date, task=task, time=time, notes=notes, decision='N')

        with self.assertRaises(ValueError):
            log.add_entry(employee_name=employee_name, raw_date=raw_date, task=None, time=time, notes=notes, decision='N')

        with self.assertRaises(ValueError):
            log.add_entry(employee_name=employee_name, raw_date=raw_date, task=task, time=-1, notes=notes, decision='N')

    def test_search_entry(self):
        pass

    def test_result_menue(self):
        pass

    def test_main_menu(self):
        pass
        #with unittest.mock.patch('builtins.input', return_value='D'):
         #   assert log.main_menu() == "Ups this doesn't seem to be a valid input."

        #with self.assertRaises(ValueError):
         #   log.main_menu("e")


if __name__ == "__main__":
    initialize()
    add_to_file()
    unittest.main()
