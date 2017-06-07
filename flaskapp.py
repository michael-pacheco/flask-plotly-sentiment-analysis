#flaskapp.py
from flask import Flask, render_template
import csv, re, operator
from textblob import TextBlob

app = Flask(__name__)

@app.route('/')
def main():
    text = ""
    values = {"positive": 0, "negative": 0, "neutral": 0}

    with open('ask_politics.csv', 'rt') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for idx, row in enumerate(reader):
            if idx > 0 and idx % 2000 == 0:
                break
            if  'text' in row:
                nolinkstext = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', row['text'], flags=re.MULTILINE)
                text = nolinkstext

            blob = TextBlob(text)
            for sentence in blob.sentences:
                sentiment_value = sentence.sentiment.polarity
                if sentiment_value >= -0.1 and sentiment_value <= 0.1:
                    values['neutral'] += 1
                elif sentiment_value < 0:
                    values['negative'] += 1
                elif sentiment_value > 0:
                    values['positive'] += 1

    values = sorted(values.items(), key=operator.itemgetter(1))
    top_ten = list(reversed(values))
    if len(top_ten) >= 11:
        top_ten = top_ten[1:11]
    else :
        top_ten = top_ten[0:len(top_ten)]

    top_ten_list_vals = []
    top_ten_list_labels = []
    for language in top_ten:
        top_ten_list_vals.append(language[1])
        top_ten_list_labels.append(language[0])

    graph_values = [{
                    'labels': top_ten_list_labels,
                    'values': top_ten_list_vals,
                    'type': 'pie',
                    'insidetextfont': {'color': '#FFFFFF',
                                        'size': '14',
                                        },
                    'textfont': {'color': '#FFFFFF',
                                        'size': '14',
                                },
                    }]

    layout = {'title': '<b>Sentiment analysis of posts in /r/ask_politics</b>'}

    return render_template('index.html', graph_values=graph_values, layout=layout)

if __name__ == '__main__':
  app.run(debug= True,host="127.0.0.1",port=5000, threaded=True)
