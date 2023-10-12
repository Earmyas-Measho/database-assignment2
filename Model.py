import mysql.connector
from csv import reader
from datetime import date

class Model:
    def __init__(self):
        self.cnn = mysql.connector.connect(
            user='root', 
            password='',
            host='localhost'
            )
        self.n_cursor = self.cnn.cursor()
        self.n_cursor.execute("CREATE DATABASE IF NOT EXISTS Speed_Comp")
        self.n_cursor.execute("USE Speed_Comp")          
        #self.new_cursor.execute("USE Speed_Comp")
        
    def make_connection(self, user, passwrd, host):
        self.user = user
        self.passwrd = passwrd
        self.host = host
        self.cnn = mysql.connector.connect(user=user, password=passwrd,
                            host=host)
        
        print(self.cnn)
        return self.cnn 
    
    def is_db_connection(self):
        return self.cnn.is_connected()
    
    def new_cursor(self):
        return self.cnn.cursor()
    
    def disconnect_db(self):
        return self.cnn.close()
    
    def create_table(self, title, tablename):
        self.title = title
        self.tablename = tablename
        colums = ""
        for name in title:
            colums += ("%s varchar(255)," % name)

        colums = colums[:-1]

        self.sql_q = (
            """CREATE TABLE IF NOT EXISTS %s (%s);"""
            ) % (tablename,colums)
        self.n_cursor.execute(self.sql_q)
        
    def add_to_table(self,table_n, column, value):
        self.table_n = table_n
        self.column = column
        self.value = value
        self.column = str(column).replace("[", "").replace("]", "").replace("'", "")
        self.value = str(self.value).replace("[", "").replace("]", "")
        self.sql_q_add = ("""INSERT INTO %s (%s) VALUES (%s);""") % (table_n, self.column, self.value)
        self.n_cursor.execute(self.sql_q_add)
        self.cnn.commit()
        
    # qualy
    def who_has_participated_most_races(self):
        self.n_cursor.execute(
            """SELECT t2.name, COUNT(t1.player_id) AS totalnumber FROM record t1 INNER JOIN attaindant t2 ON t1.player_id = t2.player_id  GROUP BY t1.player_id  ORDER BY totalnumber DESC LIMIT 1;""")
        
        
        who_and_ammount = self.n_cursor.fetchone()
       
        result_q = ("{} has participated in the most races a total of {}".format( who_and_ammount[0], who_and_ammount[1]))       
        return result_q

    def youngest_person(self):
        self.n_cursor.execute(
            """SELECT t1. computation, t2.name FROM record t1 INNER JOIN attaindant t2 ON t1.player_id = t2.player_id HAVING t1.computation = 'sailing' ORDER BY min(t2.age)"""
            )
        result_youngest = self.n_cursor.fetchone() # - Since limit is 1 anyway no need to "fetch all"
        result_age = "The youngest person whom partspated in {} race is {}.".format(result_youngest[0], result_youngest[1])
        return result_age

    def most_wins(self):
        self.n_cursor.execute(
            """SELECT t2.name, COUNT(t1.player_id) AS Total FROM record t1 INNER JOIN attaindant t2 ON t2.player_id = t1.player_id WHERE result=1 GROUP BY t2.name ORDER BY Total DESC LIMIT 1;"""
            )
        most_wins = self.n_cursor.fetchone() # - Since limit is 1 anyway no need to "fetch all"
        q_result = "{} has won the most amount of races with a total of {} victories!".format(most_wins[0], most_wins[1])
        return q_result   
    
    def common_boat_type_by_country_made_that_participated_most_races(self):
        self.n_cursor.execute(
            """SELECT t2.made_in, COUNT(t2.c_id) AS numberOfboats FROM record t1 LEFT JOIN boat t2 ON t1.c_id = t2.c_id GROUP BY t2.made_in ORDER BY numberOfboats DESC LIMIT 1;"""
            )
        result_man = self.n_cursor.fetchone()
        boat_manf = str(result_man[0]).capitalize()
        col = result_man[1]
        result_boat_color = "{} is the most common boatt manfacturor of all boats placing {}.".format(boat_manf, col)
        return result_boat_color
    
    def boat_300hp(self):
        

        self.n_cursor.execute(
            """CREATE OR REPLACE VIEW more_than_300HP_boats AS select c_id, made_in FROM boat where hours_power > 300;"""
            )
        tm = self.n_cursor.fetchone()

        self.n_cursor.execute(
            """SELECT t2.made_in, t2.hours_power FROM record t1 INNER JOIN boat t2 On t1.c_id = t2.c_id GROUP BY t1.result ORDER BY t1.result limit 1;"""
            ) 
        result_boat300 = self.n_cursor.fetchone()
        result = "{} is a boat manufacturers country with {}hp that achive better result among those all with 300hp or more.".format(result_boat300[0], result_boat300[1])        
                
        return result


