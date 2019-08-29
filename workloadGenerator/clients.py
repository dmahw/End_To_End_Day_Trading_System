import sys
import re
import multiprocessing
import time
import http.client, urllib.parse

class Instruction:
    def __init__(self, transactionNumber, command, username, message):
        self.transactionNumber = transactionNumber
        self.command = command
        self.username = username
        self.message = message

    def print(self):
        print(self.transactionNumber + "," + self.command + "," + self.username + "," + self.message)

def client(que):
    while(1):
        if not que.empty():
            instruction = que.get()
            try:

                if sys.argv[2]:
                    address = str(sys.argv[2])
                else:
                    address = "127.0.0.1"
                if sys.argv[3]:
                    port = int(sys.argv[3])
                else:
                    port = 8080
        

                params = "transactionNumber:" + instruction.transactionNumber + ",command:" + instruction.command + ",username:" + instruction.username + ",message:" + instruction.message

                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                conn = http.client.HTTPConnection(address, port)
                conn.request("POST", "", params.encode(), headers)
                response = conn.getresponse()
                print(response.status, response.reason)
                data = response.read()
                conn.close()
            except Exception as e:
                que.put(instruction)
                print(e)
        else:
            break


def main (argv):
    queueMap = {}
    m = multiprocessing.Manager()
    files = open(argv[1], encoding="utf-8")
    file = [line.rstrip('\n') for line in files]

    files.close()
    count = 0
    
    for line in file:
        match = re.search('\[(.*)\]\s(.*)', line)
        if match:
            transactionNumber = match.group(1)
            secondPart = match.group(2).split(",")
            command = secondPart[0]
            username = secondPart[1].rstrip(" ")
            message = transactionNumber + "," + match.group(2).rstrip(" ")

            instruction = Instruction(transactionNumber, command, username, message)

            if username not in queueMap:
                count = count + 1
                que = m.Queue()
                queueMap[username] = que
            que = queueMap[username]
            que.put(instruction)

        else:
            print("ERROR: INPUT FILE NOT VALID")
            break

    # processes = [multiprocessing.Process(target = client, args = (username, que) ) for username, que in queueMap.items()]

    if __name__ == '__main__':
        queueArray = [que for username, que in queueMap.items()]

        pool = multiprocessing.Pool(processes=300)
        pool.map(client, queueArray)
        # for process in processes:
        #     process.start()

main(sys.argv)