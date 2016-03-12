"""
Submits the form on a page with given parameters and returns the response
"""
import bs4
import requests
import time
import random

'''
Generates form parameters by finding all the inputs and setting
them to a given value
'''
def setFormParams(formTag, value):
    params = {}
    for input in formTag.find_all("input"):
        if not input.get('name') == None:
            params[input['name']] = value
    return params
'''
Submits all the forms on the given page with
the given parameters. HTTP Method is determined by
method specified in form
'''
def submitForms(url, session, value):
    html = session.get(url).text
    soup = bs4.BeautifulSoup(html, "html.parser", parse_only = bs4.SoupStrainer("form"))
    responses = list()
    for form in soup:
        method = form['method'].upper()
        submiturl = url[0 : url.rfind("/")] + "/" + form['action']
        parameters = setFormParams(form, value)
        start = time.time()
        response = session.request(method=method,url=submiturl, params=parameters)
        end = time.time()
        responses.append(response)
    return responses

'''
Submit a value into a random input on the page
'''
def submitRandom(url, session, value):
    params = {}
    inputOptions = list()
    html = session.get(url).text
    soup = bs4.BeautifulSoup(html, "html.parser", parse_only = bs4.SoupStrainer("input"))
    for input in soup:
        if input.get('name') != None:
            inputOptions.append(input)
    if len(inputOptions) > 0:
        ranInput = random.choice(inputOptions)
        for parent in ranInput.parents:
            if parent.name == 'form':
                form = parent
                break
        if form:
            params[ranInput['name']] = value
            submiturl = url[0 : url.rfind("/")] + "/" + form['action']
            return session.request(method=form['method'].upper(),url=submiturl, params=params)
        else:
            return False
    else:
        return False
