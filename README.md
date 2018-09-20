# PopcornU

## Description

PopcornU was developed by two persons. It is a web browser-based search App, which connects to a cloud database including thousands of records about movies and TV Series. Users are able to search items based on keywords in movie titles. Users are also allowed to filter items based on movie genres, released year, and title types. Both single-selection and multi-selection are supported in PopcornU. Users are allowed to create their own account for saving their searches.

## Dataset

Dataset is from Kaggle website: https://www.kaggle.com/ccerberus24/movies/data. It contains movies and TV series watchlist data in the format of csv.

## Database
We have stored data in two databases of firebase using json format. Watchlists database is for storing movie metadate and inverted index for searching. Users database is for storing users information and their search history.

## Implementation

1. Front-End

We used HTML5, CSS3 and Javascript language, Bootstrap as framework to develop user interfaces. It has three parts, home page, login page and search page. Each page has a nav-bar to direct user throughout the website. Users can easily interact with the web-app and perform tasks.

2. Back-End

We used Python Flask as backend framework and RESTful api to transfer data with firebase. We created inverted index for keyword search and three facets search. Keywords is extracted from titles and directors. Facets search contains types, genres and years. When users request data, server will parse keywords and search matched movies based on id number in keywords inverted index. If users add facets constrains, the interaction of facets results and keywords results will be returned.

## Running Instructions

It is a local server application. Just set up Python 2.7 environment and run 'python popcornU.py'.
