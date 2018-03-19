import json
import os.path
import sys

arguments = sys.argv

if len(arguments) < 2:
    print("Path wasn't specified. ")
else:
    path = sys.argv[1]
    if os.path.exists(path):
        try:
            data = json.load(open(path))
            tab = data["input_list"]
            print("Before sorting: " + str(tab))
            for i in range(len(tab)):
                j = len(tab) - 1
                while j > i:
                    if tab[j] < tab[j - 1]:
                        tmp = tab[j]
                        tab[j] = tab[j - 1]
                        tab[j - 1] = tmp
                    j -= 1
            print("After: " + str(tab))
        except ValueError:
            print("Decoding provided .json file failed.")
    else:
        print("Path doesn't exist.")