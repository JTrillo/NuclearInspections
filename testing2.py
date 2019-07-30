#!/usr/bin/python3

import random
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import hashlib

def upload():
    start_time = time.time()
    filename = "acq1.txt"
    f = open(filename, "w")

    content = []
    for i in range(0, 200000):
        aux = random.randint(-5000, 5000)
        content.append(aux)
        f.write(str(aux) + "\n")

    f.close()
    elapsed_time = time.time() - start_time
    print(f"Elapsed time {elapsed_time}")

    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    bucket = storage.bucket("hyperledger-jte.appspot.com")

    tfm = bucket.blob(filename)
    tfm.upload_from_filename(filename)

def download():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    bucket = storage.bucket("hyperledger-jte.appspot.com")

    tfm = bucket.get_blob('acq1.txt')
    aux = tfm.download_as_string().decode('ascii').split('\r\n')
    aux.remove('')
    print(aux, len(aux))

def sha256(fname):
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def generateIndications(tubeLength):
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

#upload()
#download()
#print(sha256("acq1.txt"))
#print(generateIndications(10))