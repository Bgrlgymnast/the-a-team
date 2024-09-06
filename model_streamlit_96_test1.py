import streamlit as st
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler

# Initialize Streamlit app
st.title("Word-Based Multi-Output Prediction")

# Sample training data (for demonstration)
X_train = pd.DataFrame({
    'word': ['apple', 'banana', 'cherry', 'date', 'elderberry'],
    'feature2': [1, 2, 3, 4, 5],
    'feature3': [10, 20, 30, 40, 50]
})

y_train = pd.DataFrame({
    'output1': [0, 1, 0, 1, 0],
    'output2': [1, 0, 1, 0, 1]
})

# Initialize the TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Standardize the numerical features
scaler = StandardScaler()
X_train[['feature2', 'feature3']] = scaler.fit_transform(X_train[['feature2', 'feature3']])

# Fit the vectorizer and transform the 'word' feature
X_train_word_vectorized = vectorizer.fit_transform(X_train['word'])

# Combine the word vector with the other features ('feature2', 'feature3')
X_train_combined = np.hstack([X_train_word_vectorized.toarray(), X_train[['feature2', 'feature3']].values])

# Initialize and fit the classifier (Gradient Boosting)
classifier = MultiOutputClassifier(GradientBoostingClassifier())
classifier.fit(X_train_combined, y_train)

# User input for a single word
input_word = st.text_input("Enter a word for prediction", "")

# Allow the user to adjust default values for 'feature2' and 'feature3'
default_feature2 = st.number_input("Enter default value for feature2", value=0)
default_feature3 = st.number_input("Enter default value for feature3", value=0)

# Button to trigger the prediction
if st.button("Predict"):
    if input_word:
        # Vectorize the input word
        input_word_vectorized = vectorizer.transform([input_word])

        # Standardize the input features
        input_combined_features = scaler.transform([[default_feature2, default_feature3]])

        # Combine the word vector with the standardized numerical features
        input_combined = np.hstack([input_word_vectorized.toarray(), input_combined_features])

        # Make the prediction
        y_pred_new = classifier.predict(input_combined)

        # Display the prediction result
        st.write("Predicted Outputs:", y_pred_new)
    else:
        st.write("Please enter a word to make a prediction.")
