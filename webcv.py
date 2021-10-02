from flask import Flask, render_template
import argparse
import base64
import os
import cv2
import math
import numpy as np

app = Flask(__name__)


def get_all_file_path_and_file_name(image_dir, show_image_num):
    file_path_list, file_name_list = [], []

    for _, _, all_file_names in os.walk(image_dir):
        for file_name in all_file_names:
            if '.jpg' or '.png' in file_name:
                file_path = os.path.join(image_dir, file_name)
                file_path_list.append(file_path)
                file_name_list.append(file_name)

    if show_image_num < len(file_path_list):
        np.random.seed(0)
        choose_idxs = np.random.choice(len(file_path_list), show_image_num)
        final_path_list, final_name_list = [], []
        for idx in choose_idxs:
            final_path_list.append(file_path_list[idx])
            final_name_list.append(file_name_list[idx])
    else:
        final_path_list, final_name_list = file_path_list, file_name_list

    return final_path_list, final_name_list


def get_image_stream(image_path, image_size, resize_type):
    image_stream = ''
    with open(image_path, 'rb') as img_file:
        image = img_file.read()
        image = cv2.imdecode(np.array(bytearray(image), dtype='uint8'),
                             cv2.IMREAD_UNCHANGED)
        origin_h, origin_w, _ = image.shape
        if resize_type == 'equal_hw':
            resize_hw = [image_size, image_size]
        elif resize_type == 'retinastyle':
            scales = (image_size, math.ceil(image_size * 1333. / 800))
            max_long_edge, max_short_edge = max(scales), min(scales)
            factor = min(max_long_edge / max(origin_h, origin_w),
                         max_short_edge / min(origin_h, origin_w))
            resize_hw = [
                math.ceil(origin_h * factor),
                math.ceil(origin_w * factor)
            ]
        elif resize_type == 'yolostyle':
            factor = image_size / max(origin_h, origin_w)
            resize_hw = [
                math.ceil(origin_h * factor),
                math.ceil(origin_w * factor)
            ]
        elif resize_type == 'keep_ratio_h':
            factor = image_size / origin_h
            resize_hw = [
                math.ceil(origin_h * factor),
                math.ceil(origin_w * factor)
            ]
        image = cv2.resize(image, (resize_hw[1], resize_hw[0]))
        if image_path.split(".")[-1] == 'jpg':
            image = np.array(cv2.imencode('.jpg', image)[1]).tobytes()
        elif image_path.split(".")[-1] == 'png':
            image = np.array(cv2.imencode('.jpg', image)[1]).tobytes()
        image_stream = base64.b64encode(image).decode()

    return image_stream


def parse_args():
    parser = argparse.ArgumentParser(description='webcv')
    parser.add_argument(
        '--image-dir',
        type=str,
        help='path for image folder,image type must be jpg or png')
    parser.add_argument('--show-mode', type=str, help='show image mode')
    parser.add_argument('--resize-type', type=str, help='resize type')
    parser.add_argument('--image-size',
                        type=int,
                        default=224,
                        help='image resize length')
    parser.add_argument('--show-image-num',
                        type=int,
                        default=10,
                        help='show image num')

    return parser.parse_args()


@app.route('/')
def show_all_images_on_web_page():
    args = parse_args()
    assert args.show_mode in [
        'equal_hw',
        'equal_h',
        'equal_h_right',
    ], 'wrong show mode!'
    assert args.resize_type in [
        'equal_hw',
        'retinastyle',
        'yolostyle',
        'keep_ratio_h',
    ], 'wrong resize type!'

    file_path_list, file_name_list = get_all_file_path_and_file_name(
        args.image_dir, args.show_image_num)

    image_infos = []
    for img_path, img_name in zip(file_path_list, file_name_list):
        img_stream = get_image_stream(img_path, args.image_size,
                                      args.resize_type)
        image_infos.append([img_stream, img_name[:-4]])

    if args.show_mode == 'equal_hw':
        return_template = render_template('equal_hw.html',
                                          image_infos=image_infos)
    elif args.show_mode == 'equal_h':
        return_template = render_template('equal_h.html',
                                          image_infos=image_infos)
    elif args.show_mode == 'equal_h_right':
        return_template = render_template('equal_h_right.html',
                                          image_infos=image_infos)

    return return_template


if __name__ == '__main__':
    # running on local host,access web page from local host
    app.run(debug=True, host='127.0.0.1', port=8080)
    # running on server,access web page from local host
    # app.run(debug=True, host='0.0.0.0', port=8080)

# --image-dir:path for image folder
# --show-mode:equal_hw,equal_h,equal_h_right
# --resize-type:equal_hw,retinastyle,yolostyle,keep_ratio_h
# --image-size:image resize length
# --show-image-num:show image num

# for classification
# python webcv.py --image-dir /home/zgcr/下载/WebCV/image --show-mode equal_hw --resize-type equal_hw  --image-size 224 --show-image-num 10

# for detection
# python webcv.py --image-dir /home/zgcr/下载/WebCV/image --show-mode equal_h --resize-type retinastyle  --image-size 400 --show-image-num 10
# python webcv.py --image-dir /home/zgcr/下载/WebCV/image --show-mode equal_h --resize-type yolostyle  --image-size 400 --show-image-num 10

# for ocr text recognition
# python webcv.py --image-dir /home/zgcr/下载/WebCV/image --show-mode equal_h_right --resize-type keep_ratio_h  --image-size 128 --show-image-num 10