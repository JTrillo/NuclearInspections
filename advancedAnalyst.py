#!/usr/bin/python3

import threading
import time
import requests
import json
import random

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
        results = self.addMultipleResolutions()
        print(f"Advanced analyst {self.analyst_name} has finished")

    def addMultipleResolutions(self):
        time_list = []
        time_list2 = []
        time_list3 = []

        for i in range(self.begin, self.begin+self.times):
            acqId = i%100
            if acqId == 0:
                acqId = 100
            
            # Get Acquisition
            acq = self.getAcquisition(acqId)
            time_list.append(acq[0])

            # Get primary and secondary Analysis
            getAnalysis = self.getAnalysis(acqId)
            time_list2.append(getAnalysis)

            # Analyzing
            if self.DEBUG:
                print(f"Advanced Analyst-{self.analyst_name} --> Analyzing {acq[1]}")
            time.sleep(random.randint(30, 60)) #ANALYZING


            # Add resolution Analysis
            analysis = self.addAnalysis(i)
            time_list3.append(analysis)
            
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
        return (elapsed_time, r.json()['filename'])
    
    def getAnalysis(self, acqId):
        acq_fqi = f"resource%3A{self.NS}.%23{acqId}"
        start_time = time.time()
        r = requests.get(f"{self.API_ENDPOINT}queries/AnalysisByAcquisition?acq_fqi={acq_fqi}")
        elapsed_time = time.time() - start_time
        if self.DEBUG:
            print(f"Indications primary analyst --> {r.json()[0]['indications']}")
            print(f"Indications secondary analyst --> {r.json()[1]['indications']}")
        return elapsed_time

    # REVISAR A PARTIR DE AQUI
    def addAnalysis(self, anaId):
        resource_url = f"{self.API_ENDPOINT}{self.NS}.AddAnalysis"
        acqId = anaId%100
        if acqId == 0:
            acqId = 100
        possibleOptions = ["Everything is OK", "Primary analysis is OK", "Secondary analysis is OK"]
        data = {
            "analysisId": anaId,
            "method": "MANUAL",
            "acqId": acqId,
            "indications": []
        }
        start_time = time.time()
        r = requests.post(resource_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        elapsed_time = time.time() - start_time
        if self.DEBUG:
            print(f"Elapsed time: {elapsed_time}")
            print(f"Response status code: {r.status_code}")
            print(r.json())
        return elapsed_time

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