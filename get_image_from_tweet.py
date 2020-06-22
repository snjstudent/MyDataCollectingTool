import tweepy
import argparse
import urllib
import os
import time
from key import Key_twitter 
from tqdm import tqdm
from baseclass_get_image import ArgParse_Base

class ArgParse(ArgParse_Base):
    def __init__(self):
        super().__init__(text='ツイートから画像を取得')

    def add_argument(self):
        self.parser.add_argument('-n', '--name', nargs='*', default="Test", help="検索するワード（複数可）")
        self.parser.add_argument('-p', '--number_of_page', default=0, help="取得する限界数（デフォルトは無限）")
        self.parser.add_argument('-d', '--directory', help="保存するディレクトリ")
        args = self.parser.parse_args()
        return args
        

class Tweet:
    def __init__(self, args):
        CONSUMER_KEY, CONSUMER_SECRET_KEY, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET_KEY = Key_twitter().sent_key_twitter()
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET_KEY)
        self.api = tweepy.API(auth)
        self.args = args
        if not os.path.exists(self.args.directory):
            os.mkdir(self.args.directory)


    def __download_image(self, url):
        time.sleep(0.1)
        self.urls_downloaded.append(url)
        url_orig = url + ":orig"
        file_name = url.split('/')[-1]
        save_path = self.args.directory + "/" + file_name
        try:
            responce = urllib.request.urlopen(url)
            with open(save_path, "wb") as f:
                f.write(responce.read())
        except Exception as e:
            print("Can't download image because : " + e)
        
        
    def get_image_from_tweet(self):
        urls = []
        max_id = 0
        for keyword in self.args.name:
            tqdm_bar = tqdm(range(1, int(self.args.number_of_page)))
            tqdm_bar.set_description("Getting url... ")
            for i in tqdm_bar:
                search_result = self.api.search(q=keyword, max_id=max_id)
                for result in search_result:
                    if 'media' in result.entities:
                        for media in result.entities['media']:
                            url = media['media_url_https']
                max_id = result.id
                time.sleep(0.1)
        urls = list(set(urls))
        tqdm_bar = tqdm(urls)
        tqdm_bar.set_description("Downloading image... ")
        for url in tqdm_bar:
            self.__download_image(url)

if __name__ == "__main__":
    parser = ArgParse()
    args = parser.add_argument()
    tweet = Tweet(args)
    tweet.get_image_from_tweet()
    

        


