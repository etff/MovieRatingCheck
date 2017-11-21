import urllib
import urllib2
import json
from urllib2 import urlopen

class NaverMovieSearch:
	def __init__(self,movie_name):
		self.movie_name = movie_name


	def search_movie(self):
		client_id = "7fcbacG7_ctZD47vteqx"
		client_secret = "Njkracrmf5"

		encText = urllib.quote(self.movie_name)
		url = "https://openapi.naver.com/v1/search/movie.json?query="+ encText
		request = urllib2.Request(url)
		request.add_header("X-Naver-Client-Id",client_id)
		request.add_header("X-Naver-Client-Secret",client_secret)
		response = urllib2.urlopen(request)
		rescode = response.getcode()
		if(rescode==200):
    			response_body = response.read()
		else:
    			print("Error Code:" + rescode)

		j = json.loads(response_body.decode('utf-8'))
		rating = 0
		item = j["items"]
		if len(item) >1:
			year = raw_input("Enter the movie's publish year.\nYear : ")
			print("\n\n")
			for i in range(0,len(item)):
				if item[i]['pubDate']==year:
					rating = item[i]['userRating']
					break
		else:
			rating = item[0]['userRating']
		return rating
