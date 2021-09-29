import pandas as pd
reviews = pd.read_csv('/home/jf/Documentos/education/phd/thesis/dev/ontologies/protege/mysql csv data/locationReviews.csv')

from textblob import TextBlob

def subjectivity(text):
    return TextBlob(text).sentiment.subjectivity
    
def polarity(text):
    return TextBlob(text).sentiment.polarity
    
reviews['Subjectivity'] = reviews.review.apply(subjectivity)
reviews['Polarity'] = reviews.review.apply(polarity)
def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'
        
reviews['Analysis'] = reviews.Polarity.apply(getAnalysis)

import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode, plot

fig = px.scatter(
    reviews,
    x     = 'Polarity',
    y     = 'Subjectivity',
    color = 'Analysis',
    size  = 'Subjectivity',
    color_discrete_sequence = ['orange', 'green', 'red']
)

fig.update_layout(
    title = 'Sentiment Analysis',
    shapes = [
        dict(
            type = 'line',
            yref = 'paper', 
            y0   = 0, 
            y1   = 1,
            xref = 'x', 
            x0   = 0, 
            x1   = 0
        )
    ]
)

plot(fig)

#import plotly.io as pio
#pio.kaleido.scope.default_format = "svg"
#fig.write_image("lulu.svg", engine="kaleido")
