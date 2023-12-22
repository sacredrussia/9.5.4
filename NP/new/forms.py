from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from allauth.account.forms import AddEmailForm
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Author
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'text',
            'category'
        ]


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        emails = []
        email = self.cleaned_data.get("email")
        emails.append(email)
        emails1 = tuple(emails)

        html_content = render_to_string(
            'welcome_letter.html',
            {
                'link': settings.SITE_URL,
                'user': user

            }
        )

        msg = EmailMultiAlternatives(
            subject='приветственное сообщение',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=emails1
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


        return user

