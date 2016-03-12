import bs4
import requests
import sys
from SubmitForm import *
from CheckVulnerability import *

"""
Release 1 -- Discover
Jeremy Friedman
Aaron Stadler
"""

"""
Uses the common words file to guess all pages that can be reached
from the given url. 
"""
def guessPages(url, commonWords, session):
    pages = []
    extensions = ["", ".php", ".jsp"]
    #result = ""
    print("FAILED PAGE GUESSES: \n------------------------------")
    for word in open(commonWords):
        for extension in extensions:
            page = url + "/" + word.strip("\n") + extension
            request = session.get(page)
            if (request.status_code == requests.codes.ok):
                pages.append(page)
            else:
                print(page)
    return pages

"""
Returns all discoverable links from a given root url.
"""
def discoverLinks(url, session):
    neighborLinks = []
    html = session.get(url).text
    
    for link in bs4.BeautifulSoup(html, "html.parser", parse_only = bs4.SoupStrainer('a')):
        if link.has_attr("href") and "hiderefer.com" not in link.get("href"):
            nLink = link.get("href")
            #if the link starts with the base url, http, or www than it is already an absolute path
            #if it is a relative path append the base url to the beginning.
            if (nLink.startswith(url) == False) and (nLink.startswith("http") == False) and (nLink.startswith("www.") == False):
                if nLink.startswith("/") or  url.endswith("/"):
                    nLink = url + nLink
                else:
                    nLink = url + "/" + nLink
            neighborLinks.append(nLink)
    return neighborLinks

"""
Returns a requests.Response object.
"""
def authenticate(authTo, session):
    #hard-coded
    if (authTo == "dvwa"):
        session.post("http://127.0.0.1/dvwa/login.php", data = {"username" : "admin", "password" : "password", "Login" : "Login"})
    elif (authTo == "bodgeit"):
        session.post("http://127.0.0.1:8080/bodgeit/login.jsp", data={'username': "admin@thebodgeitstore.com' or '1'='1", 'password': ''})
    
"""
Returns all url inputs discovered
"""
def parseURL(url):
    try:
        plainUrl, inputs = url.split("?", 1)
        inputs = inputs.split("&")
    except ValueError:
        return []
    discoveredInputs = []
    if len(inputs) > 0:
        print("BASE URL: " + plainUrl)
    for field in inputs:
        if "=" in field:
            #not an input unless it follows input=value pattern
            fieldName = field.split("=")[0]
            value = field.split("=")[1]
            discoveredInputs.append(" - input field: " + fieldName)
            discoveredInputs.append(" - input value: " + value)
        else:
            discoveredInputs.append(" - field found not an input: " + field)

    return discoveredInputs

"""
Returns cookies from the current session
"""
def getCookies(session):
    cookies = session.cookies.get_dict()
    for cookieKey in cookies.keys():
        print(cookieKey + " = " + cookies[cookieKey])

    return cookies

"""
Returns discovered form inputs
"""
def getFormInputs(session, url):
    foundInputs = list()
    html = session.get(url).text
    soup = bs4.BeautifulSoup(html, "html.parser", parse_only = bs4.SoupStrainer('input'))
    inputLines = soup.prettify()
    for line in inputLines.splitlines(keepends=False):
        curLine = line.strip()
        #check if it is an input opening tag that is not a submit button
        if curLine.startswith("<input") and 'type="submit"' not in curLine:
            foundInputs.append(curLine)

    return foundInputs

def fuzz(userArgs):
    #validate input, init vars
    numArgs = len(userArgs)
    if (numArgs != 0):
        customAuth = ""
        url = userArgs[3]
        commonWords = userArgs[4].split("=")[1]
        slow = 500
        if (numArgs >= 6):
            customAuth = userArgs[4].split("=")[1]
            commonWords = userArgs[5].split("=")[1]
            #url = userArgs[-3]
        if (numArgs >= 7):
            vectors = userArgs[5].split("=")[1]
            sensitive = userArgs[6].split("=")[1]
            if (numArgs >= 8):
                if "random" in userArgs[7]:
                    rand = userArgs[7].split("=")[1]
                elif "slow" in userArgs[7]:
                    slow = userArgs[7].split("=")[1]
                if(numArgs >= 9):
                    if "random" in userArgs[8]:
                        rand = userArgs[8].split("=")[1]
                    elif "slow" in userArgs[8]:
                        slow = userArgs[8].split("=")[1]
                slow = int(slow)
                rand = rand.lower()
    #session used in entire fuzzer        
    session = requests.session()
    if (customAuth != ""):
            authenticate(userArgs[4].split('=')[1], session)
    #discover
    guessedPages = []
    if (userArgs[2] == "discover"):
        
        guessedPages = guessPages(url, commonWords, session)
        print("\nSUCCESSFUL PAGE GUESSES: \n------------------------------")
        for page in guessedPages:
            print(page)
        
        print("\nDISCOVERED LINKS: \n------------------------------")
        foundLinks = discoverLinks(url, session)
        for link in foundLinks:
            print(link)
        
        print("\nDISCOVERED URL INPUTS: \n------------------------------")
        for link in foundLinks:
            for input in parseURL(link):
                print(input)
        
        print("\nSESSION COOKIES: \n------------------------------")
        getCookies(session)
                   
        print("\nDISCOVERED FORM INPUTS: \n------------------------------")
        for link in foundLinks:
            for inputTag in getFormInputs(session, link):
                print(inputTag)
    #test
    elif (userArgs[2] == "test"):
        print("\nFUZZING INPUT: \n------------------------------")
        foundLinks = discoverLinks(url, session)
        for link in foundLinks:
            print("CHECKING URL: " + link)
            for vector in open(vectors):
                responses = submitForms(link, session, vector)
                for response in responses:
                    httpCheck = checkHTTPCode(response[0])
                    if(httpCheck): print(httpCheck)
                    dataCheck = checkDataLeak(response[0], sensitive)
                    if(dataCheck): print(dataCheck)
                    sanitizeCheck = checkInputSanitized(response[0], vector)
                    if(sanitizeCheck): print(sanitizeCheck)
                    if(response[1] > slow): print("Response delayed")




        

if __name__ == "__main__":
    fuzz(sys.argv)
    