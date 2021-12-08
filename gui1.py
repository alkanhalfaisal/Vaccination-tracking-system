import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import tkinter.messagebox
import re
import sqlite3
from pathlib import Path
from tkinter import filedialog as fd
import csv

my_file = Path("test.db")
if my_file.is_file():
    print('database already created')
else:
    conn = sqlite3.connect("test.db")
    print ("Opened database successfully")
    conn.execute('''CREATE TABLE Vaccine
       (
        FIRST_name TEXT     NOT NULL,
        LAST_name TEXT     NOT NULL,
        Gender TEXT            NOT NULL,
        ID INT(10)  NOT NULL,
        year_of_birth int(4),
        vaccine TEXT,
        Date TEXT,
        phone_number TEXT
        );''')
    print ("Table created successfully")

class gui:

    def __init__(self):
        conn = sqlite3.connect("test.db")
        self.app = tk.Tk()
        self.app.title('Vaccines')

        self.notebook = ttk.Notebook(self.app)
        self.notebook.pack(pady=10, expand=True)

        self.labelframe = tk.LabelFrame(self.app, text="Information")
        self.labelframe2 = tk.LabelFrame(self.app, text="individual’s status")
        self.labelframe3 = tk.LabelFrame(self.app, text="Import & Export")

        self.frame = tk.Frame(self.labelframe)
        self.frame2 = tk.Frame(self.labelframe2)
        self.frame3 = tk.Frame(self.labelframe3)


        self.flname_label = tkinter.Label(self.frame, text='First,last name:')
        self.flname_entry = tkinter.Entry(self.frame, width=23)

        self.labelTop = tkinter.Label(self.frame, text="Gender: ")
        gender = ('Male', 'Female')
        selected_gender = tk.StringVar()
        self.cb = ttk.Combobox(self.frame, textvariable=selected_gender)
        self.cb['values'] = gender
        self.cb.current(0)

        self.id_label = tkinter.Label(self.frame, text='ID:')
        self.id_entry = tkinter.Entry(self.frame, width=23)

        self.year_label = tkinter.Label(self.frame, text='Year of birth:')
        self.year_entry = tkinter.Entry(self.frame, width=23)

        self.labelTop2 = tk.Label(self.frame, text="Vaccine: ")
        vaccine = ('AstraZenca', 'Pfizer', 'Moderna', 'J&J')
        selected_vaccine = tk.StringVar()
        self.cb2 = ttk.Combobox(self.frame, textvariable=selected_vaccine)
        self.cb2['values'] = vaccine
        self.cb2.current(0)


        self.flname_label.grid(column=0, row=1)
        self.flname_entry.grid(column=1, row=1)

        self.labelTop.grid(column=0, row=3,padx = 20)
        self.cb.grid(column=1, row=3)

        self.id_label.grid(column=0, row=4 ,padx = 20)
        self.id_entry.grid(column=1, row=4, )

        self.year_label.grid(column=0, row=5)
        self.year_entry.grid(column=1, row=5)

        self.labelTop2.grid(column=0, row=6,padx = 0)
        self.cb2.grid(column=1, row=6)

        self.cal = Calendar(self.frame, selectmode='day',
                       year=2020, month=5,
                       day=22, date_pattern="m/d/y")
        self.cal.grid(columnspan = 3, pady=20)

        self.button=tkinter.Button(self.frame, text="Show selected date",
               command=self.grad_date).grid(columnspan = 3)

        self.date = tkinter.Label(self.frame, text="")
        self.date.grid(columnspan = 3)

        def show():
            label = tkinter.Label(self.frame, text=hour.get() + ' : ' + mins.get()).grid(columnspan=11)

        t = tkinter.Label(self.frame, text='Time: ')
        t.grid(columnspan=1)

        hour = tkinter.Spinbox(self.frame, from_=00, to=23, width=5)
        hour.grid(column=1, row=10)
        mins = tkinter.Spinbox(self.frame, from_=0, to=59, width=5)
        mins.grid(column=2,row=10)

        self.phone_label = tkinter.Label(self.frame, text='Phone number:')
        self.phone_entry = tkinter.Entry(self.frame, width=23)
        self.phone_entry.insert(0, "05")

        self.phone_label.grid(column=0, row=13,pady=20)
        self.phone_entry.grid(column=1, row=13)


        def date_time():
            min=mins.get()
            if int(min)<10:
                min='0'+mins.get()
            if int(hour.get())<12:
                if int(hour.get()) ==0:
                    hour_format=' 12'+':'+min+ 'AM'
                else:
                    hour_format=' '+hour.get()+':'+min+ 'AM'
            else:
                if int(hour.get())==12:
                    hour_format=' '+hour.get()+':'+min+ 'PM'
                else:
                    hour_format=' '+str(int(hour.get())-12)+':'+min+ 'PM'
            return hour_format

        def submit():

            try:
                int(self.id_entry.get())
                reg = "^[0-3][5][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$"
                pat = re.compile(reg)
                valid_phone_number = re.search( pat, self.phone_entry.get())

                if int(self.year_entry.get()) <= 1900:
                    tkinter.messagebox.showinfo('Response', 'ERROR \nyear of Birth must be after 1900 ')
                elif int(self.year_entry.get()) >= 2003:
                    tkinter.messagebox.showinfo('Response', 'ERROR \nyear of Birth must be before 2003 ')
                elif int(len(self.id_entry.get())) != 10 :
                    tkinter.messagebox.showinfo('Response', 'ERROR \nID must consist of 10 digits ')
                elif valid_phone_number ==None :
                    tkinter.messagebox.showinfo('Response', 'ERROR \nInvalid phone number ')
                elif self.flname_entry.get() == '':
                    tkinter.messagebox.showinfo('Response', 'ERROR \nThe name field is empty ')
                else:
                    first, last = self.flname_entry.get().split(" ")
                    sql ="INSERT INTO Vaccine(ID,FIRST_name ,LAST_name ,Gender,year_of_birth,vaccine,Date,phone_number) VALUES(?,?,?,?,?,?,?,?)"
                    data_time=self.cal.get_date()+date_time()
                    conn.execute(sql,(self.id_entry.get(),first,last,self.cb.get(),self.year_entry.get(),self.cb2.get(),data_time,self.phone_entry.get()))
                    conn.commit()
                    tkinter.messagebox.showinfo('Response', 'Thanks\nEnterd correctly')
            except ValueError:
                tkinter.messagebox.showinfo('Response', 'ERROR\n first,last name must be in this format Firstname lastname')

        self.submit = tkinter.Button(self.frame, text='Submit', command=submit).grid(columnspan=14)

        self.checkID_label = tkinter.Label(self.frame2, text='ID:')
        self.checkID_entry = tkinter.Entry(self.frame2, width=23)
        self.checkID_label.grid(column=0, row=1, pady=30)
        self.checkID_entry.grid(column=1, row=1)

        def check():
            if len(str(self.checkID_entry.get()))==10:
                cursor = conn.execute("SELECT ID from Vaccine WHERE ID ="+str(self.checkID_entry.get()))
                number_of_Vaccine=0
                for row in cursor:
                    number_of_Vaccine+=1
                if number_of_Vaccine==0:
                    tkinter.messagebox.showinfo('Response', 'Unvaccinated')
                elif number_of_Vaccine==1:
                    tkinter.messagebox.showinfo('Response', 'Vaccinated')
                else:
                    tkinter.messagebox.showinfo('Response', 'Fully Vaccinated')
            else:
                tkinter.messagebox.showinfo('Response', 'invalid input You must enter 10 numbers as ID')


        self.check = tkinter.Button(self.frame2, text='Check', command=check).grid(columnspan=2)

        def import_():
            name = fd.askopenfilename()
            file= open(name,'r')
            csvreader = csv.reader(file)
            fields = next(csvreader)
            for row in csvreader:
                sql ="INSERT INTO Vaccine(FIRST_name ,LAST_name ,Gender,ID,year_of_birth,vaccine,Date,phone_number) VALUES(?,?,?,?,?,?,?,?)"
                conn.execute(sql,(row))

            cursor = conn.execute("SELECT ID from Vaccine")
            for row in cursor:
                print(row[0])
            conn.commit()
            file.close()
            tkinter.messagebox.showinfo('Response', 'Imported successfully')

        self.importButton = tkinter.Button(self.frame3, text='Import', command=import_).grid(columnspan=1, pady=40)

        def export():
            cursor = conn.execute("SELECT * from Vaccine")
            file_export = fd.askdirectory()

            file = open(file_export+'/test.csv', 'w')
            csvwriter = csv.writer(file)
            csvwriter.writerow(['FIRST_name' ,'LAST_name' ,'Gender','ID','year_of_birth','vaccine','Date','phone_number'])
            for row in cursor:
                phone_number ="'"+row[-1]+"'"
                row =list(row)
                row[-1]=phone_number
                csvwriter.writerow(row)
            tkinter.messagebox.showinfo('Response', 'Exported successfully to test.csv')

        self.export = tkinter.Button(self.frame3, text='Export', command=export).grid(columnspan=2)

        self.frame.pack()
        self.labelframe.pack()
        self.frame2.pack()
        self.labelframe2.pack()
        self.frame3.pack()
        self.labelframe3.pack()

        self.notebook.add(self.labelframe, text='Check in')
        self.notebook.add(self.labelframe2, text='Immunity check')
        self.notebook.add(self.labelframe3, text='Import & Export')

        tkinter.mainloop()

    def grad_date(self):
            self.date.config(text="Selected Date is: " + self.cal.get_date())

gui = gui()
