from django.urls import path

from apps.core import views

urlpatterns = [
    # path('', views.home, name='home'),
    # path('about/', views.about, name='about'),
    path('', views.homepage),
    path('search-recipes/', views.search_recipes),
    path('compare-calories/', views.compare_calories),
    path('nutrient-breakdown/', views.nutrient_breakdown)
]
