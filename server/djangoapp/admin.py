from django.contrib import admin  # Import this at the top of the file
from .models import CarMake, CarModel  # Import this at the top of the file

# Registering models with their respective admins
admin.site.register(CarMake)
admin.site.register(CarModel)
