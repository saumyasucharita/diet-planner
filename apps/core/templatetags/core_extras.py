from django import template
#Reference: https://stackoverflow.com/questions/4386168/how-to-concatenate-strings-in-django-templates
#https://stackoverflow.com/questions/40686201/django-1-10-1-my-templatetag-is-not-a-registered-tag-library-must-be-one-of

register = template.Library()

@register.filter
def concat_str(arg1, arg2):
    return str(arg1) + str(arg2)