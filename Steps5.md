# Steps to deploy 5 organizations network

### Previous steps

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
curl -sSL http://bit.ly/2ysbOFE | bash 1.2.0 1.2.0 0.4.10
```