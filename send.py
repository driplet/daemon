from websocket import create_connection
import time
import json

content = {
    "credentials": {
        "client_id": "u3992663516",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJvbG9nIiwiZW1haWwiOiJ3aGF0QHRoZS5mdWNrIiwicGFzc3dvcmQiOiIkNiRyb3VuZHM9NjU2MDAwJGFjNmZPNDFHRXgwL2MvdUQkYmZCb2NnQnM5ZDBSYURjdlprZFE2UFpWTzJKcmpIT1dGT2FnSmRtMlNCNDNiOGFHclM3Qmd5SFpJVmJuVEY5V1hyL3VDL25pb3BBcFZmY0J3c0JoVTEiLCJpZCI6InUzOTkyNjYzNTE2IiwidGltZV9jcmVhdGVkIjoxNTUzOTEwNjMzfQ.f_YBbLOreGHf_b0RPvxy6NceT2-zcPciaNAETU7G-cI"
    },
    "payload": "This is a test string"
}

ws = create_connection("ws://localhost:3143/")
while True:
    ws.send(json.dumps(content))
    result =  ws.recv()
    print("Received '%s'" % result)
    time.sleep(0.5)
ws.close()