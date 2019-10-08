#!/usr/bin/python3

import threading
import requests

class Cleaner(threading.Thread):

    def __init__(self, threadID, begin, end, API_ENDPOINT, NS, typee):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.begin = begin
        self.end = end
        self.API_ENDPOINT = API_ENDPOINT
        self.NS = NS
        self.type = typee
    
    def run(self):
        if self.type == 1:
            self.cleanAcquisitions()
        elif self.type == 2:
            self.cleanAnalysis()

    def cleanAcquisitions(self):
        for i in range(self.begin, self.end+1):
            resource_url = f"{self.API_ENDPOINT}{self.NS}.Acquisition/{i}"
            r = requests.delete(resource_url)
            if r.status_code == requests.codes.no_content:
                print(f"Acquisition {i} deleted ({self.threadID})")
            else:
                print(f"Error when deleting acquisition {i} ({self.threadID})")

    def cleanAnalysis(self):
        for i in range(self.begin, self.end+1):
            resource_url = f"{self.API_ENDPOINT}{self.NS}.Analysis/{i}"
            r = requests.delete(resource_url)
            if r.status_code == requests.codes.no_content:
                print(f"Analysis {i} deleted ({self.threadID})")
            else:
                print(f"Error when deleting analysis {i} ({self.threadID})")