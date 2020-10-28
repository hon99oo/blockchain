# 파이썬으로 블록체인 만들기

[![Build Status](https://travis-ci.org/dvf/blockchain.svg?branch=master)](https://travis-ci.org/dvf/blockchain)

원본 글과 코드는 옆의 링크에서 볼 수 있습니다. [Building a Blockchain](https://medium.com/p/117428612f46). 
한글 번역본은 [파이썬으로 블록체인 만들기](https://medium.com/caulink/%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%9C%BC%EB%A1%9C-%EB%B8%94%EB%A1%9D%EC%B2%B4%EC%9D%B8-%EB%A7%8C%EB%93%A4%EA%B8%B0-part-1-4386dbc735e)에서 볼 수 있습니다.

많은 파일들이 있지만, .py로 끝나는 파이썬 파일만 보셔도 됩니다. 
파이썬 코드에는 코딩 경험이 없으신 분들도 이해하실 수 있게 주석을 최대한 많이 달아놓았습니다. 

## Installation

1. Make sure [Python 3.6+](https://www.python.org/downloads/) is installed. 
2. Install [pipenv](https://github.com/kennethreitz/pipenv). 

```
$ pip install pipenv 
```
3. Install requirements  
```
$ pipenv install 
``` 

4. Run the server:
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

