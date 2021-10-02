   * [My ZhiHu column](#my-zhihu-column)
   * [Requirements](#requirements)
   * [How to use WebCV](#How-to-use-WebCV)
   * [Citation](#citation)

# WebCV: a tool for displaying images on a local web page
This is the implementation of WebCV.It's a useful tool for displaying multiple images on a local web page.To use WebCV, you must install python and flask.

# Requirements

```
python3
flask==2.0.1
```

# How to use WebCV
If you want to running WebCV and visit web page on the same host:
```
# add this code under if __name__ == '__main__':
app.run(debug=True, host='127.0.0.1', port=8080)
```

If you want to running WebCV on a server,and visit web page from another client host:
```
# add this code under if __name__ == '__main__':
app.run(debug=True, host='0.0.0.0', port=8080)
```

Get image folder path,and run the following command:
for classification:
```
python webcv.py --image-dir folder_path --show-mode equal_hw --resize-type equal_hw  --image-size 224 --show-image-num 10
```
for detection:
```
python webcv.py --image-dir folder_path --show-mode equal_h --resize-type retinastyle/yolostyle  --image-size 400 --show-image-num 10
```
for ocr text recognition:
```
python webcv.py --image-dir folder_path --show-mode equal_h_right --resize-type keep_ratio_h  --image-size 128 --show-image-num 10
```

--image-dir:path for image folder
--show-mode:equal_hw,equal_h,equal_h_right
--resize-type:equal_hw,retinastyle,yolostyle,keep_ratio_h
--image-size:image resize length
--show-image-num:show image num


Then open the browser and jump to the URL given in the command line:
```
# for example
http://127.0.0.1:8080/
```
You will see all images in the folder are displayed on the web page(The web page can also be zoomed).Enjoy it!

# Citation

If you find my work useful in your research, please consider citing:
```
@inproceedings{zgcr,
 title={WebCV},
 author={zgcr},
 year={2021}
}
```