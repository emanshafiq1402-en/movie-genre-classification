import joblib

model = joblib.load("genre_model.pkl")
mlb = joblib.load("genre_labels.pkl")

overview = input("Enter a movie overview: ")

prediction = model.predict([overview])
probabilities = model.predict_proba([overview])[0]

top_indices = probabilities.argsort()[-3:][::-1]
genres = mlb.classes_[top_indices]

print("Predicted genres:", genres)