from django.urls import path

from apps.core import views

urlpatterns = [
    # path('', views.home, name='home'),
    # path('about/', views.about, name='about'),
    path('', views.homepage, name='home'),
    path('search-recipes/', views.search_recipes, name='get_recipes'),
    path('create_diet_plan/', views.create_diet_plan, name='create_diet_plan'),
    path('display-diet-plan/', views.display_diet_plan, name='display_diet_plan'),
    path('update-diet-plan/', views.update_diet_plan, name='update_diet_plan'),
    path('compare-calories/', views.compare_calories),
    path('nutrient-breakdown/', views.nutrient_breakdown)
]
