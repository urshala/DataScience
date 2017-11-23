__author__ = 'Deepak Panta'

import bs4
import requests
import time
import json
from collections import Counter
import numpy as np
from matplotlib import pyplot as plt

BASE_URL = 'https://www.yelp.com'
def scrape_links():
	start = ['0', '10', '20']
	for i in start:
		url = 'https://www.yelp.com/search?find_desc=Breakfast+%26+Brunch&find_loc=Helsinki,+Finland&start={start}&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2,BusinessAcceptsCreditCards&open_time=9369'.format(start=i)
		data = requests.get(url)
		soup = bs4.BeautifulSoup(data.text, 'html.parser')

		with open('links.txt', 'a+') as f:
			for each_link in soup.find_all('a', class_='biz-name js-analytics-click'):
				f.write(each_link['href']+'\n')
		time.sleep(1)
	print('Scraped all the links')

scrape_links()

def write_to_json_file():
	with open('links.txt', 'r') as f, open('result.json', 'a+') as f2:
		for each_link in f:
			json_data = {}
			ratings = []
			each_link = BASE_URL + each_link
			data = requests.get(each_link)
			soup = bs4.BeautifulSoup(data.text, 'html.parser')
			shop = soup.h1.text.strip()
			reviews = soup.find('span', class_='review-count rating-qualifier').text.strip().split(' ')[0]
			price = soup.find('dd', class_='nowrap price-description').text.strip().replace('€', '')
			for div in soup.find_all('div', class_='biz-rating biz-rating-large clearfix'):
				for each_div in div.find_all('div'):
					if each_div.attrs:
						rating, *_ = each_div.attrs['title'].split(' ')
						ratings.append(rating)

			json_data[shop] = {'reviews': reviews, 'ratings':ratings, 'price':price}

			
			json.dump(json_data,f2)
			time.sleep(1)

write_to_json_file()

def plot_diagram(x,y,name_of_file):
	fig = plt.figure()
	width = .35
	ind = np.arange(len(y))
	plt.bar(ind, y, width=width)
	plt.xticks(ind+width/2, x)
	fig.autofmt_xdate()

	plt.savefig(name_of_file)

def top_five_restaurants():
	'''Price less than 25 euros, number of good ratings and reviews more than 5'''
	high_rated = {}
	good_price = {}
	high_reviews = {}
	X_Axis, Y_Axis, X_Reviews, Y_Reviews = [],[], [], []
	with open('result.json', 'r') as f:
		data = json.load(f)
		for item in data:
			for k,v in item.items():
				i = 0
			for rat in v['ratings']:
				if rat == '4.0' or rat =='5.0':
					i+=1
			high_rated[k]=i

			if '21' in v['price']:
				good_price[k] = v['price']

			for rev in v['reviews']:
				high_reviews[k] = v['reviews']

	counter_high_rated = Counter(high_rated)
	sorted_high_reviews = sorted(high_reviews.items(), key=lambda x: int(x[1]), reverse=True)[:5]
	
	for restaurant in counter_high_rated.most_common(5):
		res,pr = restaurant
		X_Axis.append(res)
		Y_Axis.append(pr)
		if restaurant[0] in good_price:
			print (restaurant[0])

	for restaurant in sorted_high_reviews:
		res,rev = restaurant
		X_Reviews.append(res)
		Y_Reviews.append(rev)

	#now plot ratings
	plot_diagram(X_Axis,Y_Axis,'top_rated.pdf')
	plot_diagram(X_Reviews, Y_Reviews, 'top_reviewed.pdf')


top_five_restaurants()

