from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "preferred_currency")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all'
            field.help_text = "" 
            
            # Se houver erro nesse campo após o POST, adicionamos uma borda vermelha
            if self.errors.get(field_name):
                current_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = current_classes + ' border-red-500 bg-red-50'
                
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'preferred_currency', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'preferred_currency': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'profile_picture': forms.FileInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
        }