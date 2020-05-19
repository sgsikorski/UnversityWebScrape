""" University Website Web Scraping

Scott Sikorski
May 2020
University of Rochester Undergraduate 2023

Python program that uses web scraping to collect data from university 
undergraduate research programs. Takes a .txt file with all the 
applicable schools and the hyperlinks as strings to their website.
Goes to the cooresponding website then searchs for all the hyperlinks
within the website. Visits them and collects text data and checks 
if certain keywords are mentioned. Then creates a .txt file with all the data
"""

import requests
from lxml import html

# File opening to read and write to
report = open("FullUniversityReport.txt", "w")
urls = open("URE institutional webpage.txt", "r")
u = urls.readlines()

for i in range(len(u)):
    line = list(u[i].split(","))
    url = line[0].replace('"', "")

    links = []
    aCount = 0
    eCount = 0
    gCount = 0
    pCount = 0
    fsCount = 0
    iCount = 0
    cCount = 0

    # Using lxml, gets the hyperlinks for all the hyperlinks
    response = requests.get(url)
    byte_data = response.content
    source_code = html.fromstring(byte_data)
    tree = source_code.xpath('//a/@href')

    for link in tree:
        links.append(link)
    
    sites = list(url.split("/"))
    
    for k in range(len(links)):
        # Tries the website and then gets the response if the site is valid
        try:
            site = "http://{0}{1}".format(sites[2], links[k]) 
            respond = requests.get(site)
        except:
            continue
        
        # Hot fixes to sites that threw a document empty error
        if(site == 'http://tilt.colostate.edumailto:TILT_OURA@mail.colostate.edu'):
            continue
        if(site == 'http://www.depts.ttu.edu/true/includes/'):
            continue

        # Creates a list of all the words on the page
        data = respond.content
        source = html.fromstring(data)
        string2 = source.text_content()
        entire_list = list(string2.split(" "))

        # Scans the list of words for keywords
        for i in range(len(entire_list)):
            if(entire_list[i].lower() == "assessment"):
                aCount += 1
            if(entire_list[i].lower() == "evaluation"):
                eCount += 1
            if(entire_list[i].lower() == "goal" or entire_list[i].lower() == "goals"):
                gCount += 1
            if(entire_list[i].lower() == "purpose"):
                pCount += 1
            if(entire_list[i].lower() == "faculty-student"):
                fsCount += 1
            if(entire_list[i].lower() == "independent"):
                iCount += 1
            if(entire_list[i].lower() == "collaboration"):
                cCount += 1
        
    school = line[1].replace('"', "")
    print(school)

    # File writing structuring
    s = "{0} \n Assessment: {1} \n Evaluation: {2} \n Goal(s): {3} \n Purpose: {4} \
        \n Faculty-Student: {5} \n Independent: {6} \
        \n Collaboration: {7}\n".format(school, aCount, eCount, gCount, pCount,
                                  fsCount, iCount, cCount)
    report.write(s)

report.close()
urls.close()
