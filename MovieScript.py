# Fun practice with some basic python and programming concepts to find and
# display data about film box-office performance.
#
# Author: ddeneau
# Thanks to PyGame : https://www.pygame.org/contribute.html
# Thanks to Beautiful Soup : https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# todo:
# Fix graphing all quarters together
# Add GUI
# Get more data!


import random
import re
import time

import bs4
import matplotlib.pyplot as plt
import numpy as np
import requests

#  import pygame (Not used right now)

# Some constants for swapping quarters in and out.
# Domestic early top grossing films per quarter or season, for 44 years.
JANUARY_MARCH = "https://www.boxofficemojo.com/quarter/q1/?grossesOption=calendarGrosses"
APRIL_JUNE = "https://www.boxofficemojo.com/quarter/q2/?grossesOption=calendarGrosses"
JULY_SEPTEMBER = "https://www.boxofficemojo.com/quarter/q3/?grossesOption=calendarGrosses"
OCTOBER_DECEMBER = "https://www.boxofficemojo.com/quarter/q4/?grossesOption=calendarGrosses"
SUMMER = "https://www.boxofficemojo.com/season/summer/?grossesOption=totalGrosses"
SPRING = "https://www.boxofficemojo.com/season/spring/?grossesOption=totalGrosses"
WINTER = "https://www.boxofficemojo.com/season/winter/?grossesOption=totalGrosses"
FALL = "https://www.boxofficemojo.com/season/fall/?grossesOption=totalGrosses"
MONTHLY = "https://www.boxofficemojo.com/month/february/?grossesOption=calendarGrosses"
MONTHS = ("january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
          "december")

# Top foreign films by country, weekly.
INTERNATIONAL = "https://www.boxofficemojo.com/intl/?ref_=bo_nb_ql_tab"


# Switch case function for choosing quarters.
def switch_quarter(quarter):
    switcher = {
        1: JANUARY_MARCH,
        2: APRIL_JUNE,
        3: JULY_SEPTEMBER,
        4: OCTOBER_DECEMBER,
        5: WINTER,
        6: SPRING,
        7: SUMMER,
        8: FALL
    }
    return switcher.get(quarter, "Invalid Choice")


# Switch case function for choosing months.
def switch_month(month):
    switcher = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    return switcher.get(month, "Invalid Choice")


# Switch case function for matplotlib colors.
def switch_color(color):
    switcher = {
        1: 'blue',
        2: 'red',
        3: 'green',
        4: 'yellow',
        5: 'cyan',
        6: 'magenta',
    }
    return switcher.get(color, 'yellow')


# Class for handling input. Initiates main script.
class Driver:

    def __init__(self):
        self.quarter = 0  # Fiscal quarter as a number, handled by switcher above.
        self.loop_on = True  # boolean for main loop.
        self.graphics = Graphics()  # For making graphs.
        self.months = list("")
        self.separate_month_links(self.months)
        self.main()  # Runs main prompt loop.

    # Prompts user for a selection of periods to display data from. Then prompts user to
    # continue or return and quit the loop.
    def main(self):
        while self.loop_on:
            mode = input(" Press 'M' for reports by month \n Press 'Q' for reports by quarter.")

            if mode is "M":
                try:
                    month_choice = (int(input("  Enter a number (1-12) representing a month. \n  Enter 0 to generate "
                                              "reports for each month: ")))
                except ValueError:
                    print("")

                script = MovieScript(JULY_SEPTEMBER)

                try:
                    script.find_data_by_month(self.months, month_choice, self.graphics)
                except ConnectionError:
                    print("Not connected to Internet. ")

            elif mode is "Q":
                try:
                    self.quarter = switch_quarter(int(input("   Enter a number (1-4) representing a quarter. \n "
                                                            "  Enter a number (5-8) representing a season \n"
                                                            "    5 - Winter \n"
                                                            "    6 - Spring \n"
                                                            "    7 - Summer \n"
                                                            "    8 - Fall: ")))
                except ValueError:
                    print("")

                script = MovieScript(self.quarter)  # Passes in user selection as a period of time.

                try:
                    script.populate_lists_from_url(self.quarter)
                except ConnectionError:
                    print("Not connected to Internet. ")

                script.print_report_by_season(self.quarter, self.graphics)

            else:
                script = InternationalScript()
                script.run()

            if input("Continue? (Y/N) ") is "N":
                self.loop_on = False
                return
            else:
                continue

    @staticmethod
    def separate_month_links(months):
        index = 0
        url_front = "https://www.boxofficemojo.com/month/"
        url_back = "/?grossesOption=calendarGrosses"

        for month in MONTHS:
            months.insert(index, url_front + month + url_back)
            index += 1


# Gets data from www.BoxOfficeMojo.com.
# Generates simple report of what movies performed best at the box office, by season.
class MovieScript:

    def __init__(self, site):
        self.site = ""  # Eventually turns URL string into a representation that bs4 can use.
        self.movie_collection = None  # Stores HTML code related to movie titles.
        self.gross_collection = None  # Stores HTMl code related to gross data.
        self.movies = list()  # List of titles of top box-office grosses
        self.grosses = list()  # List of top box-office grosses (as text)
        self.report = dict()  # Mapping of titles to their amounts.
        self.movie_site_url = ""  # Section of page with movie titles.
        self.gross_site_url = ""  # Section of page with gross information. 

    # Takes raw data from Box Office Mojo and turns it into a list compatible with the script.
    # Specifically a list of movie titles.
    def add_movies(self):
        index = 0

        for titles in self.movie_collection:
            if index == 0:  # Skips extraneous data in first entry.
                time.process_time_ns()
            else:
                self.movies.append(titles.text)
            index += 1

    # Takes raw data from Box Office Mojo and turns it into a list compatible with the script.
    # Specifically a list of grosses.
    def add_grosses(self, limit, divisor):
        index = 0

        for amount in self.gross_collection:
            if index < limit:  # Skips extraneous data in first three entries.
                time.process_time_ns()
            else:
                self.grosses.append(amount.text)
            index += 1

        self.clean_grosses(divisor)

    # Clears the list of grosses of extraneous strings.
    def clean_grosses(self, divisor):
        index = 0
        new_list = list()

        for item in self.grosses:
            if (index % divisor) == 0 and index > 0:  # Skips extraneous data in entries first and some other entries.
                new_list.append(item)

            index += 1

        self.grosses = new_list

    # Maps movie titles to their grosses.
    def map_information(self):
        for movie in self.movies:
            if len(self.grosses) > 0:
                self.report[movie] = self.grosses.pop(0)

    # Compiles a report
    def print_report_by_season(self, quarter, graphics):
        # Data collection and sorting.
        self.add_grosses(3, 4)
        self.add_movies()
        self.map_information()
        season = ""

        # Heading information sorting.

        if quarter is WINTER or SPRING or SUMMER or FALL:
            if quarter is WINTER:
                season = "Winter"
            elif quarter is SPRING:
                season = "Spring"
            elif quarter is SUMMER:
                season = "Summer"
            elif quarter is FALL:
                season = "Fall"

            print(season)

        else:
            if quarter is JANUARY_MARCH:
                start = "January"
                stop = "March"
                season = "Q1"
            elif quarter is APRIL_JUNE:
                start = "April"
                stop = "June"
                season = "Q2"
            elif quarter is JULY_SEPTEMBER:
                start = "July"
                stop = "September"
                season = "Q3"
            else:
                start = "October"
                stop = "December"
                season = "Q4"

            print("From " + start + " to " + stop)

        print("Title ------- Gross")

        # Outputs data to console.
        for item in list(self.report):
            print(" " + item + " ------- " + self.report.get(item))

        if input("Graph?: (Y/N") is "Y":
            graphics.graph_data(self.report, season, False)
        else:
            return

    # Finds and compiles information for films by month
    def find_data_by_month(self, months, month, graphics):
        by_month = False
        month_number = 1

        for link in months:
            self.populate_lists_from_url(link)
            self.add_movies()
            self.add_grosses(3, 4)
            self.map_information()

            if month is 0:
                self.print_report_by_month(month_number, self.report, graphics)
            elif month is month_number:
                self.print_report_by_month(month, self.report, graphics)
                return

            self.grosses.clear()
            self.movies.clear()
            self.report.clear()
            month_number += 1

    # Compiles and outputs to console information about a certain month.
    def print_report_by_month(self, month, report, graphics):
        self.map_information()

        print("Month: " + switch_month(month))

        for item in list(report):
            print(" " + item + " ------- " + self.report.get(item))

        graphics.graph_data(report, switch_month(month), True)

    # Takes raw data from Box Office Mojo and turns it into a list compatible with the script.
    def populate_lists_from_url(self, link):
        site = requests.get(link)
        self.movie_site_url = bs4.BeautifulSoup(site.text, features='lxml')
        self.movie_collection = self.movie_site_url.find_all(class_=re.compile("a-text-left "
                                                                               "mojo-field-type-release "
                                                                               "mojo-cell-wide"))
        self.gross_site_url = bs4.BeautifulSoup(site.text, features='lxml')
        self.gross_collection = bs4.BeautifulSoup(site.text, features='lxml')
        self.gross_collection = self.gross_site_url.find_all(
            class_=re.compile("a-text-right mojo-field-type-money"))


# Uses Box Office Mojo data to display report of international film data.
# todo: fix this class's output and data structuring.
class InternationalScript:

    def __init__(self):
        self.site = requests.get(INTERNATIONAL)  # turns URL string into a representation that bs4 can use.
        self.countries_collection = None  # Stores HTML text regarding country
        self.titles_collection = None  # Stores HTML text regarding title
        self.date_collection = None  # Stores HTML text regarding date
        self.titles = list()  # Stores strings of film titles.
        self.countries = list()  # Stores strings of countries
        self.dates = list()  # Stores strings of month and period of days
        self.films_to_dates = dict()  # Mapping of films to their dates of record performance.
        self.films_to_countries = dict()  # Mapping of films to countries

    # Populates information from sections on the worldwide performance.
    def find_data(self):
        self.site = bs4.BeautifulSoup(self.site.text, features='lxml')
        self.countries_collection = self.site.find_all(
            class_=re.compile("a-text-left mojo-header-column mojo-truncate mojo-field-type-area_id"))

        self.site = bs4.BeautifulSoup(self.site.text, features='lxml')
        self.titles_collection = self.site.find_all(class_=re.compile
        ("a-text-left mojo-field-type-release mojo-cell-wide"))

        self.site = bs4.BeautifulSoup(self.site.text, features='lxml')
        self.date_collection = self.site.find_all(class_=re.compile("a-text-left mojo-field-type-date_interval"))

    # Makes information more data structure friendly
    def list_data(self):
        for item in self.countries_collection:
            self.countries.append(item.text)

        for item in self.titles_collection:
            self.titles.append(item.text)

        for item in self.date_collection:
            self.dates.append(item.text)

        for title in self.titles:
            if len(self.dates) > 0:
                self.films_to_date[title] = self.dates.pop(0)

        for date in self.dates:
            if len(self.dates) > 0:
                self.films_to_countries[date] = self.countries.pop(0)

    # calls main operations
    def run(self):
        self.find_data()
        self.list_data()
        self.print()

    # Outputs results to console.
    def print(self):
        print(self.titles)
        print(self.dates)
        print(self.countries)


# Handles visualization of data.
# todo:
# Implement GUI. For now its just console based. But pygame is set up to run after the main program.
# Need to make an API for the UserInput or Driver class to add features to a pygame session.
class Graphics:

    def __init__(self):
        self.reports = list()

    # Turns text taken from HTML into numbers for numpy
    @staticmethod
    def get_gross_numbers(data):
        new_list = list()

        for value in data.values():
            chunk = ""

            for character in value:
                if character.isdigit():
                    chunk += character
            try:
                gross = re.findall(r'\d+', chunk.__str__())
                digit = int(gross.pop(0)) / 1000000
                new_list.append(digit)
                chunk = ""
            except TypeError:
                continue

        return new_list

    # Creates and displays a scatter plot .
    @staticmethod
    def graph_data(data, time_frame, monthly):
        title = "Highest Grossing film per year in " + time_frame if monthly else "Highest Grossing film per year " \
                                                                                  "during:" + time_frame

        fig, ax = plt.subplots()

        x = np.arange(0, len(data.items()))
        y = np.asarray(Graphics.get_gross_numbers(data))
        ax.set_xlabel('Years in past')
        ax.set_ylabel('Gross (Millions of Dollars) ')
        ax.set_title(title)

        for i in range(x.size):
            color = switch_color(random.randrange(1, 7))
            point_label = list(data).pop(i)
            point_label = str.strip(point_label, " ")
            plt.scatter(x[i], y[i], s=30, c=color, alpha=0.3)
            plt.text(x[i], y[i] + 2, point_label, fontsize=4)

        plt.show()


# Quick way to run the program without a GUI.
while True:
    try:
        print("Welcome to the program.")
        driver = Driver()
    except ValueError:
        print("")
    except KeyboardInterrupt:
        print("")
