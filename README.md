SWEN-331 Fuzzer -- Release 1 (Discover)

Pre-requisites:
1) Python 3.4.3 
2) Requests package. "pip install requests" to install. (documentation: http://docs.python-requests.org/en/master/user/install/#install)
3) BeautifulSoup package. "pip install beautifulsoup" to install. (documentation: http://www.crummy.com/software/BeautifulSoup/bs4/doc/)

How to run:
1) Open command prompt
2) Navigate to the directory housing the project
3) Issue the following command: python Fuzzer.py fuzz discover url OPTIONS

	discover  Output a comprehensive, human-readable list of all discovered inputs to the system. Techniques include both crawling and guessing.
	
	OPTIONS:
	  --custom-auth=string     Signal that the fuzzer should use hard-coded authentication for a specific application (e.g. dvwa). Optional.
	
	  Discover options:
	    --common-words=file    Newline-delimited file of common words to be used in page guessing and input guessing. Required.
	
	Examples:
	  # Discover inputs
	  fuzz discover http://localhost:8080 --common-words=mywords.txt
	
	  # Discover inputs to DVWA using our hard-coded authentication
	  fuzz discover http://localhost:8080 --common-words=mywords.txt
