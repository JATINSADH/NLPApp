import nlpcloud
import emoji
class API:
    def __init__(self):
        self.API_KEY = 'Your API Key'

    def sentiment_analysis(self,text,target):
        try:
            client = nlpcloud.Client("gpt-oss-120b", token=self.API_KEY, gpu=True)
            response = client.sentiment(text=text,target=target)
            scores = [i['score'] for i in response['scored_labels']]
        # sabse jayada kya h, vo batane ke liye
            index = sorted(list(enumerate(scores)), key=lambda x: x[1], reverse=True)[0][0]
            label = response['scored_labels'][index]['label']
        # for emojis
            if label.lower() == 'positive':
                return emoji.emojize("{} :smiling_face_with_smiling_eyes:").format(label)
            elif label.lower() == 'negative':
                return emoji.emojize("{} :angry_face:").format(label)
            elif label.lower() == "joy":
                return emoji.emojize("{} :grinning_face_with_big_eyes:").format(label)
            elif label.lower() == "love":
                return emoji.emojize("{} :red_heart:").format(label)
            elif label.lower() == "natural":
                return emoji.emojize("{} :neutral_face:").format(label)
            else:
                return label
        except Exception as e:
            return {"Error":str(e)}
            # {'scored_labels': [{'label': 'POSITIVE', 'score': 1}, {'label': 'joy', 'score': 1}]}

    def ner(self,text,search):
        try:
            client = nlpcloud.Client("gpt-oss-120b", token=self.API_KEY, gpu=True)
            response = client.entities(text=text, searched_entity=search)
            texts = [j['text'] for i in response.values() for j in i]
            return texts

        except Exception as e:
            return {"Error": str(e)}

    def language_detection(self,text):
        try:
            client = nlpcloud.Client("python-langdetect", token=self.API_KEY, gpu=False)
            response = client.langdetection(text=text)
            for i in response['languages']:
                for lang, score in i.items():
                    return "{}: {}".format(lang, round(score, 2))

        except Exception as e:
            return {"Error": str(e)}

    def heading_generation(self,text):
        try:
            client = nlpcloud.Client("t5-base-en-generate-headline", token=self.API_KEY, gpu=False)
            response = client.summarization(text=text)
            return response['summary_text']

        except Exception as e:
            return {"Error": str(e)}

