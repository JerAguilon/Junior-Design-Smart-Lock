import time
import calendar


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
