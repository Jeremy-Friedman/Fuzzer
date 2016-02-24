import bs4
import requests
import sys

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
        if link.has_attr("href"):
            neighborLinks.append(link.get("href"))
    return neighborLinks

"""
Returns a requests.Response object.
"""
def authenticate(authTo, session):
    #hard-coded
    if (authTo == "dvwa"):
        session.post("http://127.0.0.1/dvwa/login.php", data = {"username" : "admin", "password" : "password"})
    elif (authTo == "bodgeit"):
        session.post("http://127.0.0.1:8080/bodgeit/login.jsp", data={'username': 'admin@thebodgeitstore.com', 'password': 'password'})
    
"""
Returns all url inputs discovered
"""
def parseURL(url):
    try:
        plainUrl, inputs = url.split("?", 1)
        inputs = inputs.split("&")
    except ValueError:
        print("BASE URL: " + url)
        return []
    discoveredInputs = list()
    for field in inputs:
        fieldName = field.split("=")[0]
        discoveredInputs.append(fieldName)

    print("BASE URL: " + plainUrl)
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
        if curLine.startswith("<input"):
            foundInputs.append(curLine)

    return foundInputs

def fuzz(userArgs):
    #validate input, init vars
    numArgs = len(userArgs)
    if (numArgs != 0):
        customAuth = ""
        url = userArgs[-2]
        commonWords = userArgs[-1].split("=")[1]
        if (numArgs == 6):
            customAuth = userArgs[-2].split("=")[1]
            url = userArgs[-3]
            
    #session used in entire fuzzer        
    session = requests.session()
    
    #discover
    guessedPages = []
    if (userArgs[2] == "discover"):
        if (customAuth != ""):
            authenticate(userArgs[4].split('=')[1], session)
        
        guessedPages = guessPages(url, commonWords, session)
        print("\nSUCCESSFUL PAGE GUESSES: \n------------------------------")
        for page in guessedPages:
            print(page)
        
        print("\nDISCOVERED LINKS: \n------------------------------")
        for link in discoverLinks(url, session):
            print(link)
        
        print("\nDISCOVERED URL INPUTS: \n------------------------------")
        for input in parseURL(url):
            print(input)
        
        print("\nSESSION COOKIES: \n------------------------------")
        getCookies(session)
                   
        print("\nDISCOVERED FORM INPUTS: \n------------------------------")
        for inputTag in getFormInputs(session, url):
            print(inputTag)
    #test
    elif (userArgs[2] == "test"):
        pass #do test stuff
        

if __name__ == "__main__":
    fuzz(sys.argv)
    