# -*- coding: utf-8 -*-
"""SMS and Email Spam Delection

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aFSCcJktW_C687d8ybJ3rc3ROzK6cszg
"""

# Import necessary libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder  # Import LabelEncoder
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter
from wordcloud import WordCloud
import nltk
import string

# Input the SMS text
sms_text = input("Enter the SMS text: ")

# Sample SMS text

# Sample of the dataset
df = pd.read_csv('spam.csv', encoding='latin1')

# Rename columns
df.rename(columns={'v1':'target','v2':'text'}, inplace=True)

# Encode the target variable
encoder = LabelEncoder()
df['target'] = encoder.fit_transform(df['target'])

# Remove duplicates
df = df.drop_duplicates(keep='first')

# Add additional features - number of characters, words, and sentences
df['num_characters'] = df['text'].apply(len)

# Download necessary nltk resources
nltk.download('punkt')
nltk.download('stopwords')

# Add word and sentence count
df['num_words'] = df['text'].apply(lambda x: len(nltk.word_tokenize(x)))
df['num_sentences'] = df['text'].apply(lambda x: len(nltk.sent_tokenize(x)))

# Visualize additional features
plt.figure(figsize=(12,8))
sns.histplot(df[df['target']==0]['num_characters'])
sns.histplot(df[df['target']==1]['num_characters'], color='red')
plt.show()

plt.figure(figsize=(12,8))
sns.histplot(df[df['target']==0]['num_words'])
sns.histplot(df[df['target']==1]['num_words'], color='red')
plt.show()

# Pairplot
sns.pairplot(df, hue='target')
plt.show()

# Correlation heatmap
# Select only numerical columns for correlation computation
numerical_df = df.select_dtypes(include=['int64', 'float64'])

# Correlation heatmap
sns.heatmap(numerical_df.corr(), annot=True)
plt.show()

def transform_text(text):
    text = nltk.word_tokenize(text)
    text = [word.lower() for word in text if word.isalnum()]
    text = [word for word in text if word not in stopwords.words('english') and word not in string.punctuation]
    ps = PorterStemmer()
    text = [ps.stem(word) for word in text]
    return " ".join(text)

# Apply text transformation
df['transformed_text'] = df['text'].apply(transform_text)

# WordCloud
wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

# Vectorization
tfidf = TfidfVectorizer(max_features=1000)  # Adjust the max_features value as needed
X = tfidf.fit_transform(df['transformed_text']).toarray()

# Generate WordCloud for spam messages with adjusted parameters
spam_wc = wc.generate(" ".join(df[df['target'] == 1]['transformed_text']))

# Increase the size of the canvas and adjust the minimum font size
plt.figure(figsize=(15,10))
plt.imshow(spam_wc, interpolation='bilinear')
plt.axis('off')  # Remove axis
plt.show()

# Generate WordCloud for ham messages
ham_wc = wc.generate(" ".join(df[df['target'] == 0]['transformed_text']))

# Increase the size of the canvas and adjust the minimum font size
plt.figure(figsize=(15,10))
plt.imshow(ham_wc, interpolation='bilinear')
plt.axis('off')  # Remove axis
plt.show()

# Most common words in spam messages
spam_corpus = " ".join(df[df['target'] == 1]['transformed_text']).split()
spam_word_counts = Counter(spam_corpus)
common_spam_words = spam_word_counts.most_common(30)
common_spam_words_df = pd.DataFrame(common_spam_words, columns=['Word', 'Frequency'])

plt.figure(figsize=(12, 8))
sns.barplot(x='Word', y='Frequency', data=common_spam_words_df)
plt.xticks(rotation=45, ha='right')
plt.title('Most Common Words in Spam Messages')
plt.show()

# Most common words in ham messages
ham_corpus = " ".join(df[df['target'] == 0]['transformed_text']).split()
ham_word_counts = Counter(ham_corpus)
common_ham_words = ham_word_counts.most_common(30)
common_ham_words_df = pd.DataFrame(common_ham_words, columns=['Word', 'Frequency'])

plt.figure(figsize=(12, 8))
sns.barplot(x='Word', y='Frequency', data=common_ham_words_df)
plt.xticks(rotation=45, ha='right')

# Vectorization
tfidf = TfidfVectorizer(max_features=3000)
X = tfidf.fit_transform(df['transformed_text']).toarray()
X = np.hstack((X, df['num_characters'].values.reshape(-1,1)))
y = df['target'].values

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

# Train MultinomialNB classifier
rfc = MultinomialNB()
rfc.fit(X_train, y_train)

# Make predictions on the test data
y_pred = rfc.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Print accuracy
print("Accuracy using MultinomialNB classifier:", accuracy)


# Transform input text
transformed_sms = transform_text(sms_text)
vectorized_sms = tfidf.transform([transformed_sms]).toarray()
num_characters = len(sms_text)

# Add number of characters as additional feature
vectorized_sms = np.hstack((vectorized_sms, np.array(num_characters).reshape(-1,1)))

# Predict
prediction = rfc.predict(vectorized_sms)

# Decode prediction
prediction_label = encoder.inverse_transform(prediction)[0]

# Print result
print("Prediction for the given SMS text:", prediction_label)

# Import necessary libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder  # Import LabelEncoder
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter
from wordcloud import WordCloud
import nltk
import string

# Input the SMS text
sms_text = input("Enter the SMS text: ")

# Sample SMS text

# Sample of the dataset
df = pd.read_csv('spam.csv', encoding='latin1')

# Rename columns
df.rename(columns={'v1':'target','v2':'text'}, inplace=True)

# Encode the target variable
encoder = LabelEncoder()
df['target'] = encoder.fit_transform(df['target'])


# Remove duplicates
df = df.drop_duplicates(keep='first')

# Add additional features - number of characters, words, and sentences
df['num_characters'] = df['text'].apply(len)

# Download necessary nltk resources
nltk.download('punkt')
nltk.download('stopwords')

# Add word and sentence count
df['num_words'] = df['text'].apply(lambda x: len(nltk.word_tokenize(x)))
df['num_sentences'] = df['text'].apply(lambda x: len(nltk.sent_tokenize(x)))

# Visualize additional features
plt.figure(figsize=(12,8))
sns.histplot(df[df['target']==0]['num_characters'])
sns.histplot(df[df['target']==1]['num_characters'], color='red')
plt.show()

plt.figure(figsize=(12,8))
sns.histplot(df[df['target']==0]['num_words'])
sns.histplot(df[df['target']==1]['num_words'], color='red')
plt.show()

# Pairplot
sns.pairplot(df, hue='target')
plt.show()

# Correlation heatmap
# Select only numerical columns for correlation computation
numerical_df = df.select_dtypes(include=['int64', 'float64'])

# Correlation heatmap
sns.heatmap(numerical_df.corr(), annot=True)
plt.show()

def transform_text(text):
    text = nltk.word_tokenize(text)
    text = [word.lower() for word in text if word.isalnum()]
    text = [word for word in text if word not in stopwords.words('english') and word not in string.punctuation]
    ps = PorterStemmer()
    text = [ps.stem(word) for word in text]
    return " ".join(text)

# Apply text transformation
df['transformed_text'] = df['text'].apply(transform_text)

# WordCloud
wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

# Vectorization
tfidf = TfidfVectorizer(max_features=1000)  # Adjust the max_features value as needed
X = tfidf.fit_transform(df['transformed_text']).toarray()

# Generate WordCloud for spam messages with adjusted parameters
spam_wc = wc.generate(" ".join(df[df['target'] == 1]['transformed_text']))

# Increase the size of the canvas and adjust the minimum font size
plt.figure(figsize=(15,10))
plt.imshow(spam_wc, interpolation='bilinear')
plt.axis('off')  # Remove axis
plt.show()

# Generate WordCloud for ham messages
ham_wc = wc.generate(" ".join(df[df['target'] == 0]['transformed_text']))

# Increase the size of the canvas and adjust the minimum font size
plt.figure(figsize=(15,10))
plt.imshow(ham_wc, interpolation='bilinear')
plt.axis('off')  # Remove axis
plt.show()

# Most common words in spam messages
spam_corpus = " ".join(df[df['target'] == 1]['transformed_text']).split()
spam_word_counts = Counter(spam_corpus)
common_spam_words = spam_word_counts.most_common(30)
common_spam_words_df = pd.DataFrame(common_spam_words, columns=['Word', 'Frequency'])

plt.figure(figsize=(12, 8))
sns.barplot(x='Word', y='Frequency', data=common_spam_words_df)
plt.xticks(rotation=45, ha='right')
plt.title('Most Common Words in Spam Messages')
plt.show()

# Most common words in ham messages
ham_corpus = " ".join(df[df['target'] == 0]['transformed_text']).split()
ham_word_counts = Counter(ham_corpus)
common_ham_words = ham_word_counts.most_common(30)
common_ham_words_df = pd.DataFrame(common_ham_words, columns=['Word', 'Frequency'])

plt.figure(figsize=(12, 8))
sns.barplot(x='Word', y='Frequency', data=common_ham_words_df)
plt.xticks(rotation=45, ha='right')

# Vectorization
tfidf = TfidfVectorizer(max_features=3000)
X = tfidf.fit_transform(df['transformed_text']).toarray()
X = np.hstack((X, df['num_characters'].values.reshape(-1,1)))
y = df['target'].values

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

# Train Random Forest classifier
rfc = RandomForestClassifier()
rfc.fit(X_train, y_train)

# Make predictions on the test data
y_pred = rfc.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Print accuracy
print("Accuracy using Random Forest classifier:", accuracy)


# Transform input text
transformed_sms = transform_text(sms_text)
vectorized_sms = tfidf.transform([transformed_sms]).toarray()
num_characters = len(sms_text)

# Add number of characters as additional feature
vectorized_sms = np.hstack((vectorized_sms, np.array(num_characters).reshape(-1,1)))

# Predict
prediction = rfc.predict(vectorized_sms)

# Decode prediction
prediction_label = encoder.inverse_transform(prediction)[0]

# Print result
print("Prediction for the given SMS text:", prediction_label)