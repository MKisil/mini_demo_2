from django import forms


class CallsUploadForm(forms.Form):
    instruction = forms.CharField(widget=forms.Textarea, required=True)
    file = forms.FileField(required=True)
