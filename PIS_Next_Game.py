"""
ON OPEN:

- check for "seasons" folder
- create if not there
    - skip to GATHER FROM WEB
- pick latest year



GATHER FROM WEB
- skip "1st of season"
- open each of the five seasons
- decide if good
- create league object
- find all the links for each division within all 3 leagues
- download each schedule and name it according to league and division


"""

# imported standard modules
import requests
from bs4 import BeautifulSoup

# imported custom modules
import startup_file
import SeasonClass


# functions

def bs_obj_return(web_address):
    """
    Takes a webaddress and returns a BeautifulSoup object to be parsed.

    :param web_address: a website address to be loaded
    :return: BeautifulSoup Obj
    """
    landing_page = requests.get(web_address)
    return BeautifulSoup(landing_page.content, 'html.parser')



def collect_season_links():
    """
    Uses BeautifulSoup and requests to find all the links to the seasons on the PIS website.

    :return: list of links for the seasons
    """
    web_address = pdx_website + schedules_ext
    soup = bs_obj_return(web_address)
    season = soup.find("div", class_="entry-content")
    pages = [pdx_website + link['href'] for link in season.findAll('a', href=True) if link.text]
    return pages




#ANDTHEN: open season, verify proper files, create Season instance

def request_seasons():
    """
    Uses a list of seasons from collect_season_links() to iterate through each season using requests

    :return: None
    """
    all_seasons= collect_season_links()
    working_seasons= []
    for season in all_seasons:
        landing_page = requests.get(season)
        soup = BeautifulSoup(landing_page.content, 'html.parser')
        if not soup.findAll("a", text="FIRST GAMES") and not soup.findAll("em"):
            working_seasons.append(season)
            #TODO: download a season to find the season name and year
            # open/create a folder with the season namedate
            # open/create a season object
            # work On season(season)
    return working_seasons


#TODO: create a new Season instance using the year+season name
#ANDTHEN: iterate through each dividion
#future: look in the Seasons directory, if season pass in


#TODO: create a League class to handle adding each league
#TODO: create a Division class to handle adding each Division
#TODO: create a Team class to handle managing each team

def open_ini():
    """
    MUST RUN EVERY TIME TO GATHER PROPER VARIABLES
    Opens the dev.ini file from startup/dev.ini. Once opened ConfigParser is used to parse the sections

    :return: pdx_page, pdx_website, schedules_ext
    """
    from configparser import ConfigParser
    parser = ConfigParser()
    parser.read('startup/dev.ini')
    return parser.get('links', 'pdx_page'), parser.get('links', 'schedules_location')

# variables gathered from startup ini file
pdx_website, schedules_ext = open_ini()

def main():
    """
    main file to be executed when this file is opened and not imported
    """
    working_seasons = request_seasons()
    season = SeasonClass.Season(working_seasons[0])
    season.main()
    print(len(season.compiled_games), season.compiled_games)
    print(f"this is the start:{season.start_date}\nthis is the end:{season.end_date}")
    print(season.total_match_days)
    print(f"There are {season.total_matches} total matches and there should be {len(season.compiled_games)}")
    # print(season.match_days)



# main function running here
if __name__ == '__main__':
    main()

else:
    print("This main() function is being imported instead of ran directly. This will cause an issue")
