from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password_repeat = forms.CharField(label=_('Password Repeat'), widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name', 'password', 'password_repeat', )

    def clean_password_repeat(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')

        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError(_('Passwords does not match.'))
        return password_repeat

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name', 'password', 'language', 'is_active', 'is_staff',
                  'is_superuser', )

    def clean_password(self):
        return self.initial['password']
