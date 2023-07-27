# Last.FM RecSys with Sentiment Analysis

The goal of this project is to test sentiment-aware recommender systems by use of the Last.FM API, sentiment analysis tools, and the **NRC-VAD Lexicon** (NRC Valence, Arousal, and Dominance Lexicon).
It consists of various recommendation techniques (collaborative filtering and content-based) and sentiment analysis of textual content from different contexts (e.g Album or artist description, tracks, comments, tags, titles...) applied to recommendation. 

The tools and recommendation models are showcased in **LastMood**, a web application that can be set up with the following section's steps.

## Setup

1. To set up the required environment modules and libraries:
    - Install Conda for environment management.
    - Run `./setup.sh`.
3. To set up the database (~760 MB):
    - Install PostgreSQL.
    - Go to `/lastfm_RS` and run `make restore_db`. This creates _lastfm\_db_'s tables and loads all the necessary data.
4. To set up the recommendation data (~500 MB):
    -  Go to `/lastfm_RS` and run `make recsys_data`. This extracts the prepared dataset into `/lastfm_RS/backend/research/recbole_research/saved/`. Otherwise, the data needs to be preprocessed, which takes considerable time and memory.
5. To start the web application on localhost, go to `/lastfm_RS` and run `python3 manage.py runserver`. It will be hosted at http://localhost:8000.

**Note**: The only available recommenders are _Random_, _Pop_ and _Cosine Similarities_, due to size constraints.

## References

* [Obtaining Reliable Human Ratings of Valence, Arousal, and Dominance for 20,000 English Words](https://aclanthology.org/P18-1017) (Mohammad, ACL 2018)
* https://github.com/dwzhou/SentimentAnalysis
* https://github.com/cjhutto/vaderSentiment
* https://github.com/pylast/pylast
* https://github.com/goldsmith/Wikipedia
