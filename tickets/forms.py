from django import forms

from associates.models import Associate
from .models import Ticket, Category, FollowUp


class TicketForm(forms.ModelForm):
    """ Form for creating or updating a ticket. """

    class Meta:
        model = Ticket
        fields = (
        'title', 'type', 'description', 'uploaded_file', 'uploaded_image',
        'associate', 'category')
        widgets = {'category': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        user_department = kwargs.pop('user_department', None)
        super().__init__(*args, **kwargs)

        if user_department:
            # Filter the 'associate' field queryset based on the user's department
            associates = Associate.objects.filter(department=user_department)
            self.fields['associate'].queryset = associates


class AssignAssociateForm(forms.Form):
    associate = forms.ModelChoiceField(queryset=Associate.objects.none())

    def __init__(self, *args, **kwargs):
        user_department = kwargs.pop('user_department', None)
        super().__init__(*args, **kwargs)

        if user_department:
            # Filter the 'associate' field queryset based on the user's department
            associates = Associate.objects.filter(department=user_department)
            self.fields['associate'].queryset = associates


class TicketCategoryUpdateForm(forms.ModelForm):
    """ 
    Dynamically set the choices for the category field based on the user's role. 
    """

    class Meta:
        model = Ticket
        fields = ('category',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Set category choices based on user role
        if user.is_organizer:
            # Organizer can choose from all categories
            self.fields['category'].queryset = Category.objects.all()
        else:
            # Associate can only choose specific categories
            allowed_categories = ['work_in_progress', 'processed']
            self.fields['category'].queryset = Category.objects.filter(
                name__in=allowed_categories)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = ('notes', 'file')
