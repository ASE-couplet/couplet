# -*- coding: utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory, session
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit
from werkzeug import secure_filename
import logging

from textImage import textImage

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'secret!'
Bootstrap(app)
socketio = SocketIO(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/index', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # file_url = url_for('uploaded_file', filename=filename)
            # s = "result"
            # filename = filename.split(".")[0]
            # strs = "往后余生,风雪是你,平淡是你,清贫也是你\n荣华是你,心底温柔是你,目光所致,也是你"
            # filename = textImage(strs, filename, (0, 0, 0))
            return render_template("uploader.html", filename=filename)
    return render_template("index_new.html")

@app.route('/result/<filename>')
def result(filename):
    file_url = url_for('uploaded_file', filename=filename)
    sentence = "show_result"
    return render_template("result.html", file_url=file_url, sentence=sentence)


@socketio.on('image_url')
def process_msg(msg):
    # image_url = msg['data']
    logging.info("runnnnnnnnn")
    print('ttest')

    return "<html> hello </html>"
    # os.system("python sleep.py")
    # # read result
    # strs = "往后余生,风雪是你,平淡是你,清贫也是你\n荣华是你,心底温柔是你,目光所致,也是你"
    # filename = textImage(strs, filename, (0, 0, 0))
    # return "url_for('/result/{}'.format(filename))"

if __name__ == '__main__':
    print('test')
    socketio.run(app, host='127.0.0.1')