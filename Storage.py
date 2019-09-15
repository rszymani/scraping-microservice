# -*- coding: utf-8 -*-
import re
import requests

import os


class Storage:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))

    def create_images_dir(self, images_id):
        images_dir = "{}/scraped_resources/images/{}".format(self.base_path,images_id)
        if not os.path.isdir(images_dir):
            os.mkdir(images_dir)

    def save_txt_file(self, text, text_id):
        with open('{}/scraped_resources/texts/{}.txt'.format(self.base_path,text_id), 'w', encoding='utf8') as file:
            file.write(text)

    def save_images(self, images, images_id):
        self.create_images_dir(images_id)
        for filename, image in images:
            with open("{}/scraped_resources/images/{}/{}".format(self.base_path, images_id, filename), 'wb') as f:
                f.write(image.content)

    def read_text_from_disk(self, text_id):
        file_name = "{}/scraped_resources/texts/{}.txt".format(self.base_path, text_id)
        if not os.path.isfile(file_name):
            return None
        with open(file_name, 'r', encoding='utf8') as f:
            file_content = f.read()
        return file_content

    def list_all_images_dir(self, images_id):
        images_id_dir = "{}/scraped_resources/images/{}/".format(self.base_path, images_id)
        print(images_id_dir)
        if not os.path.isdir(images_id_dir):
            return None
        return os.listdir(images_id_dir)

    def list_all_images_ids(self):
        images_dir = "{}/scraped_resources/images".format(self.base_path)
        if not os.path.isdir(images_dir):
            return None
        return os.listdir(images_dir)

    def list_all_text_ids(self):
        text_dir = "{}/scraped_resources/texts".format(self.base_path)
        if not os.path.isdir(text_dir):
            return None
        ids = [file[:-4] for file in os.listdir(text_dir)]
        return ids

    def get_image_path(self, images_id, image):
        image_path = "{}/scraped_resources/images/{}/{}".format(self.base_path,images_id,image)
        if not os.path.isfile(image_path):
            return None
        return image_path
