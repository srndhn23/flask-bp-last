from flask.templating import render_template
from application import app
from flask import render_template, request, redirect, url_for, session #, Response, flash
from flask_mysqldb import MySQLdb, MySQL
import bcrypt

# <CHATBOT>

import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
model = load_model('application/model.h5')
import json
import random

intents = json.loads(open('application/data.json').read())
words = pickle.load(open('application/texts.pkl','rb'))
classes = pickle.load(open('application/labels.pkl','rb'))
def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))
def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result
def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

app.static_folder = 'static'

@app.route("/chatbot")
def chatbot():
    if 'islogin' in session:
        return render_template("home/chatbot.html")
    else:
        return render_template("home/page-403.html")
    
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)

# </CHATBOT>


# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'islogin' in session:
        return redirect(url_for('index'))
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM admin WHERE username=%s",(username,))
        admin = curl.fetchone()
        curl.close()

        if admin is not None and len(admin) > 0 :
            if bcrypt.hashpw(password, admin['password'].encode('utf-8')) == admin['password'].encode('utf-8'):
                session['username'] = admin ['username']
                session['email'] = admin['email']
                session['islogin'] = True
                return redirect(url_for('index'))
            else :
                return render_template('accounts/login.html',
                               msg='Wrong user or password')
        else :
            return render_template('accounts/login.html',
                               msg='Wrong user or password')
    else: 
        return render_template("accounts/login.html")

@app.route("/index")
def index():
    if 'islogin' in session:
        return render_template("home/index.html")
    else:
        return render_template("home/page-403.html")
    

@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'islogin' in session:
        if request.method=='GET':
            return render_template('accounts/register.html')
        else :
            username = request.form['username']
            no_identitas = request.form['no_identitas']
            nama = request.form['nama']
            gender = request.form['gender']
            no_hp = request.form['no_hp']
            email = request.form['email']
            tanggal_lahir = request.form['tanggal_lahir']
            alamat = request.form['alamat']
            tanggal_masuk = request.form['tanggal_masuk']
            password = request.form['password'].encode('utf-8')
            hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO admin (username, no_identitas, nama, gender, no_hp, email, tanggal_lahir, alamat, tanggal_masuk, password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (username, no_identitas, nama, gender, no_hp, email, tanggal_lahir, alamat, tanggal_masuk, hash_password)) 
            mysql.connection.commit()
            session['username'] = request.form['username']
            session['email'] = request.form['email']
            return redirect(url_for('admin'))
    else:
        return render_template("home/page-403.html")

@app.route("/masuk")
def masuk():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data_masuk")
    masuk = cur.fetchall()
    cur.close()
    
    if 'islogin' in session:
        return render_template("home/masuk.html", masuk=masuk)
    else:
        return render_template("home/page-403.html")

@app.route("/laporanmasuk")
def laporanmasuk():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `data_masuk` WHERE waktu_masuk BETWEEN CAST( CONCAT(CURDATE(), ' ', '08:00:00') AS DATETIME ) AND NOW()")
    laporanmasuk = cur.fetchall()
    cur.close()
    
    if 'islogin' in session:
        return render_template("home/laporanmasuk.html", laporanmasuk=laporanmasuk)
    else:
        return render_template("home/page-403.html")

@app.route("/keluar")
def keluar():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data_keluar")
    keluar = cur.fetchall()
    cur.close()
    
    if 'islogin' in session:
        return render_template("home/keluar.html", keluar=keluar)
    else:
        return render_template("home/page-403.html")
    
@app.route("/laporankeluar")
def laporankeluar():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `data_keluar` WHERE waktu_keluar BETWEEN CAST( CONCAT(CURDATE(), ' ', '08:00:00') AS DATETIME ) AND CAST( CONCAT(CURDATE(), ' ', '16:00:00') AS DATETIME )")
    laporankeluar = cur.fetchall()
    cur.close()
    
    if 'islogin' in session:
        return render_template("home/laporankeluar.html", laporankeluar=laporankeluar)
    else:
        return render_template("home/page-403.html")

@app.route("/admin")
def admin():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin")
    admin = cur.fetchall()
    cur.close()
    
    if 'islogin' in session:
        return render_template("home/admin.html", admin=admin)
    else:
        return render_template("home/page-403.html")

@app.route("/user")
def user():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user")
    user = cur.fetchall()
    cur.close()
    
    if 'islogin' in session:
        return render_template("home/user.html", user=user)
    else:
        return render_template("home/page-403.html")

@app.route("/userregister", methods=['GET', 'POST'])
def userregister():
    if 'islogin' in session:
        if request.method=='GET':
            return render_template('home/userregister.html')
        else :
            username = request.form['username']
            no_identitas = request.form['no_identitas']
            nama = request.form['nama']
            gender = request.form['gender']
            status = request.form['status']
            no_hp = request.form['no_hp']
            email = request.form['email']
            alamat = request.form['alamat']
            no_plat = request.form['no_plat']
            tanggal_masuk = request.form['tanggal_masuk']
            password = request.form['password'].encode('utf-8')
            hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user (username, no_identitas, nama, gender, status, no_hp, email, alamat, no_plat, tanggal_masuk, password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (username, no_identitas, nama, gender, status, no_hp, email, alamat, no_plat, tanggal_masuk, hash_password)) 
            mysql.connection.commit()
            return redirect(url_for('user'))
    else:
        return render_template("home/page-403.html")

# @app.route("/profile")
# def profile():
#     if 'islogin' in session:
#         return render_template("home/profile.html")
#     else:
#         return render_template("home/page-403.html")

@app.route("/realtime")
def realtime():
    if 'islogin' in session:
        return render_template("home/uploadrealtime.html")
    else:
        return render_template("home/page-403.html")

@app.route("/logout")
def logout():
    session.pop('islogin', None)
    session.pop('username', None)
    return render_template("accounts/login.html")

# @app.route("/coba")
# def coba():
#     return render_template("accounts/coba.html")

# delete
    
@app.route("/deletemasuk/<string:id>", methods=['GET', 'POST'])
def deletemasuk(id):
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM data_masuk WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('masuk'))

@app.route("/deletekeluar/<string:id>", methods=['GET', 'POST'])
def deletekeluar(id):
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM data_keluar WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('keluar'))

@app.route("/deleteadmin/<string:id>", methods=['GET', 'POST'])
def deleteadmin(id):
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM admin WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('admin'))

@app.route("/deleteuser/<string:id>", methods=['GET', 'POST'])
def deleteuser(id):
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM user WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('user'))

# update
@app.route("/updateadmin", methods=['GET', 'POST'])
def updateadmin():  
    if request.method=='POST':
        id = request.form['id']
        username = request.form['username']
        no_identitas = request.form['no_identitas']
        nama = request.form['nama']
        gender = request.form['gender']
        no_hp = request.form['no_hp']
        email = request.form['email']
        tanggal_lahir = request.form['tanggal_lahir']
        alamat = request.form['alamat']
        tanggal_masuk = request.form['tanggal_masuk']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE admin SET username=%s, no_identitas=%s, nama=%s, gender=%s, no_hp=%s, email=%s, tanggal_lahir=%s, alamat=%s, tanggal_masuk=%s WHERE id=%s", (username, no_identitas, nama, gender, no_hp, email, tanggal_lahir, alamat, tanggal_masuk,id))
        
        mysql.connection.commit()
        return redirect(url_for('admin'))

@app.route("/updateuser", methods=['GET', 'POST'])
def updateuser():
    if request.method=='POST':
        id = request.form['id']
        username = request.form['username']
        no_identitas = request.form['no_identitas']
        nama = request.form['nama']
        gender = request.form['gender']
        status = request.form['status']
        no_hp = request.form['no_hp']
        email = request.form['email']
        alamat = request.form['alamat']
        tanggal_masuk = request.form['tanggal_masuk']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE user SET username=%s, no_identitas=%s, nama=%s, gender=%s, status=%s, no_hp=%s, email=%s, alamat=%s, tanggal_masuk=%s WHERE id=%s", (username, no_identitas, nama, gender, status ,no_hp, email, alamat, tanggal_masuk,id,))
        mysql.connection.commit()
        return redirect(url_for('user'))