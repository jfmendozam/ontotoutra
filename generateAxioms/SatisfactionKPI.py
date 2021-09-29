import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

reviews = pd.read_csv('/home/jf/Documentos/education/phd/thesis/dev/ontologies/protege/mysql csv data/locationReviews.csv', parse_dates=['date'])
reviews['neg'] = reviews['review'].apply(lambda x:sia.polarity_scores(x)['neg'])
reviews['pos'] = reviews['review'].apply(lambda x:sia.polarity_scores(x)['pos'])
reviews['neu'] = reviews['review'].apply(lambda x:sia.polarity_scores(x)['neu'])
reviews['compound'] = reviews['review'].apply(lambda x:sia.polarity_scores(x)['compound'])

from plotly.offline import download_plotlyjs, init_notebook_mode, plot
import plotly.express as px

reviews['YearMonth'] = pd.to_datetime(reviews.date).apply(lambda x: '{year}-{month:02d}'.format(year=x.year, month=x.month))
df = reviews.groupby(reviews.YearMonth)[['pos', 'neg', 'neu']].mean()
df.reset_index(inplace=True)
df = df.rename(columns = {'YearMonth':'date'})
fig = px.line(
    df,
    x=df.date, 
    y=[df.pos],
    hover_data={'date': "|%B %d, %Y"},
    title='Satisfaction KPI'
)
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y",
    ticklabelmode="period"
)

#fig.show()
plot(fig)
