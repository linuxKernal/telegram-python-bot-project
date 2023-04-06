import requests

base_url = r"http://api.telegram.org/bot6015155943:AAFIy762-g2ZhmWzyUug_xTXkSOmL45aklo"

def send_msg(uid,msg):
    parameters = {
      "chat_id" : uid,
      "text" : msg
    }
    resp = requests.get(base_url + "/sendMessage", params=parameters)
    print(resp.text)

users = [ ]

students = ["ram","Guru","santhosh","Vignesh","Marees Kannan"]

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
     if ID in users:
        if(text=="exit"):
            send_msg(ID, "ok sir")
            users.remove(ID)
            index = 0
        elif(text!="RED" and index==0):
            send_msg(ID, "Worng Code")
            users.remove(ID)
        elif index == len(students):
            send_msg(ID, "Thanks")
            users.remove(ID)
            index = 0
        else:
            send_msg(ID, students[index])
            index+=1
     elif(text=="hi"):
        send_msg(ID, "Hello")
     elif(text=="false"):
        send_msg(ID, "Upload Success")
     elif text=="atte":
        send_msg(ID,"Secret Code")
        users.append(ID)
     else:
        send_msg(ID, "Try again")   

     if data["result"]:
       return data["result"][-1]["update_id"] + 1

offset = 0

while True:
  offset = read_msg(offset)