import pandas as pd
import numpy as np
import pickle
import streamlit as st
from pathlib import Path

# read the dataframe
series = pd.read_csv(Path.cwd()/'datasets/anime_series.csv')
series.drop(['Unnamed: 0'], axis=1, inplace=True)

# read the binary
series_similarity1 = pickle.load(open(Path.cwd()/'assets/bin/series_similarity1.pkl', 'rb'))
series_similarity2 = pickle.load(open(Path.cwd()/'assets/bin/series_similarity2.pkl', 'rb'))
series_similarity = np.concatenate((series_similarity1, series_similarity2), axis=0)

# to choose a anime from dropdown
def chooseSeries(series: pd.DataFrame) -> str:
    titles = series.title.sort_values().values
    titles = np.insert(titles, 0, '')

    selectedAnime = st.selectbox(
        'Type or Select an Anime from the dropdown',
        titles
    )

    return selectedAnime

# recommend anime based on input
def recommendSeries() -> None:
    anime = chooseSeries(series)
    index = series[series['title'] == anime].index[0]
    distances = sorted(list(enumerate(series_similarity[index])),reverse=True,key = lambda x: x[1])

    animeCount = 1
    for i in distances:
        title = series.iloc[i[0]].title

        # fetch the poster and description
        if anime not in title and animeCount <= 15:
            poster = series.iloc[i[0]].poster
            description = series.iloc[i[0]].description
            url = series.iloc[i[0]].link

            # divide the page into 2 columns
            col1, col2 = st.columns(2)

            # print the attributes on the page
            with col1:
                st.image(poster, width=200)
            with col2:
                styled_title = f'<a href="{url}" style="color:red; font-size:1.2em;">{title}</a>'
                st.markdown(styled_title, unsafe_allow_html=True)
                st.write(description[0:400] + ' ...')
            animeCount += 1
        elif anime in title:
            continue

        if animeCount > 15:
            break
    

# import pickle
# import numpy as np

# similarity = pickle.load(open('./assets/bin/series_similarity.pkl', 'rb'))
# print(similarity.shape)

# divide = (similarity.shape[0] + 1) // 2
# # print(divide)

# first_half = similarity[0:divide]
# second_half = similarity[divide:]
# print(first_half.shape, second_half.shape)

# print(type(first_half), type(similarity), type(second_half))

# pickle.dump(first_half, open('./assets/bin/series_similarity1.pkl', 'wb'))
# pickle.dump(second_half, open('./assets/bin/series_similarity2.pkl', 'wb'))