from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbjungle  # 'dbjungle'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['POST'])
def post_article():
    # 1. 클라이언트로부터 데이터를 받기
    title_receive = request.form['title_give']  # 클라이언트로부터 title 받는 부분
    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분
    # likes_receive = request.form['likes_give'] #라이크 개수 받기

    # 3. mongoDB에 데이터를 넣기
    db.memos.insert_one({'title': title_receive,'comment': comment_receive, 'likes':0})

    return jsonify({'result': 'success'})


@app.route('/memo', methods=['GET'])
def read_articles():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    result = list(db.memos.find({}, {'_id':0}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'memos': result})


@app.route('/likes', methods=['POST'])
def like_star():

    title_receive = request.form['title_give'] #받아온 타이틀값 선언
    target_title= db.memos.find_one({'title': title_receive}) #like 누른 대상 선언
    title_likes = target_title['likes'] #현재 like 수
    title_likes_new = title_likes +  1 #현재 like 수 + 1

    db.memos.update_one({'title': title_receive}, {'$set': {'likes': title_likes_new}}) #업데이트 진행

    return jsonify({'result': 'success'})

@app.route('/likes', methods=['GET'])
def read_likes():
    result = list(db.memos.find({}, {'_id':0}))
    return jsonify({'result': 'success', 'memos': result})





@app.route('/delete', methods=['POST'])
def delete_post():
    title_receive = request.form['title_give']  # title 받는 부분
    
    db.memos.delete_one({'title': title_receive}) #mongoDB에 데이터를 삭제

    return jsonify({'result': 'success'})

    



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)