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

class AdvancedAnalyst(threading.Thread):

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
        print(f"Avanced analyst {self.analyst_name} has started")
        self.addMultipleResolutions()
        print(f"Advanced analyst {self.analyst_name} has finished")

    def addMultipleResolutions(self):
        time_list = []
        time_list2 = []
        time_list3 = []

        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

        for i in range(self.begin, self.begin+self.times):
            acqId = i%100
            if acqId == 0:
                acqId = 100
            
            # Get Acquisition
            acq = self.getAcquisition(acqId)
            time_list.append(acq[0])

            # Get Filename and hash value stored
            filename = acq[1]
            hash_stored = acq[2]

            # Get acquisition file
            self.downloadFileFromRepository(filename)

            # Check hash value
            file_valid = self.checkHashSHA256(filename, hash_stored)

            if file_valid:
                # Get automatic, primary & secondary Analysis
                getAnalysis = self.getAnalysis(acqId)
                time_list2.append(getAnalysis)

                # Analyzing
                if self.DEBUG:
                    print(f"Advanced Analyst-{self.analyst_name} --> Resolving {filename}")
                time.sleep(random.randint(30, 60)) #ANALYZING

                # Add Resolution
                resolution = self.addResolution(i)
                time_list3.append(resolution)

                # Delete local file
                self.deleteLocalFile(filename)
            else:
                self.times = self.times - 1
            
        self.min_get_acq = min(time_list)
        self.avg_get_acq = sum(time_list)/self.times
        self.max_get_acq = max(time_list)

        self.min_get_ana = min(time_list2)
        self.avg_get_ana = sum(time_list2)/self.times
        self.max_get_ana = max(time_list2)

        self.min_add = min(time_list3)
        self.avg_add = sum(time_list3)/self.times
        self.max_add = max(time_list3)


    def getAcquisition(self, acqId):
        start_time = time.time()
        r = requests.get(f"{self.API_ENDPOINT}{self.NS}.Acquisition/{acqId}")
        elapsed_time = time.time() - start_time
        if self.DEBUG:
            print(r.json()['filename'])
        return (elapsed_time, r.json()['filename'], r.json()['hash'])

    def downloadFileFromRepository(self, filename):
        bucket = storage.bucket("hyperledger-jte.appspot.com")

        blob = bucket.get_blob(filename)
        blob.download_to_filename(filename)

    def checkHashSHA256(self, filename, hashStored):
        hashValue = self.sha256(filename)
        return hashValue == hashStored

    def sha256(self, fname):
        hash_sha256 = hashlib.sha256()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def getAnalysis(self, acqId):
        acq_fqi = f"resource%3A{self.NS}.%23{acqId}"
        start_time = time.time()
        r = requests.get(f"{self.API_ENDPOINT}queries/AnalysisByAcquisition?acq_fqi={acq_fqi}")
        elapsed_time = time.time() - start_time
        if self.DEBUG:
            print(f"Indications automatic analysis --> {r.json()[0]['indications']}")
            print(f"Indications primary analyst --> {r.json()[1]['indications']}")
            print(f"Indications secondary analyst --> {r.json()[2]['indications']}")
        return elapsed_time

    def addResolution(self, anaId):
        resource_url = f"{self.API_ENDPOINT}{self.NS}.AddAnalysis"
        acqId = anaId%100
        if acqId == 0:
            acqId = 100
        possibleOptions = ["Everything OK", "Primary OK", "Secondary OK", "Automatic OK", "Primary & Secondary OK", "Primary & Automatic OK", "Secondary & Automatic OK"]
        data = {
            "analysisId": anaId,
            "acqId": acqId,
            "indications": [random.choice(possibleOptions)]
        }
        start_time = time.time()
        r = requests.post(resource_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        elapsed_time = time.time() - start_time
        if self.DEBUG:
            print(f"Elapsed time: {elapsed_time}")
            print(f"Response status code: {r.status_code}")
            print(r.json())
        return elapsed_time
    
    def deleteLocalFile(self, filename):
        if(os.path.exists(filename)):
            os.remove(filename)
        else:
            print(f"File {filename} does not exist")

    def printResults(self):
        print(f"{self.analyst_name} - Fastest acquisition gotten in {self.min_get_acq} seconds")
        print(f"{self.analyst_name} - Slowest acquisition gotten in {self.max_get_acq} seconds")
        print(f"{self.analyst_name} - Average time getting acquisitions: {self.avg_get_acq} seconds")

        print(f"{self.analyst_name} - Fastest analysis couple gotten in {self.min_get_ana} seconds")
        print(f"{self.analyst_name} - Slowest analysis couple gotten in {self.max_get_ana} seconds")
        print(f"{self.analyst_name} - Average time getting analysis couple: {self.avg_get_ana} seconds")

        print(f"{self.analyst_name} - Fastest analysis added in {self.min_add} seconds")
        print(f"{self.analyst_name} - Slowest analysis added in {self.max_add} seconds")
        print(f"{self.analyst_name} - Average time adding analysis: {self.avg_add} seconds")