import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['schedulify']
users = db['users']

class User():
    def __init__(self, first_name, last_name, email, password=None, password_hash=None):
        self.username = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = generate_password_hash(password) if password_hash is None else password_hash
        self.email = email
        self.uuid = self.generate_uuid()
        self.authenticated = False

        # make sure id is not already used
        while users.find_one({'_id': self.uuid}):
            self.uuid = self.generate_uuid()

    def generate_uuid(self):
        return str(uuid.uuid4())[:8]
    
    # careful with this method!!!
    def set_uuid(self, id):
        self.uuid = id

    def save(self):

        users.insert_one({
            '_id': self.uuid,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password_hash': self.password_hash,
            'email': self.email,
        })

    @staticmethod
    def get_user(user_id):
        user_res = users.find_one({'_id': user_id})
        user = User(user_res['first_name'], user_res['last_name'], user_res['email'], password_hash=user_res['password_hash'])
        user.set_uuid(user_res['_id'])
        return user
    
    @staticmethod
    def check_password(email, password):
        user_res = users.find_one({'username': email})
        
        if check_password_hash(user_res['password_hash'], password):
            user = User(user_res['first_name'], user_res['last_name'], user_res['email'], password_hash=user_res['password_hash'])
            user.set_uuid(user_res['_id'])
            user.authenticated = True
            return user
        return None
    
    def get_id(self):
        return self.uuid
    
    def is_authenticated(self):
        return self.authenticated
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False
