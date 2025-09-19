# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>안녕하세요! 이것은 Render에서 실행되는 Flask 웹사이트입니다.</h1>'

if __name__ == '__main__':
    app.run()