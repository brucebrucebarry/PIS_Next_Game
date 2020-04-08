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
        self.rereg_deadline = None # captured post initialization
        self.mens = []
        self.womens = []
        self.coed = []
        os.chdir(season_dir) # changes the directory while open, changed back when closed

    # functions that assign init variables
    def get_season_name(self, season_name):
        """
        sets the self.name and self.year variables from season_name

        :param season_name: name of the season as a string
        """
        if not self.name and not self.year:
            self.name = season_name
            self.year = season_name[-4:]



    def gather_schedules(self):
        """"""

        soup = bs_obj_return(self.season_link)
        all_season = soup.findAll("ul", id="listyofiles")
        for season_links in all_season:
            league = season_links.findAll("a")
            for division in league:
                self.regex_obj_schedule(division.attrs['href'])



    def regex_obj_schedule(self, final_link):
        """"""

        raw_schedule_text = (bs_obj_return(final_link)).text
        regex_name = re.search("\w+\sCUP\s\d{4}",raw_schedule_text) # Creates regex match object to gather from
        self.get_season_name(regex_name.group()) # Gets season name and names this instance
        regex_
        regex_games = re.findall("[A-Z]{3}\s[A-Z]{3}\s\d*\s*\d*:\d\d.*",raw_schedule_text) # a list of games in this division






    def new_file_dump(self,file_name, to_dump):
        """"""

        f = open(file_name, "a")
        f.write(to_dump)
        f.close()



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