# Uncomment the imports before you add the code
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Path for registration
    path('register/', views.registration, name='registration'),

    # Path for login
    path('login/', views.login_user, name='login'),

    # Path for logout
    path('logout/', views.logout_request, name='logout'),

    # Path for getting cars
    path('get_cars/', views.get_cars, name='get_cars'),

    # Path for getting dealerships
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path(
        'get_dealers/<str:state>/',
        views.get_dealerships,
        name='get_dealers_by_state'
    ),

    # Path for getting dealer details
    path(
        'dealer/<int:dealer_id>/',
        views.get_dealer_details,
        name='dealer_details'
    ),

    # Path for dealer reviews view
    path(
        'reviews/dealer/<int:dealer_id>/',
        views.get_dealer_reviews,
        name='dealer_reviews'
    ),

    # Path for adding a review
    path('add_review/', views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
