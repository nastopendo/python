import socket
import json

def sendTodoList(connection):
    data = open("tasks.json").read().encode()
    print('sending Json file to the client')
    print(data)
    connection.send(data)


def addNewTaskToList(connection, oldData):
    data = json.loads(open("tasks.json").read())
    data['tasks'].append({
        'ID': str(oldData[2]),
        'taskPriority': str(oldData[1]),
        'taskName': str(oldData[3])
    })
    with open('tasks.json', 'w') as jsonFile:
        json.dump(data, jsonFile)
    info = "\nNew task added successfully"
    connection.send(info)

def deleteTaskFromList(connection, param):
    allTasks = json.loads(open("tasks.json").read())
    for i in range(len(allTasks["tasks"])):
        if allTasks["tasks"][i]["ID"] == str(param):
            allTasks["tasks"].pop(i)
            break
    with open('tasks.json', 'w') as jsonFile:
        json.dump(allTasks, jsonFile)
    info = "\nTask deleted successfully"
    connection.send(info)

def sendPriorityTodoList(connection, param):
    allTasks = json.loads(open("tasks.json").read())
    priorityTasks = {}
    priorityTasks["tasks"] = []
    for i in range(len(allTasks["tasks"])):
        if allTasks["tasks"][i]["taskPriority"] == str(param):
            priorityTasks["tasks"].append(allTasks["tasks"][i])
    print('sending Json file to the client')
    priorityTasks = json.dumps(priorityTasks)
    print(priorityTasks)
    connection.send(str(priorityTasks).encode())

def clientDisconnected():
    print('Client disconnect server')


if __name__ == '__main__':

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)
            while True:
                data = connection.recv(2000).decode()
                print('Received {}'.format(data))
                data = str(data).split("|")
                if data[0] == '1':
                    sendTodoList(connection)
                elif data[0] == '2':
                    addNewTaskToList(connection, data)
                elif data[0] == '3':
                    deleteTaskFromList(connection, data[1])
                elif data[0] == '4':
                    sendPriorityTodoList(connection, data[1])
                elif data[0] == '0':
                    clientDisconnected()
                else:
                    break

        finally:
            # Clean up the connection
            connection.close()