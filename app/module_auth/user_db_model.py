from app import db

class UserBase(db.Model):

    __abstract__ = True

    # User id
    id = db.Column(db.INTEGER, primary_key=True)


class UserStudent(UserBase):
    
    __tablename__ = 'Auth_students'

    # Student vpisna st.
    vpisna_st = db.Column(db.INTEGER)
   
    # Student name and last name
    name = db.Column(db.String(128))

    # Student email
    email = db.Column(db.String(64))

    def __int__(self, vpisna_st, name, email):

        self.name = name
        self.vpisna_st = vpisna_st
        self.email = email

