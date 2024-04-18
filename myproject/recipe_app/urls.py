from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('random/', views.random_recipe, name='random_recipe'),
    path('full_recipe/<int:recipe_id>/', views.full_recipe, name='full_recipe'),
    path('category_recipes/<slug:category_name>/', views.category_recipes, name='category_recipes'),
    path('complexity_recipes/<slug:complexity_rate>/', views.complexity_recipes, name='complexity_recipes'),
    path('author_recipes/<int:author_id>/', views.author_recipes, name='author_recipes'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('auth/', views.auth, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe')
]
