import unittest
import sys
import os

import shutil

from API import Service
from API import Storage
from API import app
sys.path.append('.')


class ServiceTests(unittest.TestCase):

    def setUp(self):
        self.service = Service()
        self.base_path = os.path.dirname(os.path.abspath("."))

    def test_extract_text_from_html(self):
        html = '''<html>
                    <body>
                        <h2>Images on Another Server</h2>
                        <img src="https://www.w3schools.com/images/w3schools_green.jpg" alt="W3Schools.com" style="width:104px;height:142px;">
                        <img data-src="https://www.wprost.pl/_thumb/eb/0a/916ecd6cd846ccd9b4bbc8bbe1ea.jpeg" style="width:104px;height:142px;">
                        <p title="I'm a tooltip">
                            Mouse over this paragraph, to display the title attribute as a tooltip.
                        </p>
                    </body>
                </html>'''
        self.assertEqual(self.service.extract_text_from_html(html), "Images on Another Server Mouse over this paragraph to display the title attribute as a tooltip")

    def test_get_images_urls(self):
        html = '''<html>
                    <body>
                        <h2>Images on Another Server</h2>
                        <img src="https://www.w3schools.com/images/w3schools_green.jpg" alt="W3Schools.com" style="width:104px;height:142px;">
                        <img data-src="https://www.wprost.pl/_thumb/eb/0a/916ecd6cd846ccd9b4bbc8bbe1ea.jpeg" style="width:104px;height:142px;">
                        <p title="I'm a tooltip">
                            Mouse over this paragraph, to display the title attribute as a tooltip.
                        </p>
                    </body>
                </html>'''
        self.assertEqual(self.service.get_images_urls(html)[0],
                         "https://www.w3schools.com/images/w3schools_green.jpg")
        self.assertEqual(self.service.get_images_urls(html)[1],
                         "https://www.wprost.pl/_thumb/eb/0a/916ecd6cd846ccd9b4bbc8bbe1ea.jpeg")


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.storage = Storage()
        self.base_path = os.path.dirname(os.path.abspath("."))

    def tearDown(self):
        try:
            os.remove("{}/scraped_resources/texts/test_text.txt".format(self.base_path))
            os.rmdir("{}/scraped_resources/images/test_dir/".format(self.base_path))
            shutil.rmtree("{}/scraped_resources/images/test_save_images/".format(self.base_path), ignore_errors=True)
        except OSError as why:
            print("Not cleaned directory")

    def test_create_images_dir(self):
        directory_path = 'test_dir'
        self.storage.create_images_dir(directory_path)
        self.assertTrue(os.path.exists("{}/scraped_resources/images/{}".format(self.base_path, directory_path)))

    def test_save_txt_file(self):
        text_text_id = "test_text"
        text = "TEST TEXT"
        self.storage.save_txt_file(text, text_text_id)
        self.assertTrue(os.path.exists('{}/scraped_resources/texts/{}.txt'.format(self.base_path, text_text_id)))

    def test_read_text_from_disk(self):
        uuid_text = "2bcb8601-9075-477e-93f1-450f8f30592a"
        text = "Wyszukiwarka Grafika Mapy Play YouTube Wiadomości Gmail Dysk Więcej » Historia online Ustawienia" \
               " Zaloguj się Szukanie zaawansowaneNarzędzia językowe Reklamuj się w " \
               "GoogleRozwiązania dla firmWszystko o GoogleGooglecom C Prywatność Warunki"
        self.assertEqual(self.storage.read_text_from_disk(uuid_text), text)

    def test_list_all_images_dir(self):
        example_ids = ["00554e7f-44cb-4675-a955-39fc065bb212"]
        images_ids = self.storage.list_all_images_ids()
        self.assertTrue(all(elem in images_ids for elem in example_ids))

    def test_list_all_images_ids(self):
        images_id = "00554e7f-44cb-4675-a955-39fc065bb212"
        images_names = self.storage.list_all_images_dir(images_id)
        example_imgs = ["1s6EApbU7HMxJM5CiOnPsn-w132-h132.jpg", "6fw3VjPmUpBZQcTzD4jcA5-w132-h132.jpg",
                        "7PwTVOCJNsFOAhookAa3Rg-w132-h132.png", "20xIWaNoTy4wQEraayzh3v-w990-h170.png"]
        self.assertTrue(all(elem in images_names for elem in example_imgs ))

    def test_list_all_text_ids(self):
        example_texts = ["64af356b-782d-47a2-95c8-09f5ebbd2151", "6766e616-e48d-4a3b-a262-a4ff81328ede"]
        images_ids = self.storage.list_all_text_ids()
        self.assertTrue(all(elem in images_ids for elem in example_texts))

    def test_get_image_path(self):
        uuid_images = "00554e7f-44cb-4675-a955-39fc065bb212"
        image = "1s6EApbU7HMxJM5CiOnPsn-w132-h132.jpg"
        path = "{}/scraped_resources/images/00554e7f-44cb-4675-a955-39fc065bb212/1s6EApbU7HMxJM5CiOnPsn-w132-h132.jpg"\
            .format(self.base_path)
        self.assertEqual(self.storage.get_image_path(uuid_images, image), path)
        self.assertFalse(self.storage.get_image_path("does_not_exists", ""))


if __name__ == '__main__':
    unittest.main()
