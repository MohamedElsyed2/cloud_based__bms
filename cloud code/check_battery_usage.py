
import time
import threading
import mysql.connector
#*********** setup the sql database ***********#
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="46045",
  database="CBBMS_DB"
)
mycursor = mydb.cursor()
#***********************************************#
mutex = threading.Lock()

def check_battery_being_used_or_not ():
    while True:
       
        timer = 0
        while timer <= 720:       # check battery usage every 720 hour= 30 days (one month).
            sql = "SELECT current FROM modules_current WHERE module_ID = 1 ORDER BY ID DESC LIMIT 1"
            mutex.acquire()
            mycursor.execute(sql)
            data = mycursor.fetchone()
            mutex.release()
            battery_current = data[0]
        
            if battery_current != 0:    # like a watchdog, if battery current is not equal to zero, then the battery is in service.
                
                sql = "INSERT INTO battery_usage (module_ID, value) VALUES (%s, %s)"
                values = (1,1)
                mutex.acquire()
                mycursor.execute(sql , values) # store the measurement value in SQL database
                mydb.commit()  # Commit the transaction
                mutex.release()
                time.sleep(60)
                timer = 0                  # to restart the timer.
            elif battery_current == 0:     # if the battery current still equals to zero then increment the timer and go to the next iteration.
                time.sleep(3600)            # 3600 second = 1 hour.
                timer += 1 
        
        sql = "INSERT INTO battery_usage (module_ID, value) VALUES (%s, %s)"
        values = (1,0)
        mutex.acquire()
        mycursor.execute(sql , values) # store the measurement value in SQL database
        mydb.commit()  # Commit the transaction
        mutex.release()
    
def run():
    print("check battery usage is running")
    check_battery_being_used_or_not()
        
#run()