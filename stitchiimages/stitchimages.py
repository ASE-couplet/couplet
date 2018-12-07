# -*- coding: utf-8 -*-
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def stitchimages_v1(image_path, poetry, QRcode_path, font_path, copyright, copyright_font_path, output_path):
    """

    :param image_path:
    :param poetry:
    :param QRcode_path:
    :param font_path:
    :param copyright:
    :param copyright_font_path:
    :param output_path:
    :return:
    """
    QR_size = 100
    if os.path.exists(image_path):
        img = Image.open(image_path)
        img_w, img_h = img.size
    else:
        raise RuntimeError('image path :{} not exists '.format(image_path))

    if os.path.exists(QRcode_path):
        QRcode = Image.open(QRcode_path)
        QRcode = resize_image(QRcode, (QR_size, QR_size))
    else:
        raise RuntimeError("QRcode path :{} not exists ".format(QRcode_path))

    poetry_image, poetry_font_size = poetry2image(poetry, font_path)
    poetry_w, poetry_h = poetry_image.size
    copyright_image= copyright2image(copyright, copyright_font_path)
    copyright_w, copyright_h = copyright_image.size
    assert poetry_h > QR_size + copyright_h, "poetry height should be larger than QRcode+copyright height"
    poetry_image.paste(copyright_image, (0, poetry_h - copyright_h))
    poetry_image.paste(QRcode, (poetry_w - QR_size, poetry_h - QR_size-copyright_h))

    assert img_w == 400 and poetry_w == 400 and copyright_w == 400, "check the width of image, poetry and copyright"

    total_w = img_w
    total_h = img_h + poetry_h + copyright_h
    final_img = Image.new('RGB', (total_w, total_h), "white")
    final_img.paste(img, (0, 0))
    final_img.paste(poetry_image, (0, img_h))

    final_img.show()
    # final_img.save(output_path)
    return final_img


def poetry2image(poetry, font_path=None):
    """
    :param poetry:
    :param font_path:
    :return:
    """
    font_size = 20
    sentences = poetry.split('\n')
    num_lines = len(sentences)

    total_h = (font_size) * (num_lines + 3)
    # total_h = max(200, total_h)
    # font_size = int(total_h / (num_lines + 2))

    image = Image.new("RGB", (400, int(total_h)), "white")
    draw = ImageDraw.Draw(image)

    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = None

    left_h = (total_h-num_lines*font_size)/2
    draw.multiline_text(xy=(font_size * 0.1, left_h), text=unicode(poetry, 'UTF-8'), fill=(0, 0, 0), font=font,
                        spacing=font_size * 0.2, align='left')
    del draw
    return image, font_size


def copyright2image(copyright, font_path=None):
    """
    :param copyright:
    :param font_path:
    :return:
    """
    length = len(copyright)
    font_size = 15
    total_h = (font_size) * 1.1

    image = Image.new("RGB", (400, int(total_h)), "white")
    draw = ImageDraw.Draw(image)

    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = None

    draw.multiline_text(xy=(font_size * 0.1, 0), text=unicode(copyright, 'UTF-8'), fill=(192, 192, 192), font=font,
                        align='left')
    del draw
    return image


def resize_image(img, size=(100, 100)):
    """
    :param img:
    :param size:
    :return:
    """
    try:
        if img.mode not in ('L', 'RGB'):
            img = img.convert('RGB')
        img = img.resize(size)
    except Exception, e:
        pass
    return img


if __name__ == "__main__":
    image_path = './im2.png'
    poetry = "一二三四五六七\n一二三四五六七\n一二三四五六七\n一二三四五六七"
    QRcode_path = './QR2.png'
    font_path = './fonts/fanti.TTF'
    output_path = '.'
    copyright = 'From PoemScape\n'
    copyright_font_path = './fonts/TEMPSITC.TTF'
    stitchimages_v1(image_path, poetry, QRcode_path, font_path, copyright, copyright_font_path, output_path)
