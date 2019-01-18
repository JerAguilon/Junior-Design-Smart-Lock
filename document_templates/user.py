import time
import calendar

from document_templates.template_utils import require_fields

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
            "createdAt": self.created_at,
        }

    @staticmethod
    @require_fields(['email'])
    def build(request_form):
        return User(
            email=request_form['email'],
            name=request_form.get('name', []),
            tokens=request_form.get('tokens', [])
        )
