import requests



URL = "http//localhost:8000/mcp"
PAYLOAD = {
    "jsonrpc" : "2.0",
    "method": "tools/list",
    "params": {},
    "id": 1
}

HEADERS = {
    "Content-Type": "application/json",
    "Accept": " application/json, text/event-stream"
}

#server Sent event - Very Important Topic  , which is one way streaming which is stateful 

respone = requests.post(URL, json=PAYLOAD, headers= HEADERS, stream=True)

for line in respone.iter_lines():
    if line:
        print(line.decode('UTF-8'))