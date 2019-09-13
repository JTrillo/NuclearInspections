#!/usr/bin/python3

import asyncio
import websockets
import json
import time
import hashlib
import os
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

API_ENDPOINT = "http://104.155.2.231:3001/api/" #2 PEERS NET
WS_ENPOINT = "ws://104.155.2.231:3001/api/" #2 PEERS NET
#API_ENDPOINT = "http://35.241.187.202:3001/api/" #5 PEERS NET
#WS_ENDPOINT = "ws://35.241.187.202:3001/api/" #5 PEERS NET
NS = "ertis.uma.nuclear"

async def eventListener():
    print("Event listener started...\r\n")
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    async with websockets.connect(WS_ENPOINT) as websocket:
        while True:
            aux = await websocket.recv()
            print("NEW EVENT")
            aux2 = json.loads(aux)
            eventId = aux2['eventId']
            acqId = aux2['acqId']
            filename = aux2['filename']
            hash_value = aux2['hash']
            print(f"Event ID: {eventId}")
            print(f"Acquisition ID: {acqId}")
            print(f"Filename: {filename}")
            print(f"Hash value: {hash_value}")

            #Waiting a little bit for file upload to repository by acquisitor process
            time.sleep(10)

            #Download file from repository
            downloadFile(filename)

            #Compare downloaded file hash value with stored hash value
            if checkHash(filename, hash_value):
                print("Valid hash")
            else:
                print("Not valid hash")

            #Get file content
            acqData = getFileContent(filename)

            #Delete local file
            deleteLocalFile(filename)

            #Send transaction
            elapsed_time = addAutomaticAnalysis(acqId, acqData)
            print(f"Elapsed time adding automatic analysis: {elapsed_time}\r\n")

def downloadFile(filename):
    bucket = storage.bucket("hyperledger-jte.appspot.com")

    blob = bucket.get_blob(filename)
    blob.download_to_filename(filename)

def checkHash(filename, hashStored):
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
        "analysisId": acqId,
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

asyncio.get_event_loop().run_until_complete(eventListener())