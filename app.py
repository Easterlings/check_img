from flask import Flask, render_template
import os
from db_img2img import db_Img2img 
from db_changebg import db_Changebg 
import json
from config import ROOT_DIR,PORT,image_path1,sw_url1,image_path2,sw_url2,image_path3,sw_url3,start_date
from utils import get_date_range
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/img2img')
def img2img_list():
    image = db_Img2img()
    date_num = image.get_date_num_starting_with_date()
    print(date_num)
    return render_template('img2img.html', datas=date_num)

@app.route('/changebg')
def change_bg_list():
    image = db_Changebg()
    date_num = image.get_date_num_starting_with_date()

    return render_template('changebg.html', datas=date_num)

@app.route('/img2img/<date>')
def info(date):
    # 获取图片
    image = db_Img2img()
    images = image.get_records_starting_with_date(date)
    new_images = []
    for image in images:
        json_str = image[4].replace("\n",",").replace(r'Lora hashes: "',r'Lora hashes: \"').replace(
            r'TI hashes: "',r'TI hashes: \"').replace(r'", TI hashes',r'\", TI hashes').replace(
            r'", Version',r'\", Version')
        # print(json_str)
        response_images = json.loads(json_str)

        # 替换图片路径为本地路径，以便在前端显示图片
        input_image_path = response_images["input_image_path"].replace(image_path1, sw_url1).replace(image_path2, sw_url2).replace(image_path3, sw_url3)
        output_mask_path = response_images["output_mask_path"].replace(image_path1, sw_url1).replace(image_path2, sw_url2).replace(image_path3, sw_url3)
        
        output = [output['path'].replace(image_path1, sw_url1).replace(image_path2, sw_url2).replace(image_path3, sw_url3)
                   for output in response_images["output"]]

        new_tuple = (*image[:4], input_image_path, output_mask_path, output)
        new_images.append(new_tuple)

    return render_template('img2img_info.html', data=new_images)

@app.route('/changebg/<date>')
def changebg_info(date):
    # 获取图片
    image = db_Changebg()
    images = image.get_records_starting_with_date(date)
    new_images = []
    for image in images:
        response_images = json.loads(image[5])
        request_data = json.loads(image[3])
        input_path = "" if not image[4] else image[4].replace(image_path1,sw_url1)
        output = [sw_url1+change_bg['change_bg_image']
                   for change_bg in response_images]
        new_tuple = (*image[:3],request_data, input_path, output)
        new_images.append(new_tuple)
        print(new_tuple)
    return render_template('changebg_info.html', data=new_images)


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=PORT)