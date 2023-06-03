import requests
url = "http://backend:8081/log"
myobj = {'unix_ts': 12323, 'user_id': 1234, 'event_name': 'login' }
event = 1
while True:
    if event == 1:
        event_name = 'login'
        event = 0
    else:
        event_name = 'logout'
        event = 1
    myobj = {'unix_ts': 12323, 'user_id': 1234, 'event_name': event_name }
    x = requests.post(url, json = myobj)
    print(x)