from django.contrib.auth.models import User
from django.db import models
from django.db.models import Manager


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=225, verbose_name='Название', unique=True)
    object = Manager()

    def __str__(self):
        return f'#{self.pk}. {self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)


class Recipe(models.Model):
    COMPLEXITY = [
        ('easy', 'easy'),
        ('medium', 'medium'),
        ('complex', 'complex'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    cooking = models.TextField()
    time = models.CharField(max_length=20)
    image = models.ImageField()
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, default='new')
    complexity = models.CharField(max_length=10, choices=COMPLEXITY)

    def __str__(self):
        return f'{self.name}'


class CategoryRecipe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
