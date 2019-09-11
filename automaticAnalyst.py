#!/usr/bin/python3

import asyncio
import websockets
import json
import time
import hashlib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

API_ENDPOINT = "http://104.155.2.231:3000/api/" #2 PEERS NET
WS_ENPOINT = "ws://104.155.2.231:3000/api/" #2 PEERS NET
#API_ENDPOINT = "http://35.241.187.202:3000/api/" #5 PEERS NET
#WS_ENDPOINT = "ws://35.241.187.202:3000/api/" #5 PEERS NET

async def eventListener():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    async with websockets.connect(WS_ENPOINT) as websocket:
        while True:
            aux = await websocket.recv()
            aux2 = json.loads(aux)
            eventId = aux2['eventId']
            acqId = aux2['acqId']
            filename = aux2['filename']
            hash_value = aux2['hash']
            print(f"Event ID: {eventId}")
            print(f"Acquisition ID: {acqId}")
            print(f"Filename: {filename}")
            print(f"Hash value: {hash_value}")

            time.sleep(2)

            #Download file from repository
            downloadFile(filename)

            #Compare downloaded file hash value with stored hash value
            if checkHash(filename, hash_value):
                print("Valid hash")
            else:
                print("Not valid hash")

            #Get file content
            acqData = getContent(filename)

            #Delete local file
            deleteLocalFile(filename)

            #Send transaction
            addAutomaticAnalysis(acqId, acqData)

def downloadFile(filename):
    bucket = storage.bucket("hyperledger-jte.appspot.com")

    blob = bucket.get_blob(filename)
    blob.download_to_filename(filename)

def checkHash(filename, hashStored):
    hashValue = self.sha256(filename)
    return hashValue == hashStored

def sha256(fname):
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def getContent(filename):
    #Change and get content from local file (recently downloaded)
    bucket = storage.bucket("hyperledger-jte.appspot.com")

    blob = bucket.get_blob(filename)
    aux = blob.download_as_string().decode('ascii').split('\r\n')
    content = [int(value) for value in aux]

    return content

def deleteLocalFile(filename):
    if(os.path.exists(filename)):
        os.remove(filename)
    else:
        print(f"File {filename} does not exist")

def addAutomaticAnalysis(acqId, acqData, DEBUG=False):
    resource_url = f"{self.API_ENDPOINT}{self.NS}.AddAutomaticAnalysis"
    data = {
        "analysisId": acqId,
        "method": "MANUAL",
        "acqId": acqId
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

        