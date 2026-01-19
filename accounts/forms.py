from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "preferred_currency")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar classes Tailwind em todos os campos automaticamente
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none'