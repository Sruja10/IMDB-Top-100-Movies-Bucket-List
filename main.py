# Getting 100 Movies BucketList

import requests
from bs4 import BeautifulSoup
import csv

movies_data = []

URL = 'https://www.imdb.com/list/ls091520106/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
result = soup.find(id='main')

movies = result.find_all('div', class_='lister-item-content')

for movie_info in movies:
    # Get Movie Title
    title_element = movie_info.find('h3', class_='lister-item-header')
    movie_name = title_element.find('a').text.strip()
    movie_year = title_element.find('span', class_='lister-item-year').text.strip()
    movie_title = f'{movie_name} {movie_year}'

    # Get Movie IMDB rating
    rating_element = movie_info.find('div', class_='ipl-rating-widget')
    imdb_rating = rating_element.find('span', class_='ipl-rating-star__rating').text.strip()

    # Get Movie description
    description_element = movie_info.find_all('p', class_="")
    movie_description = description_element[0].text.strip()

    # Get Movie Cast
    movie_cast_element = movie_info.find_all('p', class_="text-muted")
    movie_cast = movie_cast_element[1]
    director_element = movie_cast.find('a')
    director_name = director_element.text.strip()
    actors_element = [star.text for star in movie_cast.find_all('a')[1:]]
    stars = ",".join(actors_element)

    movie_data = {
        'Movie Title': movie_title,
        'IMDB Rating': imdb_rating,
        'Description': movie_description,
        'Director': director_name,
        'Stars': stars
    }

    movies_data.append(movie_data)

# To get the list in a csv file
file_name = "IMDB_Top_100_Movies_Bucket_List.csv"
with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Movie Title', 'IMDB Rating', 'Description', 'Director', 'Stars']
    writer = csv.DictWriter(file, fieldnames)

    writer.writeheader()

    writer.writerows(movies_data)
