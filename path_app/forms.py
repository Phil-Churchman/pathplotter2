from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.forms import ValidationError
from .models import *
from crispy_forms.helper import FormHelper
from .validator import *
from .utilities import current_user, current_version
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import NON_FIELD_ERRORS

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from itertools import chain


# class PassChangeForm(PasswordChangeForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']    

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists!")
        return email 

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["email"].required = True

class VersionForm(forms.ModelForm):

    class Meta: 
        model = Version 
        fields = '__all__'
        exclude = ['current', 'state', 'number', "archive"
                #    , "user"
                   ]
        widgets = {'user': forms.HiddenInput()}  
            
    def __init__(self, *args, user, other_users, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        groups = list(Group.objects.filter(user=user))
        username_list = [user]
        for group in groups:
            group_users = list(group.user_set.all())
            for u in group_users:
                if u.username not in username_list:
                    username_list.append(u.username)
        if other_users:
            self.fields['user'].queryset = User.objects.filter(username__in=username_list)
        else:
            self.fields['user'].queryset = User.objects.filter(username=user.username)

class VersionCopyForm(forms.ModelForm):

    class Meta: 
        model = Version 
        fields = '__all__'
        exclude = ['current', 'state', 'number', "archive"
                #    , "user"
                   ]
        # widgets = {'user': forms.HiddenInput()}  
            
    def __init__(self, *args, user, other_users, **kwargs):
        super(VersionCopyForm, self).__init__(*args, **kwargs)
        groups = list(Group.objects.filter(user=user))
        username_list = [user]
        for group in groups:
            group_users = list(group.user_set.all())
            for u in group_users:
                if u.username not in username_list:
                    username_list.append(u.username)
        if other_users:
            self.fields['user'].queryset = User.objects.filter(username__in=username_list)
        else:
            self.fields['user'].queryset = User.objects.filter(username=user.username)


class LoopForm(forms.ModelForm):

    class Meta: 
        model = Loop 
        fields = '__all__'
        exclude = [
            # 'version', 
            'links', 'copied_to'
            # , 'enabled'
            ]
        widgets = {'version': forms.HiddenInput()}  

    def __init__(self, *args, version, **kwargs):
        self.version = version
        super(LoopForm, self).__init__(*args, **kwargs)
        # self.fields['version'].queryset = Version.objects.filter(id=version.id)
        for field in self.fields.keys():
            if field in ["enabled"]:
                self.fields[field].widget.attrs.update({
                'disabled': True,
            })     

class NodeForm(forms.ModelForm):

    def clean_node_code(self):
        # version=self.cleaned_data["version"]
        node_code=self.cleaned_data["node_code"]            
        category=self.cleaned_data["category"]
        node_code_check = Node.objects.filter(version = self.version, node_code=node_code, category=category)
        if node_code_check.count() != 0:
            if self.instance.id != None:
                if self.instance.id != node_code_check[0].id:
                    raise ValidationError('Node with with category and node code already exists.')
            else:
                raise ValidationError('Node with with category and node code already exists.')            

        return node_code

    def clean_node_text(self):
        # version=self.cleaned_data["version"]
        node_text=self.cleaned_data["node_text"]            
        category=self.cleaned_data["category"]
        node_text_check = Node.objects.filter(version = self.version, node_text=node_text, category=category)
        if node_text_check.count() != 0:
            if self.instance.id != None:
                if self.instance.id != node_text_check[0].id:
                    raise ValidationError('Node with with category and node text already exists.')
            else:
                raise ValidationError('Node with with category and node text already exists.')            

        return node_text

    class Meta: 
        model = Node
        fields = '__all__'
        exclude = [
            # 'version',
            # 'xpos', 'ypos', 'placed', 
            'copied_to', 'selected', 'connected_to_goal', "connected_to_goal_enabled", "weight", "temp"]   
        widgets = {'xpos': forms.HiddenInput(), 'ypos': forms.HiddenInput(), 'placed': forms.HiddenInput(), 'version': forms.HiddenInput()}    
        # error_messages = {
        #     NON_FIELD_ERRORS: {
        #         'unique_together': "Category and node code are not unique.",
        #     }
        # }


    def __init__(self, *args, version, **kwargs):
    # def __init__(self, *args, **kwargs):
        self.version = version
        super(NodeForm, self).__init__(*args, **kwargs)
        # self.fields['version'].queryset = Version.objects.filter(id=version.id)

        self.fields['category'].queryset = Category.objects.filter(version=version)
        self.fields['duration'].validators.append(val_duration)
        self.fields['duration'].error_messages={"Duration needs to be greater than or equal to zero"}

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category 
        fields = '__all__'
        exclude = [
            # 'version', 
            'copied_to', 'selected_from', 'selected_to']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Category code is not unique.",
            }
        }    
        widgets = {'version': forms.HiddenInput()}


    def __init__(self, *args, version, **kwargs):
        self.version = version
        super(CategoryForm, self).__init__(*args, **kwargs)
        # self.fields['version'].queryset = Version.objects.filter(id=version.id)
                
class LinkForm(forms.ModelForm):
    class Meta: 
        model = Link 
        fields = '__all__'
        exclude = ['xmid', 'ymid', 'in_enabled_loop', 'in_enabled_group', 'in_loop', 'in_group', "weight",
                    # 'version',
                      'copied_to']
        widgets = {'version': forms.HiddenInput()}


    def __init__(self, *args, version, **kwargs):
        self.version = version
        super(LinkForm, self).__init__(*args, **kwargs)
        # self.fields['version'].queryset = Version.objects.filter(id=version.id)
        self.fields['from_node'].queryset = Node.objects.filter(version=version)
        self.fields['to_node'].queryset = Node.objects.filter(version=version)
        # self.fields['weight'].validators.append(val_weight)
        # self.fields['weight'].error_messages={}

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class NetworkParamForm(forms.ModelForm):
    class Meta: 
        model = NetworkParam 
        fields = '__all__'
        exclude = ['text', 'version', 'copied_to', "Enabled_loops_only"]
    
    def __init__(self, *args, **kwargs):
        super(NetworkParamForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            if field in ["Slow_motion", "Hide_links", "Link_midpoints", "Show_arrows", "Include_Goals_in_key", "Show_unconnected"]:
                continue
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

class GanttParamForm(forms.ModelForm):
    class Meta: 
        model = GanttParam 
        fields = '__all__'
        exclude = ['text', 'version', 'copied_to']

    def __init__(self, *args, **kwargs):
        super(GanttParamForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            if field in ["Show_out_seq", "Enabled_only", "Apply_groups"]:
                continue
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

class GroupedForm(forms.ModelForm):
    class Meta: 
        model = Grouped 
        fields = '__all__'
        exclude = [
            # 'version', 
            'loops', 'copied_to'
            # , 'enabled'
            ]
        widgets = {'version': forms.HiddenInput()}  

    def __init__(self, *args, version, **kwargs):
        super(GroupedForm, self).__init__(*args, **kwargs)
        self.fields['version'].queryset = Version.objects.filter(id=version.id)
        for field in self.fields.keys():
            if field in ["enabled"]:
                self.fields[field].widget.attrs.update({
                'disabled': True,
            })     
  
