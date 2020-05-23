# Emotional-Analysis-on-Twitter-data
Scrapes tweets and and performs Emotional analysis on them.

# Design
Flask-App directory holds the Flask application and the dependencies for Heroku app, which is the root direcory of the webpage.

dash-app directory holds the dashboard, made from Plotly-Dash api, along with dependencies for the live twitter streaming.

emotionalanalysis.py is the python file which has source code for predicting the emotions,
twitterscrape.py is the python file for the source code to handle att twitter related operations.

Notebook.ipynb is the python notebook file to demonstrate every operation in the code.
It also has EDA on the dataset
