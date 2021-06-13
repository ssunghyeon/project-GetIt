from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'GETIT'

client = MongoClient('localhost', 27017)
db = client.getit


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,
        "password": password_hash,
        "profile_name": username_receive,
        "profile_pic": "",
        "profile_pic_real": "profile_pics/profile_placeholder.png",
        "profile_info": ""
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_recevie = request.form["username_give"]
    exists = bool(db.users.find_one({"username": username_recevie}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/sign_in', methods=['POST'])
def sign_in():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/user/<username>')
def user(username):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload['id'])
        user_info = db.users.find_one({"username": username}, {'_id': False})
        return render_template('user.html', user_info=user_info, status=status, payload=payload)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        name_receive = request.form["name_give"]
        about_receive = request.form["about_give"]
        new_doc = {
            "profile_name": name_receive,
            "profile_info": about_receive
        }
        if 'file_give' in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{username}.{extension}"
            file.save("./static/" + file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
        db.users.update_one({'username': payload['id']}, {'$set': new_doc})
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/write/<username>')
def write(username):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": username}, {'_id': False})
        return render_template('write.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload['id']})
        time_receive = request.form['time_give']
        tag_receive = request.form['tag_give']
        date_receive = request.form['date_give']
        blogbox_receive = request.form['blogbox_give']
        file = request.files['file_give']
        extension = file.filename.split('.')[-1]
        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M')
        filename = f'{user_info["username"]}-{mytime}'
        save_to = f'static/titleimg/{filename}.{extension}'
        file.save(save_to)
        doc = {
            'username': user_info["username"],
            'profile_name': user_info["profile_name"],
            'profile_pic_real': user_info["profile_pic_real"],
            'tag': tag_receive,
            'time': time_receive,
            'file': f'{filename}.{extension}',
            'date': date_receive,
            'blogbox': blogbox_receive
        }
        db.cards.insert_one(doc)
        return jsonify({"result": "success", 'msg': '저장 완료!'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/listing', methods=['GET'])
def listing():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username_receive = request.args.get("username_give")
        if username_receive == "":
            cards = list(db.cards.find({"stat": True}).sort("date", -1).limit(30))
        else:
            cards = list(db.cards.find({"username": username_receive}).sort("date", -1))
        for card in cards:
            card["_id"] = str(card["_id"])
            card_info = db.users.find_one({"username": card["username"]})
            card['profile_pic_real'] = card_info['profile_pic_real']
            card["count_heart"] = db.likes.count_documents({"card_id": card["_id"], "type": "heart"})
        return jsonify({"result": "success", 'cards': cards})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/hotsting', methods=['GET'])
def hotsting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        cards = list(db.cards.find({"stat": True}))
        for card in cards:
            card["_id"] = str(card["_id"])
            card_info = db.users.find_one({"username": card["username"]})
            card['profile_pic_real'] = card_info['profile_pic_real']
            card["count_heart"] = db.likes.count_documents({"card_id": card["_id"], "type": "heart"})
        hotcards = sorted(cards, key=lambda card: card["count_heart"], reverse=True)
        return jsonify({"result": "success", 'cards': cards, 'hotcards': hotcards})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/starsting', methods=['GET'])
def starsting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = payload['id']
        cards = list(db.cards.find({user: True}).sort("date", -1))
        for card in cards:
            card["_id"] = str(card["_id"])
            card_info = db.users.find_one({"username": card["username"]})
            card['profile_pic_real'] = card_info['profile_pic_real']
            card["count_heart"] = db.likes.count_documents({"card_id": card["_id"], "type": "heart"})
        return jsonify({"result": "success", 'cards': cards})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/searchsting', methods=['POST'])
def searchsting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        searchtext_receive = request.form['searchtext_give']
        print(searchtext_receive)
        cards = list(db.cards.find({"tag": {'$regex': searchtext_receive}}).sort("date", -1))
        print(cards)
        for card in cards:
            card["_id"] = str(card["_id"])
            card_info = db.users.find_one({"username": card["username"]})
            card['profile_pic_real'] = card_info['profile_pic_real']
            card["count_heart"] = db.likes.count_documents({"card_id": card["_id"], "type": "heart"})
        return jsonify({"result": "success", 'cards': cards})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/detail/<username>/<code>')
def detail(username, code):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": username})
        bson_id = ObjectId(code)
        card_info = db.cards.find_one({"_id": bson_id})
        card_info["_ide"] = str(card_info["_id"])
        card_info["heart_by_me"] = bool(
            db.likes.find_one({"card_id": card_info["_ide"], "type": "heart", "username": payload["id"]}))
        status = (card_info['username'] == payload['id'])
        myid = payload['id']
        return render_template('detail.html', user_info=user_info, card_info=card_info, status=status, myid=myid,
                               payload=payload)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/post_card', methods=['POST'])
def post_card():
    token_receive = request.cookies.get('mytoken')
    try:
        code_receive = request.form['code_give']
        type_receive = request.form['type_give']
        bson_id = ObjectId(code_receive)
        card_info = db.cards.find_one({"_id": bson_id})
        if type_receive == 'open':
            db.cards.update_one({'_id': bson_id}, {'$set': {'stat': True}})
        else:
            db.cards.update_one({'_id': bson_id}, {'$set': {'stat': False}})
        return jsonify({"result": "success"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/delete_card', methods=['POST'])
def delete_card():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        code_receive = request.form['code_give']
        bson_id = ObjectId(code_receive)
        db.cards.delete_one({"_id": bson_id})
        return jsonify({"result": "success", "msg": '삭제 완료!'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/update_type', methods=['POST'])
def update_type():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload['id']})
        card_id_receive = request.form["card_id_give"]
        type_receive = request.form["type_give"]
        action_receive = request.form["action_give"]
        bson_id = ObjectId(card_id_receive)
        if 'star' in type_receive:
            if action_receive == "like":
                db.cards.update_one({'_id': bson_id}, {'$set': {user_info['username']: True}})
            else:
                db.cards.update_one({'_id': bson_id}, {'$set': {user_info['username']: False}})
            return jsonify({"result": "success", 'msg': 'updated'})
        if 'heart' in type_receive:
            doc = {
                "card_id": card_id_receive,
                "username": user_info["username"],
                "type": type_receive
            }
            if action_receive == "like":
                db.likes.insert_one(doc)
            else:
                db.likes.delete_one(doc)
            count = db.likes.count_documents({"card_id": card_id_receive, "type": type_receive})
            return jsonify({"result": "success", 'msg': 'updated', "count": count})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
