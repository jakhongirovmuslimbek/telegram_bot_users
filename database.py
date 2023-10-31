import sqlite3

class Database:
    conn = sqlite3.connect("sqlite_bot.db")
    cursor = conn.cursor()

    def create_table_users(self):
        self.cursor.execute("create table if not exists Users (\
                            telegram_id int, \
                            username varchar(150), \
                            name varchar(150), \
                            phone varchar(20), \
                            location text \
                            )")
        
    def select_users(self, telegram_id):
        self.cursor.execute("select * from Users where telegram_id={}".format(telegram_id))
        return self.cursor.fetchone()

    def insert_users(self, telegram_id, username, name, phone, location):
        self.cursor.execute("insert into Users values ({}, '{}', '{}', '{}', '{}')".format(telegram_id, username, name, phone, location))
        self.conn.commit()