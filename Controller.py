from cmath import e
from statistics import mode
from tkinter import *
from tkinter import filedialog as fd
import os
from csv import reader


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model = model
        self.view.button_conn1["command"] = self.crate_db_connection
        self.view.button_conn["command"] = self.crate_db_connection       
        self.view.button_stop["command"] = self.disconnet_db
        self.view.button_open['command'] =lambda: self.display_csv_files()
        self.view.button_import['command'] = lambda: self.import_csv_to_db()
        self.view.button_excute_q['command'] = lambda: self.excute_queries()
     
    def crate_db_connection(self):
        user = self.view.get_user_data()
        passwrd = self.view.get_password_data()
        host = self.view.get_hostname_data()
        self.model.make_connection(user, passwrd, host)
        self.view.button_conn.grid_remove()
        self.view.button_conn1.grid_remove()
        self.view.status_label['text'] = 'connected'
        self.view.status_label['foreground'] = 'green'
        self.view.button_stop.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'w')
        print(self.model.is_db_connection())
        
    def disconnet_db(self):
        self.model.disconnect_db()
        self.view.button_stop.grid_remove()
        self.view.button_conn.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'e')
        self.view.button_conn1.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = 'e')
        self.view.status_label['text'] = 'stoped'
        self.view.status_label['foreground'] = 'red'
        print(self.model.is_db_connection())
        
    def get_all_csv(self, _path):
        self._path = _path
        every_things = os.listdir(_path) 
        return list(filter(lambda each_f: (each_f.endswith('.csv')), every_things))
    
    def display_csv_files(self):
        _path = fd.askdirectory(title="Choose a drictory that holds the csv files")
        for csv_filename in self.get_all_csv(_path): self.view.csv_list_text.insert('1.0', csv_filename + '\n')
        #self.view.csv_list_text.insert('1.0', self.get_all_csv(_path))
        self.view.path_label['text'] = _path
        self.view.path_label.pack(fill='both', ipadx=5, pady=5)
        self.view.csv_list_text.pack(fill='both', expand=True, ipadx=5, pady=5)
        self.view.button_import.pack()
        self.view.button_open.pack_forget()
        
    def import_csv_to_db(self):
        self._path = self.view.path_label['text']
        for file in self.get_all_csv(self._path):
            with open((self._path +'/'+ file), 'r') as read_obj:
                scv_reader = reader(read_obj)
                header = next(scv_reader)
                table_n = file.replace('.csv','')
                self.model.create_table(header, table_n)
                try:
                    while True:
                        self.model.add_to_table(table_n, header, next(scv_reader)) 
                except:
                    print(" -- No more rowns for file {:13} --".format(file))
                    
    def excute_queries(self):
        _varable = self.view.qur_selcted.get()
        if _varable == 1:
            result_o_q = self.model.who_has_participated_most_races()
        elif _varable == 2:
            result_o_q = self.model.avrage_age_of_winner()
        elif _varable == 3:
               result_o_q = self.model.most_wins()         
        elif _varable == 4:    
            result_o_q = self.model.car_color4th_place()          
        else:
            result_o_q = ('Please select one quary to excute..')
            
        self.view.label_q_result.config(text= result_o_q)    
                
        #print(_varable)

