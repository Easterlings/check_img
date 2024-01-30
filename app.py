from flask import Flask, render_template
import os
from image import Image 
app = Flask(__name__)

@app.route('/')
def image_list():
    root_dir = '/ssd/cjy/saiwei-wardrobe/static/img2img/'  # 替换为你的根目录路径

    dirs = []
    for dirpath, _, filenames in os.walk(root_dir):
        # for filename in filenames:
        # if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        dirs.append(dirpath)

    return render_template('img2imgs.html', dirs=dirs)

@app.route('/img2img/<date>')#date = "2023-11-09"
def info(date):
    # 获取图片
    image = Image()
    p_info = image.get_records_starting_with_date(date)
    return render_template('info.html', data=p_info)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)