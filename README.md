# Last.FM RecSys with Sentiment Analysis

The goal of this project is to test sentiment-aware recommender systems by use of the Last.FM API, sentiment analysis tools, and the **NRC-VAD Lexicon** (NRC Valence, Arousal, and Dominance Lexicon).
It consists of various recommendation techniques (collaborative filtering and content-based) and sentiment analysis of textual content from different contexts (e.g Album or artist description, tracks, comments, tags, titles...) applied to recommendation.

## Setup

- To set up the required environment modules and libraries, run `./setup.sh`.
- To set up the database, go to `/lastfm_RS` and run `make restore_db` to create _lastfm\_db_'s tables and load the necessary data.
- To start the application on localhost, go to `/lastfm_RS` and run `python3 manage.py runserver`. It will be hosted at http://localhost:8000.

**Note**: Only available recommenders are _Cosine Similarities_ and _Random_, due to size constraints.

## References

* [Obtaining Reliable Human Ratings of Valence, Arousal, and Dominance for 20,000 English Words](https://aclanthology.org/P18-1017) (Mohammad, ACL 2018)
* https://github.com/dwzhou/SentimentAnalysis
* https://github.com/cjhutto/vaderSentiment