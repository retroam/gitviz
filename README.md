# gitviz
<img width="1190" alt="appimage" src="https://user-images.githubusercontent.com/6335831/110005778-b878da80-7ccd-11eb-944b-093bc06a018e.png">


## Installation
1. Clone repo to local
2. Create virtualenv
```python
virtualenv venv
source venv/bin/activate
```
3. Install requirements file
```
pip install -r requirements.txt
```
4. Generate a token by following this [tutorial](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

5. Create a .config file similar to below in root folder (replace credentials with own)
```
[GITHUB]
token=aaabbbccc1234!!!@@@
username=abc1234
```
6. Run server by running the following command:
```
uvicorn app:app --port=8888
```
7. Enter a public github repo e.g. airbnb/knowledge-repo
**Note**
Has only been tested on python 3.7+
