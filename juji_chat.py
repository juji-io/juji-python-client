import requests
import websocket
import json
import threading
import argparse
from time import sleep

### Define Arguments
parser = argparse.ArgumentParser(description='Juji chat client on Python.')
parser.add_argument('chatbot_url', type=str, help='Chatbot URL')
parser.add_argument('--firstname', type=str, default='Stranger', help='First Name')
parser.add_argument('--email', type=str, help='First Name')
parser.add_argument('--lastname', type=str, help='First Name')


def create_participation(chatbot_url, firstname, email=None, lastname=None):
    r = requests.post(chatbot_url, 
        data={'firstName': firstname})
    r.raise_for_status()
    return r.json()

def init_chat(ws, participation_id):
    ws.send("""
        subscription {{
                chat(input: {{
                    participationId: "{0}"
                }}) {{
                    role
                    text
                    type
                    display{{
                        data{{
                            questions{{
                                heading
                                kind
                            }}
                        }}
                    }}
                }}
            }}""".format(participation_id))

def send_chat_msg(ws, participation_id, user_msg):
    ws.send("""
        mutation {{
                    saveChatMessage(input: {{
                        type: "normal"
                        pid: "{0}"
                        text: "{1}"
                    }}) {{
                        success
                    }}
                }}
        """.format(participation_id, user_msg))


def on_message(ws, message):
    # print(message)
    parsed = json.loads(message)
    if "data" in parsed:
        if "chat" in parsed["data"]:
            chat_data = parsed["data"]["chat"]
            if "role" in chat_data and chat_data["role"] == "rep":
                if chat_data["type"] == "normal":
                    print(chat_data["text"])
                elif chat_data["type"] == "user-joined":
                    print("=== Welcome to Juji Bot ===")


def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":

    args = parser.parse_args()

    chat_info = create_participation(**vars(args))
    print(chat_info)

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(chat_info["websocketUrl"],
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

    conn_timeout = 5
    while not ws.sock.connected and conn_timeout:
        sleep(1)
        conn_timeout -= 1

    init_chat(ws, chat_info["participationId"])

    while ws.sock.connected:
        # ws.send('Hello world %d'%msg_counter)
        sleep(1)
        user_msg = input("")
        send_chat_msg(ws, chat_info["participationId"], user_msg)

