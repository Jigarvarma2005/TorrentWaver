import pymongo
import secrets
import datetime

class MongoDB(object):
    def __init__(self, db_url):
        self.client = pymongo.MongoClient(db_url)
        self.client = self.client["TorrentWaver"]
        self.user_logins = self.client["user_logins"]
        self.user_cookies = self.client["user_cookies"]
        self.user_cookies.create_index(
                "expire_at", 
                expireAfterSeconds=3600
            )
    
    def get_all_logins(self):
        return self.user_logins.find({})
    
    def validate_login(self, username, password):
        return bool(
            is_exist := self.user_logins.find_one(
                {"uname": username, "pass": password}
            )
        )
    
    def new_login(self, username, password):
        self.user_logins.insert_one({"uname": username, "pass": password})
    
    def delete_login(self, username, password):
        self.user_logins.delete_many({"uname": username, "pass": password})
        self.delete_cookies(username)
    
    def save_cookies(self, username):
        expire_at = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        uid = secrets.token_hex(16)
        self.user_cookies.insert_one({"username": username,
                                      "uid": uid,
                                      "expire_at": expire_at})
        return uid
    
    def get_cookies(self, uid):
        if is_exist := self.user_cookies.find_one({"uid": uid}):
            return is_exist
        return False
    
    def delete_cookies(self, username):
        self.user_cookies.delete_many({"username": username})