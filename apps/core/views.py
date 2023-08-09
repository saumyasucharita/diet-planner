import requests
import ast
from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
import pygal  
import traceback
from django.core.cache import cache
from .models import DietPlan

#How to fetch from a env file (TBD HW-2)
api_key = "99033f8fe5554466ac9ef2e7657a10fc"

class NutrientForm(forms.Form):
    minCalories = forms.IntegerField(label = "Minimum calories", widget=forms.TextInput(attrs={'placeholder': 100}))
    maxCalories = forms.IntegerField(label = "Maximum calories", required=False)
    minCarbs = forms.IntegerField(min_value=0, label = "Minimum carbs(grams)", required=False)
    maxCarbs = forms.IntegerField(min_value=0, label = "Maximum carbs(grams)", required=False)
    minProtein = forms.IntegerField(min_value=0, label = "Minimum protein(grams)", required=False)
    maxProtein = forms.IntegerField(min_value=0, label = "Maximum protein(grams)", required=False)
    minFat = forms.IntegerField(min_value=0, label = "Minimum fat(grams)", required=False)
    maxFat = forms.IntegerField(min_value=0, label = "Maximum fat(grams)", required=False)
    diet_plan_name = forms.CharField(max_length=127, label = "Diet Plan Name")
    
# Helper function
def spoonacular_api_call(request):
	#Spoonacular API url
	url = "https://api.spoonacular.com/recipes/findByNutrients?apiKey="+ api_key + "&number=7"

	params = {
		key: value
		for key, value in request.GET.items()
		if value
	}
	
	response = requests.get(url, params=params)
	
	# How to check for API response header?
	print(response)
	return response.json()

# Create your views here.
def homepage(request):
	print('Homepage')
	
	form = NutrientForm() # Make a new blank form
	context = {
		'form': form,
	}
	return render(request, 'pages/homepage.html', context)

def search_recipes(request):
	print('In search recipes view')
	error = None

	if 'minCalories' in request.GET:
		form = NutrientForm(request.GET) # Make a form instance from GET data
	
		if form.is_valid(): # Check if valid (and as side-effect, generate cleaned_data dict)
			try:
				if 'recipe_data' not in cache:
					recipe_data = spoonacular_api_call(request)
					# Saving data (15 minutes timeout)
					cache.set('recipe_data', recipe_data, 60*60)
				
				else:
					# Retrieving data
					print("Data in cache")
					print(cache.get('recipe_data'))
					recipe_data = cache.get('recipe_data')
			except Exception as e:
				recipe_data = []
				error = str(e)
				print(traceback.format_exc())
			#Loop through the recipe_data list
			for recipe in recipe_data:
				recipe_id = recipe['id']
				#Set the recipe url(another api call)
				recipe_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?includeNutrition=false&apiKey={api_key}'
				print(recipe_url)
				#Revert this
				#recipe_info = requests.get(recipe_url).json()
				#Add another field recipe_link to the recipe json
				#recipe['recipe_link'] = recipe_info['sourceUrl']
				recipe['recipe_link'] = 'https://www.indianhealthyrecipes.com/chilli-chicken-dry-recipe-indo-chinese-style/'
			diet_plan_name = form.cleaned_data['diet_plan_name']

	else:
		form = NutrientForm()
		
	context = {
		'recipes' : recipe_data,
		'diet_plan_name' : diet_plan_name,
		'error' : error
	}
	return render(request, 'pages/recipes.html', context)

#Create diet plan(C of CRUD)
def create_diet_plan(request):
	print('In create diet plan view')
	
	if request.method == 'POST':
		recipe_data = request.POST.getlist('recipes')
		print(request.POST.get('diet_plan_name'))

		for recipe in recipe_data:
			recipe_dict = ast.literal_eval(recipe) #Why json.loads didn't work?

			DietPlan.objects.create(
						recipe_name=recipe_dict['title'],
						calories=recipe_dict['calories'],
						protein=recipe_dict['protein'],
						fat=recipe_dict['fat'],
						carbs=recipe_dict['carbs'],
						user = request.user,
						diet_plan_name = request.POST.get('diet_plan_name'),
			)

	return redirect('home') #TBD


# #Read diet plan(R of CRUD)
# def display_diet_plan(request):
# 	print('')
# 	context = {
# 	}
# 	return render(request, 'pages/recipes.html', context)

# #Update diet plan(U of CRUD)
# def update_diet_plan(request):
# 	print('')
# 	context = {
# 	}
# 	return render(request, 'pages/recipes.html', context)


# #Delete recipes from diet plan(D of CRUD)
# def delete_recipe(request):
# 	print('')
# 	context = {
# 	}
# 	return render(request, 'pages/recipes.html', context)

def compare_calories(request):
	print('In compare calories view')

	if 'recipe_data' not in cache:
		recipe_data = spoonacular_api_call(request)
		cache.set('recipe_data', recipe_data, 15*60)
				
	else:
		print("Data in cache")
		recipe_data = cache.get('recipe_data')

	# Extracting the titles and calories from the API response
	titles = [recipe['title'] for recipe in recipe_data]
	calories = [recipe['calories'] for recipe in recipe_data]

	bar_chart = pygal.Bar()
	bar_chart.title = 'Calories per Recipe'
	#bar_chart.x_labels = titles
	
	# Adding the data to the chart 
	for idx, calorie in enumerate(calories):
		bar_chart.add(titles[idx], [calorie])

	# Displaying the color legend 
	bar_chart.legend_at_right = True
	bar_chart.x_label_rotation = 30

	chart_svg_as_datauri = bar_chart.render_data_uri()

	context = {
		"rendered_chart_svg_as_datauri": chart_svg_as_datauri,
	}

	return render(request, 'pages/calorie_comparision.html', context)

def nutrient_breakdown(request):
	print('In nutrient breakdown view')

	if 'recipe_data' not in cache:
		recipe_data = spoonacular_api_call(request)
		cache.set('recipe_data', recipe_data, 15*60)
				
	else:
		print("Data in cache")
		recipe_data = cache.get('recipe_data')
	titles = [recipe['title'] for recipe in recipe_data]

	#Plot a stacked bar chart having breakdown of protein, fat and carbs for each recipe
	bar_chart = pygal.StackedBar()
	bar_chart.title = 'Nutrient breakdown of recipes'
	bar_chart.x_labels = titles
	bar_chart.x_label_rotation = 30
	#Convert the protein/fat/carbs values received from API to int for plotting
	bar_chart.add('Protein', [int(recipe['protein'][:-1]) for recipe in recipe_data])
	bar_chart.add('Fat',  [int(recipe['fat'][:-1]) for recipe in recipe_data])
	bar_chart.add('Carbs', [int(recipe['carbs'][:-1]) for recipe in recipe_data])
	
	#Include chart on HTML page	
	bar_as_datauri = bar_chart.render_data_uri()

	context={
		"rendered_chart_svg_as_datauri": bar_as_datauri,
	}
	return render(request, 'pages/calorie_comparision.html', context)