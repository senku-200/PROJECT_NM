from django.forms import ModelForm
from . import models
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ['email','username','firstname','lastname']
class ObjectDectectorForm(ModelForm):
    class Meta:
        model = models.ObjectDetector
        fields = ['image']


