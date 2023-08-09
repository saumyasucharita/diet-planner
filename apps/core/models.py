from django.db import models

# Create your models here.
class DietPlan(models.Model):

    recipe_name = models.CharField(max_length=127)
    calories = models.IntegerField(null=True)
    protein = models.CharField(max_length=127, null=True)
    fat = models.CharField(max_length=127, null=True)
    carbs = models.CharField(max_length=127, null=True)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE) 
    diet_plan_name = models.CharField(max_length=127)