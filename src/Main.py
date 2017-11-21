from CheckMovieRating import CheckMovieRating
from SelectMovieData import SelectMovieData
from NaverMovieSearch import NaverMovieSearch
from DaumMovieSearch import DaumMovieSearch
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
from PIL import Image
import numpy as np
import sys

def sort_list_from_key(key_lst, value_lst):
    length = len(key_lst)

    k_lst=[]
    v_lst=[]
    dual_lst=[]
    for i in range(0,length):
        dual_lst.append([int(key_lst[i]),value_lst[i]])
    dual_lst.sort(reverse=True)

    for i in range(0,length):
        k_lst.append(dual_lst[i][0])
        v_lst.append(dual_lst[i][1])
 
    return k_lst, v_lst


if __name__ == '__main__':
    #read movie name
    movie_name = raw_input("Enter the movie name.\nMovie Name : ") #python 2.7
    #movie_name = input("Enter the movie name.\n")    #python 3.5
    
    movie_name = movie_name.lower().replace(" ","")
    print("Wait please... \n\n")

    #set real movie name    
    switch_movie_name={'thedarkknight':'The Dark Knight',
                       'forrestgump':'The Forrest Gump',
                       'inception':'Inception',
                       'savingprivateryan':'Saving Private Ryan'}
    real_movie_name = switch_movie_name[movie_name]
    
    #search web site movie rating
    naver_movie_name_to_search={'thedarkknight':'the dark knight',
			  'forrestgump':'forrest gump',
			  'inception':'inception',
			  'savingprivateryan':'saving private ryan'}
    search_name = naver_movie_name_to_search[movie_name]
    naver_ms = NaverMovieSearch(search_name)
    naver_rating = naver_ms.search_movie()

    daum_movie_name_to_search={'thedarkknight':'the dark knight',
			  'forrestgump':'forrest gump',
			  'inception':'inception',
			  'savingprivateryan':'saving private ryan'}
    search_name = daum_movie_name_to_search[movie_name]
    daum_ms = DaumMovieSearch(search_name)
    daum_rating = daum_ms.search_movie()

    #select movie data
    smd = SelectMovieData(movie_name)
    smd.select_data()

    #make mrjob instance
    cmr = CheckMovieRating()
    #run mapreduce
    cmr.run()

    #top 5 result
    top5_key_lst, top5_value_lst = cmr.get_top5_result()
    #all result
    all_key_lst, all_value_lst = cmr.get_all_result()

    #error exception
    if len(top5_key_lst)==0:
        print("\nThere are no movies to look for.")
        sys.exit(1)

    #sort by key
    top5_key_lst, top5_value_lst = sort_list_from_key(top5_key_lst, top5_value_lst)
    all_key_lst, all_value_lst = sort_list_from_key(all_key_lst, all_value_lst)

    #calculate top 5 average rating
    top5_num=0
    top5_rating_sum=0
    for i in range(0,5):
        top5_num+=top5_value_lst[i]

    for i in range(0,5):
        top5_rating_sum+=float(top5_value_lst[i])*float(top5_key_lst[i])

    top5_average_rating = round(top5_rating_sum/top5_num,2)

    #calculate all average rating
    all_num=0
    all_rating_sum=0
    for i in range(0,10):
        all_num+=all_value_lst[i]
    for i in range(0,10):
        all_rating_sum+=float(all_value_lst[i])*float(all_key_lst[i])
    all_average_rating = round(all_rating_sum/all_num,2)

    #save chart to image and render
    trace1 = go.Pie(
	labels=top5_key_lst,
	values=top5_value_lst,
	domain=dict(x=[0,0.4], y=[0,0.4]),
        sort=False,
	hole=0.4
    )
    trace2 = go.Bar(
	x=top5_key_lst,
	y=top5_value_lst,
	xaxis='x2',
	yaxis='y2',
	marker=dict(color="maroon"),
	showlegend=False
    ) 
    trace3 = go.Pie(
	labels=all_key_lst,
	values=all_value_lst,
	domain=dict(x=[0,0.4], y=[0.6,1]),
        sort=False,
	hole=0.4
    )
    trace4 = go.Bar(
	x=all_key_lst,
	y=all_value_lst,
	xaxis='x3',
	yaxis='y3',
	marker=dict(color="maroon"),
	showlegend=False
    )
 
    data=[trace3, trace4, trace1, trace2]
    layout = go.Layout(
	title=real_movie_name+" Rating Chart",
	width=700,
	height=800,
	xaxis2=dict(domain=[0.6,1],anchor='y2'),
        yaxis2=dict(domain=[0,0.4],anchor='x2'),
        xaxis3=dict(domain=[0.6,1],anchor='y3'),
        yaxis3=dict(domain=[0.6,1],anchor='x3'),
    )
    fig=go.Figure(data=data,layout=layout)
    py.image.save_as(fig, filename='./result/result_chart.png')

    #make table and save as image
    data_matrix = [['Top5 Rating Count','Average of Top5',
                   'All Rating Count','Average of All',
		   'Daum Rating','Naver Rating'],
                    [top5_num,top5_average_rating,all_num,all_average_rating,
		    daum_rating, naver_rating]]
    table=ff.create_table(data_matrix, height_constant=20)
    py.image.save_as(table,filename='./result/result_table.png')    
    
    #combine chart image and table image
    list_im = ['./result/result_chart.png', './result/result_table.png']
    imgs = [Image.open(i) for i in list_im]
    imgs_comb = np.vstack((np.asarray(i) for i in imgs))
    imgs_comb = Image.fromarray(imgs_comb)
    imgs_comb.save('./result/result.png')

    #show result image
    result_img = Image.open('./result/result.png')
    result_img.show()
