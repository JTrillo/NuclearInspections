#!/usr/bin/python3

import threading
import time
import requests
import json
import random

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
        for i in range(self.begin, self.begin+self.times):
            # Acquiring
            time.sleep(random.randint(30, 60)) #GETTING DATA

            # Add Acquisition
            elapsedtime = self.addAcquisition(i)
            time_list.append(elapsedtime)

        self.min = min(time_list)
        self.avg = sum(time_list)/self.times
        self.max = max(time_list)

    def addAcquisition(self, acqId):
        resource_url = f"{self.API_ENDPOINT}{self.NS}.AddAcquisition"
        tubeId = acqId%100
        if tubeId == 0:
            tubeId = 100
        data = {
            "acqId": acqId,
            "filename": f"acq{acqId}.raw",
            "hash": "1234567890ABCDEF",
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