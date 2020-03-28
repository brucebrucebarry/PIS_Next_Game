import requests
from bs4 import BeautifulSoup

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

base_page= 'https://pdxindoorsoccer.com'


def collect_season_links():
    """
    Uses BeautifulSoup and requests to find all the links to the seasons on the PIS website.
    :return: list of links for the seasons
    """
    landing_page = requests.get(base_page + '/teams/schedules/')
    soup = BeautifulSoup(landing_page.content, 'html.parser')
    season = soup.find("div", class_="entry-content")
    pages = [base_page + link['href'] for link in season.findAll('a', href=True) if link.text]
    return pages

#ANDTHEN: open season, verify proper files, create Season instance

def request_seasons():
    # TODO: iterate through list of pages using requests to open the season

    """
    Uses a list of seasons to iterate through each season using requests
    :return:
    """
    all_seasons= collect_season_links()
    x=0
    for season in all_seasons:
        landing_page = requests.get(season)
        soup = BeautifulSoup(landing_page.content, 'html.parser')
        # TODO: search if <em>="No files found.", if non season has games scheduled
        if not soup.findAll("a", text="FIRST GAMES") and not soup.findAll("em"):
            print(x)
            #FIXME: Add the download tool to allow txt file to be downloaded by
            print(soup)
        x += 1

request_seasons()

#TODO: create a new Season instance using the year+season name
#ANDTHEN: iterate through each dividion
#Future: look in the Seasons directory, if season pass in


#TODO: create a League class to handle adding each league
#TODO: create a Division class to handle adding each Division
#TODO: create a Team class to handle managing each team
