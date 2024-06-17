from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)  # Store password directly
    

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password
    
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(int(user_id))
