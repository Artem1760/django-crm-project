from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class AssociateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set first_name and last_name as required fields
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True    
