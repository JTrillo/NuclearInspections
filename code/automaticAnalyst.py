#!/usr/bin/python3

import asyncio
import websockets
import json
import time
import hashlib
import os
import requests
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

#API_ENDPOINT = "http://35.187.19.191:3000/api/" #TESTING NET
#API_ENDPOINT = "http://104.155.2.231:3001/api/" #2 PEERS NET
#WS_ENDPOINT = "ws://104.155.2.231:3000/api/" #2 PEERS NET
API_ENDPOINT = "http://34.76.123.255:3001/api/" #3 ORGS NET
WS_ENDPOINT = "ws://34.76.123.255:3000/api/" #3 ORGS NET
#API_ENDPOINT = "http://35.241.200.124:3001/api/" #5 ORGS NET
#WS_ENDPOINT = "ws://35.241.200.124:3000/api/" #5 ORGS NET
NS = "ertis.uma.nuclear"

# USING EVENTS
async def eventListener(DEBUG=False):
    print("EVENT LISTENER STARTED")
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    async with websockets.connect(WS_ENDPOINT) as websocket:
        with open('results.txt', 'w') as f:
            if DEBUG:
                print("Waiting for new event...")
            cont = 0
            time_list = []
            while cont<100:
                aux = await websocket.recv()
                if DEBUG:
                    print("NEW EVENT")
                aux2 = json.loads(aux)
                eventId = aux2['eventId']
                acqId = aux2['acqId']
                filename = aux2['filename']
                hash_value = aux2['hash']
                if DEBUG:
                    print(f"Event ID: {eventId}")
                    print(f"Acquisition ID: {acqId}")
                    print(f"Filename: {filename}")
                    print(f"Hash value: {hash_value}")
                print(f"Event ID: {eventId}", file=f)
                print(f"Acquisition ID: {acqId}", file=f)
                print(f"Filename: {filename}", file=f)
                print(f"Hash value: {hash_value}", file=f)

                #Waiting a little bit for file upload to repository by acquisitor process
                time.sleep(10)

                #Download file from repository
                downloadFileFromRepository(filename)

                #Compare downloaded file hash value with stored hash value
                if checkHashSHA256(filename, hash_value):
                    if DEBUG:
                        print("Valid hash")

                    #Get file content
                    acqData = getFileContent(filename)

                    #Delete local file
                    deleteLocalFile(filename)

                    #Send transaction
                    elapsed_time = addAutomaticAnalysis(acqId, acqData)
                    time_list.append(elapsed_time)
                    if DEBUG:
                        print(f"Elapsed time adding automatic analysis: {elapsed_time}\r\n")
                    print(f"Elapsed time adding automatic analysis: {elapsed_time}\r\n", file=f)
                else:
                    if DEBUG:
                        print("Not valid hash\r\n")
                cont = cont+1

            minimum = min(time_list)
            min5avg = sum(time_list[0:5])/5
            average = sum(time_list)/len(time_list)
            maximum = max(time_list)
            max5avg = sum(time_list[len(time_list)-5:len(time_list)])/5
            if DEBUG:
                print(f"Fastest automatic analysis: {minimum}")
                print(f"Average 5 fastest: {min5avg}")
                print(f"Average time while executing automatic analysis: {average}")
                print(f"Slowest automatic analysis: {maximum}")
                print(f"Average 5 slowest: {max5avg}")
            print(f"Fastest automatic analysis: {minimum}", file=f)
            print(f"Average 5 fastest: {min5avg}", file=f)
            print(f"Average time while executing automatic analysis: {average}", file=f)
            print(f"Slowest automatic analysis: {maximum}", file=f)
            print(f"Average 5 slowest: {max5avg}", file=f)

# RETRIEVING FILES FROM REPOSITORY
def addMultipleAutomaticAnalysis():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    time_list = []
    for i in range(1, 101):
        filename = "acq"
        if i < 10:
            filename = filename + "00" + str(i) + ".txt"
        elif i < 100:
            filename = filename + "0" + str(i) + ".txt"
        else:
            filename = filename + str(i) + ".txt"

        #Download file from repository
        downloadFileFromRepository(filename)

        #Get file content
        acqData = getFileContent(filename)

        #Delete local file
        deleteLocalFile(filename)

        #Send transaction
        elapsed_time = addAutomaticAnalysis(i, acqData)
        time_list.append(elapsed_time)
        print(f"Elapsed time adding automatic analysis for acquisition {i}: {elapsed_time}")
        time.sleep(2)
    
    print(f"Fastest --> {min(time_list)}")
    print(f"Slowest --> {max(time_list)}")
    print(f"Average --> {sum(time_list)/len(time_list)}")

def downloadFileFromRepository(filename):
    bucket = storage.bucket("hyperledger-jte.appspot.com")

    blob = bucket.get_blob(filename)
    blob.download_to_filename(filename)

def checkHashSHA256(filename, hashStored):
    hashValue = sha256(filename)
    return hashValue == hashStored

def sha256(fname):
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def getFileContent(filename):
    content = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            content.append(int(lines[i]))
    return content

def deleteLocalFile(filename):
    if(os.path.exists(filename)):
        os.remove(filename)
    else:
        print(f"File {filename} does not exist")

def addAutomaticAnalysis(acqId, acqData, DEBUG=False):
    resource_url = f"{API_ENDPOINT}{NS}.AddAutomaticAnalysis"
    data = {
        "analysisId": acqId+200,
        "analysisDate": generateDateTime(),
        "acqId": acqId,
        "acqData": acqData
    }
    start_time = time.time()
    r = requests.post(resource_url, data=data)
    elapsed_time = time.time() - start_time
    if DEBUG:
        print(f"Elapsed time: {elapsed_time}")
        print(f"Response status code: {r.status_code}")
        print(r.json())
    return elapsed_time

def generateDateTime():
    x = str(datetime.datetime.now()).replace(" ", "T")
    x2 = x[:len(x)-3]+"Z"

    return x2

#asyncio.get_event_loop().run_until_complete(eventListener(True))
addMultipleAutomaticAnalysis()