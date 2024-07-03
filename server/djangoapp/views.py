# Uncomment the required imports before adding the code
import json
import logging
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt

from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create a `login_user` view to handle sign-in requests
@csrf_exempt
def login_user(request):
    """Authenticate user and log them in."""
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    response_data = {"userName": username}

    if user is not None:
        login(request, user)
        response_data.update({"status": "Authenticated"})
    return JsonResponse(response_data)


# Create a `logout_request` view to handle sign-out requests
def logout_request(request):
    """Log out the current user."""
    logout(request)
    return JsonResponse({"userName": ""})


# Create a `registration` view to handle sign-up requests
@csrf_exempt
def registration(request):
    """Register a new user and log them in."""
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')

    if User.objects.filter(username=username).exists():
        response_data = {
            "userName": username,
            "error": "Already Registered"
        }
    else:
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        user = authenticate(username=username, password=password)
        login(request, user)
        response_data = {
            "userName": username,
            "status": "Authenticated"
        }
        logger.debug(f"{username} is a new user")

    return JsonResponse(response_data)


# Fetch and return a list of cars
def get_cars(request):
    """Return a list of cars with their make and model."""
    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        }
        for car_model in car_models
    ]

    return JsonResponse({"CarModels": cars})


# Render a list of dealerships
def get_dealerships(request, state="All"):
    """Return a list of dealerships, optionally filtered by state."""
    endpoint = f"/fetchDealers/{state}" if state != "All" else "/fetchDealers"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Fetch and return the reviews of a specific dealer
def get_dealer_reviews(request, dealer_id):
    """Return reviews for a specific dealer with sentiment analysis."""
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        if reviews is None:
            return JsonResponse({"status": 500, "message": "Error fetching reviews"})

        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response.get('sentiment', "unknown")

        return JsonResponse({"status": 200, "reviews": reviews})

    return JsonResponse({"status": 400, "message": "Bad Request"})


# Fetch and return the details of a specific dealer
def get_dealer_details(request, dealer_id):
    """Return details for a specific dealer."""
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})

    return JsonResponse({"status": 400, "message": "Bad Request"})


# Submit a review
def add_review(request):
    """Submit a review for a dealer."""
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
