# -*- coding: utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory, session
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit
from werkzeug import secure_filename
import logging
import random
from img2tag import img2tag
import sys
from flask import redirect
# sys.path.append(os.path.join(sys.path[0], "predict_couplet"))
sys.path.append(os.path.join(sys.path[0], "predict_poetry"))
import PIL
from PIL import Image
from stitchimages import stitchimages_v1
import time

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "uploader")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'secret!'
Bootstrap(app)
socketio = SocketIO(app)

# from web_test import Main_Poetry_maker
# maker = Main_Poetry_maker()

from web_test_poem import Main_Poetry_maker as Poetry_maker
Poetry = Poetry_maker()
    
def img_compress(file_path):
    img = Image.open(file_path)
    w, h = img.size
    new_w = 400
    new_h = int(h * 400 / w)
    new_img = img.resize((new_w, new_h))
    name, ext = os.path.splitext(file_path)
    new_file_path = name + "_compressed" + ext
    new_img.save(new_file_path)
    return os.path.basename(new_file_path)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/AboutUs")
def AboutUs():
    return render_template("AboutUs.html")

@app.route("/FeedBack", methods=['POST', 'GET'])
def FeedBack():
    if request.method == "POST":
        return redirect('/index')
    return render_template("FeedBack.html")
    
@app.route('/uploads/<filename>/<randseed>')
def uploads(filename, randseed):
    remote_ip = request.remote_addr + randseed
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'],remote_ip),
                               filename)


@app.route('/jueju_submit/<filename>/<randseed>', methods=['GET', 'POST'])
def jueju_submit(filename, randseed):
    if request.method == 'POST':
        remote_ip = request.remote_addr + randseed
        poetry = request.form.get("jueju_display")
        image_path = "/home/site/wwwroot/uploader/" + remote_ip + '/' + filename
        QRcode_path = "/home/site/wwwroot/static/image/QRcode.png"
        font_path = "/home/site/wwwroot/static/fonts/STFANGSO.TTF"
        output_path = "/home/site/wwwroot/uploader/" + remote_ip + '/final.jpg'
        copyright = '来自 PoetScape\n'
        copyright_font_path = '/home/site/wwwroot/static/fonts/text.TTF'
        stitchimages_v1(image_path, poetry, QRcode_path, font_path, copyright, copyright_font_path, output_path)
        return redirect(url_for('uploads', filename="final.jpg", randseed=randseed))


@app.route('/duilian_submit/<filename>/<randseed>', methods=['GET', 'POST'])
def duilian_submit(filename, randseed):
    if request.method == 'POST':
        remote_ip = request.remote_addr + randseed
        poetry = request.form.get("duilian_display")
        image_path = "/home/site/wwwroot/uploader/" + remote_ip + '/' + filename
        QRcode_path = "/home/site/wwwroot/static/image/QRcode.png"
        font_path = "/home/site/wwwroot/static/fonts/STFANGSO.TTF"
        output_path = "/home/site/wwwroot/uploader/" + remote_ip + '/final.jpg'
        copyright = '来自 PoetScape\n'
        copyright_font_path = '/home/site/wwwroot/static/fonts/text.ttf'
        stitchimages_v1(image_path, poetry, QRcode_path, font_path, copyright, copyright_font_path, output_path)
        return redirect(url_for('uploads', filename="final.jpg", randseed=randseed))

@app.route('/index', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            remote_ip = request.remote_addr
            randseed = str(random.randint(100, 10000))
            remote_ip = remote_ip + randseed
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], remote_ip))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], remote_ip, filename))
            filename=img_compress(os.path.join(app.config['UPLOAD_FOLDER'], remote_ip, filename))
            return render_template("uploader.html", filename=filename, randseed=randseed)
    return render_template("welcome.html")

@app.route('/result/<filename>/<randseed>', methods=['GET', 'POST'])
def result(filename, randseed):
    remote_ip = request.remote_addr
    if request.method == "POST":
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            remote_ip = request.remote_addr
            randseed = str(random.randint(100, 10000))
            remote_ip = remote_ip + randseed
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], remote_ip))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], remote_ip, filename))
            filename=img_compress(os.path.join(app.config['UPLOAD_FOLDER'], remote_ip, filename))
            return render_template("uploader.html", filename=filename, randseed=randseed)
    
    with open("/home/site/wwwroot/uploader/" + remote_ip + randseed + "/strs.txt", "r") as f:
        strs = f.readlines()
    strs = "\n".join(strs)
    file_url = "https://poempicture.azurewebsites.net/uploads/" + filename + "/" + randseed

    return render_template("result.html", file_url=file_url, sentence=strs, filename=filename, randseed=randseed)

@app.route('/test')
def test():
    return render_template("uploader.html", filename="daf", randseed="12312")


@socketio.on('image_url')
def process_msg(msg):
    remote_ip = request.remote_addr
    # filename = os.path.join(app.config['UPLOAD_FOLDER'], remote_ip + msg['randseed'], msg['data'])
    # os.system("python tag2img/predict.py &")
    # os.system("start python sleep.py")
    file_url = "https://poempicture.azurewebsites.net/uploads/" + msg["data"] + "/" + msg["randseed"]
    savepath = "/home/site/wwwroot/uploader/" + remote_ip + msg["randseed"] + "/" + "result.txt"
    # keywords = img2tag(file_url)
    os.system("python get_tag.py -f {} -p {} &".format(file_url, savepath))
    emit('wait', {'data': msg['data'], 'randseed': msg['randseed'], 'status':False})

@socketio.on('inquiry')
def inquiry_for_result(msg):
    remote_ip = request.remote_addr
    result_path = "/home/site/wwwroot/uploader/" + remote_ip + msg["randseed"] + "/" + "result.txt"
    if os.path.isfile(result_path):
        f = open(result_path, "r")
        keywords = f.readline()
        f.close()
        strs = Poetry.predict(keywords)
        f = open("/home/site/wwwroot/uploader/" + remote_ip + msg["randseed"] + "/strs.txt", "w")
        f.writelines(strs)
        f.close()
        # filename = os.path.join(app.config['UPLOAD_FOLDER'], remote_ip + msg['randseed'], msg['data'])
        # filename = textImage(strs, filename, (0, 0, 0), os.path.join(app.config['UPLOAD_FOLDER'], remote_ip + msg['randseed']))
        emit('response', {'data': msg['data'], 'randseed': msg['randseed']})
    else:
        time.sleep(1)
        emit('wait', {'data': msg['data'], 'randseed': msg['randseed'], 'status':False})

# @socketio.on('jump')
# def jump(msg):
#     return redirect(url_for('result', filename=msg['filename'], randseed=msg['randseed']))

if __name__ == '__main__':
    socketio.run(app)