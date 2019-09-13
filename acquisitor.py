#!/usr/bin/python3

import threading
import time
import requests
import json
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import hashlib
import os

class Acquisitor(threading.Thread):

    def __init__(self, thread_id, acq_name, times, begin, API_ENDPOINT, NS, DEBUG = False):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.acq_name = acq_name
        self.times = times
        self.begin = begin
        self.API_ENDPOINT = API_ENDPOINT
        self.NS = NS
        self.DEBUG = DEBUG

    def run(self):
        print(f"Acquisitor {self.acq_name} has started")
        results = self.addMultipleAcquisitions()
        print(f"Acquisitor {self.acq_name} has finished")

    def addMultipleAcquisitions(self):
        time_list = []

        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

        for i in range(self.begin, self.begin+self.times):
            # Acquiring
            #time.sleep(random.randint(30, 60)) #GETTING DATA

            # Generating file
            filename = self.generateFilename(i)
            acq_data = self.generateFile(filename)

            # Calculating hash sha256
            hash_value = self.sha256(filename)

            # Add Acquisition
            elapsedtime = self.addAcquisition(i, filename, hash_value)
            time_list.append(elapsedtime)

            # Uploading file to repository
            self.uploadFile(filename)

            # Deleting local file
            self.deleteLocalFile(filename)

        self.min = min(time_list)
        self.avg = sum(time_list)/self.times
        self.max = max(time_list)

    def addAcquisition(self, acqId, filename, hash_value):
        resource_url = f"{self.API_ENDPOINT}{self.NS}.AddAcquisition"
        tubeId = acqId%100
        if tubeId == 0:
            tubeId = 100
        data = {
            "acqId": acqId,
            "filename": filename,
            "hash": hash_value,
            "calId": "1",
            "tubeId": tubeId,
        }
        start_time = time.time()
        r = requests.post(resource_url, data=data)
        elapsed_time = time.time() - start_time
        if self.DEBUG:
            print(f"Elapsed time: {elapsed_time}")
            print(f"Response status code: {r.status_code}")
            print(r.json())
        return elapsed_time

    def printResults(self):
        print(f"{self.acq_name} - Fastest acquisition added in {self.min} seconds")
        print(f"{self.acq_name} - Slowest acquisition added in {self.max} seconds")
        print(f"{self.acq_name} - Average time adding acquisitions: {self.avg} seconds")

    def generateFilename(self, acqId):
        if acqId < 10:
            aux = "00" + str(acqId)
        elif acqId < 100:
            aux = "0" + str(acqId)
        else:
            aux = str(acqId)
        
        return f"acq{aux}.txt"

    def generateFile(self, filename):
        start_time = time.time()
        f = open(filename, "w")

        content = []
        n = 100000
        for i in range(0, n):
            aux = random.randint(-5000, 5000)
            content.append(aux)
            if i == n-1:
                f.write(str(aux))
            else:
                f.write(str(aux) + "\n")

        f.close()
        elapsed_time = time.time() - start_time
        if self.DEBUG:
            print(f"Elapsed time generating file: {elapsed_time}")

    def uploadFile(self, filename):
        bucket = storage.bucket("hyperledger-jte.appspot.com")

        tfm = bucket.blob(filename)
        tfm.upload_from_filename(filename)

    def sha256(self, filename):
        hash_sha256 = hashlib.sha256()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def deleteLocalFile(self, filename):
        if(os.path.exists(filename)):
            os.remove(filename)
        else:
            print(f"File {filename} does not exist")