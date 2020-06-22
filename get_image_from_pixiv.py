from pixivpy3 import *
import json
import argparse
import urllib
import os
import time
from key import Key_pixiv
from tqdm import tqdm
from baseclass_get_image import ArgParse_Base

class ArgParse(ArgParse_Base):
    def __init__(self):
        super().__init__(text='Pixivから画像を取得する。')

    def add_argument(self):
        self.parser.add_argument(
            '-n', '--name', nargs='*', default="Test", help="検索するワード（複数可）")
        self.parser.add_argument(
            '-p', '--number_of_page', default=0, help="取得する限界数（デフォルトは無限）")
        self.parser.add_argument('-d', '--directory', help="保存するディレクトリ")
        args = self.parser.parse_args()
        return args


class Pixiv:
    def __init__(self, args):
        self.api = PixivAPI()
        self.aapi = AppPixivAPI()
        key = Key_pixiv().sent_key_pixiv()
        self.api.login(key[0], key[1])
        self.aapi.login(key[0], key[1])
        self.args = args
        if not os.path.exists(self.args.directory):
            os.mkdir(self.args.directory)
    
    def get_image_from_pixiv(self):
        urls = []
        for keyword in self.args.name:
            #検索文字に一致するページ数を取得（Maxページ数がわからないので）
            results = self.api.search_works(query=keyword, page=1, period='all')
            amount_pages = min(self.args.number_of_page, results['pagination']['pages'])\
                if self.args.number_of_page > 0 else results['pagination']['pages']
            for i in range(1, amount_pages):
                results = self.api.search_works(query=keyword, page=i, period='all')
                for image in results['response']:
                    urls.append(image['image_urls']['large'])
        urls = list(set(urls))
        tqdm_bar = tqdm(urls)
        tqdm_bar.set_description("Downloading image... ")
        for url in tqdm_bar:
            self.aapi.download(url=url, path=self.args.directory)
            time.sleep(0.1)


if __name__ == "__main__":
    parser = ArgParse()
    args = parser.add_argument()
    pixiv = Pixiv(args)
    pixiv.get_image_from_pixiv()  
