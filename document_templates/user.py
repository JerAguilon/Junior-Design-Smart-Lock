import time
import calendar


class User(object):
    def __init__(
        self,
        id,
        email,
        name='',
        created_at=calendar.timegm(time.gmtime())
    ):
        self.id = id
        if not name:
            name = ''
        self.email = email
        self.name = name
        self.created_at = created_at

    def serialize(self):
        return {
            "email": self.email,
            "name": self.name,
            "createdAt": self.created_at,
        }

    @staticmethod
    def build(request_form):
        return User(
            id=request_form['id'],
            email=request_form['email'],
            name=request_form.get('name', ''),
        )

    @staticmethod
    def from_database(uid, json_dict):
        return User(
            id=uid,
            email=json_dict['email'],
            name=json_dict['name'],
            created_at=json_dict['createdAt']
        )
