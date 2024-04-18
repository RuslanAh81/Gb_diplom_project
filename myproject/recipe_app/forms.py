from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, CharField, PasswordInput
from django.contrib.auth.forms import AuthenticationForm
from .models import Category, Recipe, CategoryRecipe
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    pass


class UserRegistrationForm(ModelForm):
    password = CharField(label='Password', widget=PasswordInput)
    password2 = CharField(label='Repeat password', widget=PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Passwords don\'t match.')
        return cd['password2']


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'description', 'cooking', 'time', 'image', 'categories', 'complexity')


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('title',)


class RecipeToCategoryForm(ModelForm):
    model = CategoryRecipe
    fields = ()
