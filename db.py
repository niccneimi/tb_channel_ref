import sqlite3,time

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)",(user_id,))
        
    def get_try_free(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT try_free FROM users WHERE user_id = ?",(user_id,)).fetchone()[0]
        
    def edit_try_free(self,user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET try_free = 1 WHERE user_id = ?",(user_id,))        

    def get_inv_url(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT inv_url FROM users WHERE user_id = ?",(user_id,)).fetchone()[0]
        
    def add_inv_url(self,user_id,inv_link):
        with self.connection:
            return self.cursor.execute("UPDATE users SET inv_url = ? WHERE user_id = ?",(inv_link,user_id,))    

    def add_new(self, user_id,username_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO new (username, username_id) VALUES (?,?)",(user_id,username_id,))

    def new_exists(self, username):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM new WHERE username_id = ?", (username,)).fetchall()
            return bool(len(result))
    
    def edit_balance(self,inv_url):
        with self.connection:
            return self.cursor.execute("UPDATE users SET balance = balance + 1 WHERE inv_url = ?",(inv_url,)) 
    
    def get_balance(self,user_id):
        with self.connection:
            return self.cursor.execute("SELECT balance FROM users WHERE user_id = ?",(user_id,)).fetchone()[0]
        
    def edit_money(self,inv_url,count):
        with self.connection:
            return self.cursor.execute("UPDATE users SET money = money + ? WHERE inv_url = ?",(count,inv_url,)) 
    
    def get_money(self,user_id):
        with self.connection:
            return self.cursor.execute("SELECT money FROM users WHERE user_id = ?",(user_id,)).fetchone()[0]
        
    def get_users_count(self):
        with self.connection:
            return len(self.cursor.execute("SELECT * FROM users").fetchall())
        
    def get_all_users(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM users").fetchall()
        
    def add_new_ref_id(self,inv_url,username_id):
        with self.connection:
            ref_id = self.cursor.execute("SELECT user_id FROM users WHERE inv_url = ?",(inv_url,)).fetchone()
            if ref_id != None:
                return self.cursor.execute("UPDATE new SET ref_id = ? WHERE username_id = ?",(ref_id[0],username_id,))
        
    def get_new_by_ref_id(self,user_id):
        with self.connection:
            return self.cursor.execute("SELECT username,username_id FROM new WHERE ref_id = ?",(user_id,)).fetchall()
        
    def edit_change(self,change_new):
        with self.connection:
            return self.cursor.execute("UPDATE change SET change_price = ?",(change_new,))  

    def get_change(self):
        with self.connection:
            return self.cursor.execute("SELECT change_price FROM change").fetchone()[0]  
        
    def fast_ed_money(self, user_id,new_money):
        with self.connection:
            return self.cursor.execute("UPDATE users SET money = ? WHERE user_id = ?",(new_money,user_id,)) 
# print(Database(r'/home/niccneimi/Documents/data/domophone.db').get_new_by_ref_id(718802381))