#!/usr/bin/python3

import threading
import requests
import json
import random
import plotly
import plotly.graph_objs as go
import time
import datetime
from acquisitor import *
from analyst import *
from advancedAnalyst import *
from automaticAnalyst import *
from cleaner import *

#API_ENDPOINT = "http://104.155.2.231:3000/api/" #2 PEERS NET
API_ENDPOINT = "http://34.76.123.255:3000/api/" #3 PEERS NET
API_ENDPOINT_2 = "http://34.76.123.255:3001/api/" #3 PEERS NET
#API_ENDPOINT = "http://35.241.200.124:3000/api/" #5 PEERS NET
NS = "ertis.uma.nuclear"

#RUN SERVER WITH CARD ADMIN BEFORE EXECUTE THIS FUNCTION
def cleanMultithreading(num_threads, tub, acq, ana, begin=-1, totalDeletes=100):
    threads_tub = []
    threads_acq = []
    threads_ana = []

    if tub == True:
        if begin == -1:
            # Get total number of tubes
            resource_url = f"{API_ENDPOINT}{NS}.Tube"
            r = requests.get(resource_url)
            total = len(r.json())
            deletes_per_thread = int(total / num_threads)

            # Create threads
            for i in range(num_threads):
                thread = Cleaner(f"Thread-{i}", 1+deletes_per_thread*i, deletes_per_thread*(i+1), API_ENDPOINT, NS, 1)
                threads_tub.append(thread)
        else:
            deletes_per_thread = int(totalDeletes / num_threads)

            # Create threads
            for i in range(num_threads):
                thread = Cleaner(f"Thread-{i}", begin+deletes_per_thread*i, begin+deletes_per_thread*(i+1)-1, API_ENDPOINT, NS, 1)
                threads_tub.append(thread)

        # Start threads
        for i in range(num_threads):
            threads_tub[i].start()
            
        # Join threads
        for i in range(num_threads):
            threads_tub[i].join()

    if acq == True:
        if begin == -1:
            # Get total number of acquisitions
            resource_url = f"{API_ENDPOINT}{NS}.Acquisition"
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
    # Check for next tube id
    resource_url = f"{API_ENDPOINT}{NS}.Tube"
    r = requests.get(resource_url)
    next_id = len(r.json()) + 1

    resource_url = f"{API_ENDPOINT}{NS}.RegisterTube"

    for i in range(n_tubes):
        data = {
            "tubeId": i+next_id,
            "posX": random.randint(0, 100),
            "posY": random.randint(0, 100),
            "length": random.randint(5, 20)
        }
        r = requests.post(resource_url, data=data)
        if r.status_code == requests.codes.ok:
            print(f"Added tube {i+next_id}")
        else:
            print(f"Error when adding tube {i+next_id}")

def cleanCalibrations():
    # Check how many calibrations exist
    resource_url = f"{API_ENDPOINT}{NS}.Calibration"
    r = requests.get(resource_url)
    num_cals = len(r.json())

    for i in range(num_cals):
        resource_url = f"{API_ENDPOINT}{NS}.Calibration/{i+1}"
        r = requests.delete(resource_url)
        if r.status_code == requests.codes.no_content:
            print(f"Calibration {i+1} deleted")
        else:
            print(f"Error when deleting calibration {i+1}")

def addWorkAndCalibrations():
    #Create work 1
    resource_url = f"{API_ENDPOINT}{NS}.CreateWork"
    data = {
        "workId": "1",
        "workDate": generateDateTime(),
        "description": "Testing"
    }
    r = requests.post(resource_url, data=data)
    if r.status_code == requests.codes.ok:
        print(f"Work 1 created")
    else:
        print(f"Error when creating work 1")

    # Check how many tubes exist
    resource_url = f"{API_ENDPOINT}{NS}.Tube"
    r = requests.get(resource_url)
    n_tubes = len(r.json())
    n_calibrations = int(n_tubes / 25)

    resource_url = f"{API_ENDPOINT}{NS}.AddCalibration"
    for i in range(1, n_calibrations+1):
        #Add calibration i
        data = {
            "calId": i,
            "calDate": generateDateTime(),
            "equipment": "DRONE",
            "workId": "1"
        }
        r = requests.post(resource_url, data=data)
        if r.status_code == requests.codes.ok:
            print(f"Added calibration {i}")
        else:
            print(f"Error when adding calibration {i}")

def addAcquisitionTest(num_acquisitors, filename):
    # Get num tubes
    resource_url = f"{API_ENDPOINT}{NS}.Tube"
    r = requests.get(resource_url)
    num_tubes = len(r.json())

    acquisitor_threads = []
    acquisitions_per_worker = int(num_tubes/num_acquisitors)

    # Check for next acquisition id
    resource_url = f"{API_ENDPOINT}{NS}.Acquisition"
    r = requests.get(resource_url)
    next_id = len(r.json()) + 1

    # Create threads
    for i in range(num_acquisitors):
        thread = Acquisitor(i, f"Acquisitor-{i}", acquisitions_per_worker, next_id+acquisitions_per_worker*i, num_tubes, API_ENDPOINT, NS)
        acquisitor_threads.append(thread)

    start_time = time.time()
    # Start threads
    for i in range(num_acquisitors):
        acquisitor_threads[i].start()

    # Join threads
    for i in range(num_acquisitors):
        acquisitor_threads[i].join()

    total_elapsed_time = time.time() - start_time
        
    # Print results
    min = acquisitor_threads[0].min
    min5avg = acquisitor_threads[0].min5avg
    avg = acquisitor_threads[0].avg
    max = acquisitor_threads[0].max
    max5avg = acquisitor_threads[0].max5avg
    acquisitor_threads[0].printResults()
    for i in range(1, num_acquisitors):
        if acquisitor_threads[i].min < min:
            min = acquisitor_threads[i].min
            
        min5avg = min5avg + acquisitor_threads[i].min5avg

        avg = avg + acquisitor_threads[i].avg

        if acquisitor_threads[i].max > max:
            max = acquisitor_threads[i].max
            
        max5avg = max5avg + acquisitor_threads[i].max5avg

        acquisitor_threads[i].printResults()

    with open(filename, 'w') as f:
        print(f"MIN --> {min}", file=f)
        print(f"MIN 5 AVG --> {min5avg/num_acquisitors}", file=f)
        print(f"AVG --> {avg/num_acquisitors}", file=f)
        print(f"MAX --> {max}", file=f)
        print(f"MAX 5 AVG --> {max5avg/num_acquisitors}", file=f)
        print("")
        print(f"TOTAL ELAPSED TIME --> {total_elapsed_time}", file=f)

def addAutomaticAnalysisTest(filename):
    # Get num acqs
    resource_url = f"{API_ENDPOINT}{NS}.Acquisition"
    r = requests.get(resource_url)
    num_acqs = len(r.json())

    # Check for next analysis id
    resource_url = f"{API_ENDPOINT}{NS}.Analysis"
    r = requests.get(resource_url)
    next_id = len(r.json()) + 1

    start_time = time.time()

    # Create automatic analyst
    auto_analyst = AutomaticAnalyst(num_acqs, next_id, API_ENDPOINT, NS)

    total_elapsed_time = time.time() - start_time

    with open(filename, 'w') as f:
        print(f"MIN --> {auto_analyst.min}", file=f)
        print(f"MIN 5 AVG --> {auto_analyst.min5avg}", file=f)
        print(f"AVG --> {auto_analyst.avg}", file=f)
        print(f"MAX --> {auto_analyst.max}", file=f)
        print(f"MAX 5 AVG --> {auto_analyst.max5avg}", file=f)
        print("")
        print(f"TOTAL ELAPSED TIME --> {total_elapsed_time}", file=f)

def getCalibrations(role):
    # Check how many calibrations exist
    resource_url = f"{API_ENDPOINT}{NS}.Calibration"
    r = requests.get(resource_url)
    n_calibrations = len(r.json())
    
    resource_url = f"{API_ENDPOINT}{NS}.GetCalibration"
    for i in range(1, n_calibrations+1):
        #Add calibration i
        data = {
            "calId": i,
            "type": role
        }
        r = requests.post(resource_url, data=data)
        if r.status_code == requests.codes.ok:
            print(f"Gotten calibration {i}")
        else:
            print(f"Error when getting calibration {i}")

def addAnalysisTest(num_analysts, filename):
    # Get num acqs
    resource_url = f"{API_ENDPOINT}{NS}.Acquisition"
    r = requests.get(resource_url)
    num_acqs = len(r.json())

    analyst_threads = []
    analysis_per_worker = int(num_acqs/num_analysts)
    
    # Check for next analysis id
    resource_url = f"{API_ENDPOINT}{NS}.Analysis"
    r = requests.get(resource_url)
    next_id = len(r.json()) + 1
    
    # Create threads
    for i in range(num_analysts):
        #PRIMARY ANALYSTS
        thread = Analyst(i, f"Analyst-{i}", analysis_per_worker, next_id+analysis_per_worker*i, num_acqs, API_ENDPOINT, NS)
        analyst_threads.append(thread)
        #SECONDARY ANALYSTS
        thread = Analyst(i+num_analysts, f"Analyst-{i+num_analysts}", analysis_per_worker, next_id+num_acqs+analysis_per_worker*i, num_acqs, API_ENDPOINT_2, NS)
        analyst_threads.append(thread)
        
    start_time = time.time()
    # Start threads
    for i in range(len(analyst_threads)):
        analyst_threads[i].start()
        
    # Join threads
    for i in range(len(analyst_threads)):
        analyst_threads[i].join()

    total_elapsed_time = time.time() - start_time
        
    # Print results
    min_get = analyst_threads[0].min_get
    min5avg_get = analyst_threads[0].min5avg_get
    avg_get = analyst_threads[0].avg_get
    max_get = analyst_threads[0].max_get
    max5avg_get = analyst_threads[0].max5avg_get
    
    min_add = analyst_threads[0].min_add
    min5avg_add = analyst_threads[0].min5avg_add
    avg_add = analyst_threads[0].avg_add
    max_add = analyst_threads[0].max_add
    max5avg_add = analyst_threads[0].max5avg_add
    
    analyst_threads[0].printResults()
    for i in range(1, num_analysts):
        if analyst_threads[i].min_get < min_get:
            min_get = analyst_threads[i].min_get
        
        min5avg_get = min5avg_get + analyst_threads[i].min5avg_get

        avg_get = avg_get + analyst_threads[i].avg_get

        if analyst_threads[i].max_get > max_get:
            max_get = analyst_threads[i].max_get
            
        max5avg_get = max5avg_get + analyst_threads[i].max5avg_get
            
        if analyst_threads[i].min_add < min_add:
            min_add = analyst_threads[i].min_add
            
        min5avg_add = min5avg_add + analyst_threads[i].min5avg_add
            
        avg_add = avg_add + analyst_threads[i].avg_add
        
        if analyst_threads[i].max_get > max_get:
            max_add = analyst_threads[i].max_add
        
        max5avg_add = max5avg_add + analyst_threads[i].max5avg_add

        analyst_threads[i].printResults()

    with open(filename, 'w') as f:
        print(f"MIN GET ACQ --> {min_get}", file=f)
        print(f"MIN 5 GET ACQ --> {min5avg_get/num_analysts}", file=f)
        print(f"AVG GET ACQ --> {avg_get/num_analysts}", file=f)
        print(f"MAX GET ACQ --> {max_get}", file=f)
        print(f"MAX 5 GET ACQ --> {max5avg_get/num_analysts}", file=f)
        print("")
        
        print(f"MIN ADD ANA --> {min_add}", file=f)
        print(f"MIN 5 GET ANA --> {min5avg_add/num_analysts}", file=f)
        print(f"AVG ADD ANA --> {avg_add/num_analysts}", file=f)
        print(f"MAX ADD ANA --> {max_add}", file=f)
        print(f"MAX 5 GET ANA --> {max5avg_add/num_analysts}", file=f)
        print("")

        print(f"TOTAL ELAPSED TIME --> {total_elapsed_time}", file=f)

    print("Add Analysis Test Finalized")

def endCalibrations(role):
    # Check how many calibrations exist
    resource_url = f"{API_ENDPOINT}{NS}.Calibration"
    r = requests.get(resource_url)
    n_calibrations = len(r.json())
    
    resource_url = f"{API_ENDPOINT}{NS}.EndCalibration"
    for i in range(1, n_calibrations+1):
        #End calibration i
        data = {
            "calId": i,
            "type": role
        }
        r = requests.post(resource_url, data=data)
        if r.status_code == requests.codes.ok:
            print(f"Ended calibration {i}")
        else:
            print(f"Error when ending calibration {i}")

def addResolutionTest(num_analysts, filename):
    # Get num acqs
    resource_url = f"{API_ENDPOINT}{NS}.Acquisition"
    r = requests.get(resource_url)
    num_acqs = len(r.json())

    analyst_threads = []
    analysis_per_worker = int(num_acqs/num_analysts)
    
    # Check for next analysis id
    resource_url = f"{API_ENDPOINT}{NS}.Analysis"
    r = requests.get(resource_url)
    next_id = len(r.json()) + 1
    
    # Create threads
    for i in range(num_analysts):
        thread = AdvancedAnalyst(i, f"Advanced Analyst-{i}", analysis_per_worker, next_id+analysis_per_worker*i, num_acqs, API_ENDPOINT, NS)
        analyst_threads.append(thread)
        
    start_time = time.time()
    # Start threads
    for i in range(len(analyst_threads)):
        analyst_threads[i].start()
        
    # Join threads
    for i in range(len(analyst_threads)):
        analyst_threads[i].join()

    total_elapsed_time = time.time() - start_time
        
    # Print results
    min_get_acq = analyst_threads[0].min_get_acq
    min5avg_get_acq = analyst_threads[0].min5avg_get_acq
    avg_get_acq = analyst_threads[0].avg_get_acq
    max_get_acq = analyst_threads[0].max_get_acq
    max5avg_get_acq = analyst_threads[0].max5avg_get_acq
    
    min_get_ana = analyst_threads[0].min_get_ana
    min5avg_get_ana = analyst_threads[0].min5avg_get_ana
    avg_get_ana = analyst_threads[0].avg_get_ana
    max_get_ana = analyst_threads[0].max_get_ana
    max5avg_get_ana = analyst_threads[0].max5avg_get_ana
    
    min_add = analyst_threads[0].min_add
    min5avg_add = analyst_threads[0].min5avg_add
    avg_add = analyst_threads[0].avg_add
    max_add = analyst_threads[0].max_add
    max5avg_add = analyst_threads[0].max5avg_add
    
    analyst_threads[0].printResults()
    for i in range(1, num_analysts):
        if analyst_threads[i].min_get_acq < min_get_acq:
            min_get_acq = analyst_threads[i].min_get_acq
        
        min5avg_get_acq = min5avg_get_acq + analyst_threads[0].min5avg_get_acq

        avg_get_acq = avg_get_acq + analyst_threads[i].avg_get_acq

        if analyst_threads[i].max_get_acq > max_get_acq:
            max_get_acq = analyst_threads[i].max_get_acq
        
        max5avg_get_acq = max5avg_get_acq + analyst_threads[0].max5avg_get_acq
        
        if analyst_threads[i].min_get_ana < min_get_ana:
            min_get_ana = analyst_threads[i].min_get_ana
        
        min5avg_get_ana = min5avg_get_ana + analyst_threads[0].min5avg_get_ana

        avg_get_ana = avg_get_ana + analyst_threads[i].avg_get_ana

        if analyst_threads[i].max_get_ana > max_get_ana:
            max_get_ana = analyst_threads[i].max_get_ana
        
        max5avg_get_ana = max5avg_get_ana + analyst_threads[0].max5avg_get_ana
            
        if analyst_threads[i].min_add < min_add:
            min_add = analyst_threads[i].min_add
            
        min5avg_add = min5avg_add + analyst_threads[0].min5avg_add
            
        avg_add = avg_add + analyst_threads[i].avg_add
        
        if analyst_threads[i].max_add > max_add:
            max_add = analyst_threads[i].max_add
        
        max5avg_add = max5avg_add + analyst_threads[0].max5avg_add

        analyst_threads[i].printResults()

    with open(filename, 'w') as f:
        print(f"MIN GET ACQ --> {min_get_acq}", file=f)
        print(f"MIN 5 GET ACQ --> {min5avg_get_acq/num_analysts}", file=f)
        print(f"AVG GET ACQ --> {avg_get_acq/num_analysts}", file=f)
        print(f"MAX GET ACQ --> {max_get_acq}", file=f)
        print(f"MAX 5 GET ACQ --> {max5avg_get_acq/num_analysts}", file=f)
        print()
        
        print(f"MIN GET ANA --> {min_get_ana}", file=f)
        print(f"MIN 5 GET ANA --> {min5avg_get_ana/num_analysts}", file=f)
        print(f"AVG GET ANA --> {avg_get_ana/num_analysts}", file=f)
        print(f"MAX GET ANA --> {max_get_ana}", file=f)
        print(f"MAX 5 GET ANA --> {max5avg_get_ana/num_analysts}", file=f)
        print()
        
        print(f"MIN ADD ANA --> {min_add}", file=f)
        print(f"MIN 5 ADD ANA --> {min5avg_add/num_analysts}", file=f)
        print(f"AVG ADD ANA --> {avg_add/num_analysts}", file=f)
        print(f"MAX ADD ANA --> {max_add}", file=f)
        print(f"MAX 5 ADD ANA --> {max5avg_add/num_analysts}", file=f)
        print()

        print(f"TOTAL ELAPSED TIME --> {total_elapsed_time}", file=f)

    print("Add Resolution Test Finalized")

def generateDateTime():
    x = str(datetime.datetime.now()).replace(" ", "T")
    x2 = x[:len(x)-3]+"Z"

    return x2

#cleanMultithreading(10, False, False, True, 1501, 3000) #Primer booleano tubos, segundo adquisiciones y tercero análisis
#addTubes(500)
#cleanCalibrations()
#addWorkAndCalibrations()
#addAcquisitionTest(1, 'Acq_3Peers_1500tubes_250KB_faster.txt') #Acquisitors, filename to export results
#addAutomaticAnalysisTest('Auto_3Peers_1000tubes_250KB_faster.txt')
#getCalibrations('PRIMARY')
#getCalibrations('SECONDARY')
#addAnalysisTest(10, 'Analysis_3Peers_1500tubes_250KB_10perRole_faster.txt') #Analysts, filename to export results
#endCalibrations('PRIMARY')
#endCalibrations('SECONDARY')
#getCalibrations('RESOLUTION')
#addResolutionTest(10, 'Resolution_3Peers_1500tubes_250KB_10resolutors_faster.txt') #Advanced analysts, filename to export results

print("\r\nNETWORK CURRENT STATE\r\n")

resource_url = f"{API_ENDPOINT}{NS}.Tube"
r = requests.get(resource_url)
print(f"Total tubes: {len(r.json())}")

resource_url = f"{API_ENDPOINT}{NS}.Calibration"
r = requests.get(resource_url)
print(f"Total calibrations: {len(r.json())}")

resource_url = f"{API_ENDPOINT}{NS}.Acquisition"
r = requests.get(resource_url)
print(f"Total acquisitions: {len(r.json())}")

resource_url = f"{API_ENDPOINT}{NS}.Analysis"
r = requests.get(resource_url)
print(f"Total analysis: {len(r.json())}")

an_fqi = f"resource%3A{NS}.Staff%23auto"
resource_url = f"{API_ENDPOINT}queries/AnalysisByAnalyst?an_fqi={an_fqi}"
r = requests.get(resource_url)
print(f"Num. analysis made by auto: {len(r.json())}")

an_fqi = f"resource%3A{NS}.Staff%23esc"
resource_url = f"{API_ENDPOINT}queries/AnalysisByAnalyst?an_fqi={an_fqi}"
r = requests.get(resource_url)
print(f"Num. analysis made by esc: {len(r.json())}")

an_fqi = f"resource%3A{NS}.Staff%23llopis"
resource_url = f"{API_ENDPOINT}queries/AnalysisByAnalyst?an_fqi={an_fqi}"
r = requests.get(resource_url)
print(f"Num. analysis made by llopis: {len(r.json())}")

an_fqi = f"resource%3A{NS}.Staff%23trillo"
resource_url = f"{API_ENDPOINT}queries/AnalysisByAnalyst?an_fqi={an_fqi}"
r = requests.get(resource_url)
print(f"Num. analysis made by trillo: {len(r.json())}")