#!/usr/bin/python3
import wikipedia
import os
import argparse
from bcolors import *

#get the complete path of curr directory's parent dir
CURR_DIR = (os.path.dirname(os.path.abspath(__file__)))

def wiki_to_txt(titles) :
    #NOT DONE : check if wiki_files directory exists
    for title in titles:
        try :
            page = wikipedia.WikipediaPage(title)
            f = open(CURR_DIR+ '/wiki_files/' + title ,'w')
            f.write("== Summary ==\n")
            f.write(page.content);
            f.close();
            print (bcolors.OKGREEN + "Finished for " + title + bcolors.ENDC)
        except wikipedia.exceptions.DisambiguationError:
            print (bcolors.FAIL + "could not download " + title + " page due to dissambiguty" )
        except wikipedia.exceptions.PageError :
            print(bcolors.FAIL + "page not found with title = " + title + " Skipping." + bcolors.ENDC )
        except:
            print (bcolors.FAIL + "some new error on " + title + bcolors.ENDC)

#generate list of all titles
def genlist(title_list):
    print (bcolors.OKGREEN + "Generated title list" + bcolors.ENDC)
    titles = [ title.rstrip('\n') for title in open(CURR_DIR + "/" + title_list)]
    return titles

#get the filename containing all titles from the argument passed
def getfile():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help = "mention the file name/path which list of titles you want the wikipedia data for.There should be one title in each line." , type=str)
    args = parser.parse_args()
    return args.file_name

def main():
    file_name = getfile()
    titles = genlist(file_name)
    wiki_to_txt(titles)

if __name__ == "__main__":
    main()
