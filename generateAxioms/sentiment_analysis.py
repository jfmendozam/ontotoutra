import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import seaborn as sns
import matplotlib.pyplot as plt

# https://towardsdatascience.com/sentiment-analysis-for-hotel-reviews-3fa0c287d82e

# import location reviews
reviews = pd.read_csv('/home/jf/Documentos/education/phd/thesis/dev/ontologies/protege/mysql csv data/locationReviews.csv')

sia = SentimentIntensityAnalyzer()

# apply sla and transform them into the dataframe
reviews['neg'] = reviews['review'].apply(lambda x:sia.polarity_scores(x)['neg'])
reviews['neu'] = reviews['review'].apply(lambda x:sia.polarity_scores(x)['neu'])
reviews['pos'] = reviews['review'].apply(lambda x:sia.polarity_scores(x)['pos'])
reviews['compound'] = reviews['review'].apply(lambda x:sia.polarity_scores(x)['compound'])

pos_review = [j for i, j in enumerate(reviews['review']) if reviews['compound'][i] > 0.2]
neu_review = [j for i, j in enumerate(reviews['review']) if 0.2 >= reviews['compound'][i] >= -0.2]
neg_review = [j for i, j in enumerate(reviews['review']) if reviews['compound'][i] < -0.2]

print("Percentage of positive review: {}%".format(len(pos_review) * 100 / len(reviews['review'])))
print("Percentage of neutral review: {}%".format(len(neu_review) * 100 / len(reviews['review'])))
print("Percentage of negative review: {}%".format(len(neg_review) * 100 / len(reviews['review'])))

top10_df = reviews.groupby('country').size().reset_index().sort_values(0, ascending = False).head(10)
top10_df.columns = ['country', 'Counts']
print("Top 10 countries ranked by review counts")
print(top10_df)

top10_list = top10_df['country'].tolist()
top10 = reviews[reviews.country.isin(top10_list)]

fig, ax = plt.subplots()
fig.set_size_inches(20, 5)
ax = sns.violinplot(
    x = 'country', 
    y = 'score', 
    data = top10, 
    order = top10_list,
    linewidth = 2
) 
plt.suptitle('Scores of the reviewers') 
plt.xticks(rotation=45);
plt.show()