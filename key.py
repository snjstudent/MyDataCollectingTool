class Base:
    def sent_key(self, key_list: list):
        return key_list


class Key_twitter(Base):
    def __init__(self):
        self.CONSUMER_KEY = ""
        self.CONSUMER_SECRET_KEY = ""
        self.ACCESS_TOKEN_KEY = ""
        self.ACCESS_TOKEN_SECRET_KEY = ""

    def sent_key_twitter(self):
        return super().sent_key([self.CONSUMER_KEY, self.CONSUMER_SECRET_KEY, self.ACCESS_TOKEN_KEY, self.ACCESS_TOKEN_SECRET_KEY])


class Key_pixiv(Base):
    def __init__(self):
        self.MAIL_ADDRESS = ""
        self.PASSWORD = ""

    def sent_key_pixiv(self):
        return super().sent_key([self.MAIL_ADDRESS, self.PASSWORD])
