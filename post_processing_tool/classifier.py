from typing import Tuple

import pandas as pd
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.utils import Bunch


def train() -> Tuple[SVC, TfidfVectorizer, Bunch]:
    newsgroups = fetch_20newsgroups(subset='all',
                                    categories=['soc.religion.christian',
                                                'talk.religion.misc',
                                                'talk.politics.misc'],
                                    shuffle=True, random_state=42)
    data = newsgroups.data
    target = newsgroups.target

    df = pd.DataFrame({'text': data, 'label': target})
    vectorizer = TfidfVectorizer(stop_words='english',
                                 strip_accents='ascii',
                                 max_df=0.7)

    X = vectorizer.fit_transform(df['text'])
    y = df['label']
    X_train, _, y_train, _ = train_test_split(X, y,
                                                        test_size=0.3,
                                                        random_state=42)

    clf = SVC(kernel='linear')
    clf.fit(X_train, y_train)

    return clf, vectorizer, newsgroups


def predict_category(text: str,
                     clf: SVC,
                     vectorizer: TfidfVectorizer,
                     newsgroups: Bunch):
    """
    Predict the category of a given text using the trained classifier.
    """
    text_vec = vectorizer.transform([text])
    prediction = clf.predict(text_vec)
    return newsgroups.target_names[prediction[0]]


def classify(text: str):
    clf, vectorizer, newsgroups = train()
    res = predict_category(text,
                           clf,
                           vectorizer,
                           newsgroups)
    print(f'The predicted category is: {res}')

    return res
