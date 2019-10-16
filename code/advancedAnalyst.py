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
import datetime

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
        if self.analyst_name == 'Advanced Analyst-0':
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.initialize_app(cred, name=self.analyst_name)

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
                time.sleep(random.randint(5, 10)) #ANALYZING

                # Add Resolution
                resolution = self.addResolution(i)
                time_list3.append(resolution)

                # Delete local file
                self.deleteLocalFile(filename)
            else:
                print(f"HASH NOT VALID {filename}")
        
        time_list.sort()
        self.min_get_acq = min(time_list)
        self.min5avg_get_acq = sum(time_list[0:5])/5
        self.avg_get_acq = sum(time_list)/self.times
        self.max_get_acq = max(time_list)
        self.max5avg_get_acq = sum(time_list[len(time_list)-5:len(time_list)])/5

        time_list2.sort()
        self.min_get_ana = min(time_list2)
        self.min5avg_get_ana = sum(time_list2[0:5])/5
        self.avg_get_ana = sum(time_list2)/self.times
        self.max_get_ana = max(time_list2)
        self.max5avg_get_ana = sum(time_list2[len(time_list2)-5:len(time_list2)])/5

        time_list3.sort()
        self.min_add = min(time_list3)
        self.min5avg_add = sum(time_list3[0:5])/5
        self.avg_add = sum(time_list3)/self.times
        self.max_add = max(time_list3)
        self.max5avg_add = sum(time_list3[len(time_list3)-5:len(time_list3)])/5


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
        acq_fqi = f"resource%3A{self.NS}.Acquisition%23{acqId}"
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
            "analysisDate": self.generateDateTime(),
            "acqId": acqId,
            "indications": [random.choice(possibleOptions), ""]
        }
        start_time = time.time()
        r = requests.post(resource_url, data=data)
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
        print(f"{self.analyst_name} - Avg. 5 fastest acqs gotten: {self.min5avg_get_acq} seconds")
        print(f"{self.analyst_name} - Slowest acquisition gotten in {self.max_get_acq} seconds")
        print(f"{self.analyst_name} - Avg. 5 slowest acqs gotten: {self.max5avg_get_acq} seconds")
        print(f"{self.analyst_name} - Average time getting acquisitions: {self.avg_get_acq} seconds")

        print(f"{self.analyst_name} - Fastest analyses gotten in {self.min_get_ana} seconds")
        print(f"{self.analyst_name} - Avg. 5 fastest analyses gotten: {self.min5avg_get_ana} seconds")
        print(f"{self.analyst_name} - Slowest analyses gotten in {self.max_get_ana} seconds")
        print(f"{self.analyst_name} - Avg. 5 slowest analyses gotten: {self.max5avg_get_ana} seconds")
        print(f"{self.analyst_name} - Average time getting analyses: {self.avg_get_ana} seconds")

        print(f"{self.analyst_name} - Fastest analysis added in {self.min_add} seconds")
        print(f"{self.analyst_name} - Avg. 5 fastest analysis added: {self.min5avg_add} seconds")
        print(f"{self.analyst_name} - Slowest analysis added in {self.max_add} seconds")
        print(f"{self.analyst_name} - Avg. 5 slowest analysis added: {self.max5avg_add} seconds")
        print(f"{self.analyst_name} - Average time adding analysis: {self.avg_add} seconds")

    def generateDateTime(self):
        x = str(datetime.datetime.now()).replace(" ", "T")
        x2 = x[:len(x)-3]+"Z"

        return x2