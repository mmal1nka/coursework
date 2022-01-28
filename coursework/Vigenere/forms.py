from django import forms

CHOICES = [('encrypt', 'encrypt'),
         ('decrypt', 'decrypt')]
class CipherForm(forms.Form):
    Mess = forms.CharField(max_length=1000, required=True)
    Key = forms.CharField(max_length=1000, required=True)
    EncryptedMessage = forms.CharField(max_length=1000, required=False)
    Mess.widget.attrs.update({'placeholder': "Enter a message: "})
    Key.widget.attrs.update({'placeholder': "Enter a key: "})
