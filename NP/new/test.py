from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
