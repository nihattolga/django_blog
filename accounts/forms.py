from django.db.models import Q
from django import forms
from .models import User

class SigUpForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'email']

	def clean_password(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords do not match")
		return password2

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = User.objects.exclude(pk=self.instance.pk).get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = User.objects.exclude(pk=self.instance.pk).get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)

	def save(self, commit=True):
		user = super(SigUpForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])

		if commit:
			user.save()
		return user


class LoginForm(forms.Form):
	query = forms.CharField(label='Username / Email')
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		query = self.cleaned_data.get('query')
		password = self.cleaned_data.get('password')
		user_qs_final = User.objects.filter(
				Q(username__iexact=query) |
				Q(email__iexact=query)
			).distinct()
		if not user_qs_final.exists() and user_qs_final.count != 1:
			raise forms.ValidationError("Invalid credentials - user does note exist")
		user_obj = user_qs_final.first()
		if not user_obj.check_password(password):
			raise forms.ValidationError("Credentials are not correct")
		self.cleaned_data["user_obj"] = user_obj
		return super(LoginForm, self).clean(*args, **kwargs)

class UpdateForm(forms.ModelForm):

	class Meta:
	    model = User
	    fields = ('username', 'email', 'bio', 'avatar',)

	def clean_email(self):
	    email = self.cleaned_data['email'].lower()
	    try:
	        account = User.objects.exclude(pk=self.instance.pk).get(email=email)
	    except User.DoesNotExist:
	        return email
	    raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
	    username = self.cleaned_data['username']
	    try:
	        account = User.objects.exclude(pk=self.instance.pk).get(username=username)
	    except User.DoesNotExist:
	        return username
	    raise forms.ValidationError('Username "%s" is already in use.' % username)


	def save(self, commit=True):
	    account = super(UpdateForm, self).save(commit=False)
	    account.username = self.cleaned_data['username']
	    account.email = self.cleaned_data['email'].lower()
	    account.avatar = self.cleaned_data['avatar']
	    account.bio = self.cleaned_data['bio']
	    if commit:
	        account.save()
	    return account
