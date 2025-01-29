import requests
import json
import math
import csv
import requests
import json
from .states_abb import STATE_ABBREVIATIONS
from django.conf import settings
api_key = settings.ORS_API_KEY


def get_route(api_key, start, finish):
    """
    Fetches the route between start and finish using OpenRouteService.
    """
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "coordinates": [
            [float(coord) for coord in start.split(",")],  # Convert start to [lon, lat]
            [float(coord) for coord in finish.split(",")]  # Convert finish to [lon, lat]
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)  # Use POST instead of GET
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching route: {e}")
        return None


import requests
import time


def get_state_from_coordinates(lat, lon):
    """
    Fetches the state name from OpenStreetMap Nominatim API.
    Uses a proper User-Agent header to prevent 403 errors.
    """
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {
        "User-Agent": "FuelOptimizer/1.0 (sawerakhadium557@gmail.com)",  # Use your email/domain
        "Accept-Language": "en"
    }

    time.sleep(1)

    try:
        response = requests.get(url, headers=headers, timeout=3)  # Add timeout to avoid slow requests
        response.raise_for_status()
        data = response.json()
        return data.get("address", {}).get("state", None)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching state: {e}")

    return None

def calculate_fuel_stops_and_cost(route, fuel_prices):
    """
    🚀 Optimized: Ensures fuel price lookup works using **uppercase state abbreviations**.
    ✅ Converts full state names to abbreviations before lookup.
    ✅ Fixes missing price lookup issue.
    ✅ Logs missing states for debugging.
    """
    try:
        segments = route['features'][0]['properties'].get('segments', [])
        if not segments:
            print("Error: No route segments found.")
            return [], 0

        total_distance = segments[0].get('distance', 0) / 1609.34  # Convert meters to miles
        max_range = 500  # Max vehicle range before refueling
        mpg = 10  # Miles per gallon
        fuel_needed = total_distance / mpg  # Total gallons of fuel needed
        fuel_cost = 0
        stops = []

        waypoints = route['features'][0]['geometry']['coordinates']
        remaining_range = max_range
        current_distance = 0

        for step in segments[0].get('steps', []):
            distance = step.get('distance', 0) / 1609.34  # Convert meters to miles
            current_distance += distance
            remaining_range -= distance

            if remaining_range <= 0:  # Time to refuel
                waypoint_index = min(math.floor(len(waypoints) * (current_distance / total_distance)), len(waypoints) - 2)
                fuel_stop = waypoints[waypoint_index]  # Get lat/lon of the fuel stop
                lat, lon = fuel_stop[1], fuel_stop[0]

                # 🚀 Fetch state for this fuel stop
                state = get_state_from_coordinates(lat, lon)

                # 🚀 Convert full state name to abbreviation
                state_abbr = STATE_ABBREVIATIONS.get(state.strip().title(), None)

                # 🚀 Convert abbreviation to uppercase for lookup
                if state_abbr:
                    state_abbr = state_abbr.upper()
                    fuel_price = fuel_prices.get(state_abbr, None)
                    if fuel_price is None:
                        print(f"⚠️ Warning: No fuel price found for {state} ({state_abbr}), defaulting to $3.5")
                        fuel_price = 3.5
                else:
                    print(f"⚠️ Warning: No valid state abbreviation found for {state}, defaulting to $3.5")
                    fuel_price = 3.5

                stops.append({
                    "coordinates": fuel_stop,
                    "distance_to_stop": round(current_distance, 2),
                    "fuel_price": fuel_price,
                    "state": state
                })

                # 🚀 Accurately calculate total fuel cost
                fuel_cost += (max_range / mpg) * fuel_price
                remaining_range = max_range  # Reset range after refueling

        return stops, round(fuel_cost, 2)

    except Exception as e:
        print(f"Error in fuel calculation: {e}")
        return [], 0

def get_fuel_prices():
    """
    ✅ Reads fuel prices from CSV and ensures state abbreviations are in uppercase.
    ✅ Fixes column name mismatches and incorrect case.
    ✅ Uses state abbreviations directly if provided.
    ✅ Handles missing or malformed fuel prices.
    """
    fuel_prices = {}
    try:
        with open('route_optimizer/fuel_prices.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                state_abbr = row.get("State", "").strip().upper()  # Convert to uppercase

                try:
                    price = float(row.get("Retail Price", 3.5))  # Default to $3.5 if missing

                    if state_abbr in STATE_ABBREVIATIONS.values():  # Validate abbreviation
                        fuel_prices[state_abbr] = price
                    else:
                        print(f"⚠️ Warning: State abbreviation '{state_abbr}' in CSV does not match known US states.")

                except ValueError:
                    print(f"Skipping invalid fuel price for {state_abbr}: {row.get('Retail Price')}")
    except Exception as e:
        print(f"Error reading fuel prices: {e}")

    return fuel_prices
