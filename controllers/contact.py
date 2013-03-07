import utils
from google.appengine.api import mail


class ContactHandler(utils.BaseHandler):
    def get(self):
        """Basic contact form"""
        self.render('contact.html')

    def post(self):
        """Send an email from the customer"""
        owner = "Autumn Christie <autumnchristie@ymail.com>"
        from_address = self.request.get('from')
        body = self.request.get('message')
        message = mail.EmailMessage(sender=owner, subject="Request for information")
        message.to = "Autumn Christie <autumnchristie@ymail.com>"
        message.cc = "Dylan Thomas <dvhthomas@gmail.com>"
        body = from_address + '\n\n' + body
        message.body = body
        message.send()
        self.redirect('/thanks')


class ContactCompleteHandler(utils.BaseHandler):
    def get(self):
        """Email sent - say something nice"""
        self.render('contact-complete.html')
