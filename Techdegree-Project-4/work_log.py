#!/usr/bin/env python3

import datetime
import os

from algorithm import Search, WorkLog

data = WorkLog()
start = Search(data.select())


def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")


def add_entry():
    '''Menu to add a new entry to the database'''

    while True:
        clear_screen()
        print("Welcome, please type in your name.")
        try:
            employee_name = input(">  ")
            if employee_name:
                try:
                    int(employee_name)
                    clear_screen()
                    input("Your input is not valid, press enter to try again.")
                    continue
                except ValueError:
                    break
            else:
                raise ValueError
        except ValueError:
            clear_screen()
            input("Your input is not valid, press enter to try again.")
            continue

    while True:
        clear_screen()
        print("What is the date of the task?")
        raw_date = input("Use the format DD/MM/YYYY  >  ")
        try:
            date = datetime.datetime.strptime(raw_date, "%d/%m/%Y")
            break
        except ValueError:
            clear_screen()
            print("Ups! Seems like '{}' isn't a valid date.".format(raw_date))
            input("Press enter to try again")
            continue

    while True:
        task = None
        clear_screen()
        print("What is the task name?")
        try:
            task = input(">  ")
            if task:
                break
            else:
                raise ValueError
        except ValueError:
            clear_screen()
            print("You have to give your task a name")
            input("Press enter to try again")
            continue

    while True:
        try:
            clear_screen()
            print("How much time did it take in rounded minutes?")
            time = int(input(">  "))
            if time < 0:
                raise ValueError
            break
        except ValueError:
            clear_screen()
            print("Ups this doesn't seem to be a valid rounded minutes input")
            input("Press enter to try again.")
            continue

    clear_screen()
    print("Additional notes...if you dont have any notes please press enter")
    notes = input(">  ")

    clear_screen()
    print("Thank you! Do you want to submit your entry? Y/N")
    decision = input(">  ")

    if decision.upper() == 'Y':
        start.add_to_file(employee_name, date, task, time, notes)
        clear_screen()
        input("The entry has been added successfully! Press enter to continue")
    else:
        clear_screen()
        input("Your entry will not be saved, press enter to continue")


def search_entry():
    '''Menu to search for an existing entry'''
    date1 = None
    date2 = None
    input_user = None

    while True:
        clear_screen()
        print("How would you like to search for an entry?")
        print("a) By Date")
        print("b) Between dates")
        print("c) By Time Spent")
        print("d) By search term")
        print("e) By name of employee")
        print("f) Back to main menue")
        input_search = input("  > ")

        if input_search == "a":
            # search by a date
            clear_screen()
            text = "Please enter a date from the dates above"
            print("\nList of dates in the database:\n")
            print("="*len(text))
            for date in start.show_all_dates():
                print(date)
            print("="*len(text)+"\n")
            print(text)
            raw_date_input = input("Use the format DD/MM/YYYY:  ")
            try:
                input_user = datetime.datetime.strptime(raw_date_input,
                                                        "%d/%m/%Y")
                search_file = start.search_date(input_user)
                result_menue(search_file)
                break
            except ValueError:
                clear_screen()
                print("Ups! Seems like '{}' isn't a valid date."
                      .format(raw_date_input))
                print("Press enter to try again or 'R' "
                      "to return to the main menu.")
                user_input = input(">  ")
                if user_input.upper() == "R":
                    break
                else:
                    continue

        elif input_search == "b":
            # search between two dates
            clear_screen()
            print("Please enter the first date")
            raw_date1_input = input("Use the format DD/MM/YYYY:  ")
            try:
                date1 = datetime.datetime.strptime(raw_date1_input, "%d/%m/%Y")
            except ValueError:
                clear_screen()
                print("Ups! Seems like '{}' isn't a valid date."
                      .format(raw_date1_input))
                print("Press enter to try again or 'R' "
                      "to return to the main menu.")
                user_input = input(">  ")
                if user_input.upper() == "R":
                    break
                else:
                    continue
            clear_screen()
            print("Please enter the second date")
            raw_date2_input = input("Use the format DD/MM/YYYY:  ")
            try:
                date2 = datetime.datetime.strptime(raw_date2_input, "%d/%m/%Y")
            except ValueError:
                clear_screen()
                print("Ups! Seems like '{}' isn't a valid date."
                      .format(raw_date2_input))
                print("Press enter to try again or 'R' "
                      "to return to the main menu.")
                user_input = input(">  ")
                if user_input.upper() == "R":
                    break
                else:
                    continue
            search_file = start.search_between_date(date1, date2)
            result_menue(search_file)
            break

        elif input_search == "c":
            # search for time spent
            clear_screen()
            print("Please enter how much time the task took in minutes")
            try:
                input_user = int(input("EXAMPLE: Use the format "
                                       "45 for 45 minutes:  "))
                search_file = start.search_time(input_user)
                result_menue(search_file)
                break
            except ValueError:
                clear_screen()
                print("Ups this doesn't seem to "
                      "be a valid rounded minutes input")
                input("Press enter to try again.")
                continue

        elif input_search == "d":
            # search for string in title, notes or name of employee
            clear_screen()
            input_user = None
            print("Please enter a word")
            print("It can be in the Title, Notes or the name of employee.")
            try:
                input_user = input(">  ")
                if input_user:
                    search_file = start.search_string(input_user)
                    result_menue(search_file)
                    break
                else:
                    raise ValueError
            except ValueError:
                clear_screen()
                input("Seems like you havn't entered anything, "
                      "press enter to try again.")
                continue

        elif input_search == "e":
            # search for name of employee
            clear_screen()
            input_user = None
            text = "Please enter a name or a portion of the name from above"
            print("\nList of employee names in the database:\n")
            print("="*len(text))
            for employees in start.show_all_employees():
                print(employees)
            print("="*len(text)+"\n")
            print(text)
            try:
                input_user = input(">  ")
                if input_user:
                    search_file = start.search_employee(input_user)
                    result_menue(search_file)
                    break
                else:
                    raise ValueError
            except ValueError:
                clear_screen()
                input("Seems like you havn't entered anything, "
                      "press enter to try again.")
                continue

        elif input_search == "f":
            break

        else:
            clear_screen()
            print("Ups this doesn't seem to be a valid input.")
            input("Press enter to try again")
            continue


def result_menue(search_file):
    '''Displays the search results in a meaningful way'''
    total_page = len(search_file)
    current_page = 1
    loop = True

    while loop:
        clear_screen()

        if search_file.exists():
            for value in search_file:
                timestamp = value.timestamp.strftime('%A %B %d, %Y %I:%M%p')
                date = value.date.strftime('%d/%m/%Y')
                print("\n""Entry added: "+timestamp)
                print('='*(len(timestamp)+13))
                print("Name of employee: "+value.employee_name)
                print("Date of task: "+date)
                print("Task name: "+value.task)
                print("Duration task: {} minutes".format(str(value.time)))
                print("Additional notes: "+value.notes)
                print('='*(len(timestamp)+13))
                print("\nResult {} of {}".format(current_page, total_page))
                print("\n[N]ext, [E]dit, [D]elete, [R]eturn to search menu")
                user_input = input(">  ")
                if user_input.upper() == "N":
                    if current_page < total_page:
                        clear_screen()
                        current_page += 1
                        continue
                    else:
                        clear_screen()
                        current_page = 1
                        continue
                elif user_input.upper() == "E":
                    # Menue to edit entrys
                    clear_screen()
                    print("Which entry would you like to edit?")
                    print("(1)Name of employee, (2)Date of task, "
                          "(3)Task name, (4)Duration task, "
                          "(5)Additional notes")
                    input_key = int(input(">  "))
                    clear_screen()
                    print("Please type in your updated entry and press enter")
                    input_user = input(">  ")
                    start.edit_entry(value, input_key, input_user)
                    clear_screen()
                    input("Update sucessful! Press enter to continue")
                    break

                elif user_input.upper() == "D":
                    # Menue to delete entrys
                    clear_screen()
                    print("\nAre you sure you want to delete this entry? Y/N")
                    user_input = input(">  ")
                    if user_input.upper() == "Y":
                        start.delete_entry(value)
                        clear_screen()
                        input("Deleting successful press enter to continue")
                        loop = False
                    continue
                elif user_input.upper() == "R":
                    search_entry()
                    loop = False
                else:
                    clear_screen()
                    print("Ups this doesn't seem to be a valid input.")
                    input("Press enter to try again")
                    continue
        else:
            input("No search result, press enter to try again")
            search_entry()
            break


def main_menu():
    '''Displays the main menu of the application'''
    while True:
        clear_screen()
        print("WORK LOG")
        print("What would you like to do?")
        print("a) Add new entry")
        print("b) Search for an existing entry")
        print("c) Quit program")
        input_menue = input("  > ")
        if input_menue.upper() == "A":
            add_entry()
            continue
        elif input_menue.upper() == "B":
            try:
                search_entry()
                continue
            except FileNotFoundError:
                clear_screen()
                print("No file, please add entry before search")
                input("Press enter to continue")
                continue
        elif input_menue.upper() == "C":
            break
        else:
            clear_screen()
            print("Ups this doesn't seem to be a valid input.")
            input("Press enter to continue")
            continue


if __name__ == "__main__":
    start.initialize()
    main_menu()
