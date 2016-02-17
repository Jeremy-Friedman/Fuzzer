import requests
import sys

"""
Release 1 -- Discover
Jeremy Friedman
Aaron Stadler
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
            return (fuzzArg and fuzzMode and url and commonWords)
        elif len(userArgs) == 6:
            customAuth = "--custom-auth=" in userArgs[4]
            commonWords = "--common-words=" in userArgs[5]
            return (fuzzArg and fuzzMode and url and customAuth and commonWords)
    except IndexError:
        print("***Invalid args*** \nUsage: fuzz discover <url> [--custom-auth=<string>] --common-words=<filename>")
        sys.exit()


def fuzz(userArgs):
    validateInput(userArgs)


if __name__ == "__main__":
    fuzz(sys.argv)
    