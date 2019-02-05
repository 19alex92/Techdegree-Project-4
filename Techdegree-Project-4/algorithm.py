import csv
import datetime
import os
import re


class Search:

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def open_file(self, dict_files):
        with open('log.csv', newline='') as file:
            reader = csv.DictReader(file)
            data = list(reader)

            for row in data:
                dict_files.append(dict(row))

    def add_to_file(self, date, task, time, notes):
        with open('log.csv', 'a', newline='') as file:
            file_is_empty = os.stat('log.csv').st_size == 0
            fieldnames = ['Date', 'Task name', 'Time spent', 'Notes']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if file_is_empty:
                writer.writeheader()
            writer.writerow({'Date': date, 'Task name': task,
                             'Time spent': time, 'Notes': notes})

    def backup_file(self, initial_file):
        '''Creates a backup file in case someting goes bad while updating'''
        for data in initial_file:
            with open('log_backup.csv', 'a', newline='') as file:
                file_is_empty = os.stat('log_backup.csv').st_size == 0
                write = csv.DictWriter(file, data.keys())
                if file_is_empty:
                    write.writeheader()
                write.writerow(data)

    def update_file(self, initial_file):
        '''Deletes the current file and updates it, in the end deletes the
           backup file in case everything worked as expected
        '''
        os.remove('log.csv')
        for data in initial_file:
            with open('log.csv', 'a', newline='') as file:
                file_is_empty = os.stat('log.csv').st_size == 0
                write = csv.DictWriter(file, data.keys())
                if file_is_empty:
                    write.writeheader()
                write.writerow(data)
        os.remove('log_backup.csv')

    def search_string(self, initial_file, search_file,
                      task_name, task_notes, input_user, index_track):
        iteration = 0

        for data in initial_file:
            if (task_name and input_user.upper() in
                    initial_file[iteration][task_name].upper()):
                index_track.append(iteration)
                search_file.append(dict(data))
                iteration += 1
            elif (task_notes and input_user.upper() in
                    initial_file[iteration][task_notes].upper()):
                index_track.append(iteration)
                search_file.append(dict(data))
                iteration += 1
            else:
                iteration += 1

    def search_time(self, initial_file, search_file,
                    task_minutes, input_user, index_track):
        iteration = 0

        for data in initial_file:
            if (task_minutes and input_user in
                    initial_file[iteration][task_minutes]):
                index_track.append(iteration)
                search_file.append(dict(data))
                iteration += 1
            else:
                iteration += 1

    def search_regex(self, initial_file, search_file,
                     regex, input_user, index_track):
        iteration = 0

        for _ in initial_file:
            key_iter = 0
            if regex:
                    for _ in regex:
                        pattern = re.search(input_user,
                                            initial_file[iteration]
                                                        [regex[key_iter]])
                        if pattern is None:
                            key_iter += 1
                            continue
                        elif (pattern.group() in
                                initial_file[iteration][regex[key_iter]]):
                            index_track.append(iteration)
                            search_file.append(dict(initial_file[iteration]))
                            key_iter += 1
                            break
                        else:
                            key_iter += 1
                    iteration += 1
            else:
                iteration += 1

    def search_date(self, initial_file, search_file, date_search,
                    date1, date2, input_user, index_track):
        iteration = 0

        for data in initial_file:
            if date_search:
                if str(input_user) == initial_file[iteration][date_search]:
                    index_track.append(iteration)
                    search_file.append(dict(data))
                    iteration += 1
                elif date1 and date2:
                    saved_date = datetime.datetime.strptime(initial_file
                                                            [iteration]
                                                            [date_search],
                                                            "%Y-%m-%d %X")
                    if date1 <= saved_date and date2 >= saved_date:
                        index_track.append(iteration)
                        search_file.append(dict(data))
                        iteration += 1
                    else:
                        iteration += 1
                else:
                    iteration += 1
            else:
                iteration += 1

    def format_date(self, search_file):
        '''Formates the date back to a nice format'''
        for data in search_file:
            for value in data.values():
                try:
                    output_date = datetime.datetime.strptime(value,
                                                             "%Y-%m-%d %X")
                    data.update({'Date': output_date.strftime('%d/%m/%Y')})
                except ValueError:
                    continue

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

    def delete_entry(self, initial_file, delete_index):
        del initial_file[delete_index]
        return initial_file
