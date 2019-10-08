# Steps to deploy 3 organizations network

### 1. Change CA's private keys

In files ***docker-compose-org1.yml***, ***docker-compose-org2.yml*** and ***docker-compose-org3.yml*** you have to change the constant **CA*n*_PRIVATE_KEY** for the real private key of each organization certification authority. Those private keys can be found here:

```
# Org1
crypto-config/peerOrganizations/org1.example.com/ca/*_sk
# Org2
crypto-config/peerOrganizations/org2.example.com/ca/*_sk
# Org3
crypto-config/peerOrganizations/org3.example.com/ca/*_sk
```

### 2. Change IP adresses

It necessary to inform other machines' IP addresses in **extra_host** section. Next table shows which files and services must be updated.

| File                         | Services                        |
| ---------------------------- | ------------------------------- |
| *docker-compose-orderer.yml* | "orderer.example.com"           |
| *docker-compose-org1.yml*    | "peer0.org1.example.com", "cli" |
| *docker-compose-org2.yml*    | "peer0.org2.example.com", "cli" |
| *docker-compose-org3.yml*    | "peer0.org3.example.com", "cli" |

### 3. Create containers and run them
These operations are executed through some scripts

#### 3.1. Scripts to create containers (called *firstTime.sh*)
Orderer machine
```
#!/bin/bash

set -ev
docker-compose -f docker-compose-orderer.yml down -v
docker-compose -f docker-compose-orderer.yml up -d
```
Orgs machines
```
#!/bin/bash

set -ev
docker-compose -f docker-compose-orgn.yml down -v
docker-compose -f docker-compose-orgn.yml up -d
```

#### 3.2. Scripts to start containers (called *start.sh*)
Orderer machine
```
#!/bin/bash

set -ev
docker-compose -f docker-compose-orderer.yml start
```
Orgs machines
```
#!/bin/bash

set -ev
docker-compose -f docker-compose-orgn.yml start
```

#### 3.3. Scripts to stop containers (called *stop.sh*)
Orderer machine
```
#!/bin/bash

set -ev
docker-compose -f docker-compose-orderer.yml stop
```
Orgs machines
```
#!/bin/bash

set -ev
docker-compose -f docker-compose-orgn.yml stop
```

#### 3.4. Grant user execution permission to those scripts
```
chmod u+x scriptFile.sh
```

#### 3.5. Create containers and start them
```
./firstTime.sh
./start.sh
```
### 4. Setup channel

#### 4.1. Create channel by Org1 Peer Node
```
docker exec -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/users/Admin@org1.example.com/msp" peer0.org1.example.com peer channel create -o orderer.example.com:7050 -c mychannel -f /etc/hyperledger/configtx/channel.tx
```

#### 4.2. This Peer Node joins the channel
```
docker exec -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/users/Admin@org1.example.com/msp" peer0.org1.example.com peer channel join -b mychannel.block
```

#### 4.3. Orgs 2 & 3 Peer Nodes have to fetch the channel config and then join to the channel
Org2 Peer Node

```
docker exec -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/users/Admin@org2.example.com/msp" peer0.org2.example.com peer channel fetch config -o orderer.example.com:7050 -c mychannel
```

```
docker exec -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/users/Admin@org2.example.com/msp" peer0.org2.example.com peer channel join -b mychannel_config.block
```

Org3 Peer Node

```
docker exec -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/users/Admin@org3.example.com/msp" peer0.org3.example.com peer channel fetch config -o orderer.example.com:7050 -c mychannel
```

```
docker exec -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/users/Admin@org3.example.com/msp" peer0.org3.example.com peer channel join -b mychannel_config.block
```

### 5. Install business network in all nodes

#### 5.1. Edit *connectionProfile-threenet.json*
In Orderer machine
```
mkdir -p /tmp/composer/org1
mkdir /tmp/composer/org2
mkdir /tmp/composer/org3
cp ~/NuclearInspections/connectionProfile-files/connectionProfile-threenet.json /tmp/composer/connectionProfile.json
```
* Replace all instances of the text **INSERT_ORDERER_IP** with the IP address of that machine.
* Replace all instances of the text **INSERT_ORDERER_CA_CERT** with the Orderer CA certificate. Use the following command to get the certificate from the .pem file:

```
awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' ~/fabric-samples/first-network/crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/tls/ca.crt > /tmp/composer/ca-orderer.txt
```
* Replace all instances of the text **INSERT_ORG1_IP** with the IP address of that machine.
* Replace all instances of the text **INSERT_ORG1_CA_CERT** with the Org1 CA certificate. Use the following command to get the certificate from the .pem file:

```
awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' ~/fabric-samples/first-network/crypto-config/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt > /tmp/composer/org1/ca-org1.txt
```
* Replace all instances of the text **INSERT_ORG2_IP** with the IP address of that machine.
* Replace all instances of the text **INSERT_ORG2_CA_CERT** with the Org2 CA certificate. Use the following command to get the certificate from the .pem file:

```
awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' ~/fabric-samples/first-network/crypto-config/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt > /tmp/composer/org2/ca-org2.txt
```
* Replace all instances of the text **INSERT_ORG3_IP** with the IP address of that machine.
* Replace all instances of the text **INSERT_ORG3_CA_CERT** with the Org3 CA certificate. Use the following command to get the certificate from the .pem file:

```
awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' ~/fabric-samples/first-network/crypto-config/peerOrganizations/org3.example.com/peers/peer0.org3.example.com/tls/ca.crt > /tmp/composer/org3/ca-org3.txt
```

#### 5.2. Customizing the connection profile for each organization
Next code must be placed between ***version*** and ***channel*** section of connection profile archive. You have to change the name of the organization for eache one.

In Orderer machine
```
"client": {
    "organization": "OrgN",
    "connection": {
        "timeout": {
            "peer": {
                "endorser": "300",
                "eventHub": "300",
                "eventReg": "300"
            },
            "orderer": "300"
        }
    }
},
```

#### 5.3. Copy public and private key of admins
You must copy in the temporal folder the public and the private key of each organization admin.

In Orderer machine for Org1
```
# Public Key
cp -p ~/fabric-samples/first-network/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/signcerts/A*.pem /tmp/composer/org1
# Private Key
cp -p ~/fabric-samples/first-network/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/*_sk /tmp/composer/org1
```

In Orderer machine for Org2
```
# Public Key
cp -p ~/fabric-samples/first-network/crypto-config/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp/signcerts/A*.pem /tmp/composer/org2
# Private Key
cp -p ~/fabric-samples/first-network/crypto-config/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp/keystore/*_sk /tmp/composer/org2
```

In Orderer machine for Org3
```
# Public Key
cp -p ~/fabric-samples/first-network/crypto-config/peerOrganizations/org3.example.com/users/Admin@org3.example.com/msp/signcerts/A*.pem /tmp/composer/org3
# Private Key
cp -p ~/fabric-samples/first-network/crypto-config/peerOrganizations/org3.example.com/users/Admin@org3.example.com/msp/keystore/*_sk /tmp/composer/org3
```

#### 5.4. Create Peer Admin cards for each organization
In Orderer machine for Org1
```
composer card create -p /tmp/composer/org1/connectionProfile.json -u PeerAdmin -c /tmp/composer/org1/A*.pem -k /tmp/composer/org1/*_sk -r PeerAdmin -r ChannelAdmin -f /tmp/composer/org1/PeerAdmin@nuclear-org1.card
```

In Orderer machine for Org2
```
composer card create -p /tmp/composer/org2/connectionProfile.json -u PeerAdmin -c /tmp/composer/org2/A*.pem -k /tmp/composer/org2/*_sk -r PeerAdmin -r ChannelAdmin -f /tmp/composer/org2/PeerAdmin@nuclear-org2.card
```

In Orderer machine for Org3
```
composer card create -p /tmp/composer/org3/connectionProfile.json -u PeerAdmin -c /tmp/composer/org3/A*.pem -k /tmp/composer/org3/*_sk -r PeerAdmin -r ChannelAdmin -f /tmp/composer/org3/PeerAdmin@nuclear-org3.card
```

#### 5.5. Send cards to org machines
Org1 machine
```
gcloud compute scp /tmp/composer/org1/PeerAdmin@nuclear-org1.card jokinator20@threenet-1:~/
```

Org2 machine
```
gcloud compute scp /tmp/composer/org2/PeerAdmin@nuclear-org2.card jokinator20@threenet-2:~/
```

Org3 machine
```
gcloud compute scp /tmp/composer/org3/PeerAdmin@nuclear-org3.card jokinator20@threenet-3:~/
```

#### 5.6. Import the business network cards
On Org1 machine
```
composer card import -f ~/PeerAdmin@nuclear-org1.card --card PeerAdmin@nuclear-org1
```

On Org2 machine
```
composer card import -f ~/PeerAdmin@nuclear-org2.card --card PeerAdmin@nuclear-org2
```

On Org3 machine
```
composer card import -f ~/PeerAdmin@nuclear-org3.card --card PeerAdmin@nuclear-org3
```
#### 5.7. Create the business network archive and install it
For all Orgs machines
```
cd
mkdir /tmp/composer
git clone https://github.com/JTrillo/HyperledgerComposer.git ~/HyperledgerComposer
composer archive create -t dir -n ~/HyperledgerComposer/nuclear_auto -a /tmp/composer/archive.bna
```

For Org1 machine
```
composer network install -a /tmp/composer/archive.bna -c PeerAdmin@nuclear-org1
```

For Org2 machine
```
composer network install -a /tmp/composer/archive.bna -c PeerAdmin@nuclear-org2
```

For Org3 machine
```
composer network install -a /tmp/composer/archive.bna -c PeerAdmin@nuclear-org3
```

### 6. Define the endorsement policy
Create the file ***/tmp/composer/endorsement-policy.json*** with this content (only on Org1 machine):
```
{
    "identities": [
        {
            "role": {
                "name": "member",
                "mspId": "Org1MSP"
            }
        },
        {
            "role": {
                "name": "member",
                "mspId": "Org2MSP"
            }
        },
        {
            "role": {
                "name": "member",
                "mspId": "Org3MSP"
            }
        }
    ],
    "policy": {
        "3-of": [
            {
                "signed-by": 0
            },
            {
                "signed-by": 1
            },
            {
                "signed-by": 2
            }
        ]
    }
}
```

### 7. Start the business network

#### 7.1. Retrieve business network admin certificates
Org 1 machine
```
mkdir -p /tmp/composer/org1
mkdir -p /tmp/composer/org2
mkdir -p /tmp/composer/org3
composer identity request -c PeerAdmin@nuclear-org1 -u admin -s adminpw -d /tmp/composer/org1
```

Org 2 machine
```
mkdir -p /tmp/composer/org2
composer identity request -c PeerAdmin@nuclear-org2 -u admin -s adminpw -d /tmp/composer/org2
gcloud compute scp /tmp/composer/org2/admin-pub.pem jokinator20@threenet-1:/tmp/composer/org2
```

Org 3 machine
```
mkdir -p /tmp/composer/org3
composer identity request -c PeerAdmin@nuclear-org3 -u admin -s adminpw -d /tmp/composer/org3
gcloud compute scp /tmp/composer/org3/admin-pub.pem jokinator20@threenet-1:/tmp/composer/org3
```

#### 7.2. Start business network
Org 1 machine
```
composer network start -c PeerAdmin@nuclear-org1 -n nuclear_auto -V 0.0.1 -o endorsementPolicyFile=/tmp/composer/endorsement-policy.json -A admin-org1 -C /tmp/composer/org1/admin-pub.pem -A admin-org2 -C /tmp/composer/org2/admin-pub.pem -A admin-org3 -C /tmp/composer/org3/admin-pub.pem
```

#### 7.3. Import Business Network Admin Cards
Orderer machine
```
gcloud compute scp /tmp/composer/org1/connectionProfile.json jokinator20@threenet-1:/tmp/composer/org1/
gcloud compute scp /tmp/composer/org2/connectionProfile.json jokinator20@threenet-2:/tmp/composer/org2/
gcloud compute scp /tmp/composer/org3/connectionProfile.json jokinator20@threenet-3:/tmp/composer/org3/
```

Org 1 machine
```
composer card create -p /tmp/composer/org1/connectionProfile.json -u admin-org1 -n nuclear_auto -c /tmp/composer/org1/admin-pub.pem -k /tmp/composer/org1/admin-priv.pem -f /tmp/composer/org1/admin-org1@nuclear_auto
composer card import -f /tmp/composer/org1/admin-org1@nuclear_auto.card -c admin-org1@nuclear_auto
composer network ping -c admin-org1@nuclear_auto
```

Org 2 machine
```
composer card create -p /tmp/composer/org2/connectionProfile.json -u admin-org2 -n nuclear_auto -c /tmp/composer/org2/admin-pub.pem -k /tmp/composer/org2/admin-priv.pem -f /tmp/composer/org2/admin-org2@nuclear_auto
composer card import -f /tmp/composer/org2/admin-org2@nuclear_auto.card -c admin-org2@nuclear_auto
composer network ping -c admin-org2@nuclear_auto
```

Org 3 machine
```
composer card create -p /tmp/composer/org3/connectionProfile.json -u admin-org3 -n nuclear_auto -c /tmp/composer/org3/admin-pub.pem -k /tmp/composer/org3/admin-priv.pem -f /tmp/composer/org3/admin-org3@nuclear_auto
composer card import -f /tmp/composer/org3/admin-org3@nuclear_auto.card -c admin-org3@nuclear_auto
composer network ping -c admin-org3@nuclear_auto
```

### 8. Interact with the deployed business network
You can interact with the business network through the REST Server, Composer CLI or Playground.

### 9. Upgrade the business network

#### 9.1. Modifiy package.json
All Org machines
```
# Modify section 'version' of this file. This section must match with the new version number of the business network.
~/HyperledgerComposer/nuclear_auto/package.json
```

#### 9.2. Create a new Business Network archive and install it
For all Orgs machines
```
composer archive create -t dir -n ~/HyperledgerComposer/nuclear_auto -a /tmp/composer/archive.bna
```

For Org1 machine
```
composer network install -a /tmp/composer/archive.bna -c PeerAdmin@nuclear-org1
```

For Org2 machine
```
composer network install -a /tmp/composer/archive.bna -c PeerAdmin@nuclear-org2
```

For Org3 machine
```
composer network install -a /tmp/composer/archive.bna -c PeerAdmin@nuclear-org3
```

### 9.3 Upgrade the network
Org1 machine
```
composer network upgrade -c PeerAdmin@nuclear-org1 -n nuclear_auto -V NETWORK-VERSION
```

Org2 machine
```
composer network upgrade -c PeerAdmin@nuclear-org2 -n nuclear_auto -V NETWORK-VERSION
```

Org3 machine
```
composer network upgrade -c PeerAdmin@nuclear-org3 -n nuclear_auto -V NETWORK-VERSION
```