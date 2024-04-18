from random import choice, randint

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect

from .forms import LoginForm, UserRegistrationForm, RecipeForm
from django.contrib.auth import logout
from .models import Category, Recipe


# Create your views here.


def index(request):
    all_recipes = Recipe.objects.all()
    recipes_amount = len(all_recipes)
    ids = [i for i in range(1, recipes_amount + 1)]
    recipes = []
    for i in range(5):
        number = choice(ids)
        recipes.append(Recipe.objects.get(pk=number))
        ids.remove(number)
    context = {'type': 'main', 'recipes': recipes}
    return render(request, 'rand_recipes.html', context)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'


def auth(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            print("new_user")
            new_user.set_password(user_form.cleaned_data['password'])
            # new_user.set_group('author')
            new_user.save()
            return render(request, 'auth_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'auth.html', {'user_form': user_form})


def logout_view(request):
    logout(request)
    return redirect(index)


def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return render(request, 'add_recipe.html', {'form': form, 'saved_form': recipe})
        else:
            form = RecipeForm()
    else:
        form = RecipeForm()
    return render(request, 'add_recipe.html', {'form': form})


def edit_recipe(request, recipe_id):
    post = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=post)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('full_recipe', recipe_id=recipe.pk)
    else:
        form = RecipeForm(instance=post)
    return render(request, 'add_recipe.html', {'form': form})


def full_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {'recipe': recipe}
    return render(request, 'full_recipe.html', context)


def read_recipe(request, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk)
    context = {
        'name': 'Название рецепта',
        'cooking_step_list': recipe.cooking_steps.split('\r'),
        'recipe': recipe
    }
    return render(request, 'read_recipe.html', context)


def author_recipes(request, author_id):
    author = get_object_or_404(User, pk=author_id)
    recipes = Recipe.objects.filter(author=author)
    context = {'type': author, 'recipes': recipes}
    return render(request, 'rand_recipes.html', context)


def category_recipes(request, category_name):
    category = get_object_or_404(Category, title=category_name)
    recipes = []
    for recipe in Recipe.objects.all():
        for category in recipe.categories.all():
            if category.title == category_name:
                recipes.append(recipe)
    context = {'type': category_name, 'recipes': recipes}
    return render(request, 'rand_recipes.html', context)


def complexity_recipes(request, complexity_rate):
    recipes = Recipe.objects.filter(complexity=complexity_rate)
    context = {'type': complexity_rate, 'recipes': recipes}
    return render(request, 'rand_recipes.html', context)


def random_recipe(request):
    all_recipes = Recipe.objects.all()
    number = randint(1, len(all_recipes))
    recipe = Recipe.objects.get(pk=number)
    context = {'recipe': recipe}
    return render(request, 'full_recipe.html', context)
