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

def collect_season_links():
    """
    Uses BeautifulSoup and requests to find all the links to the seasons on the PIS website.
    :return: list of links for the seasons
    """
    landing_page = requests.get(pdx_website + schdules_ext)
    soup = BeautifulSoup(landing_page.content, 'html.parser')
    season = soup.find("div", class_="entry-content")
    pages = [pdx_website + link['href'] for link in season.findAll('a', href=True) if link.text]
    return pages

#ANDTHEN: open season, verify proper files, create Season instance

def request_seasons():
    # TODO: iterate through list of pages using requests to open the season

    """
    Uses a list of seasons from collect_season_links() to iterate through each season using requests
    :return: None
    """
    all_seasons= collect_season_links()
    x=0
    for season in all_seasons:
        landing_page = requests.get(season)
        soup = BeautifulSoup(landing_page.content, 'html.parser')
        if not soup.findAll("a", text="FIRST GAMES") and not soup.findAll("em"):
            #TODO: download a season to find the season name and year
            # open/create a folder with the season namedate
            # open/create a season object

            x += 1


#request_seasons()

#TODO: create a new Season instance using the year+season name
#ANDTHEN: iterate through each dividion
#future: look in the Seasons directory, if season pass in


#TODO: create a League class to handle adding each league
#TODO: create a Division class to handle adding each Division
#TODO: create a Team class to handle managing each team

def open_ini ():
    """
    START UP IN main()
    Opens the dev.ini file from startup/dev.ini. Once opened ConfigParser is used to parse the sections
    :return: base_page
    """
    from configparser import ConfigParser
    parser = ConfigParser()
    parser.read('startup/dev.ini')
    return parser.get('links', 'pdx_page'), parser.get('links', 'schedules_location')



def main():
    if __name__ == '__main__':
        import startup_file
        return open_ini()
        request_seasons()

    else:
        print("This main() function is being imported instead of ran directly. This will cause an issue")
        return "no information because this module was loaded by another program"

pdx_website, schdules_ext= main()
print(pdx_website)
