import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import ast

df = pd.read_csv("cleaned_movies.csv")

df["genres"] = df["genres"].apply(
    lambda x: [g.strip() for g in x.split(",")]
)

X = df["overview"]
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(df["genres"])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=20000,
                              stop_words="english")),
    ("classifier", OneVsRestClassifier(
        LogisticRegression(max_iter=1000)
    ))
])

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Model training complete!")
print("Exact-match accuracy:",
      accuracy_score(y_test, predictions))
print("Genres:", list(mlb.classes_))

import joblib
joblib.dump(model, "genre_model.pkl")
joblib.dump(mlb, "genre_labels.pkl")

print("Model saved successfully!")
from sklearn.metrics import f1_score

y_pred = model.predict(X_test)

print("F1 Score:", f1_score(y_test, y_pred, average="micro"))
