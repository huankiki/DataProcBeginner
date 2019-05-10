from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
texts = [
    "good movie", "not a good movie", "did not like",
    "i like it", "good one"
]
# using default tokenizer in TfidfVectorizer
tfidf = TfidfVectorizer(min_df=2, max_df=0.5, ngram_range=(1, 2))
features = tfidf.fit_transform(texts)
print(pd.DataFrame(
    features.todense(),
    columns=tfidf.get_feature_names()
))
'''
   good movie      like     movie       not
0    0.707107  0.000000  0.707107  0.000000
1    0.577350  0.000000  0.577350  0.577350
2    0.000000  0.707107  0.000000  0.707107
3    0.000000  1.000000  0.000000  0.000000
4    0.000000  0.000000  0.000000  0.000000
'''


# using default tokenizer in TfidfVectorizer
tfidf = TfidfVectorizer(min_df=1, ngram_range=(1, 2))
features = tfidf.fit_transform(texts)
print(pd.DataFrame(
    features.todense(),
    columns=tfidf.get_feature_names()
))

'''
       did  did not      good  good movie  good one        it      like   like it     movie       not  not good  not like      one
0  0.00000  0.00000  0.506204    0.609818   0.00000  0.000000  0.000000  0.000000  0.609818  0.000000  0.000000   0.00000  0.00000
1  0.00000  0.00000  0.363135    0.437464   0.00000  0.000000  0.000000  0.000000  0.437464  0.437464  0.542226   0.00000  0.00000
2  0.48214  0.48214  0.000000    0.000000   0.00000  0.000000  0.388988  0.000000  0.000000  0.388988  0.000000   0.48214  0.00000
3  0.00000  0.00000  0.000000    0.000000   0.00000  0.614189  0.495524  0.614189  0.000000  0.000000  0.000000   0.00000  0.00000
4  0.00000  0.00000  0.427993    0.000000   0.63907  0.000000  0.000000  0.000000  0.000000  0.000000  0.000000   0.00000  0.63907
'''

