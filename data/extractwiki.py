#!/usr/bin/python
import wikipedia
import os
from bcolors import *


#get the working directory as the parent directory
CURR_DIR = (os.path.dirname(os.path.abspath(__file__)))

countries = [ country.rstrip('\n') for country in open(CURR_DIR +'/country_list')]
todelete = []
for country in countries[44:]:
    with open(CURR_DIR+ '/wiki_files/' + country ,'w') as f:
        try :
            page = wikipedia.WikipediaPage(country)
            f.write("== Summary ==\n")
            f.write(page.content);
            print (bcolors.OKGREEN + "Finished for " + country + bcolors.ENDC)
        except wikipedia.exceptions.DisambiguationError:
            print (bcolors.FAIL + "could not download page due to dissambiguation. Adding" + country + " to todelete" + bcolors.ENDC)
            todelete.append(country)
        except wikipedia.exceptions.PageError :
            print(bcolors.FAIL + "page not found with given title. Ignoring " + country + " Adding to todelete")
            todelete.append(country)
        except:
            print (bcolors.FAIL + "some new error on " + country + bcolors.ENDC)

print (todelete)
