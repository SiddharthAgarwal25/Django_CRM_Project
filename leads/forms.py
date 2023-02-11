from django import forms
from .models import Lead, Agent, Category
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
        )


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}

# This form will allow the organiser to choose the agent they want to assign to a particular task.
class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        print(request.user)
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )

class LeadCategoryUpdateForm(forms.ModelForm):

    class Meta:
        model = Lead
        fields = (
            'category',
        )

