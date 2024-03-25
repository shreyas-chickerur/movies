import psycopg2,traceback
class db: 
    def __init__(self,host,database):
        user = 'cs407'
        password = 'boilerzone'
        self.host = host
        self.database = database
        self.con = psycopg2.connect(host=self.host, dbname=self.database, user=user, password=password,port=5432)
        self.cur = self.con.cursor()
    
    def getCon(self):
        return self.con()

    def getTables(self):
        self.cur.execute("select * from resources;")
        return self.cur.fetchall()
    
    def fetchAll(self,command):
        self.cur.execute(command)
        return self.cur.fetchall()

    def fetchOne(self,command):
        self.cur.execute(command)
        return self.cur.fetchone()

    def executeCommand(self,command):
        try:
            #print(command)
            self.cur.execute(command)
            self.con.commit()
            return True
        except Exception as e:
            #print("E:",e)
            ##print(traceback.print_stack())
            self.con.rollback()
            return False
    

    def getuser_id(self,username):
        self.cur.execute("select user_id from client where username = '{0}'".format(username))
        user_id = self.cur.fetchone()
        user_id = user_id[0]
        return user_id