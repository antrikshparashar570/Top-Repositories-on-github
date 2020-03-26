import urllib.request, urllib.parse, urllib.error 
import urllib.request, urllib.error, urllib.parse 
import http.cookiejar 
import requests
import re 
from lxml import html 
from lxml import etree 
from bs4 import BeautifulSoup 
import requests
import operator 
from flask_restful import Resource, Api
from flask import Flask, request, jsonify
  


class OpenWebsite(Resource):

	def post(self):
		username = request.form["username"]
		n = request.form["n"]
		m = request.form["m"]
		return jsonify(self.openWebsite(username, int(n), int(m)))
    
	def openWebsite(self, username, n, m): 
      
		#username = str(input("enter GitHub username: ")) 

		repo_dict = {} 
		min = 0

		url = "https://github.com/"+username+"?tab=repositories"
  
		#while True:

		cj = http.cookiejar.CookieJar()
		opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)) 
		resp = opener.open(url) 
		doc = html.fromstring(resp.read()) 
        
		repo_name = doc.xpath('//li[@class="public source d-block py-4 border-bottom"]/div[@class="flex-justify-between d-flex"]/div[@class="flex-auto "]/h3/a/text()') 

		repo_list = []

		for name in repo_name: 
			name = ' '.join(''.join(name).split()) 
			repo_list.append(name) 
			repo_dict[name] = 0

		response = requests.get(url) 
		soup = BeautifulSoup(response.text, 'html.parser') 
        
		soup = BeautifulSoup(response.text, 'html.parser') 
		div = soup.find_all('li', {'class': 'public source d-block py-4 border-bottom'}) 
 	
		for d in div: 
			temp = d.find_all('div',{'class':'text-gray f6 mt-2'})
			for t in temp: 

				x = t.find_all('a', attrs={'href': re.compile("^\/[a-zA-Z0-9\-\_\.]+\/[a-zA-Z0-9\.\-\_]+\/network/members")}) 
				forks = 0
				if len(x) is not 0: 
					name = x[0].get('href') 
					name = name[len(username)+2:-11]
					if len(repo_dict) == 0:
						repo_dict[name] = int(x[0].text)
						min = int(x[0].text)

					elif len(repo_dict) < m:
						if int(x[0].text) <= min:
							min = int(x[0].text)
						repo_dict[name] = int(x[0].text)

					else:
						if int(x[0].text) <= min:
							min = int(x[0].text)
							repo_dict[name] = int(x[0].text)

			"""div = soup.find('a',{'class':'next_page'}) 
  
			if div is not None: 
				url = div.get('href') 
				url = "https://github.com"+url 
			else: 
				break"""

		i = 0
		sorted_repo = sorted(iter(repo_dict.items()), key = operator.itemgetter(1)) 
		repos = []

		for val in reversed(sorted_repo): 
			repos.append(val[0])
			repo_url = "https://github.com/" + username + "/" + val[0] 
			print("\nrepo name : ",val[0], "\nrepo url  : ",repo_url, "\nforks     : ",val[1]) 
			i = i + 1
			if i >= n: 
				break

		return div


#if __name__ == "__main__": 
    #openWebsite() 
