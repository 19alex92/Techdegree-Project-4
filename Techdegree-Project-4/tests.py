import datetime
import unittest
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
        TestData.create(employee_name='Test Person',
                        date=datetime.datetime(2019, 1, 1, 0, 0, 0, 0),
                        task='Test Task', time=55, notes='Test note')


class AlgorithmTests(unittest.TestCase):

    def setUp(self):

        data = WorkLog()
        data = data.select()

        self.employee_name = 'Test Person'
        self.date = datetime.datetime(2019, 1, 1, 0, 0, 0, 0)
        self.raw_date = "12/12/2019"
        self.task = 'Test Task'
        self.time = 55
        self.notes = "agtzuiklmnbew"

        self.search_solution = data.where(
            WorkLog.notes.contains("agtzuiklmnbew")
        )
        self.search_entry_date_solution = data.where(
            WorkLog.date.contains(datetime.datetime.strptime(self.raw_date,
                                                             "%d/%m/%Y"))
        )

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
        method = start_testing.search_between_date(self.date,
                                                   self.date, TestData)
        self.assertEqual(method, data)

    def test_show_all_employees(self):
        method = start_testing.show_all_employees(TestData)
        self.assertEqual([data for data in method], [self.employee_name])

    def test_show_all_dates(self):
        method = start_testing.show_all_dates(TestData)
        self.assertEqual([data for data in method], ['01/01/2019'])

    def test_edit_entry(self):
        method = start_testing.edit_entry(TestData.get(), 1,
                                          self.employee_name)
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
        log.add_entry(self.employee_name, self.raw_date, self.task,
                      self.time, self.notes, decision='Y', access=False)

        self.assertEqual([value.notes for value in self.search_solution],
                         [self.notes])

        for value in self.search_solution:
            value.delete_instance()

        self.assertEqual(log.add_entry(self.employee_name, self.raw_date,
                                       self.task, self.time,
                                       self.notes, decision='N',
                                       access=False), 'test_successful')

        with self.assertRaises(ValueError):
            log.add_entry(employee_name=self.employee_name,
                          raw_date='45', task=self.task, time=self.time,
                          notes=self.notes, decision='N', access=False)

        with self.assertRaises(ValueError):
            log.add_entry(employee_name=None, raw_date=self.raw_date,
                          task=self.task, time=self.time, notes=self.notes,
                          decision='N', access=False)

        with self.assertRaises(ValueError):
            log.add_entry(employee_name=self.employee_name,
                          raw_date=self.raw_date, task=None, time=self.time,
                          notes=self.notes, decision='N', access=False)

        with self.assertRaises(ValueError):
            log.add_entry(employee_name=self.employee_name,
                          raw_date=self.raw_date, task=self.task, time=-1,
                          notes=self.notes, decision='N', access=False)

    def test_search_entry(self):
        log.add_entry(self.employee_name, self.raw_date, self.task, self.time,
                      self.notes, decision='Y', access=False)

        self.assertEqual([value.date for value in log.search_entry(
            input_search='a', raw_date_input=self.raw_date, access=False)],
            [value.date for value in self.search_entry_date_solution]
            )
        self.assertEqual([value.date for value in log.search_entry(
            input_search='b', raw_date1_input="11/12/2019",
            raw_date2_input="13/12/2019", access=False)],
            [value.date for value in self.search_entry_date_solution]
            )
        self.assertEqual([value.time for value in log.search_entry(
            input_search='c', input_user=self.time, access=False)],
            [self.time]
            )
        self.assertEqual([value.notes for value in log.search_entry(
            input_search='d', input_user=self.notes, access=False)],
            [self.notes]
            )
        self.assertEqual([value.employee_name for value in log.search_entry(
            input_search='e', input_user=self.employee_name, access=False)],
            [self.employee_name]
            )

        for value in self.search_solution:
            value.delete_instance()

        self.assertEqual(log.search_entry(input_search='h',
                                          access=False), 'test_successful')

        with self.assertRaises(ValueError):
            log.search_entry(input_search='a', raw_date_input='32/02/2019',
                             access=False)
        with self.assertRaises(ValueError):
            log.search_entry(input_search='a', raw_date_input='32/02/2019',
                             user_input_2='R', access=False)
        with self.assertRaises(ValueError):
            log.search_entry(input_search='b', raw_date1_input="35-11-2019",
                             raw_date2_input="36-12-2019", access=False)
        with self.assertRaises(ValueError):
            log.search_entry(input_search='b', raw_date1_input="35-11-2019",
                             raw_date2_input="36-12-2019", user_input_2='R',
                             access=False)
        with self.assertRaises(ValueError):
            log.search_entry(input_search='b', raw_date1_input="11/12/2019",
                             raw_date2_input="36-12-2019", access=False)
        with self.assertRaises(ValueError):
            log.search_entry(input_search='b', raw_date1_input="11/12/2019",
                             raw_date2_input="36-12-2019", user_input_2='R',
                             access=False)
        with self.assertRaises(ValueError):
            log.search_entry(input_search='c', input_user='test', access=False)
        with self.assertRaises(ValueError):
            log.search_entry(input_search='d', input_user=None, access=False)
        with self.assertRaises(ValueError):
            log.search_entry(input_search='e', input_user=None, access=False)

    def test_result_menue(self):
        log.add_entry(self.employee_name, self.raw_date, self.task, self.time,
                      self.notes, decision='Y', access=False)

        self.assertEqual(log.result_menue(self.search_solution, user_input='N',
                                          access=False), 'test_successful')
        self.assertEqual(log.result_menue(self.search_solution, user_input='N',
                                          page_count=True,
                                          access=False), 'test_successful')
        self.assertEqual(log.result_menue(self.search_solution, user_input='E',
                                          access=False), 'test_successful')
        self.assertEqual(log.result_menue(self.search_solution, user_input='D',
                                          user_input_2='Y',
                                          access=False), 'test_successful')
        self.assertEqual(log.result_menue(self.search_solution, user_input='D',
                                          user_input_2='N',
                                          access=False), 'test_successful')
        self.assertEqual(log.result_menue(self.search_solution, user_input='R',
                                          access=False), 'test_successful')
        self.assertEqual(log.result_menue(self.search_solution, user_input='G',
                                          access=False), 'test_successful')

        for value in self.search_solution:
            value.delete_instance()

    def test_main_menu(self):
        self.assertEqual(log.main_menu(input_menue='a',
                                       access=False), 'test_successful')
        self.assertEqual(log.main_menu(input_menue='c',
                                       access=False), 'test_successful')

        log.add_entry(self.employee_name, self.raw_date, self.task,
                      self.time, self.notes, decision='Y', access=False)

        self.assertEqual(log.main_menu(input_menue='b',
                                       access=False), 'test_successful')

        with self.assertRaises(ValueError):
            log.main_menu(input_menue='b', entry=False, access=False)

        for value in self.search_solution:
            value.delete_instance()

        with self.assertRaises(ValueError):
            log.main_menu(input_menue='e', access=False)


if __name__ == "__main__":
    initialize()
    add_to_file()
    unittest.main()
