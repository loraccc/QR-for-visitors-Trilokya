# from django import forms
# from .models import CustomUser,Review,Role

# from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
# from django.core.validators import RegexValidator
# from django.core.exceptions import ValidationError
# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password1', 'password2']
#     def clean_phone_number(self):
#         phone_number = self.cleaned_data.get('phone_number')
#         if CustomUser.objects.filter(phone_number=phone_number).exists():
#             raise forms.ValidationError("This phone number is already in use.")
#         return phone_number
    
# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.CharField(
#         max_length=254,
#         widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Username'})
#     )
#     password = forms.CharField(
#         strip=False,
#         widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
#     )

# def validate_phone_number_length(value):
#     """
#     Validator to ensure that the phone number is exactly 10 digits long.
#     """
#     if len(str(value)) != 10: 

#         raise ValidationError(
#             'Phone number must be exactly 10 digits long.',
#             code='invalid_phone_number_length'
#         )

# class PhoneNumberForm(forms.Form):
#     """
#     Form for collecting a visitor's phone number.
#     """
#     phone_number = forms.CharField(
#         required=True, 
#         label='Phone Number',
#         widget=forms.TextInput(attrs={
#             'placeholder': 'Enter your phone number',
#             'type': 'tel',  # Use type 'tel' for numeric input on mobile devices
#         }),
#         validators=[validate_phone_number_length]
#     )

# class FullReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['name', 'phone_number', 'email', 'department', 'purpose', 'other_purpose', 'review']
#         widgets = {
#             'review': forms.Textarea(attrs={'placeholder': 'Enter your review here...'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(FullReviewForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'form-control'})
#         self.order_fields(['name', 'phone_number', 'email', 'department', 'purpose', 'other_purpose', 'review'])
#         if self.instance and self.instance.purpose != 'Other':
#             self.fields['other_purpose'].widget.attrs['style'] = 'display:none;'

#     def clean(self):
#         cleaned_data = super().clean()
#         purpose = cleaned_data.get('purpose')
#         other_purpose = cleaned_data.get('other_purpose')

#         if purpose == 'Other' and not other_purpose:
#             self.add_error('other_purpose', 'Please specify your purpose if "Other" is selected.')
#         elif purpose != 'Other' and other_purpose:
#             self.add_error('other_purpose', 'The additional details should only be filled if "Other" is selected.')

#         return cleaned_data

# class SimpleReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['name', 'phone_number', 'email', 'department', 'purpose', 'other_purpose', 'review']
#         # fields = ['name', 'phone_number', 'email', 'review']  # Include all fields you want to handle
#         widgets = {
#             'review': forms.Textarea(attrs={'placeholder': 'Update your review here...'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(SimpleReviewForm, self).__init__(*args, **kwargs)
#         # Set fields as read-only if needed
#         if self.instance and self.instance.pk:
#             self.fields['name'].widget.attrs['readonly'] = 'readonly'
#             self.fields['phone_number'].widget.attrs['readonly'] = 'readonly'
#             self.fields['email'].widget.attrs['readonly'] = 'readonly'
