from django.db import models
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_multipart_email(subject, html_template, from_email, to_email):
    html = render_to_string(html_template)
    text_content = strip_tags(html)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html, "text/html")
    msg.send()


class UserEmail(models.Model):
    '''A model to store the emails allowed to register in the CASV sistem.'''

    email = models.EmailField()

    def __str__(self):
        return '%s' % self.email

    def save(self, *args, **kwargs):
        super(UserEmail, self).save(*args, **kwargs)
        subject = 'Cadastre-se no sistema CASV do CSR/IBAMA'
        send_multipart_email(subject, 'register_email.html',
            'nao_responda@ibama.gov.br', self.email)