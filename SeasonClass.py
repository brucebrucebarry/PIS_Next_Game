"""
This file houses the Seasons class.
"""
import os
from PIS_Next_Game import bs_obj_return
import re
import datetime
from datetime import timedelta
import itertools

cd = os.getcwd()
season_dir = cd + "\seasons"

MONTHS = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}

class Season:

    def __init__(self, season_link):
        self.season_link = season_link
        self.name = None                # captured post initialization get_season_name()
        self.year = None                # captured post initialization get_season_name()
        self.start_date = None          # captured post initialization set_season_start_end()
        self.end_date = None            # captured post initialization set_season_start_end()
        self.rereg_deadline = None      # captured post initialization set_rereg_deadline()
        self.all_games = []             # populated by organize_raw_games(), all games in an encapsulated list[division[games]]
        self.compiled_games = []        # organized by datetime organize_raw_games()
        self.total_matches = None       # captured post initialization add_match_number()
        self.total_match_days = None    # captured post initialization return_season_length()
        self.match_days = []            # captured post initialization
        os.chdir(season_dir)            # TODO: changes the directory while open, *NTD(changed back when closed)*

    def __len__(self):
        print(f"This season has:{len(self.all_games)} divisions. Returning number of games in this season")
        return len(self.all_games)

    def __repr__(self):
        return (f"This is the self.__class__.__name__: {self.__class__.__name__}")

    def main(self):
        """
        runs the season after the season object is created to make sure everything is populated in the correct order

        :return: None
        """
        self.gather_schedules()             # gathers all the external data from PDXindoorsoccer.com
        self.sort_by_first_dt_element()     # sorts the games by date and removes duplicated games
        self.set_season_start_end()         # gathers the dates of the start and end of the season
        self.add_match_number()             # gives each game a match number
        self.return_season_length()         # calculates the number of match days in the season

    # Date functions
    def create_datetime_object(self, month_str, day_str, hour, minutes):
        """
        Will create a datetime object out of self.year, month, day, hour, minutes

        :param month_str:
        :param day_str:
        :param hour:
        :param minutes:

        :return: datetime object
        """
        month = MONTHS[month_str]
        day = int(day_str)
        datetime_obj = datetime.datetime(self.year, month, day, hour, minutes)
        return datetime_obj

    def create_date_object(self, month_int, day_int):
        """
        Creates and returns a date object

        :param month_int:
        :param day_str:
        :return: a date object
        """

        return datetime.date(self.year, month_int, day_int).strftime("%B %d, %Y")

    # functions that assign init variables
    def get_season_name(self, season_name):
        """
        sets the self.name and self.year variables from season_name

        :param season_name: name of the season as a string
        """
        if not self.name and not self.year:
            self.name = season_name
            self.year = int(season_name[-4:])

    def set_rereg_deadline(self, raw_deadline):
        """
        checks if self.rereg_deadline is not set, if True, Adds the year as the last parameter and append to self.rereg_deadline
        :param deadline:
        :return: None
        """
        if not self.rereg_deadline:
            month = MONTHS[raw_deadline[1]]
            day = int(raw_deadline[2])
            self.rereg_deadline = self.create_date_object(month, day)

    def set_season_start_end(self):
        """
        finds start and end date of the season then updates them to the object

        :return: None
        """
        if not self.start_date:
            self.start_date = self.compiled_games[0][0]
        if not self.end_date:
            self.end_date = self.compiled_games[-1][0]

    def add_match_number(self):
        """
        Ran in self.main()

        this itertes through each game (self.compiled_games) and does 2 things:
        1.  adds the match number to the last element of each game
        2.  sets self.total_matches on the last iteration

        :return: None
        """
        if not self.total_matches:
            match_number = 0
            for match in self.compiled_games:
                self.compiled_games[match_number].append(match_number + 1)
                match_number += 1
            self.total_matches = match_number

    # main functions to gather and format schedules
    def gather_schedules(self):
        """
        Uses BS to go through each divisions schedule and append it as a list to self.all_games

        :return: None
        """

        soup = bs_obj_return(self.season_link)
        all_season = soup.findAll("ul", id="listyofiles")
        for season_links in all_season:
            league = season_links.findAll("a")
            for division in league:
                self.regex_obj_schedule(division.attrs['href'])

    def regex_obj_schedule(self, final_link):
        """
        Used in gather_schedules to RegEx from the string version of the schedule.

        :param final_link: webaddress to the divisions schedule
        :return:None
        """

        raw_schedule_text = (bs_obj_return(final_link)).text # converts to a string
        regex_name = re.search("\w+\sCUP\s\d{4}",raw_schedule_text) # Creates regex match object finding the season name & year
        self.get_season_name(regex_name.group()) # Gets season name and names this instance
        regex_division = re.search("[A-Z]{3,5}\sDIVISION\s\d[A-Z]?",raw_schedule_text) # finds the league and division
        regex_games = re.findall("([A-Z]{3})\s([A-Z]{3})\s*(\d*)\s*(\d*:\d\d)\s*(AM|PM)\s*(.*)",raw_schedule_text) # a list of games in this division
        self.organize_raw_games(regex_games, regex_division.group()) #cleans and adds the proper information to self.all_games
        regex_rereg_geadline = re.search("([A-Z]{3})\s([A-Z]{3})\s*(\d*)\s*DEADLINE TO RE-REGISTER FOR THE NEXT SEASON!",raw_schedule_text)
        self.set_rereg_deadline(regex_rereg_geadline.groups())

    def organize_raw_games(self, raw_games, tagline):
        # TODO make it an easy datetime obj (year, month, day, hour, min, second)
        """
        used in regex_obj_schedule() to clean the raw schedule and append it to self.all_games

        :param raw_games: list of strings gathered from BS scrape of web page.

        Below is the list created
        [0]year
        [1]month
        [2]day
        [3]time
        [4]am/pm
        [5]day of week
        [6]home team
        [7]away team
        [8]league division

        :return: None
        """
        cleaned_games = [] # adds the name of the league and division
        for game in raw_games:
            day_of_week = game[0]       # DOW
            month = game[1]             # month
            day = game[2]               # day
            hour, minutes = self.military_time(game[3], game[4])        # time , AM/PM
            home_team, away_team = self.harvest_teams_names(game[5])    # teams
            dt_obj = self.create_datetime_object(month, day, hour, minutes)
            to_add = [dt_obj, day_of_week, home_team, away_team, tagline]

            cleaned_games.append(to_add)
            self.compiled_games.append(to_add)
        self.all_games.append(cleaned_games)

    def sort_by_first_dt_element(self):
        """
        sorts the self.compiled_games list by its datetime element
        :return: None
        """
        almost_ready = sorted(self.compiled_games, key=lambda x: x[0])
        self.compiled_games = list(almost_ready for almost_ready,_ in itertools.groupby(almost_ready))

    def harvest_teams_names(self, game_line):
        """
        separates the home and away team using "vs" as a deliminator and strip() to remove whitespace

        :param game_line: a string with '  vs  ' seperating the 2 home vs the away
        :return: home team and away team as str
        """
        both_teams = game_line.split("  vs ")
        return both_teams[0].strip(), both_teams[1].strip() # returns home team, away team

    def military_time(self, raw_time, am_pm):
        """
        converts 12 Hr string time format to 24 Hr int format

        :param raw_time: str
        :param am_pm:
        :return:
        """
        split_time = raw_time.split(":")
        hour = int(split_time[0])
        minute = int(split_time[1])
        am_pm = am_pm.lower()
        if am_pm == "pm":
            hour += 12
        return hour, minute

    def new_file_dump(self, file_name, to_dump):
        """
        creates a new file and dumps all the info into it

        :param file_name: path where the files is that needs to be dumped
        :param to_dump: the information that needs to be dumped
        """
        with open(file_name, "a") as f:
            f.write(to_dump)


    def return_season_length(self):
        """
        Calculates the number of days the season last by returning the difference from the first day to the last.
        Updates self.total_match_days through
        """
        raw_match_days_count = self.end_date - self.start_date
        self.total_match_days = raw_match_days_count.days


    def match_day_set_start_time(self, match_day_datetime):
        """
        used in create_match_days. Takes in a datetime, adds a day, and sets the time to 10AM
        :param match_day_datetime:
        :return:
        """
        new_day_start_time = match_day_datetime + timedelta(days=1)
        return new_day_start_time.replace(hour=10, minute=0)

    def create_match_days(self):
        """
        Loops through self.completed_games to check if any games fall within each match day,
        then compilesthem into a list, appends that days games to self.match_days
        :return:
        """
        copy_of_matches = self.compiled_games.copy()
        end_of_day = self.match_day_set_start_time(self.start_date)
        #TODO working on this but need to update software and reboot. Will continue once I am back in action
        while copy_of_matches:
            while copy_of_matches[0][0] < end_of_day:
                pass

    # ACTIVEWORK gather team names and leagues from self.compiled_games and puts them into a dictionary with the team name as key and league as the value
    def gather_team_names(self):
        """
        Gathers the names and league
        :return:
        """
        pass


        # FUTURE create the loop that runs through each match day
        """
        #This is an almost working version of the loop to create each match day
        
        
            matches_toadd = []
            for match in copy_of_matches:
                if match[0] < end_of_day:
                    removed_match = copy_of_matches.pop(0)
                    matches_toadd.append(removed_match)
                else:
                    self.match_days.append(matches_toadd)
                    matches_toadd = []
                    start_of_day = end_of_day
                    end_of_day = self.match_day_set_start_time(start_of_day)
        print(f"\n\nthis list should be empty {copy_of_matches}")
        """




