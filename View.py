
from importlib.resources import path
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib import style

from pyparsing import White, rest_of_line
from setuptools import Command


class View:
    def __init__(self, master):
        self.master = master
        self.master.title("Mini Database managment system")
        self.createnotebook(self.master)
        master.configure(background='lightgray')
        
    def createnotebook(self, master):
        self.master =master       
        notebook = ttk.Notebook(self.master)
        
             
        
        #frame1    
        frame1 = ttk.Frame(notebook, width=600, height=500, relief=RIDGE)
        self.create_conn_widgets(frame1)
        self.create_status_widgets(frame1)  
        frame1.pack(fill='both', expand=True)
        
        notebook.add(frame1, text='DB connection')
       
        #frame2
        frame2 = ttk.Frame(notebook, width=600, height=500)       
        self.create_csv_importer_widgets(frame2)
               
        notebook.add(frame2, text='Import CSV')
        
        #frame3
        frame3 = ttk.Frame(notebook, width=400, height=500)
        self.create_db_queries_widgets(frame3)
        frame3.pack(fill='both', expand=True)
        
        notebook.add(frame3, text='DB Queries')
        
        notebook.pack(pady=10, expand=True)             
        
    def create_conn_widgets(self, master):
        self.master = master
        lablframe = ttk.LabelFrame(self.master, text='Setup new connection', width=400, height=600, relief=RIDGE)
        lablframe.pack(fill='both', expand=True, ipadx=5, pady=5)
        
        ttk.Label(lablframe, text = 'Hostname:').grid(row = 0, column = 0, padx = 5, sticky = 'sw')
        ttk.Label(lablframe, text = 'Port:').grid(row = 0, column = 1, padx = 5, sticky = 'sw')
        ttk.Label(lablframe, text = 'Username:').grid(row = 2, column = 0, padx = 5, sticky = 'sw')
        ttk.Label(lablframe, text = 'Password:').grid(row = 2, column = 1, padx = 5, sticky = 'sw')
        
        self.entry_hostname_textvar = StringVar()    
        self.entry_hostname = ttk.Entry(lablframe, textvariable= self.entry_hostname_textvar, width = 24, font = ('Arial', 10))
        
        self.entry_port = ttk.Entry(lablframe,  width = 24, font = ('Arial', 10))
        
        self.entry_user_textvar = StringVar()
        self.text_username = ttk.Entry(lablframe, textvariable= self.entry_user_textvar, width = 24, font = ('Arial', 10))
        
        self.entry_password_textvar = StringVar()
        self.text_password = ttk.Entry(lablframe, textvariable= self.entry_password_textvar, width = 24, font = ('Arial', 10))
        
        self.entry_hostname.grid(row = 1, column = 0, padx = 5)
        self.entry_port.grid(row = 1, column = 1, padx = 5)
        self.text_username.grid(row = 3, column = 0, padx = 5)
        self.text_password.grid(row = 3, column = 1, padx = 5)
    
        self.button_conn1 = Button(lablframe, text="Connect")
        self.button_conn1.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = 'e')
        print(self.button_conn1.winfo_class())
        self.button_conn1.config(foreground='green')  
        
    def create_status_widgets(self, master):
        self.master = master
    
        lablframe = ttk.LabelFrame(self.master, text='Connection status', width=350, height=240, relief=RIDGE)
        lablframe.pack(ipadx=0, pady=5)
        
        ttk.Label(lablframe, text = 'The database connection instance is').grid(row = 0, column = 0, padx = 5, sticky = 'sw')
        self.status_label = ttk.Label(lablframe, text = 'Stoped', foreground='red')
        self.status_label.grid(row = 1, column = 0, padx = 5, sticky = 'sw')
        
        self.button_stop = Button(lablframe, text="Stop")
        self.button_stop.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'w')
        self.button_stop.config(foreground='red')
        
        self.button_conn = Button(lablframe, text="Connect")
        self.button_conn.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'e')
        self.button_conn.config(foreground='green')
        
        self.button_conn['command'] = lambda: self.make_connection()
        self.button_stop['command'] = lambda: self.stop_connection()
        
    def create_csv_importer_widgets(self, master):
        self.master = master
        #style = ttk.Style(master)
        self.lbel_text = ttk.Label(master, text = "please choose a folder that the CSV files.....blablablablablaaaaa.....blablablablablaaaaa.....blablablablablaaaaa.....blablablablablaaaaa.....", justify= LEFT)
        self.lbel_text.pack( expand=True)
        self.button_open = Button(self.master, text="Open")
        
        self.button_open.config(foreground='blue')     
        self.button_open.pack()#.grid(row=0, column=1, ipadx=5,ipady=5)
        
        #.grid(row = 0, column = 0, padx = 5, sticky = 'sw')
        self.path_label = Label(master, text = '')
        #.grid(row = 0, column = 2, sticky = 'w')
        # Text editor
        self.csv_list_text = Text(master, height=5)
        #.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.button_open['command'] =lambda: self.get_csv_files_path()
               
        self.button_import = Button(self.master, text="Import")
        self.button_import.config(foreground='blue')   
        #self.button_import.pack()#.grid(row=2, column=1, ipadx=5,ipady=5, sticky = 'w')
        
        #self.button_import['command'] = lambda: self.import_csv_to_db()
         
        self.imp_result=Label(master, text = 'CSV files are secsussfully imported to DB.')#.grid(row = 0, column = 0, padx = 5, sticky = 'sw') 
        
        #self.imp_result
    
    def print_quary_result(self):
        selection = 'The selected query is: ' + str(self.qur_selcted.get())
        self.label_q_result.config(text= selection)
        self.label_q_result.pack(fill='x', anchor = W )
        #print('test print')    
        
    def create_db_queries_widgets(self, master):
        self.master = master
        
        self.lablframe1 = ttk.LabelFrame(self.master, text='Select one sql query to execute:', width=420, height=100, relief=RIDGE,padding=5)
        
        # Tuble of quaries
        my_quaries=((1, 'Who has participated most of the competitions.'),
                    (2, 'Show the average age of the person winning a race.'),
                    (3, 'Show who has won the most amount of competitions.'),
                    (4, 'Show the most common boat manfacturor in the competitions placing frist.')
                    )
            
        #make selection list using radio button
        self.qur_selcted = IntVar()
        for quary in my_quaries:

            r = Radiobutton(self.lablframe1, 
                             text=(quary[1]),
                             value=(quary[0]),
                             variable=self.qur_selcted
                             )           
            r.pack(fill='x', anchor = W )
       
        self.lablframe1.pack()

        
        
        #add button
        self.button_excute_q = Button(self.master, text="Excute", padx=5, pady=5, foreground='green', command= lambda: self.print_quary_result())
        #self.button_excute_q[Command] = lambda: print('test print')#lambda: self.print_quary_result() #self.print_quary_result      
        self.button_excute_q.pack(anchor = W,padx=5,pady=5)#grid(column=2, row=2, padx=5,pady=5)
        
        
        self.lablframe2 = ttk.LabelFrame(self.master, text='Query result:', width=420, height=100, relief=RIDGE,padding=5)           
        self.lablframe2.pack()
        
        self.label_q_result = Label(self.lablframe2, text='Quary result..')
        self.label_q_result.pack(fill='x', anchor = E)
        

        
    #some help functions   
    def get_csv_files_path(self):
        _path = fd.askdirectory(title="Choose a drictory that holds the csv files.")
        self.csv_list_text.insert('1.0', _path)
        self.path_label['text'] = _path
        self.button_open.pack_forget()
        return _path        

    def import_csv_to_db(self):
        self.imp_result.pack()
        self.button_import.pack_forget()
        
    def make_connection(self):     
        self.button_conn.grid_remove()
        self.button_stop.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'w')
        self.status_label['text'] = 'connected'
        self.status_label['foreground'] = 'green'
        #print(widget, 'stop', self.status_label['text'])
    
    def stop_connection(self):
        self.button_stop.grid_remove()
        self.button_conn.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'e')
        self.button_conn1.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = 'e')
        self.status_label['text'] = 'stoped'
        self.status_label['foreground'] = 'red'     

    def get_user_data(self):
        return self.entry_user_textvar.get()

    def get_password_data(self):
        return self.entry_password_textvar.get()

    def get_hostname_data(self):
        return self.entry_hostname_textvar.get()
        
#root = Tk()
#root.geometry('500x400')
#myview = View(root)
#root.mainloop()