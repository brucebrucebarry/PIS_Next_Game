"""
This is the first file called when the program starts. It is used to check if the needed operational files are created.
If the files are already present then the process is skipped.
If the files are not present they are created
"""

#imports
from configparser import ConfigParser
import os

# Current DIR
#TODO update from ini file to xml
cd= os.getcwd()
ini = cd +"\dev.ini"

print(cd,ini)

config = ConfigParser()

config['links'] = {
    'base_page' : 'https://pdxindoorsoccer.com',
}

def push_file():
    with open( './dev.ini', 'w') as f:
        config.write(f)
        print(f"\nChanges have been pushed to {cd}")


push_file()