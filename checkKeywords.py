import os
import operator
import glob
from collections import Counter
from bs4 import BeautifulSoup
import requests
import json
import string
import re
import config



class Job:
    
    def __init__(self,job):
        self.jobTitle = job['title']
        self.description = job['description']
        self.cleanDescription = cleanText(self.description)
        self.identifier = job['identifier']
        self.jobID = self.identifier['value']
        self.datePosted = job['datePosted']
        self.yearPosted = self.datePosted[:4]
        self.monthPosted = self.datePosted[5:7]
        self.dayPosted = self.datePosted[-2:]

    def TitleChecker(self,requestedTitle):
        """
        check if the job title contains the provided string - all lowercase
        """
        cleanRequestedtitle = requestedTitle.lower().strip()
        if self.jobTitle.lower().find(cleanRequestedtitle) >= 0:
            return True
        else:
            return False
class Page:

    def getPage(id):
        """
        GET to the url with the job ID
        returns full HTML
        """
        response = requests.get(config.url + str(id))
        return response.text    
    def checkPage(html):

        """
        checks for the JSON metadata in each page
        returns truw if it exists
        """
        
        if html.find("application/ld+json") > 0:
            return True
        else:
            return False
    def parseHTML(html):

        """
        gets a n HTML file and returned formatted JSON of the job metadata
        """
        #get the  HTML source code
        #insert to a BS object
        soup = BeautifulSoup(html, 'html.parser')
        #slice the metadata JSON
        metadata = soup.find_all(type="application/ld+json")[0]
        #slice the string to a correct JSON format
        JSON_Prep = str(metadata)[35:-9]
        #load to a JSON object
        metadataJSON = json.loads(JSON_Prep)
        
        return metadataJSON
class Description:
    """
    gets a list with all words in the description
    """
    def removeHebrew(desc):

        """
        Takes a list of words and removes non english charachters
        """
        
        englishOnly = []
        for i in desc:
            english_check = re.compile(r'[a-z]')
            if english_check.match(i[0]) and english_check.match(i[-1]):
                englishOnly.append(i)
        return englishOnly

    def unique(data):
        return list(dict.fromkeys(data))

    def removeCommon(data):
        l = []
        for i in data:
            if i not in config.commonWords:
                l.append(i)
        return l

def getjobIdFromSearchResults(url):
    """
    Gets search URL and returns the JobIDs for that URL
    Per 1 Page
    According to the job-box-container string before each ID
    """
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = soup.find("div", {"id": "divResults"})
    j = jobs.find("div", {"id": "divOrganicContainer"})
    p = j.find("div", {"class": "organic-container-jobs"})
    o = p.find_all("div", {"class": "job-box-mask"})

    jobIdList =[]
    for i in o:
        jobIdList.append(str(i))
        # jobIdList.append(str(i[20:30]))
    
    finalList = []
    for i in jobIdList:
        finalList.append(i[42:49])
    
    return finalList
def cleanText(text):
    """
    Clean text and return as a list of words
    """
    return text.replace('\n', ' ').replace('\r', '').replace(',', '').replace('(', '').replace(')', '').replace('.', '').lower().split()
def buildJobIdList(title):
    jobIdListFromAllPages = []
    for x in range(1,11):
        search = 'https://www.alljobs.co.il/SearchResultsGuest.aspx?page=%s&freetxt=%s' % (x, title)
        for i in getjobIdFromSearchResults(search):
            jobIdListFromAllPages.append(i)
    
    return jobIdListFromAllPages

def putInElasticsearch(year,month,word,jobID):
    headers = {
                'Content-Type': 'application/json'
            }
                    
    params = (
        ('pretty' ,'')
        )
                    
    data = { 
        "year": year,
        "month": month,
        "keyword": word
    } 

    dataJSON = json.dumps(data)
    docID = str(jobID) +str(word)
    url = config.elasticURL + docID

    response = requests.put(url, headers=headers,data=dataJSON)
    print(response.text)


def main():
    #checks that the job is still valid
    #if valid create a job object

    for x in buildJobIdList(config.title):
        print(x)
        if Page.checkPage(Page.getPage(x)):
            j = Job(Page.parseHTML(Page.getPage(x)))
            print(j.jobTitle)
        #check title & remove hebrew & remove duplicates
            if Job.TitleChecker(j,config.title):
                keywordList = Description.removeCommon(Description.unique(Description.removeHebrew(j.cleanDescription)))
                print(keywordList)
                for i in keywordList:
                    putInElasticsearch(j.yearPosted,j.monthPosted,i,x)

if __name__ == "__main__":
    main()
    



