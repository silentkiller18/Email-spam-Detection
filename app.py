import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

# Download nltk resources if not already present
nltk.download('punkt')
nltk.download('stopwords')

ps = PorterStemmer()

# Function to preprocess the text
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

# Load pre-trained model and vectorizer
tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

# Page title and background style with custom image
st.markdown(
    """
    <style>
    body {
        background-image: url(""); /* Replace with your image URL */
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.title("Email/SMS Spam Classifier")

# Input text area
input_sms = st.text_area("Enter the message")

# Prediction button
if st.button('Predict'):
    # Preprocess input
    transformed_sms = transform_text(input_sms)
    # Vectorize
    vector_input = tfidf.transform([transformed_sms])
    # Predict
    result = model.predict(vector_input)[0]
    # Display prediction result
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")
