from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Review

class RegistrationForm(UserCreationForm):
  password1 = forms.CharField(
      label=_("Password"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
  )
  password2 = forms.CharField(
      label=_("Password Confirmation"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Confirmation'}),
  )

  class Meta:
    model = User
    fields = ('username', 'email', )

    widgets = {
      'username': forms.TextInput(attrs={
          'class': 'form-control',
          'placeholder': 'Username'
      }),
      'email': forms.EmailInput(attrs={
          'class': 'form-control',
          'placeholder': 'Email'
      })
    }


class LoginForm(AuthenticationForm):
  username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
  password = forms.CharField(
      label=_("Password"),
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
  )

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")
    

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Old Password'
    }), label='Old Password')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")


def validate_phone_number_length(value):
    """
    Validator to ensure that the phone number is exactly 10 digits long.
    """
    if len(str(value)) != 10:
        raise ValidationError(
            'Phone number must be exactly 10 digits long.',
            code='invalid_phone_number_length'
        )



class PhoneNumberForm(forms.Form):
    """
    Form for collecting a visitor's phone number.
    """
    phone_number = forms.CharField(
        required=True, 
        label='Phone Number',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your phone number',
            'type': 'tel',  # Numeric input on mobile devices
            'pattern': '[0-9]{10}',  # Ensures the input is numeric and exactly 10 digits long
            'title': 'Phone number must be 10 digits long'  # Tooltip for users
        }),
        validators=[validate_phone_number_length]
    )


class FullReviewForm(forms.ModelForm):
    purpose_of_visit = forms.CharField(
        label='Purpose of Visit',
        widget=forms.Textarea(attrs={'placeholder': 'Enter the purpose of your visit here...'}),
        required=False
    )

    class Meta:
        model = Review
        fields = ['name', 'phone_number', 'email', 'department', 'purpose', 'other_purpose', 'purpose_of_visit']
        widgets = {
            'purpose_of_visit': forms.Textarea(attrs={'placeholder': 'Enter the purpose of your visit here...'}),
        }

    def __init__(self, *args, **kwargs):
        super(FullReviewForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'readonly': 'readonly'})
        self.order_fields(['name', 'phone_number', 'email', 'department', 'purpose', 'other_purpose', 'purpose_of_visit'])

        # Hide 'other_purpose' field if purpose is not 'Other' (handled by JS in templates)
        if self.instance and self.instance.purpose and self.instance.purpose != 'Other':
            self.fields['other_purpose'].widget.attrs.update({'style': 'display:none;'})

    def clean(self):
        cleaned_data = super().clean()
        purpose = cleaned_data.get('purpose')
        other_purpose = cleaned_data.get('other_purpose')

        if purpose == 'Other' and not other_purpose:
            self.add_error('other_purpose', 'Please specify your purpose if "Other" is selected.')
        elif purpose != 'Other' and other_purpose:
            self.add_error('other_purpose', 'Additional details should only be filled if "Other" is selected.')

        return cleaned_data


class SimpleReviewForm(forms.ModelForm):
    """
    Form for handling existing reviews.
    """
    class Meta:
        model = Review
        fields = ['name', 'phone_number', 'email', 'department', 'purpose', 'other_purpose', 'review']
        widgets = {
            'review': forms.Textarea(attrs={'placeholder': 'Update your review here...'}),
        }

    def __init__(self, *args, **kwargs):
        super(SimpleReviewForm, self).__init__(*args, **kwargs)
        # Set fields as read-only if needed
        if self.instance and self.instance.pk:
            self.fields['name'].widget.attrs['readonly'] = 'readonly'
            self.fields['phone_number'].widget.attrs['readonly'] = 'readonly'
            self.fields['email'].widget.attrs['readonly'] = 'readonly'
    class Meta:
        model = Review
        fields = ['name', 'phone_number', 'email', 'department', 'purpose', 'other_purpose', 'review']
        widgets = {
            'Purpose Of Visit': forms.Textarea(attrs={'placeholder': 'Update your Purpose here...'}),
        }

    def __init__(self, *args, **kwargs):
        super(SimpleReviewForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['name'].widget.attrs['readonly'] = 'readonly'
            self.fields['phone_number'].widget.attrs['readonly'] = 'readonly'
            self.fields['email'].widget.attrs['readonly'] = 'readonly'

class ManualForm(forms.ModelForm):
    created_at = forms.DateTimeField(required=True, widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM:SS'}))  # Allow manual entry of created_at

    class Meta:
        model = Review
        fields = ['name', 'email', 'phone_number', 'department', 'purpose', 'other_purpose', 'review', 'created_at']
        labels = {
            'review': 'Purpose',  # Changed the label for the review field into "Purpose"
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'phone_number': forms.NumberInput(attrs={'placeholder': 'Enter your phone number'}),
            'other_purpose': forms.TextInput(attrs={'placeholder': 'Enter any other purpose'}),
            'review': forms.Textarea(attrs={'placeholder': 'Enter the purpose of your review'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(str(phone_number)) != 10:  # Ensure it has exactly 10 digits
            raise forms.ValidationError('Phone number must be exactly 10 digits.')
        return phone_number