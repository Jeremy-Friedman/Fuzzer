import requests
import sys

"""
Release 1 -- Discover
Jeremy Friedman
Aaron Stadler
"""

"""
Partial validation. 
@args userArgs -- user input
@return: number of inputs
"""
def validateInput(userArgs):
    try:
        fuzzArg = userArgs[1] == "fuzz"
        fuzzMode = userArgs[2] == "discover"
        url = userArgs[3] 
        customAuth = False
        commonWords = False
        if len(userArgs) == 5:
            commonWords = "--common-words=" in userArgs[4]
            return (len(userArgs))
        elif len(userArgs) == 6:
            customAuth = "--custom-auth=" in userArgs[4]
            commonWords = "--common-words=" in userArgs[5]
            return (len(userArgs))
    except IndexError:
        print("***Invalid args*** \nUsage: fuzz discover <url> [--custom-auth=<string>] --common-words=<filename>")
        sys.exit()

def guessPages(url, commonWords):
    extensions = [".php", ".jsp"]
    pages = []
    for word in open(commonWords):
        for extension in extensions:
            request = requests.get(url + "/" + word.strip("\n") + extension)
            if (request.status_code != 404):
                pages.append('http://127.0.0.1/' + word.strip() + extension)
    print(pages)

"""
Returns a requests.Response object
"""
def authenticate(authTo):
    session = requests.session()
    #hard-coded
    if (authTo == "dvwa"):
        pass
    elif (authTo == "bodgeit"):
        pass
        

def fuzz(userArgs):
    #validate input
    numArgs = validateInput(userArgs)
    
    #init vars
    customAuth = ""
    url = userArgs[-2]
    commonWords = userArgs[-1].split("=")[1]
    if (numArgs == 6):
        customAuth = userArgs[-2].split("=")[1]
        url = userArgs[-3]

    #discover
    guessedPages = []
    if (userArgs[2] == "discover"):
        if (customAuth != ""):
            authenticate(userArgs[4].split('=')[1])
        guessedPages = guessPages(url, commonWords)
    
    elif (userArgs[2] == "test"):
        pass #do test stuff
        



if __name__ == "__main__":
    fuzz(sys.argv)
    