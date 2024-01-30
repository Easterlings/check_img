from flask import Flask, render_template
import os
from image import Image 
import json
app = Flask(__name__)

@app.route('/')
def image_list():
    root_dir = '/ssd/cjy/saiwei-wardrobe/static/img2img/'  # 替换为你的根目录路径

    dirs = []
    for dirpath, _, filenames in os.walk(root_dir):
        if dirpath == root_dir:
            continue  # 跳过根目录
        dirs.append(dirpath)

    return render_template('img2imgs.html', dirs=dirs)

@app.route('/img2img/<date>')
def info(date):
    # 获取图片
    image = Image()
    images = image.get_records_starting_with_date(date)
    new_images = []
    for image in images:
        json_str = image[4].replace("\n",",").replace(r'Lora hashes: "',r'Lora hashes: \"').replace(
            r'TI hashes: "',r'TI hashes: \"').replace(r'", TI hashes',r'\", TI hashes').replace(
            r'", Version',r'\", Version')
        # print(json_str)
        response_images = json.loads(json_str)

        output = [output['path'].replace('/ssd/cjy/saiwei-wardrobe', 'http://192.168.200.143:5550')
                   for output in response_images["output"]]

        input_image_path = response_images["input_image_path"].replace('/ssd/cjy/saiwei-wardrobe', 'http://192.168.200.143:5550')
        output_mask_path = response_images["output_mask_path"].replace('/ssd/cjy/saiwei-wardrobe', 'http://192.168.200.143:5550')
        
        new_tuple = (*image[:4], input_image_path, output_mask_path, output)
        new_images.append(new_tuple)

    return render_template('info.html', data=new_images)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)