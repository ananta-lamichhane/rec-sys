# !!PROJECT MOVED OVER TO GITLAB ON PROJECT COORDINATOR'S REQUEST!!
## Introduction
Recommendation systems are at the heart of many modern services. A good recommendation system helps you find a new item that may suit you on amazon and myriad of other e-commerce sites. Netflix's recommendation system can help you find a movie you'd want to watch. A good recommendation system can suggest you articles and books to read, podcasts and music to listen to, and much more. The ubiquity and relevance of recommender systesms in multitude of industries underscores a necessity of research into the implementation and effectiveness of various tools and algorithms that help to generate reommendation based on some existing data.

Collaborative filtering is a subset of recommer system methods that produce a user-specific recommendation based on patterns of ratings or usage, usually without the need of exogenous information about either items or users. Kickstarted by the Netflix prize in 2006 to search for the most accurate recommeder system, collaborative filtering has attracted a lot of interest in the subsequent years.

This project provides a web portal where researchers will be able to conduct surveys, extract survey information and compare the accuracy of various collaborative filtering algorithms. Users (survey participants) will be able to log in, fill in the survey questionnaire and rate the recommendations.

## How to install
### System requirements
1. Linux (Tested on Ubuntu 20.04)
2. Python 3.8

### Install steps
Since the project is a web-app. You'll need a domain name to make it available on the internet. To run web-app locally on a web-server for development, follow steps. 
1. Clone
2. Set up a [python virtual environment.](https://docs.python.org/3/library/venv.html)
3. Install requirements.`pip install -r requirements.txt`
4. Export environment variable: `export FLASK_APP=run.py`
5. `flask run`

The flask web server serves the app on port 5000 (can be changed by editing run.py)

## Install on docker



