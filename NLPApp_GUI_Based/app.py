from tkinter import *

from pip._internal import commands

from mydb import Database
from tkinter import messagebox
from myapi import API
class NLPApp:

    def __init__(self):
        # create db object
        self.dbo = Database()
        self.apio = API()

        # load login Gui
        self.root = Tk()
        self.root.title("NLPApp")
        self.root.iconbitmap("resources/icon.ico")
        self.root.geometry("350x600")
        self.root.configure(bg='#34495E')

        self.login_gui()

        self.root.mainloop()

    def login_gui(self):
        self.clear()
        heading = Label(self.root, text="NLPApp",bg='#34495E',fg='white')
        heading.pack(pady=(30,30))
        heading.configure(font=("Arial", 24,'bold'))

        label1 = Label(self.root,text="Enter Email")
        label1.pack(pady=(10,10))
        self.email_input = Entry(self.root,width=45)
        self.email_input.pack(pady=(5,10),ipady=3)

        label2 = Label(self.root, text="Enter Password")
        label2.pack(pady=(10, 10))
        self.password_input = Entry(self.root, width=45, show='*')
        self.password_input.pack(pady=(5, 10), ipady=3)

        login_btn = Button(self.root,text='Login',width=25,height=2,command=self.perform_login)
        login_btn.pack(pady=(10, 10))

        label3 = Label(self.root, text="Not A Member?")
        label3.pack(pady=(20, 10))
        redirect_btn = Button(self.root, text='Register Now',command=self.register_gui)
        redirect_btn.pack(pady=(10, 10))

    def register_gui(self):
        self.clear()
        heading = Label(self.root, text="NLPApp", bg='#34495E', fg='white')
        heading.pack(pady=(30, 30))
        heading.configure(font=("Arial", 24, 'bold'))

        label0 = Label(self.root, text="Enter Name")
        label0.pack(pady=(10, 10))
        self.name_input = Entry(self.root, width=45)
        self.name_input.pack(pady=(5, 10), ipady=3)

        label1 = Label(self.root, text="Enter Email")
        label1.pack(pady=(10, 10))
        self.email_input = Entry(self.root, width=45)
        self.email_input.pack(pady=(5, 10), ipady=3)

        label2 = Label(self.root, text="Enter Password")
        label2.pack(pady=(10, 10))
        self.password_input = Entry(self.root, width=45, show='*')
        self.password_input.pack(pady=(5, 10), ipady=3)

        login_btn = Button(self.root, text='Register', width=25, height=2,command=self.perform_registration)
        login_btn.pack(pady=(10, 10))

        label3 = Label(self.root, text="Already A Member?")
        label3.pack(pady=(20, 10))
        redirect_btn = Button(self.root, text='Login Now', command=self.login_gui)
        redirect_btn.pack(pady=(10, 10))

    def clear(self):
        # clear the existing gui
        for i in self.root.pack_slaves():
            i.destroy()

    def perform_registration(self):
        # fetch data from gui
        name = self.name_input.get()
        email = self.email_input.get()
        password = self.password_input.get()

        response = self.dbo.add_data(name,email,password)

        if response == 1:
            messagebox.showinfo("Success", "Registration Successful. You can login Now.")
        else:
            messagebox.showerror('Error', 'Email Already Exists.')

    def perform_login(self):
        email = self.email_input.get()
        password = self.password_input.get()

        response = self.dbo.search(email,password)

        if response == 1:
            messagebox.showinfo("Success", "Login Successful.")
            self.home_gui()
        else:
            messagebox.showerror('Error', 'incorrect Email or Password.')

    def home_gui(self):

        self.clear()

        heading = Label(self.root, text="NLPApp", bg='#34495E', fg='white')
        heading.pack(pady=(30, 30))
        heading.configure(font=("Arial", 24, 'bold'))

        sentiment_btn = Button(self.root, text='Sentiment Analysis', width=25, height=3, command=self.sentiment_gui)
        sentiment_btn.pack(pady=(10, 10))

        ner_btn = Button(self.root, text='Named Entity Recognition', width=25, height=3, command=self.ner_gui)
        ner_btn.pack(pady=(10, 10))

        language_btn = Button(self.root, text='Language Detection', width=25, height=3, command=self.language_gui)
        language_btn.pack(pady=(10, 10))

        heading_btn = Button(self.root, text='Heading Generation', width=25, height=3, command=self.heading_gui)
        heading_btn.pack(pady=(10, 10))

        logout_btn = Button(self.root, text='Logout', command=self.login_gui)
        logout_btn.pack(pady=(10, 10))

    def sentiment_gui(self):
        self.clear()
        heading = Label(self.root, text="NLPApp", bg='#34495E', fg='white')
        heading.pack(pady=(30, 30))
        heading.configure(font=("Arial", 24, 'bold'))

        heading2 = Label(self.root, text="Sentiment Analysis", bg='#34495E', fg='white')
        heading2.pack(pady=(10, 20))
        heading2.configure(font=("Arial", 20))

        label1 = Label(self.root, text="Enter the Text")
        label1.pack(pady=(10, 10))
        self.sentiment_input = Entry(self.root, width=45)
        self.sentiment_input.pack(pady=(5, 10), ipady=3)

        label2 = Label(self.root, text="Enter the Target")
        label2.pack(pady=(10, 10))
        self.target_input = Entry(self.root, width=35)
        self.target_input.pack(pady=(5, 10), ipady=3)

        sentiment_analysis_btn = Button(self.root, text='Analyze Sentiment',command=self.do_sentiment_analysis)
        sentiment_analysis_btn.pack(pady=(10, 10))

        self.sentiment_result = Label(self.root, text='',bg='#34495E', fg='white')
        self.sentiment_result.pack(pady=(10, 10))
        self.sentiment_result.configure(font=("Arial", 16))

        goback_btn = Button(self.root, text='Go Back', command=self.home_gui)
        goback_btn.pack(pady=(10, 10))

    def do_sentiment_analysis(self):
        text = self.sentiment_input.get()
        target = self.target_input.get()

        response = self.apio.sentiment_analysis(text,target)
        self.sentiment_result["text"] = response
        # Agar response dict hai aur usme error key hai
        if isinstance(response, dict) and "Error" in response:
            # agar error aya to showerror
            messagebox.showerror("Error", f"Analysis Failed: {response}")
        else:
            messagebox.showinfo("Success", f"Analysis Successful: {response}")

    def ner_gui(self):
        self.clear()
        heading = Label(self.root, text="NLPApp", bg='#34495E', fg='white')
        heading.pack(pady=(30, 30))
        heading.configure(font=("Arial", 24, 'bold'))

        heading2 = Label(self.root, text="Named Entity Recognition", bg='#34495E', fg='white')
        heading2.pack(pady=(10, 20))
        heading2.configure(font=("Arial", 20))

        label1 = Label(self.root, text="Enter the Text")
        label1.pack(pady=(10, 10))
        self.ner_input = Entry(self.root, width=45)
        self.ner_input.pack(pady=(5, 10), ipady=3)

        label2 = Label(self.root, text="Entity to Search")
        label2.pack(pady=(10, 10))
        self.search_input = Entry(self.root, width=35)
        self.search_input.pack(pady=(5, 10), ipady=3)

        ner_btn = Button(self.root, text='Analyze NER',command=self.do_ner)
        ner_btn.pack(pady=(10, 10))

        self.ner_result = Label(self.root, text='',bg='#34495E', fg='white')
        self.ner_result.pack(pady=(10, 10))
        self.ner_result.configure(font=("Arial", 16))

        goback_btn = Button(self.root, text='Go Back', command=self.home_gui)
        goback_btn.pack(pady=(10, 10))


    def do_ner(self):
        text = self.ner_input.get()
        search = self.search_input.get()

        response = self.apio.ner(text,search)
        self.ner_result["text"] = response
        # Agar response dict hai aur usme error key hai
        if isinstance(response, dict) and "Error" in response:
            # agar error aya to showerror
            messagebox.showerror("Error", f"Analysis Failed: {response}")
        else:
            messagebox.showinfo("Success", f"Analysis Successful: {response}")

    def language_gui(self):
        self.clear()
        heading = Label(self.root, text="NLPApp", bg='#34495E', fg='white')
        heading.pack(pady=(30, 30))
        heading.configure(font=("Arial", 24, 'bold'))

        heading2 = Label(self.root, text="Heading Generation", bg='#34495E', fg='white')
        heading2.pack(pady=(10, 20))
        heading2.configure(font=("Arial", 20))

        label1 = Label(self.root, text="Enter the Text")
        label1.pack(pady=(10, 10))
        self.language_input = Entry(self.root, width=45)
        self.language_input.pack(pady=(5, 10), ipady=3)

        language_btn = Button(self.root, text='Generate',command=self.do_language_detection)
        language_btn.pack(pady=(10, 10))

        self.language_result = Label(self.root, text='',bg='#34495E', fg='white')
        self.language_result.pack(pady=(10, 10))
        self.language_result.configure(font=("Arial", 16))

        goback_btn = Button(self.root, text='Go Back', command=self.home_gui)
        goback_btn.pack(pady=(10, 10))

    def do_language_detection(self):
        text = self.language_input.get()

        response = self.apio.language_detection(text)
        self.language_result["text"] = response
        # Agar response dict hai aur usme error key hai
        if isinstance(response, dict) and "Error" in response:
            # agar error aya to showerror
            messagebox.showerror("Error", f"Detection Failed: {response}")
        else:
            messagebox.showinfo("Success", f"Detection Successful: {response}")


    def heading_gui(self):
        self.clear()
        heading = Label(self.root, text="NLPApp", bg='#34495E', fg='white')
        heading.pack(pady=(30, 30))
        heading.configure(font=("Arial", 24, 'bold'))

        heading2 = Label(self.root, text="Heading Generation", bg='#34495E', fg='white')
        heading2.pack(pady=(10, 20))
        heading2.configure(font=("Arial", 20))

        label1 = Label(self.root, text="Enter the Text")
        label1.pack(pady=(10, 10))
        self.heading_input = Entry(self.root, width=45)
        self.heading_input.pack(pady=(5, 10), ipady=3)

        heading_btn = Button(self.root, text='Generate',command=self.do_heading_generate)
        heading_btn.pack(pady=(10, 10))

        self.heading_result = Label(self.root, text='',bg='#34495E', fg='white')
        self.heading_result.pack(pady=(10, 10))
        self.heading_result.configure(font=("Arial", 16))

        goback_btn = Button(self.root, text='Go Back', command=self.home_gui)
        goback_btn.pack(pady=(10, 10))

    def do_heading_generate(self):
        text = self.heading_input.get()

        response = self.apio.heading_generation(text)
        self.heading_result["text"] = response
        # Agar response dict hai aur usme error key hai
        if isinstance(response, dict) and "Error" in response:
            # agar error aya to showerror
            messagebox.showerror("Error", f"Generation Failed: {response}")
        else:
            messagebox.showinfo("Success", f"Generation Successful: {response}")

nlp = NLPApp()