from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from .utils import get_fuel_prices, get_route, calculate_fuel_stops_and_cost
from django.conf import settings

def route_optimization_api(request):
    start = request.GET.get('start')  # e.g., "-74.0060,40.7128"
    finish = request.GET.get('finish')  # e.g., "-118.2437,34.0522"

    if not start or not finish:
        return JsonResponse({"error": "Start and finish locations are required."}, status=400)

    # Fetch route
    api_key = settings.ORS_API_KEY
    route = get_route(api_key, start, finish)

    if not route:
        return JsonResponse({"error": "Could not fetch route information."}, status=500)

    # Calculate fuel stops and cost (Now optimized 🚀)
    fuel_prices = get_fuel_prices()
    stops, total_cost = calculate_fuel_stops_and_cost(route, fuel_prices)

    return JsonResponse({
        "total_distance_miles": round(route['features'][0]['properties']['segments'][0]['distance'] / 1609.34, 2),
        "total_duration_hours": round(route['features'][0]['properties']['segments'][0]['duration'] / 3600, 2),
        "total_fuel_cost_usd": total_cost,
        "fuel_stops": stops,
        "route": route  # Include full route for debugging
    })
