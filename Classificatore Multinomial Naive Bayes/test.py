import pandas as pd
import numpy as np
import pickle

with open('Model/estimator.pkl', 'rb') as fid1:
    classifier = pickle.load(fid1)

with open('Model/vectorizer.pkl', 'rb') as fid2:
    features = pickle.load(fid2)

# Test data 
test_data = pd.read_csv("Test/data_test.csv")
test_data = test_data[:100]

X_tf = features.transform(test_data['full_text'])

predicted = classifier.predict(X_tf)

print('We got an accuracy of',np.mean(predicted == test_data['category'])*100, '% over the test data.')


