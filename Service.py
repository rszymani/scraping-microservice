# -*- coding: utf-8 -*-
import html2text
import re
import string
import requests

from bs4 import BeautifulSoup as soup

from urllib.parse import urlparse


class Service:
    def get_html_text(self, url):
        r = requests.get(url)
        return r.text

    def extract_text_from_html(self, html):
        h = html2text.HTML2Text()
        h.wrap_links = False
        h.skip_internal_links = True
        h.inline_links = True
        h.ignore_anchors = True
        h.ignore_images = True
        h.ignore_emphasis = True
        h.ignore_links = True
        output_text = h.handle(html)
        output = re.sub(r'\w*\d\w*', ' ', output_text)
        urls_removed = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))
                                    +(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', output)
        exclude = set(string.punctuation)
        clear_text = ''.join(ch for ch in urls_removed if ch not in exclude)
        clear_text = re.sub('\s+' ,' ' ,clear_text )
        return clear_text.strip()

    def get_images_urls(self, html):
        soup_page = soup(html, features="html.parser")
        img_tags = soup_page.find_all('img')
        img_urls = []
        for img in img_tags:
            url = img.get('src', img.get('data-src'))
            if url:
                img_urls.append(url)
        return img_urls

    def download_images_content(self, site_url,  img_urls):
        netloc = urlparse(site_url).netloc
        scheme = urlparse(site_url).scheme
        site = "{}://{}".format(scheme, netloc)
        images = []
        for url in img_urls:
            filename = url[url.rfind("/")+1:]
            if any(x in filename for x in ['jpg', 'png', 'jpeg', 'tiff']):
                filename = re.sub("[^(A-Za-z.\-_0-9)]", "", filename)
                if 'http' not in url:
                    url = '{}{}'.format(site, url)
                img_response = requests.get(url)
                filename_image = (filename, img_response.content)
                images.append(filename_image)
        return images
