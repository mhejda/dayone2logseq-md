#!/usr/bin/env python
import json
import io
import sys
import os
import re
from datetime import datetime


#all is a dict [u'entries', u'metadata']
#metadata is not intersting (contains only a version number 1.0)

#all['entries'] is a list of dict.
#on entry is the following dict:
# [u'uuid', u'tags', u'text', u'richText', u'creationOSVersion',
# u'creationDeviceModel', u'creationDevice', u'modifiedDate',
# u'creationOSName', u'creationDeviceType', u'duration', u'timeZone',
# u'starred', u'creationDate', u'weather', u'location'

#entry2md is a function that will convert one single DayOne journal entry as
#a markdown file.

single_entries = 0
multi_entries = 0

def entry2md(entry,entries_dates):
    multientry = False
    
    date = datetime.strptime(entry['creationDate'],'%Y-%m-%dT%H:%M:%SZ')
    #date as the filename
    #it is assumed that there cannot be two entries in the same second.
    #If this is nevertheless the case, one of the two will be lost

    yyyymmdd = date.strftime("%Y_%m_%d")
    filename = yyyymmdd+".md"
    text = "publication-date:: "+str(date)+"\n\n- ### #diary "
    if yyyymmdd in entries_dates:
        print('-- Additional entry on '+yyyymmdd)    
        multientry = True
        
        with open(filename, 'r', encoding='utf-8') as mdentry:
            text = mdentry.read()
            text = text+'\n--------------\n- ### #diary '
        
    entries_dates.append(yyyymmdd)
    print(filename,end='')
    #Add date as the title

    
    #The code will check for a header. If there is none, it will try to make a header from first paragraph, if it is shorter than 30 characters
    # Otherwise, it will use generic name "DayOne Entry"

    # if the entry has no text, make sure it is still processed
    if 'text' in entry:
        if entry['text'][0] == '#':
            #text = text+entry['text'][2:]
            text = text+re.sub(r'\n\n', r'\n\n\t- ', entry['text'][2:])
        else:
            #text = text+'DayOne Entry\n'+entry['text']
            match = re.search(r'\n', entry['text'][0:30])
            if match != None:
                mfrom, mto = match.span()
                text = text+entry['text'][0:mfrom]+re.sub(r'\n\n', r'\n\n\t- ', entry['text'][mfrom:])
            else:
                text = text+'DayOne Entry\n'+re.sub(r'\n\n', r'\n\n\t- ', entry['text'])
    else:
        text = ''
        
    #for some reason, "." and () are escaped
    text = text.replace("\.",".").replace("\(","(").replace("\)",")").replace("\-","-")
    tags = ""
	#we add tags at the ends of each entry with the tag symbol
    #but only if the tag is not already in the text
    if 'tags' in entry.keys():
        for t in entry['tags']:
            tag = " %s%s" %(tag_symbol,t)
            if tag not in text:
                tags += tag

	#we convert the dayone-moment photo link to local markdown link
    photos = dict()
    if 'photos' in entry.keys():
        for p in entry['photos']:
            #print(p)
			#for each photos, we create a pair identifier/filename
                        #it looks that, sometimes, the photo was lost (no md5)
            if 'md5' in p:
                photos[p['identifier']] = "%s.%s" %(p['md5'],p['type'])
                
        for ph in photos:
            original = "![](dayone-moment://%s)" %ph
            new = "![diary_photo](../assets/dayone/%s)" %photos[ph]
            text = text.replace(original,'')
            text = text+'\n'+new+'\n'
        #we add tags at the end of the text
        text += "\n%s" %tags
        #we add location
        if 'location' in entry.keys():
            location = entry['location']
            #print(location)
            place = "\t- Location:\n\tcollapsed:: true\n\t"
            for t in ['placeName','localityName','administrativeArea','country']:
                if t in location.keys():
                    place += location[t]+"\n\t"
            if 'longitude' in location.keys() and 'latitude' in location.keys():
                place += ""
                place += "long: "+str(location['longitude'])
                place += ", lat: "+str(location['latitude'])
            text += place

    #Remove orphaned blocks
    text = re.sub(r'\n\t- \n', r'', text)
    
    for i in range(3):
        text = re.sub(r'\n\n\n', r'\n\n', text)
    
    #print(repr(text))     
    #print(text)   
    with open(filename, 'w', encoding='utf-8') as fp:
        fp.write(text)
        fp.close()
    if multientry == False:
        print(' - OK')
        global single_entries
        single_entries = single_entries + 1
    else:
        print(' - Merged, OK')
        global multi_entries
        multi_entries = multi_entries + 1
    return entries_dates

#%%
tag_symbol = "#"
filename = ''

if len(sys.argv) > 1:
    filename = sys.argv[1]
    print('DayOne2md: Python3 script for conversion of DayOne JSON into Markdown entries (aimed for import into Logseq).')
    print('v0.2 (alpha)')
    print()

else:
    print('You need to pass a filename in argument. Ex: python do2md.py Journal.json')
    sys.exit()
    
with open(filename, 'r', encoding='utf-8') as fp:
    journal = json.load(fp)

# Make sure folder four outputs exists, change the workdir to it    
try:
    os.mkdir('do2md')
except:
    pass
os.chdir(os.path.join(os.getcwd(),'do2md'))

entries_dates = [0]
for entry in journal['entries']:  
    entries_dates = entry2md(entry, entries_dates)

print()
print(f'FINISHED. Created {single_entries} dated entries, {multi_entries} entries merged into their respective days.')
