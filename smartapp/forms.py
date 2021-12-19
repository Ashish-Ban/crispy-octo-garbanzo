from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class':'form-control mb-3'}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control mb-3'}))

    def clean(self):
        cleandata = self.cleaned_data
        if len(cleandata.get('username')) <5:
            self.add_error('username',"Username should atleast contain 5 letters")
        return super().clean()