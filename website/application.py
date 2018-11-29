# -*- coding: utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory, session
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit
from werkzeug import secure_filename
import logging
import random
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "uploader")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'secret!'
Bootstrap(app)
socketio = SocketIO(app)



def textImage(strs, sourceimage, color, savepath="./"):
    
    fp = open(sourceimage, "rb")
    im = Image.open(fp)
    out = im.resize((800, 600))
    textout = Image.new("RGB", (800, 600), "white")
    draw = ImageDraw.Draw(textout)
    fontSize = 50
    
    x = 700
    y = 20
    
    #设置字体，如果没有，也可以不设置
    font = ImageFont.truetype(os.path.join(os.getcwd(), "Fonts/STXINGKA.TTF"), fontSize)
    
    right = 0       #往右位移量
    down = 0        #往下位移量
    w = 500         #文字宽度（默认值）
    h = 500         #文字高度（默认值）
    row_hight = 0   #行高设置（文字行距）
    word_dir = 0    #文字间距

    for k,s2 in enumerate(strs):            
        if k == 0:
            w,h = font.getsize(s2)   #获取第一个文字的宽和高
        if s2 == "," or s2 == "\n" :  #换行识别
            right = right + w + row_hight
            down = 0
            continue
        else :
            down = down+h + word_dir          

        draw.text((x-right, y+down),s2,(0,0,0),font=font) #设置位置坐标 文字 颜色 字体
    
    del draw
    out = Image.blend(out, textout, 0.2)
    filename = "out.jpg"
    new_filename = os.path.join(savepath, filename)
    out.save(new_filename)
    im.close()
    fp.close()
    return filename
    
    
    
        

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
    # os.system("python ./tag2img/predict.py")
    os.system("python ./sleep.py")
    f = open("./result.txt", "r")
    strs = f.readlines()
    f.close()
    # strs = "往后余生,风雪是你,平淡是你,清贫也是你\n荣华是你,心底温柔是你,目光所致,也是你"
    print(strs)
    filename = textImage(strs, filename, (0, 0, 0), os.path.join(app.config['UPLOAD_FOLDER'], remote_ip + msg['randseed']))
    emit('response', {'data': filename, 'randseed': msg['randseed']})
    # return "<html> hello </html>"
    # os.system("python sleep.py")
    # # read result
    # 
    # 
    # return "url_for('/result/{}'.format(filename))"

if __name__ == '__main__':
    socketio.run(app)