from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from datetime import timedelta


class EmailService(object):
    @classmethod
    def send_activate_email(cls, user):
        subject, from_email, to = 'Hello from Saturn', 'activate@saturn.com', user.email
        htmly = get_template('email/activate.html')
        url = 'http://%s/accounts/activate/?email=%s&verification_code=%s' \
                          % (settings.DOMAIN, user.email, user.account.verification_code)
        html_content = htmly.render(Context(locals()))
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
