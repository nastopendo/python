import socket
import sys
import uuid
import json

def showMenu():
    print("1 - show todo list")
    print("2 - add new task")
    print("3 - delete task")
    print("4 - show todo list with priority")
    print("0 - exit")

def showTodoList(sock):
    message = str(1) + "|" + str("") # 1-read tasks from Json file
    print('sending {}\n'.format(message))
    sock.send(message.encode())
    data = sock.recv(2000).decode()
    print('received {}\n'.format(data))
    dataJson = json.loads(data)
    for entry in dataJson['tasks']:
        print('ID: ' + entry['ID'] + ' | Priorytet: ' + entry['taskPriority'] + ' | Tresc zadania: ' + entry['taskName'])
    print("")

def addNewTask(sock, taskName, taskPriority):
    uniqueID = (str(uuid.uuid4())[:8])
    message = str(2) + "|" + str(taskPriority) + "|" + uniqueID + "|" + taskName # 2-add new task to Json file
    print('sending {}\n'.format(message))
    sock.sendall(message)
    data = sock.recv(2000).decode()
    print('received {}\n'.format(data))

def deleteTask(sock, deleteID):
    message = str(3) + "|" + str(deleteID)  # 3-delete task
    print('sending {}\n'.format(message))
    sock.sendall(message)
    data = sock.recv(2000).decode()
    print('received {}\n'.format(data))

def showPriorityTodoList(sock, taskPriorityToShow):
    message = str(4) + "|" + str(taskPriorityToShow) # 4-read tasks with priority from Json file
    print('sending {}\n'.format(message))
    sock.send(message.encode())
    data = sock.recv(2000).decode()
    print('received {}\n'.format(data))
    dataJson = json.loads(data)
    for entry in dataJson['tasks']:
        print('ID: ' + entry['ID'] + ' | Priorytet: ' + entry['taskPriority'] + ' | Tresc zadania: ' + entry['taskName'])
    print("")

def exitProgram(sock):
    message = str(0) + "|" + str("")  # 0-client dissconected
    print('sending {}\n'.format(message))
    sock.sendall(message)
    sys.exit()

if __name__ == '__main__':
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)


    try:
        run = True
        while run:
            showMenu()
            num = input("\nYour choice: ")

            if num == 0:
                run = False
                exitProgram(sock)
            elif num == 1:
                showTodoList(sock)
            elif num == 2:
                taskName = input("\nTask name: ")
                taskPriority = input("Set priority number [0-5]: ")
                addNewTask(sock, taskName, taskPriority)
            elif num == 3:
                deleteID = input("\nTask ID to delete: ")
                deleteTask(sock, deleteID)
            elif num == 4:
                taskPriorityToShow = input("\nPriority number to show tasks [0-5]: ")
                showPriorityTodoList(sock, taskPriorityToShow)
            else:
                print("\nNot found. Try again.")

    finally:
        print('closing socket')
        sock.close()