# -*- coding: utf-8 -*-
import os
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


def textImage(strs, sourceimage, color, savepath="./"):
    im = Image.open(sourceimage)
    out = im.resize((800, 600))
    textout = Image.new("RGB", out.size, "white")
    im.close()
    draw = ImageDraw.Draw(textout)
    fontSize = 50
    
    x = 700
    y = 20
    
    #设置字体，如果没有，也可以不设置
    font = ImageFont.truetype("./Fonts/STXINGKA.TTF", fontSize)
    
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
        # print("序号-值",k,s2)
        # print("宽-高",w,h)
        # print("位移",right,down)
        # print("坐标",x+right, y+down)
        draw.text((x-right, y+down),s2,(0,0,0),font=font) #设置位置坐标 文字 颜色 字体
    
    del draw
    out = Image.blend(out, textout, 0.2)
    filename = "out.jpg"
    new_filename = os.path.join(savepath, filename)
    out.save(new_filename)
    return filename

if __name__ == "__main__":
    #初始化字符串
    strs = "往后余生,风雪是你,平淡是你,清贫也是你\n荣华是你,心底温柔是你,目光所致,也是你"
    #模板图片
    imageFile = ".\\test.jpg"
    #新文件保存路径
    file_save_dir = ".\\"
    out = textImage(strs, imageFile, (0, 0, 0))
