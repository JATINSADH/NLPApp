import nlpcloud
import emoji
class NLPApp:

    # API_KEY = "YOUR_API_KEY_FROM_NLP_CLOUD_WEBSITE"
    API_KEY = "YOUR API KEY"

    def __init__(self):
        self.__database = {}
        self.__logged_in = False
        self.current_email = None
        self.__first_menu()

    def __first_menu(self):
        first_input = input("""
        Hi! how would you like to proceed?
        1. New User, Ragister
        2. Already a Customer, Login
        3. Exit.""")

        if first_input == '1':
            self.__register()
        elif first_input == '2':
            self.__login()
        else:
            exit()

    def __second_menu(self):
        second_input = input("""
        hi! how would you like to proceed?
        1. NER (Entity Extaction)
        2. Language Detection
        3. Sentiment Anlaysis
        4. Question Answer
        5. Headline Generation
        6. Logout.""")

        if second_input == '1':
            self.__ner()
        elif second_input == '2':
            self.__language_detection()
        elif second_input == '3':
            self.__sentiment_analysis()
        elif second_input == '4':
            self.__question_answer()
        elif second_input == '5':
            self.__headline_generation()
        else:
            self.__logout()
        
    def __register(self):
        name = input('enter name: ')
        email = input('enter email: ')
        password = input('enter password:')
        if email in self.__database:
            print('user alredy exists')
        else:
            self.__database[email] = [name,password]
            print('Rajistration Succesuful, Now login')
            print('*'*20)
        self.__first_menu()

    def __login(self):
        email = input('enter email: ')
        password = input('enter password:')
        if email in self.__database:
            if self.__database[email][1] == password:
                print('Login Successfull.')
                self.__logged_in = True
                self.current_email = email
                print('*'*20)
                self.__second_menu()
            else:
                print('wrong password')
                self.__login()
        else:
            print('user does not exist')
            self.__first_menu()
        
    def __logout(self):
        if self.__logged_in:
            print(f"Closing connection to {self.__database[self.current_email][0]} for ({self.current_email})")
            self.__logged_in = False
            self.current_email = None
            print("Logout successful")
            print('*'*20)
        else:
            print("Already logged out")
        self.__first_menu()

    def __ner(self):
        para = input("""enter paragraph: """)
        search_term = input("enter what you want to search:")
        client = nlpcloud.Client("gpt-oss-120b", NLPApp.API_KEY, gpu=True)
        response = client.entities(para,searched_entity=search_term)
        texts = [j['text'] for i in response.values() for j in i]
        print(texts)
        print('*'*20)
        self.__second_menu()

    def __language_detection(self):
        para = input("""enter paragraph: """)
        client = nlpcloud.Client("python-langdetect", NLPApp.API_KEY, gpu=False)
        response = client.langdetection(para)
        for i in response['languages']:
            for lang, score in i.items():  
                print("{}: {}".format(lang,round(score,2)))
        print('*'*20)
        self.__second_menu()

    def __sentiment_analysis(self):
        para = input("""enter paragraph: """)
        target_term = input("enter taget term:")
        client = nlpcloud.Client("gpt-oss-120b", NLPApp.API_KEY, gpu=True)
        response = client.sentiment(para,target=target_term)
        scores = [i['score'] for i in response['scored_labels']]
        # sabse jayad akya h vo batane ke liye
        index = sorted(list(enumerate(scores)),key=lambda x:x[1], reverse=True)[0][0]
        label = response['scored_labels'][index]['label']
        # for emojis
        if label.lower() == 'positive':
            print(emoji.emojize("{} :smiling_face_with_smiling_eyes:").format(label))
        elif label.lower() == 'negative':
            print(emoji.emojize("{} :angry_face:").format(label))
        elif label.lower() == "joy":
                print(emoji.emojize("{} :grinning_face_with_big_eyes:").format(label))
        elif label.lower() == "love":
                print(emoji.emojize("{} :red_heart:").format(label))
        else:
            print(emoji.emojize("{} :neutral_face:").format(label))
        print('*'*20)
        self.__second_menu()

    def __question_answer(self):
        question = input("enter question: ")
        context = input("""enter context:""")
        client = nlpcloud.Client("gpt-oss-120b", NLPApp.API_KEY, gpu=True)
        response = client.question(question=question,context=context)
        print(response['answer'])
        print('*'*20)
        self.__second_menu()

    def __headline_generation(self):
        para = input("""enter paragraph: """)
        client = nlpcloud.Client("t5-base-en-generate-headline", NLPApp.API_KEY, gpu=False)
        response = client.summarization(para)
        print('Headline :',response['summary_text'])
        print('*'*20)
        self.__second_menu()

if __name__ == "__main__":
    obj = NLPApp()