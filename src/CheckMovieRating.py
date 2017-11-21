from mrjob.job import MRJob
from mrjob.step import MRStep

class CheckMovieRating(MRJob):
    all_key_result = []
    all_value_result = []
    top5_key_result = []
    top5_value_result = []

    #top5 result getter
    def get_top5_result(self):
        return  CheckMovieRating.top5_key_result, CheckMovieRating.top5_value_result

    #all result getter
    def get_all_result(self):
        return CheckMovieRating.all_key_result, CheckMovieRating.all_value_result

    #set mapreduce step
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_ratings,
                   reducer=self.reducer_count_ratings),
            MRStep(mapper=self.mapper_passthrough,
		   reducer = self.reducer_top5)
        ]

    #count mapper
    def mapper_get_ratings(self, _, line):
        (movieName, rating) = line.split('\t')
        yield rating, 1
    
    #no role mapper
    def mapper_passthrough(self, key, value):
        CheckMovieRating.all_key_result.append(str(value[1]))
        CheckMovieRating.all_value_result.append(value[0])
        yield key, value

    #sum reducer
    def reducer_count_ratings(self, key, values):
	yield None, (sum(values),key)

    #top5 reducer
    def reducer_top5(self, _, pairs):
        self.aList = []
        for v in pairs:
            self.aList.append(v)
	self.aList.sort(reverse=True)
	for i in range(0,5):
	    CheckMovieRating.top5_value_result.append(self.aList[i][0])
            self.length = len(self.aList[i][1])
	    CheckMovieRating.top5_key_result.append(str(self.aList[i][1]))


