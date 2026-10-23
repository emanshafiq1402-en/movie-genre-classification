# movie-genre-classification
A Natural Language Processing (NLP) project to collect movie descriptions and genres using the TMDB API and build a movie genre classification model.

# Movie Genre Classification

A machine learning project that predicts movie genres from movie overviews using Natural Language Processing (NLP).

# Features

* Movie dataset preprocessing
* Text vectorization using TF-IDF
* Multi-label genre classification
* Model training and evaluation
* Genre prediction for new movie descriptions

# Technologies Used

* Python
* Pandas
* Scikit-learn
* Joblib
* TF-IDF Vectorization

# Project Files

* create_dataset.py — collects movie data
* convert_genres.py — converts genre information
* preprocess_data.py — cleans the dataset
* train_model.py — trains and saves the model
* test_model.py — predicts genres for a movie overview

# How to Run

1. Install the required Python packages.
2. Prepare the dataset.
3. Run python train_model.py.
4. Run python test_model.py and enter a movie overview.

# Security

Keep your TMDB API key in a local .env file and never upload secrets to GitHub.
