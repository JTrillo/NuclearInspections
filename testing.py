#!/usr/bin/python3

import threading
import requests
import json
import random
import plotly
import plotly.graph_objs as go
from acquisitor import *
from analyst import *
from cleaner import *

#API_ENDPOINT = "http://104.155.2.231:3000/api/" #2 PEERS NET
API_ENDPOINT = "http://35.195.161.115:3000/api/" #3 PEERS NET
#API_ENDPOINT = "http://35.241.187.202:3000/api/" #5 PEERS NET
NS = "ertis.uma.nuclear"

#RUN SERVER WITH CARD ADMIN BEFORE EXECUTE THIS FUNCTION
def cleanMultithreading(num_threads, acq, ana, begin=-1, totalDeletes=100):
    threads_acq = []
    threads_ana = []

    if acq == True:
        if begin == -1:
            # Get total number of acquisitions
            resource_url = f"{API_ENDPOINT}{NS}.Acquisitions"
            r = requests.get(resource_url)
            total = len(r.json())
            deletes_per_thread = int(total / num_threads)

            # Create threads
            for i in range(num_threads):
                thread = Cleaner(f"Thread-{i}", 1+deletes_per_thread*i, deletes_per_thread*(i+1), API_ENDPOINT, NS, 1)
                threads_acq.append(thread)
        else:
            deletes_per_thread = int(totalDeletes / num_threads)

            # Create threads
            for i in range(num_threads):
                thread = Cleaner(f"Thread-{i}", begin+deletes_per_thread*i, begin+deletes_per_thread*(i+1)-1, API_ENDPOINT, NS, 1)
                threads_acq.append(thread)

        # Start threads
        for i in range(num_threads):
            threads_acq[i].start()
            
        # Join threads
        for i in range(num_threads):
            threads_acq[i].join()

    if ana == True:
        if begin == -1:
            # Get total number of analysis
            resource_url = f"{API_ENDPOINT}{NS}.Analysis"
            r = requests.get(resource_url)
            total = len(r.json())
            deletes_per_thread = int(total / num_threads)

            # Create threads
            for i in range(num_threads):
                thread = Cleaner(f"Thread-{i}", 1+deletes_per_thread*i, deletes_per_thread*(i+1), API_ENDPOINT, NS, 2)
                threads_ana.append(thread)
        else:
            deletes_per_thread = int(totalDeletes / num_threads)

            # Create threads
            for i in range(num_threads):
                thread = Cleaner(f"Thread-{i}", begin+deletes_per_thread*i, begin+deletes_per_thread*(i+1)-1, API_ENDPOINT, NS, 2)
                threads_ana.append(thread)

        # Start threads
        for i in range(num_threads):
            threads_ana[i].start()
            
        # Join threads
        for i in range(num_threads):
            threads_ana[i].join()

def addTubes(n_tubes):
    resource_url = f"{API_ENDPOINT}{NS}.RegisterTube"
    for i in range(n_tubes):
        data = {
            "tubeId": i,
            "posX": random.randint(0, 100),
            "posY": random.randint(0, 100),
            "length": random.randint(5, 20)
        }
        r = requests.post(resource_url, data=data)
        if r.status_code == requests.codes.ok:
            print(f"Added tube {i}")
        else:
            print(f"Error when adding tube {i}")

def workAndCalibration():
    #Create work 1
    resource_url = f"{API_ENDPOINT}{NS}.CreateWork"
    data = {
        "workId": "1",
        "description": "Testing"
    }
    r = requests.post(resource_url, data=data)
    if r.status_code == requests.codes.ok:
        print(f"Work 1 created")
    else:
        print(f"Error when creating work 1")

    #Add calibration 1
    resource_url = f"{API_ENDPOINT}{NS}.AddCalibration"
    data = {
        "calId": "1",
        "equipment": "DRONE",
        "workId": "1"
    }
    r = requests.post(resource_url, data=data)
    if r.status_code == requests.codes.ok:
        print("Added calibration 1")
    else:
        print("Error when adding calibration 1")

    

def addAcquisitionTest(num_acquisitors, num_tubes):
    acquisitor_threads = []
    acquisitions_per_worker = int(num_tubes/num_acquisitors)

    # Check for next acquisition id
    resource_url = f"{API_ENDPOINT}{NS}.Acquisition"
    r = requests.get(resource_url)
    next_id = len(r.json()) + 1

    # Create threads
    for i in range(num_acquisitors):
        thread = Acquisitor(i, f"Acquisitor-{i}", acquisitions_per_worker, next_id+acquisitions_per_worker*i, API_ENDPOINT, NS)
        acquisitor_threads.append(thread)

    # Start threads
    for i in range(num_acquisitors):
        acquisitor_threads[i].start()

    # Join threads
    for i in range(num_acquisitors):
        acquisitor_threads[i].join()
        
    # Print results
    min = acquisitor_threads[0].min
    avg = acquisitor_threads[0].avg
    max = acquisitor_threads[0].max
    acquisitor_threads[0].printResults()
    for i in range(1, num_acquisitors):
        if acquisitor_threads[i].min < min:
            min = acquisitor_threads[i].min

        avg = avg + acquisitor_threads[i].avg

        if acquisitor_threads[i].max > max:
            max = acquisitor_threads[i].max

        acquisitor_threads[i].printResults()

    print(f"MIN ADD ACQ --> {min}")
    print(f"AVG ADD ACQ --> {avg/num_acquisitors}")
    print(f"MAX ADD ACQ --> {max}")

def addAnalysisTest(num_analysts, num_acqs):
    analyst_threads = []
    analysis_per_worker = int(num_acqs/num_analysts)
    
    # Check for next analysis id
    resource_url = f"{API_ENDPOINT}{NS}.Analysis"
    r = requests.get(resource_url)
    next_id = len(r.json()) + 1
    
    # Create threads
    for i in range(num_analysts):
        thread = Analyst(i, f"Analyst-{i}", analysis_per_worker, next_id+analysis_per_worker*i, API_ENDPOINT, NS)
        analyst_threads.append(thread)
        
    # Start threads
    for i in range(num_analysts):
        analyst_threads[i].start()
        
    # Join threads
    for i in range(num_analysts):
        analyst_threads[i].join()
        
    # Print results
    min_get = analyst_threads[0].min_get
    avg_get = analyst_threads[0].avg_get
    max_get = analyst_threads[0].max_get
    min_add = analyst_threads[0].min_add
    avg_add = analyst_threads[0].avg_add
    max_add = analyst_threads[0].max_add
    analyst_threads[0].printResults()
    for i in range(1, num_analysts):
        if analyst_threads[i].min_get < min_get:
            min_get = analyst_threads[i].min_get

        avg_get = avg_get + analyst_threads[i].avg_get

        if analyst_threads[i].max_get > max_get:
            max_get = analyst_threads[i].max_get
            
        if analyst_threads[i].min_add < min_add:
            min_add = analyst_threads[i].min_add
            
        avg_add = avg_add + analyst_threads[i].avg_add
        
        if analyst_threads[i].max_get > max_get:
            max_get = analyst_threads[i].max_get

        analyst_threads[i].printResults()

    print(f"MIN GET ACQ --> {min_get}")
    print(f"AVG GET ACQ --> {avg_get/num_analysts}")
    print(f"MAX GET ACQ --> {max_get}")
    print(f"MIN ADD ANA --> {min_add}")
    print(f"AVG ADD ANA --> {avg_add/num_analysts}")
    print(f"MAX ADD ANA --> {max_add}")

    print("Add Analysis Test Finalized")

def addAdvancedAnalysisTest(num_analysts, num_acqs):
    analyst_threads = []
    analysis_per_worker = int(num_acqs/num_analysts)
    
    # Check for next analysis id
    resource_url = f"{API_ENDPOINT}{NS}.Analysis"
    r = requests.get(resource_url)
    next_id = len(r.json()) + 1
    
    # Create threads
    for i in range(num_analysts):
        thread = AdvancedAnalyst(i, f"Advanced Analyst-{i}", analysis_per_worker, next_id+analysis_per_worker*i, API_ENDPOINT, NS)
        analyst_threads.append(thread)
        
    # Start threads
    for i in range(num_analysts):
        analyst_threads[i].start()
        
    # Join threads
    for i in range(num_analysts):
        analyst_threads[i].join()
        
    # Print results
    min_get_acq = analyst_threads[0].min_get_acq
    avg_get_acq = analyst_threads[0].avg_get_acq
    max_get_acq = analyst_threads[0].max_get_acq
    min_get_ana = analyst_threads[0].min_get_ana
    avg_get_ana = analyst_threads[0].avg_get_ana
    max_get_ana = analyst_threads[0].max_get_ana
    min_add = analyst_threads[0].min_add
    avg_add = analyst_threads[0].avg_add
    max_add = analyst_threads[0].max_add
    analyst_threads[0].printResults()
    for i in range(1, num_analysts):
        if analyst_threads[i].min_get_acq < min_get_acq:
            min_get_acq = analyst_threads[i].min_get_acq

        avg_get_acq = avg_get_acq + analyst_threads[i].avg_get_acq

        if analyst_threads[i].max_get_acq > max_get_acq:
            max_get_acq = analyst_threads[i].max_get_acq
        
        if analyst_threads[i].min_get_ana < min_get_ana:
            min_get_ana = analyst_threads[i].min_get_ana

        avg_get_ana = avg_get_ana + analyst_threads[i].avg_get_ana

        if analyst_threads[i].max_get_ana > max_get_ana:
            max_get_ana = analyst_threads[i].max_get_ana
            
        if analyst_threads[i].min_add < min_add:
            min_add = analyst_threads[i].min_add
            
        avg_add = avg_add + analyst_threads[i].avg_add
        
        if analyst_threads[i].max_get > max_get:
            max_get = analyst_threads[i].max_get

        analyst_threads[i].printResults()

    print(f"MIN GET ACQ --> {min_get_acq}")
    print(f"AVG GET ACQ --> {avg_get_acq/num_analysts}")
    print(f"MAX GET ACQ --> {max_get_acq}")
    print(f"MIN GET ANA --> {min_get_ana}")
    print(f"AVG GET ANA --> {avg_get_ana/num_analysts}")
    print(f"MAX GET ANA --> {max_get_ana}")
    print(f"MIN ADD ANA --> {min_add}")
    print(f"AVG ADD ANA --> {avg_add/num_analysts}")
    print(f"MAX ADD ANA --> {max_add}")

    print("Add Analysis Test Finalized")

#cleanMultithreading(10, True, True, 1)
#addTubes(100)
#workAndCalibration()
addAcquisitionTest(1, 1) #Acquisitors, Acquisitions to do
#addAnalysisTest(10, 100) #Analysts, Analysis to do
#addAdvancedAnalysisTest(1, 100)

