import os
import json
import requests
from database import DB

class db_Changebg(DB):

    def __init__(self):
        super().__init__("change_bg")

    def get_data_one(self, data):
        r = super().get_data_one(data)
        return self._mapData(r)

    def get_data(self, data):
        result = super().get_data(data)
        r = []
        if result is not None:
            for item in result:
                r.append(self._mapData(item))
        return r

    def _mapData(self,data):
        return {
            'id':data[0],
            'user_name':data[1],
            'job_no':data[2],
            'request_data':data[3],
            'input_path':data[4],
            'response_images':data[5],
            'created_at':data[6].strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def get_images_list(images):
        return json.loads(images)

    @staticmethod
    def get_images_path(asin):
        return f"./images/{asin}/10_clothing/"

    def download_images(self, data):
        images_list = self.get_images_list(data['images'])
        path = self.get_images_path(data['asin'])
        for k in images_list:
            print(images_list[k])
            filename = path + k + '.jpg'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            img_content = requests.get(images_list[k]).content
            with open(filename, 'wb') as handler:
                handler.write(img_content)