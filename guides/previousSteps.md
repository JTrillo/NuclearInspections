# Previous steps
Follow this guide before reading the others. Complete it in **one single machine**.

* Create a machine with these requirements on Google Cloud
    * Region **europe-west1**
    * Zone **europe-west1-b**
    * 1 vCPU
    * 6,5 GB RAM
    * OS **Ubuntu 16.04 LTS**
    * 15 GB Disk
    * Change Compute Engine access to read and write
    * Allow HTTP and HTTPS traffic

* Install prerequisites
```
curl -O https://hyperledger.github.io/composer/latest/prereqs-ubuntu.sh
chmod u+x prereqs-ubuntu.sh
./prereqs-ubuntu.sh
```

* Install development environment
```
npm i -g composer-cli
npm i -g composer-rest-server
npm i -g composer-playground
```

* Download fabric samples
```
curl -sSL http://bit.ly/2ysbOFE | bash -s 1.2.0 1.2.0 0.4.10
```

* Go to first-network folder
```
cd fabric-samples/first-network
```

* Modify file ***crypto-config.yaml***

You have to indicate how many orderers, organizations and nodes you want. Now you can see and example of how this file must look.
```
# ---------------------------------------------------------------------------
# "OrdererOrgs" - Definition of organizations managing orderer nodes
# ---------------------------------------------------------------------------
OrdererOrgs:
  # ---------------------------------------------------------------------------
  # Orderer
  # ---------------------------------------------------------------------------
  - Name: Orderer
    Domain: example.com
    Specs:
      - Hostname: orderer
# ---------------------------------------------------------------------------
# "PeerOrgs" - Definition of organizations managing peer nodes
# ---------------------------------------------------------------------------
PeerOrgs:
  # ---------------------------------------------------------------------------
  # Org1
  # ---------------------------------------------------------------------------
  - Name: Org1
    Domain: org1.example.com
    Template:
      Count: 1 #Number of peer nodes
    Users:
      Count: 1 #Number of users in addition to organization admin
  # ---------------------------------------------------------------------------
  # Org2                                   
  # ---------------------------------------------------------------------------
  - Name: Org2
    Domain: org2.example.com
    Template:
      Count: 1 #Number of peer nodes
    Users:
      Count: 1 #Number of users in addition to organization admin
    .
    .
    .
    .
  # ---------------------------------------------------------------------------
  # OrgN                                   
  # ---------------------------------------------------------------------------
  - Name: OrgN
    Domain: orgN.example.com
    Template:
      Count: 1 #Number of peer nodes
    Users:
      Count: 1 #Number of users in addition to organization admin
```

* Modify file ***configtx.yaml***

You have to modify *Organizations* and *Profiles* sections.

How *Organizations* section should look:
```
Organizations:
    
    - &OrdererOrg
        Name: OrdererOrg
        ID: OrdererMSP
        MSPDir: crypto-config/ordererOrganizations/example.com/msp

    - &Org1
        Name: Org1MSP
        ID: Org1MSP
        MSPDir: crypto-config/peerOrganizations/org1.example.com/msp
        AnchorPeers:
            - Host: peer0.org1.example.com
              Port: 7051

    - &Org2
        Name: Org2MSP
        ID: Org2MSP
        MSPDir: crypto-config/peerOrganizations/org2.example.com/msp
        AnchorPeers:
            - Host: peer0.org2.example.com
              Port: 7051
    .
    .
    .
    .
    - &OrgN
        Name: OrgNMSP
        ID: OrgNMSP
        MSPDir: crypto-config/peerOrganizations/orgN.example.com/msp
        AnchorPeers:
            - Host: peer0.orgN.example.com
              Port: 7051
```
How *Profiles* section should look:
```
Profiles:

    NOrgsOrdererGenesis:
        Orderer:
            <<: *OrdererDefaults
            Organizations:
                - *OrdererOrg
        Consortiums:
            NuclearConsortium:
                Organizations:
                    - *Org1
                    - *Org2
                    .
                    .
                    .
                    .
                    - *OrgN
    NOrgsChannel:
        Consortium: NuclearConsortium
        Application:
            <<: *ApplicationDefaults
            Organizations:
                - *Org1
                - *Org2
                .
                .
                .
                .
                - *OrgN
```

* Modify script ***byfn.sh***

You have to modify function **generateChannelArtifacts()**. The next lines:
```
# Orderer genesis block generation
configtxgen -profile NOrgsOrdererGenesis -outputBlock ./channel-artifacts/genesis.block
# Channel configuration transaction 'channel.tx' generation
configtxgen -profile NOrgsChannel -outputCreateChannelTx ./channel-artifacts/channel.tx -channelID $CHANNEL_NAME
# For each organization add this
configtxgen -profile NOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/OrgNMSPanchors.tx -channelID $CHANNEL_NAME -asOrg OrgNMSP
```

* Execute script ***byfn.sh*** on generate mode
```
/byfn.sh generate
```
The execution of the script will generate folders ***crypto-config*** and ***channel-artifacts***.

* Remove useless files and folders
```
rm docker-compose-*
rm byfn.sh eyfn.sh README.md .gitignore
rm -R base/ org3-artifacts/ scripts/
```

* Clone *NuclearInspections* repository into home folder
```
cd
git clone https://github.com/JTrillo/NuclearInspections.git
```

* Shutdown machine and make and make a snapshot
* Create other machines from this snapshot and this requirements:
    * Region **europe-west1**
    * Zone **europe-west1-b**
    * 1 vCPU
    * 6,5 GB RAM
    * Change Compute Engine access to read and write
    * Allow HTTP and HTTPS traffic