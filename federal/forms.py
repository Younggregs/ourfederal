from django.contrib.auth.models import User
from .models import Account , Feedback , ForgotPassword
from django import forms


class Signin(forms.ModelForm):

    username = forms.EmailField( widget=forms.TextInput(attrs={'placeholder': 'Email e.g you@gmail.com'}) )
    password = forms.CharField(max_length = 50,widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password']

class Signup(forms.ModelForm):

    firstname = forms.CharField(max_length = 30)
    lastname = forms.CharField(max_length = 30)
    username = forms.EmailField( widget=forms.TextInput(attrs={'placeholder': 'Email e.g you@gmail.com'}) )
    password = forms.CharField(max_length = 50,widget=forms.PasswordInput)
   
    class Meta:
        model = User
        fields = ['firstname','lastname','username','password']


class CommentTemplate(forms.ModelForm):

    comment = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'post comment here'}) )

    class Meta:
        model = User
        fields = ['comment']


class ReplyTemplate(forms.ModelForm):

    reply = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'post reply here'}) )

    class Meta:
        model = User
        fields = ['reply']


class ThreadTemplate(forms.ModelForm):

    thread = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

    media = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                    'required': False}),required=False)

    def __init__(self, *args, **kwargs):
        super(ThreadTemplate, self).__init__(*args, **kwargs)
        self.fields['thread'].label = ""
        self.fields['media'].label = "Attach media"
        self.fields['thread'].widget.attrs = {'rows':6,
                                            'cols':30}
        self.fields['media'].widget.attrs = {'multiple' : True}

    class Meta:
        model = User
        fields = ['thread']




class ProfileTemplate(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['display_pic']



class FeedbackTemplate(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['feed']


class FeedbackNewTemplate(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['firstname','lastname','feed']

class ForgotPasswordTemplate(forms.ModelForm):

    class Meta:
        model = ForgotPassword
        fields = ['username']

class ResetPasswordTemplate(forms.ModelForm):

    username = forms.EmailField( widget=forms.TextInput(attrs={'placeholder': 'Email e.g you@gmail.com'}) )
    reset_password = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username','reset_password']



class EditProfileTemplate(forms.ModelForm):

    password = forms.CharField(max_length = 50,widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['password']

