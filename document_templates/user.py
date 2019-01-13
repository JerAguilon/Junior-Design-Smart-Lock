import time
import calendar

from utils.decorators import require_fields


class User(object):
    def __init__(
        self,
        email,
        name,
        tokens,
        created_at=calendar.timegm(time.gmtime())
    ):
        self.email = email
        self.name = name
        self.tokens = tokens
        self.created_at = created_at

    def serialize(self):
        return {
            self.email: {
                "name": self.name,
                "tokens": self.tokens,
                "created_at": self.created_at,
            }
        }

    @staticmethod
    @require_fields(['email', 'name', 'tokens'])
    def build(request_form):
        return User(
            email=request_form['email'],
            name=request_form['name'],
            tokens=request_form['tokens']
        )
