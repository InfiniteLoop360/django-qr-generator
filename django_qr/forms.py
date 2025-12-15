from django import forms

# --- Form for Generating Secure QR ---
class QRCodeForm(forms.Form):
    title = forms.CharField(
        max_length=50,
        label='Mission / Project Title',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'e.g., Operation Alpha'
        })
    )
    data = forms.CharField(
        label='Confidential Data',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the secret message or coordinates to encrypt...',
            'rows': 4,
            'style': 'resize: none;'
        })
    )
    password = forms.CharField(
        max_length=50,
        label='Encryption Key',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Set a strong password'
        })
    )

# --- New Form for Decrypting ---
class DecryptForm(forms.Form):
    qr_image = forms.ImageField(
        label='Upload Secure QR Image',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'})
    )
    encrypted_data = forms.CharField(
        label='OR Paste Scrambled Text',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Paste the random text string here if you do not have the image...'
        })
    )
    password = forms.CharField(
        label='Decryption Key',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter the shared password to unlock'
        })
    )