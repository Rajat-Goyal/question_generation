import os
import nltk
from nltk.tag import StanfordNERTagger
import argparse
from itertools import groupby

from bcolors import *
import random

CURR_DIR = (os.path.dirname(os.path.abspath(__file__)))
#DATA_DIR = CURR_DIR + "/../data/wiki_files/"
st = StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz')

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help = "file to feed NER" , type=str)
args = parser.parse_args()
fn = args.file_name

loc=[]
per=[]
org=[]
mny=[]
prcnt=[]
date=[]
tym=[]
oth=[]
named_entities_str_tag=[]

def get_continuous_chunks(tagged_sent):
    continuous_chunk = []
    current_chunk = []
    paracount = 0

    for token, tag in tagged_sent:
        if tag != "O":
            current_chunk.append((token, tag))
        else:
            if current_chunk: # if the current chunk is not empty
                continuous_chunk.append(current_chunk)
                current_chunk = []
    # Flush the final current_chunk into the continuous_chunk, if any.
    if current_chunk:
        continuous_chunk.append(current_chunk)
    return continuous_chunk


def gen_sample_fitb_ques(ppl1):
    #ppl1 = loc[int(len(per)/2)];
    #print (ppl1)
    #ppl2 = per[int(len(per)/2 + 1)];
    qsample = 0
    with open(CURR_DIR+"/"+fn,'r') as f :
        while True:
            para = f.readline()
            if (para==""):
                break
            if ( para == "== See also =="):
                break
            if (para[0] == "=" ) or (para[0] == "\n") :
                continue
            if ppl1 in para:
                lines = para.split(". ")
                pre = -2
                nxt =0
                for x in lines[:-1] :
                    pre = pre + 1
                    nxt = nxt+1
                    if ppl1 in x:
                        print(x)
                        # if pre != -1 :
                        #     print(lines[pre] +". " + x + ". " + lines[nxt] )
                        # else :
                        #     print (x + lines[nxt])
                        blank = "_"*len(ppl1)
                        x=x.replace(ppl1,blank)
                        # if pre != -1 :
                        #     print(bcolors.OKBLUE + " QUES : "+ bcolors.ENDC + lines[pre]+ ". " + x + lines[nxt] )
                        # else :
                        #     print (bcolors.OKBLUE + " QUES : "+ bcolors.ENDC + x + ". " + lines[nxt])
                        print (bcolors.OKBLUE + " QUES : "+ bcolors.ENDC + x + ". ")
                        print("\n")
                        qsample = qsample+1
                        break

                if qsample == 2:
                    break

paracount =0
with open(CURR_DIR+"/"+fn,'r') as f :
    while True:
        x = f.readline()
        if (x==""):
            break
        if ( x == "== See also =="):
            break
        #print (x)
        if (x[0] == "=" ) or (x[0] == "\n") :
            continue

        line = x
        line = line.replace('. ',' . ').replace(',',' ,').replace(';',' ;').replace(':',' :').replace('(','( ').replace(')',' )')
        #print (line)

        pre_tagged = (st.tag(line.split()))
        ne_tagged_sent = pre_tagged
        named_entities = get_continuous_chunks(ne_tagged_sent)
        named_entities = get_continuous_chunks(ne_tagged_sent)
        named_entities_str = [" ".join([token for token, tag in ne]) for ne in named_entities]
        named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]

        '''for tag, chunk in groupby(tagged_out, lambda x:x[1]):
            if tag != "O":
                print("%-12s"%tag, " ".join(w for w, t in chunk))
        '''
        #print (named_entities_str_tag)

        #break;

        for item in named_entities_str_tag :
            if (item[1] == 0):
                continue
            elif (item[1] =="LOCATION"):
                if item[0] not in loc:
                    loc.append(item[0])
            elif (item[1] =="PERSON"):
                if item[0] not in per:
                    per.append(item[0])
            elif (item[1] =="ORGANIZATION"):
                if item[0] not in org:
                    org.append(item[0])
            elif (item[1] =="MONEY"):
                if item[0] not in mny:
                    mny.append(item[0])
            elif (item[1] =="PERCENT"):
                break
                if item[0] not in prcnt:
                    prcnt.append(item[0])
            elif (item[1] =="DATE"):
                if item[0] not in date:
                    date.append(item[0])
            elif (item[1] =="TIME"):
                if item[0] not in tym:
                    tym.append(item[0])
            else:
                if item[0] not in loc:
                    oth.append(item[0])

        # paracount= paracount+1
        # if (paracount == 40 ):
        #     break
        #break

print (bcolors.OKGREEN +"LOCATION      : "+ bcolors.ENDC, loc  ); print("\n\n")
print (bcolors.OKGREEN +"PERSON        : "+ bcolors.ENDC, per  ); print("\n\n")
print (bcolors.OKGREEN +"ORGANIZATION  : "+ bcolors.ENDC, org  ); print("\n\n")
print (bcolors.OKGREEN +"MONEY         : "+ bcolors.ENDC, mny  ); print("\n\n")
print (bcolors.OKGREEN +"PERCENT       : "+ bcolors.ENDC, prcnt); print("\n\n")
print (bcolors.OKGREEN +"DATE          : "+ bcolors.ENDC, date ); print("\n\n")
print (bcolors.OKGREEN +"TIME          : "+ bcolors.ENDC, tym  ); print("\n\n")
print (bcolors.OKGREEN +"MISC.         : "+ bcolors.ENDC, oth  ); print("\n\n")

print ("LOCATION")
gen_sample_fitb_ques(loc[int(len(loc)/2)])
gen_sample_fitb_ques(random.choice(loc))

print("PERSONS")
gen_sample_fitb_ques(per[int(len(per)/2)])
gen_sample_fitb_ques(random.choice(per))

print("ORGANIZATION")
gen_sample_fitb_ques(org[int(len(org)/2)])
gen_sample_fitb_ques(random.choice(org))
