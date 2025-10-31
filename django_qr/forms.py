from django import forms


class QRCodeForm(forms.Form):
    title = forms.CharField(
        max_length=50,
        label='Title',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a title for your QR code'
        })
        )
    url = forms.URLField(
        max_length=200, 
        label='URL',
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the full URL (e.g., https://...)'
        })
        )