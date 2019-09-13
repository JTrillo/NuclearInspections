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

class Analyst(threading.Thread):

    def __init__(self, thread_id, analyst_name, times, begin, API_ENDPOINT, NS, DEBUG = False):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.analyst_name = analyst_name
        self.times = times
        self.begin = begin
        self.API_ENDPOINT = API_ENDPOINT
        self.NS = NS
        self.DEBUG = DEBUG

    def run(self):
        print(f"Analyst {self.analyst_name} has started")
        results = self.addMultipleAnalysis()
        print(f"Analyst {self.analyst_name} has finished")

    def addMultipleAnalysis(self):
        time_list = []
        time_list2 = []
        for i in range(self.begin, self.begin+self.times):
            acqId = i%100
            if acqId == 0:
                acqId = 100
            
            # Get Acquisition
            acq = self.getAcquisition(acqId)
            time_list.append(acq[0])

            # Get acquisition file
            self.downloadFile(acq[1])

            # Check hash value
            file_valid = self.checkHash(acq[1], acq[2])

            # Get tube info
            tube_length = self.getTube(acq[3])

            # Analyzing
            if self.DEBUG:
                print(f"Analyst-{self.analyst_name} --> Analyzing {acq[1]}")
            time.sleep(random.randint(30, 60)) #ANALYZING

            # Add Analysis
            analysis = self.addAnalysis(i, tube_length)
            time_list2.append(analysis)

            # Delete local file
            self.deleteLocalFile(filename)
            
        self.min_get = min(time_list)
        self.avg_get = sum(time_list)/self.times
        self.max_get = max(time_list)

        self.min_add = min(time_list2)
        self.avg_add = sum(time_list2)/self.times
        self.max_add = max(time_list2)


    def getAcquisition(self, acqId):
        start_time = time.time()
        r = requests.get(f"{self.API_ENDPOINT}{self.NS}.Acquisition/{acqId}")
        elapsed_time = time.time() - start_time
        if self.DEBUG:
            print(r.json()['filename'])
        return (elapsed_time, r.json()['filename'], r.json()['hash'], r.json()['tube'])

    def getTube(self, tubeId):
        #start_time = time.time()
        r = requests.get(f"{self.API_ENDPOINT}{self.NS}.Tube/{tubeId}")
        #elapsed_time = time.time() - start_time
        tubeData = r.json()
        return tubeData['length']

    def addAnalysis(self, anaId, tubePosX, tubePosY):
        resource_url = f"{self.API_ENDPOINT}{self.NS}.AddAnalysis"
        acqId = anaId%100
        if acqId == 0:
            acqId = 100
        data = {
            "analysisId": anaId,
            "acqId": acqId,
            "indications": self.generateIndications(tubePosX, tubePosY)
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
        print(f"{self.analyst_name} - Fastest acquisition gotten in {self.min_get} seconds")
        print(f"{self.analyst_name} - Slowest acquisition gotten in {self.max_get} seconds")
        print(f"{self.analyst_name} - Average time getting acquisitions: {self.avg_get} seconds")

        print(f"{self.analyst_name} - Fastest analysis added in {self.min_add} seconds")
        print(f"{self.analyst_name} - Slowest analysis added in {self.max_add} seconds")
        print(f"{self.analyst_name} - Average time adding analysis: {self.avg_add} seconds")

    def downloadFile(self, filename):
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

        bucket = storage.bucket("hyperledger-jte.appspot.com")

        blob = bucket.get_blob(filename)
        blob.download_to_filename(filename)

    def checkHash(self, filename, hashStored):
        hashValue = self.sha256(filename)
        return hashValue == hashStored

    def sha256(self, fname):
        hash_sha256 = hashlib.sha256()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def generateIndications(self, tubeLength):
        n_ind = random.randint(0, 4)

        indications = []
        for i in range(n_ind):
            indication = "Detected "
            ind_type = random.randint(0, 2)
            if ind_type == 0:
                indication += "fissure" # Grieta
            elif ind_type == 1:
                indication += "break" # Rotura
            elif ind_type == 2:
                indication += "dent" # Abolladura

            # Random position
            pos = random.random() * tubeLength

            indication += f", position {pos}"

            # Add indication
            indications.append(indication)

        return indications
    
    def deleteLocalFile(self, filename):
        if(os.path.exists(filename)):
            os.remove(filename)
        else:
            print(f"File {filename} does not exist")