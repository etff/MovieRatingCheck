import simplejson, urllib

class DaumMovieSearch:
	def __init__(self,movie_name):
		self.movie_name = movie_name


	def search_movie(self, **args):
		apikey = "8d00c408c07ceac00e0db88b6a389745"
		SEARCH_BASE ="https://apis.daum.net/contents/movie"
		args.update({'apikey': apikey,
				'q': self.movie_name,
				'output': 'json'
    		})
		url = SEARCH_BASE + '?' + urllib.urlencode(args)
		result = simplejson.load(urllib.urlopen(url))
		info = result['channel']
		rating=-1
		for item in info['item']:
	    		rating = item['grades']
		return rating[0]['content']


