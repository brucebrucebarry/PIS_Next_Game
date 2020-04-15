"""
This file houses the Seasons class.
"""
import os
from PIS_Next_Game import bs_obj_return
import re

cd = os.getcwd()
season_dir = cd + "\seasons"


class Season:

    def __init__(self, season_link):
        self.season_link = season_link
        self.name = None # captured post initialization get_season_name()
        self.year = None # captured post initialization get_season_name()
        self.start_date = None # captured post initialization
        self.end_date = None # captured post initialization
        self.rereg_deadline = None # captured post initialization set_rereg_deadline()
        self.all_games = [] # populated by organize_raw_games(), all games in an encapsulated list[division[games]]
        os.chdir(season_dir) # TODO: changes the directory while open, *NTD(changed back when closed)*




    def __len__(self):
        print(f"This season has:{len(self.all_games)} divisions")
        return len(self.all_games)



    def __repr__(self):
        return (f"This is the self.__class__.__name__: {self.__class__.__name__}")


    # functions that assign init variables
    def get_season_name(self, season_name):
        """
        sets the self.name and self.year variables from season_name

        :param season_name: name of the season as a string
        """
        if not self.name and not self.year:
            self.name = season_name
            self.year = season_name[-4:]



    def set_rereg_deadline(self, raw_deadline):
        """
        checks if self.rereg_deadline is not set, if True, Adds the year as the last parameter and append to self.rereg_deadline
        :param deadline:
        :return:
        """
        if not self.rereg_deadline:
            clean_deadline = list(raw_deadline)
            clean_deadline.append(self.year)
            self.rereg_deadline = clean_deadline


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

        :param raw_games: list of strings gathered from BS scrape.
        [0]day_of_week
        [1]month
        [2]day
        [3]time
        [4]am_pm
        [5]teams
        :return: None
        """
        cleaned_games = [] # adds the name of the league and division
        for game in raw_games:
            to_add=[]
            day_of_week = game[0]# DOW
            month = game[1]# month
            day = game[2]# day
            time = game[3]# time
            am_pm = game[4]# AM/PM
            home_team, away_team = self.harvest_teams(game[5])# teams
            to_add.extend([day_of_week, month, day, time, am_pm, home_team, away_team, tagline])
            cleaned_games.append(to_add)
        self.all_games.append(cleaned_games)



    def harvest_teams(self, game_line):
        """
        separates the home and away team using "vs" as a deliminator and strip() to remove whitespace

        :param game_line: a string with '  vs  ' seperating the 2 home vs the away
        :return: home team and away team as str
        """
        both_teams = game_line.split("  vs ")
        return both_teams[0].strip(), both_teams[1].strip() # returns home team, away team


    # Use datetime to create datetime objects from each game

    def convert_allgames_to_datetime(self):
        """"""

        datetime_games = []
        for division in self.all_games:
            map(self)
            # use map() to filter each game



    def  datetime_eachgame(self, game):
        pass



    def new_file_dump(self,file_name, to_dump):
        """"""
        with open(file_name, "a") as f:
            f.write(to_dump)



















class Division:

    def __init__(self, name, league, year):
        self.name = name
        self.league = league
        self.year = year
        self.start_date = None  # captured post initialization
        self.end_date = None  # captured post initialization
        self.rereg_deadline = None  # captured post initialization
        self.teams = []
        # extra
        self.goal_limit = False
        self.sportmanship_league = False