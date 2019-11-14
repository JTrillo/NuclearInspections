#!/usr/bin/python3

import time
import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import hashlib
import os
import datetime

class AutomaticAnalyst():

    def __init__(self, times, begin, API_ENDPOINT, NS, DEBUG = False):
        self.times = times
        self.begin = begin
        self.API_ENDPOINT = API_ENDPOINT
        self.NS = NS
        self.DEBUG = DEBUG

        self.addMultipleAutomaticAnalysis()

    def addMultipleAutomaticAnalysis(self):
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

        time_list = []
        for i in range(self.begin, self.begin+self.times):
            filename = "acq"
            if i < 10:
                filename = filename + "000" + str(i) + ".txt"
            elif i < 100:
                filename = filename + "00" + str(i) + ".txt"
            elif i < 1000:
                filename = filename + "0" + str(i) + ".txt"
            else:
                filename = filename + str(i) + ".txt"

            #Download file from repository
            self.downloadFileFromRepository(filename)

            #Get file content
            acqData = self.getFileContent(filename)

            #Send transaction
            elapsed_time = self.addAutomaticAnalysis(i, acqData)
            if elapsed_time != -1:
                time_list.append(elapsed_time)
                print(f"Analysis {i} added. Elapsed time --> {elapsed_time}")

            #Delete local file
            self.deleteLocalFile(filename)
    
        time_list.sort()
        self.min = min(time_list)
        self.min5avg = sum(time_list[0:5])/5
        self.avg = sum(time_list)/len(time_list)
        self.max = max(time_list)
        self.max5avg = sum(time_list[len(time_list)-5:len(time_list)])/5

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

    def getFileContent(self, filename):
        content = []
        with open(filename, 'r') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                content.append(int(lines[i]))
        return content

    def deleteLocalFile(self, filename):
        if(os.path.exists(filename)):
            os.remove(filename)
        else:
            print(f"File {filename} does not exist")

    def addAutomaticAnalysis(self, analysisId, acqData, DEBUG=False):
        resource_url = f"{self.API_ENDPOINT}{self.NS}.AddAutomaticAnalysis"
        acqId = analysisId % self.times
        if acqId == 0:
            acqId = self.times
        data = {
            "analysisId": analysisId,
            "analysisDate": self.generateDateTime(),
            "acqId": acqId,
            "acqData": acqData
        }
        try:
            start_time = time.time()
            r = requests.post(resource_url, data=data)
            elapsed_time = time.time() - start_time
        except:
            print(f"Error when trying to add analysis {analysisId}")
            elapsed_time = -1
        if DEBUG:
            print(f"Elapsed time: {elapsed_time}")
            print(f"Response status code: {r.status_code}")
            print(r.json())
        return elapsed_time

    def generateDateTime(self):
        x = str(datetime.datetime.now()).replace(" ", "T")
        x2 = x[:len(x)-3]+"Z"
        return x2