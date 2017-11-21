class SelectMovieData:
	def __init__(self,movie_name):
                #save movie name
		self.movie_name=movie_name

	def select_data(self):
		read_f=open("./data/movie.txt",'r')
		write_f=open("./data/selected_data.txt",'w')
		while True:
			#read all movie rating data
			line = read_f.readline()
			if not line: break
			(movieName, rating) = line.split('\t')
			#write data if movie name equals to entered name
			if movieName==self.movie_name:
				write_f.write(movieName+"\t"+rating)
		read_f.close()
		write_f.close()
