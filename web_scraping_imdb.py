from urllib import request
from requests import get
from bs4 import BeautifulSoup
from warnings import warn
from time import sleep
from random import randint
import numpy as np, pandas as pd
import statistics as st

pages = np.arange(1000, 8000, 50)
headers = {'Accept-Language': 'en-US,en;q=0.8'}

titles = []
runtimes = []

for page in pages:

   response = get("https://www.imdb.com/search/title/?release_date=2018-01-01,2018-12-31&sort=num_votes,desc"
                  + "&start="
                  + str(page)
                  + "&ref_=adv_nxt", headers=headers)
  
   sleep(randint(8,15))
   
   if response.status_code != 200:
       warn('Request: {}; Status code: {}'.format(request, response.status_code))

   page_html = BeautifulSoup(response.text, 'html.parser')
      
   movie_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')
  
   for container in movie_containers:
    title = container.h3.a.text
    titles.append(title)

    if container.p.find('span', class_ = 'runtime') is not None:
        time = int(container.p.find('span', class_ = 'runtime').text.replace(" min", ""))
        runtimes.append(time)

    else:
        runtimes.append(time)

if len(titles) != len(runtimes):

    if len(titles) > len(runtimes):
        mean_width = st.mean(runtimes)
        runtimes += (len(titles)-len(runtimes)) * [mean_width]
    elif len(titles) < len(runtimes):
        mean_length = st.mean(titles)
        titles += (len(runtimes)-len(titles)) * [mean_length]

movie_df = pd.DataFrame({'movie': titles,
                      'runtime_min': runtimes})

movie_df.head()

movie_df.dtypes

movie_df

movies = dict(zip(titles, runtimes))
print(max(runtimes))
print(max(movies, key=lambda k: movies[k]))

movie_df.to_csv('movies.csv')