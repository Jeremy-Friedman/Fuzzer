"""
Submits the form on a page with given parameters and returns the response
"""
import bs4
import requests

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
        response = session.request(method=method,url=submiturl, params=parameters)
        responses.append(response)
    return responses
