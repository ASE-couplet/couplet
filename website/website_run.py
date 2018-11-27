# -*- coding: utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory, session
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit
from werkzeug import secure_filename
import logging
import random

from textImage import textImage

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "uploader")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'secret!'
Bootstrap(app)
socketio = SocketIO(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    
@app.route('/uploads/<filename>/<randseed>')
def uploaded_file(filename, randseed):
    remote_ip = request.remote_addr + randseed
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'],remote_ip),
                               filename)


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
            return render_template("uploader.html", filename=filename, randseed=randseed)
    return render_template("index_new.html")

@app.route('/result/<filename>/<randseed>')
def result(filename, randseed):
    file_url = url_for('uploaded_file', filename=filename, randseed=randseed)
    sentence = "show_result"
    return render_template("result.html", file_url=file_url, sentence=sentence)


@socketio.on('image_url')
def process_msg(msg):
    remote_ip = request.remote_addr
    filename = os.path.join(app.config['UPLOAD_FOLDER'], remote_ip + msg['randseed'], msg['data'])
    os.system("python sleep.py")
    strs = "往后余生,风雪是你,平淡是你,清贫也是你\n荣华是你,心底温柔是你,目光所致,也是你"
    filename = textImage(strs, filename, (0, 0, 0), os.path.join(app.config['UPLOAD_FOLDER'], remote_ip + msg['randseed']))
    emit('response', {'data': filename, 'randseed': msg['randseed']})
    # return "<html> hello </html>"
    # os.system("python sleep.py")
    # # read result
    # 
    # 
    # return "url_for('/result/{}'.format(filename))"

if __name__ == '__main__':
    print('test')
    socketio.run(app, host='127.0.0.1')