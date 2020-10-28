# 파이썬으로 블록체인 만들기

[![Build Status](https://travis-ci.org/dvf/blockchain.svg?branch=master)](https://travis-ci.org/dvf/blockchain)

원본 글과 코드는 옆의 링크에서 볼 수 있습니다. [Building a Blockchain](https://medium.com/p/117428612f46).  
한글 번역본은 [파이썬으로 블록체인 만들기](https://medium.com/caulink/%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%9C%BC%EB%A1%9C-%EB%B8%94%EB%A1%9D%EC%B2%B4%EC%9D%B8-%EB%A7%8C%EB%93%A4%EA%B8%B0-part-1-4386dbc735e)에서 볼 수 있습니다.

많은 파일들이 있지만, .py로 끝나는 파이썬 파일만 보셔도 됩니다.  
파이썬 코드에는 코딩 경험이 없으신 분들도 이해하실 수 있게 주석을 최대한 많이 달아놓았습니다. 

VS Code나 다른 IDE 그리고 파이썬은 설치가 되어있다고, 가정을 합니다.

위의 원본 혹은 번역글에 적혀있는 것처럼, 코드가 잘 작동하는지 확인하고 결과를 눈으로 보기 위해서는 Postman을 설치하고 실행시켜야 합니다.  
Postman 설치는 이 [링크](https://www.postman.com/downloads/)에서 하실 수 있습니다.  

VS Code, Python, Postman 설치가 완료되었으면 이제 실행하면 됩니다. 하지만, 실행 전 개발환경 설정 과정에서 2가지를 추가로 설치해야합니다. (각자의 상황에 따라 1가지 혹은 설치 없이 진행하실수도 있습니다.)  

## Installation

### pip 설치 

pip는 파이썬 패키지 소프트웨어 설치 및 관리 시스템입니다. pip 설치가 되어있는지를 먼저 확인해야 합니다.
아래의 명령어를 사용하여 확인합니다. 

``` 
pip --version
```

위의 명령어는 pip의 버전을 확인하는 명령어로 설치가 되어있다면, 버전이 나올 것입니다.  
만약에 pip 설치가 되어있지 않다면, pip를 설치합니다. 

#### 윈도우
```
curl https://bootstap.pypa.io/get-pip.py -o get-pip.py  
python get-pip.py
```

#### 맥
```
sudo easy_install pip
```

#### 리눅스
```
sudo apt-get install python3-pip
```

이미 설치가 되어있는 분들중, 버전 업그레이드가 필요하신 분들은 아래의 명령어를 입력하시면 됩니다. 

#### 윈도우
```
python -m pip install -upgrade pip
```

#### 맥, 리눅스
```
pip install -U pip
```

이제 pip 설치가 완료되었으면, 코드를 실행하면 됩니다.   
가상 환경을 사용하는 경우와 그렇지 않은 경우가 나누어집니다.  

### 가상 환경을 사용하지 않는 경우

* `$python blockchain.py`
* `$python blockchain.py -p 5001`
* `$python blockchain.py --port 5002`


### 가상 환경을 사용하는 경우

1. Install [pipenv](https://github.com/kennethreitz/pipenv). 

```
$ pip install pipenv 
```
2. Install requirements  
```
$ pipenv install 
``` 

3. Run the server:
    * `$ pipenv run python blockchain.py` 
    * `$ pipenv run python blockchain.py -p 5001`
    * `$ pipenv run python blockchain.py --port 5002`
    
## Docker

Another option for running this blockchain program is to use Docker.  Follow the instructions below to create a local Docker container:

1. Clone this repository
2. Build the docker container

```
$ docker build -t blockchain .
```

3. Run the container

```
$ docker run --rm -p 80:5000 blockchain
```

4. To add more instances, vary the public port number before the colon:

```
$ docker run --rm -p 81:5000 blockchain
$ docker run --rm -p 82:5000 blockchain
$ docker run --rm -p 83:5000 blockchain
```

## Installation (C# Implementation)

1. Install a free copy of Visual Studio IDE (Community Edition):
https://www.visualstudio.com/vs/

2. Once installed, open the solution file (BlockChain.sln) using the File > Open > Project/Solution menu options within Visual Studio.

3. From within the "Solution Explorer", right click the BlockChain.Console project and select the "Set As Startup Project" option.

4. Click the "Start" button, or hit F5 to run. The program executes in a console window, and is controlled via HTTP with the same commands as the Python version.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

