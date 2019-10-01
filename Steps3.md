# Steps to deploy 3 organizations network

### 1. Change CA's private keys

In files ***docker-compose-org1.yml***, ***docker-compose-org2.yml*** and ***docker-compose-org3.yml*** you have to change the constant **CA*n*_PRIVATE_KEY** for the real private key of each certification authority.

### 2. Change IP adresses

It necessary to inform other machines' IP addresses in **extra_host** section. Next table shows which files and services must be updated.

| File                         | Services                        |
| ---------------------------- | ------------------------------- |
| *docker-compose-orderer.yml* | "orderer.example.com"           |
| *docker-compose-org1.yml*    | "peer0.org1.example.com", "cli" |
| *docker-compose-org2.yml*    | "peer0.org2.example.com", "cli" |
| *docker-compose-org3.yml*    | "peer0.org3.example.com", "cli" |

### 3. Create containers and run them

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

#### 5.1. Edit *connectionProfile.json*
* Replace all instances of the text **INSERT_ORDERER_IP** with the IP address of that machine.
* Replace all instances of the text **INSERT_ORDERER_CA_CERT** with the Orderer CA certificate. Use the following command to get the certificate from the .pem file:

```
awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/tls/ca.crt > /tmp/composer/ca-orderer.txt
```
* Replace all instances of the text **INSERT_ORG1_IP** with the IP address of that machine.
* Replace all instances of the text **INSERT_ORG1_CA_CERT** with the Org1 CA certificate. Use the following command to get the certificate from the .pem file:

```
awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' crypto-config/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt > /tmp/composer/org1/ca-org1.txt
```
* Replace all instances of the text **INSERT_ORG2_IP** with the IP address of that machine.
* Replace all instances of the text **INSERT_ORG2_CA_CERT** with the Org2 CA certificate. Use the following command to get the certificate from the .pem file:

```
awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' crypto-config/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt > /tmp/composer/org2/ca-org2.txt
```
* Replace all instances of the text **INSERT_ORG3_IP** with the IP address of that machine.
* Replace all instances of the text **INSERT_ORG3_CA_CERT** with the Org3 CA certificate. Use the following command to get the certificate from the .pem file:

```
awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' crypto-config/peerOrganizations/org3.example.com/peers/peer0.org3.example.com/tls/ca.crt > /tmp/composer/org3/ca-org3.txt
```

#### 5.2. Customizing the connection profile for each organization
Next code must be placed between ***version*** and ***channel*** section of connection profile archive. You have to change the name of the organization for eache one.
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
```
# Public Key
cp -p crypto-config/peerOrganizations/orgn.example.com/users/Admin@orgn.example.com/msp/signcerts/A*.pem /tmp/composer/orgn
# Private Key
cp -p crypto-config/peerOrganizations/orgn.example.com/users/Admin@orgn.example.com/msp/keystore/*_sk /tmp/composer/orgn
```

#### 5.4. Create Peer Admin cards for each organization
```
composer card create -p /tmp/composer/orgn/connectionProfile.json -u PeerAdmin -c /tmp/composer/orgn/A*.pem -k /tmp/composer/orgn/*_sk -r PeerAdmin -r ChannelAdmin -f /tmp/composer/orgn/PeerAdmin@nuclear-orgn.card
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
```
composer card import -f PeerAdmin@nuclear-orgn.card --card PeerAdmin@nuclear-orgn
``` 