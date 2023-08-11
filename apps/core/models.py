from django.db import models

# Create your models here.
class DietPlan(models.Model):

    recipe_name = models.CharField(max_length=127)
    calories = models.IntegerField(null=True)
    protein = models.CharField(max_length=127, null=True)
    fat = models.CharField(max_length=127, null=True)
    carbs = models.CharField(max_length=127, null=True)
    image = models.URLField(null=True)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE) 
    date_assigned = models.DateField(null=True, blank=True) #Difference between null=True & blank=True
    #diet_plan_name = models.CharField(max_length=127)