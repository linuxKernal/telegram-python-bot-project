import requests
from openpyxl import Workbook ,load_workbook
import sqlite3
from json import loads
con = sqlite3.connect("simple.db")
cur = con.cursor()


base_url = r"http://api.telegram.org/bot6015155943:AAFIy762-g2ZhmWzyUug_xTXkSOmL45aklo"

key = "6015155943:AAFIy762-g2ZhmWzyUug_xTXkSOmL45aklo"


def send_msg(uid,msg):
    parameters = {
      "chat_id" : uid,
      "text" : msg
    }
    resp = requests.get(base_url + "/sendMessage", params=parameters)
    print(resp.text)

def fetchStudent(subject):
    res = cur.execute(f"select * from master where subjectcode='{subject}'").fetchone()
    tableName = res[2]
    batch = res[1]
    students = ""
    if batch=="all":
        students = cur.execute(f"select * from {tableName}").fetchall()
    else:
        students = cur.execute(f"select * from {tableName} where batch='{batch}'").fetchall()
    print(students)
    return students

def fetchStudentData(tabName):
    book = load_workbook(f"static/{tabName}.xlsx") 
    sheet = book.active 

    def studentSubCodeAndBatchType():
        course = []
        for i in range(3,sheet.max_column+1):
            subjectcode  =  sheet.cell(row = 1, column = i).value
            student  =  sheet.cell(row = 2, column = i).value
            course.append({"ID":subjectcode,"Type":student})
        return course

    def storeStudentSqlite():
        batch = 1
        for i in range(2,sheet.max_row+1):
            regno =  sheet.cell(row = i, column = 1).value
            name  =  sheet.cell(row = i, column = 2).value
            if(not regno or  not name):
                batch = 2
                continue
            cur.execute(f"INSERT INTO {yearName} VALUES('{regno}','{name}','{batch}');")

    def storeTableMetaData(course):
        for i in course:
            ID = i['ID']
            Type = i['Type']
            cur.execute(f"insert into master values('{ID}','{Type}','{yearName}')")

    storeStudentSqlite()

    course = studentSubCodeAndBatchType()

    storeTableMetaData(course)




def receiveImage(uid,dict1):
    
    if(dict1["message"].get("document","NULL")!="NULL"):
        FILE_URL = dict1["message"]["document"]
    else:
        FILE_URL = dict1["message"]["photo"][2] 

    url = requests.get('https://api.telegram.org/bot'+str(key)+"/getFile?file_id="+str(FILE_URL['file_id']))
    path = loads(url.content)["result"]["file_path"]
    img = requests.get('https://api.telegram.org/file/bot'+str(key)+'/'+path)

    with open(f"static/{dict1['message']['caption']}.xlsx","wb") as file:
        file.write(img.content) 

users = [ ]

students = ["ram","peter","england","john wick","iron man"]

index = 0

def read_msg(offset):
  global index  
  parameters = {
      "offset" : offset
  }

  resp = requests.get(base_url + "/getUpdates", params= parameters)
  data = resp.json()

  print(data)


  for result in data["result"]:
     ID = result["message"]["chat"]["id"]
     text = result["message"].get("text","false").lower()
     
     print(ID,text)
     if ID in users:
        if text=="false":
            send_msg(ID, "Processing file...")
            receiveImage(ID, result)
            users.remove(ID)
            send_msg(ID, "processing done")
     elif(text=="hi"):
        send_msg(ID, "Hello")
     elif text == "upload":
        send_msg(ID, "send the Excel File and give named caption")
        users.append(ID)
     elif text.split()[0]== "get":
        subjectCode = text.split()[1].upper()
        print("Query: ",subjectCode)
        send_msg(ID,fetchStudent(subjectCode))
     else:
        send_msg(ID, "Try again")   

     if data["result"]:
       return data["result"][-1]["update_id"] + 1

offset = 0

while True:
  offset = read_msg(offset)