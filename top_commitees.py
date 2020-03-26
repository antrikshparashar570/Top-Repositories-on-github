import urllib.request, urllib.parse, urllib.error 
import urllib.request, urllib.error, urllib.parse 
import http.cookiejar 
import requests 
from lxml import html 
from lxml import etree 
from bs4 import BeautifulSoup 
import re 
import operator 
import top_repositories
from flask_restful import Resource, Api
from flask import jsonify, request

class OpenRepository(Resource):
    
    def post(self):
        username = request.form["username"]
        n = request.form["n"]
        m = request.form["m"]
        repositories_class = top_repositories.OpenWebsite()
        repo_list = repositories_class.openWebsite(username, int(n), int(m))
        return jsonify({"repositories": repo_list, "commitees": self.openRepository(username, int(n), int(m))})

    def openRepository(self, username, n, m): 
      
        class_repositories = top_repositories.OpenWebsite()
        repositories = class_repositories.openWebsite(username, n, m)

        for repository in repositories:
      

            url = "https://github.com/"+username+"/"+repository+"/commits/master"
            print(url)  
            
            commitees = {}
            while True:
                response = requests.get(url) 
                soup = BeautifulSoup(response.text, 'html.parser') 
            
                soup = BeautifulSoup(response.text, 'html.parser') 
                div = soup.find_all('ol', {'class': 'commit-group Box Box--condensed'}) 
                
                for d in div:
                    temp = d.find_all('div',{'class': 'f6 text-gray min-width-0'})
                    for t in temp: 

                        x = t.find_all('a') 
                        if len(x) is not 0:
                            name = x[0].text
                            if name not in commitees:
                                commitees[name] = 1
                            else: 
                                commitees[name] += 1  

                div = soup.find_all('a',{'class': 'btn btn-outline BtnGroup-item'}) 
                
                if len(div) == 1:
                    if div[0].text == "Older":
                        url = div[0].get('href')
                    else:
                        break
                elif len(div) > 1:
                    url = div[1].get('href')
                else:
                    break

            i = 0
            sorted_repo = sorted(iter(commitees.items()), key = operator.itemgetter(1)) 
            comm = []
            for val in reversed(sorted_repo): 
                comm.append(val[0])
                print("\ncommitee name : ",val[0],"\ncommits     : ",val[1]) 
                i = i + 1
                if i > m: 
                    break

        return comm  

#if __name__ == "__main__": 
    #openRepository() 
