"""
This is the first file called when the program starts. It is used to check if the needed operational files are created.
If the files are already present then the process is skipped.
If the files are not present they are created
"""

#imports
from configparser import ConfigParser
import os
from pathlib import Path

# Current DIR
cd = os.getcwd()
startup_dir = cd + "\startup"
ini = startup_dir +"\dev.ini"
cd_files = os.listdir()


config = ConfigParser()

config['links'] = {
    'pdx_page' : 'https://pdxindoorsoccer.com',
    'schedules_location' : '/teams/schedules/',
}


def first_run():
    """
    checks if the startup directory is created, if not it is created with all the needed files

    :return: None
    """
    if "startup" not in cd_files:
        make_folder('startup')
        make_folder('seasons')
        push_file()



def make_folder(name):
    """
    Creates a new folder if non already exist

    :param name: name/path of the new folder
    :return: None
    """
    p = Path(name)
    p.mkdir(exist_ok=True)



def push_file():
    """
    updates/creates the dev.ini file with the changes made to config variable
    :return: None
    """
    with open('startup\dev.ini', 'w') as f:
        config.write(f)
        print(f"\nChanges have been pushed to {ini}")



#Future: create a retutrn to default settings def that overrides the file with initial settings


first_run()