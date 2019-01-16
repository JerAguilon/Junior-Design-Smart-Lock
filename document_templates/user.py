import time
import calendar

from utils.decorators import require_fields

class User(object):
    def __init__(
        self,
        email,
        name='',
        created_at=calendar.timegm(time.gmtime())
    ):
        if not name:
            name = ''
        self.email = email
        self.name = name
        self.created_at = created_at

    def serialize(self):
        return {
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at,
        }

    @staticmethod
    @require_fields(['email', 'name', 'tokens'])
    def build(request_form):
        return User(
            email=request_form['email'],
            name=request_form['name'],
            tokens=request_form['tokens']
        )
