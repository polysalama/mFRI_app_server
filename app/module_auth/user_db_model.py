from app import db


# Abstract Base model
class UserBaseModel(db.Model):

    __abstract__ = True

    # User id
    id = db.Column(db.INTEGER, primary_key=True)
    # Moodle user token
    token = db.Column(db.String(64))
    # Moodle role
    token = db.Column(db.String(64))

# Users model
class UserModel(UserBaseModel):
    
    __tablename__ = 'mod_users_users'

    # Student vpisna st.
    vpisna_st = db.Column(db.INTEGER)
    # Student name and last name
    name = db.Column(db.String(128))
    # Student email
    email = db.Column(db.String(64))

    def __int__(self, vpisna_st, name, email, token):

        self.name = name
        self.vpisna_st = vpisna_st
        self.email = email
        self.token = token

db.create_all()
