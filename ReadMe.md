Here's a **well-structured README** for your Django API project. This will help reviewers understand and test your project easily.  

---

# 🚀 **Fuel Optimizer API**
### **Optimized Route & Fuel Cost Calculator for US Road Trips**

## **📌 Overview**
This Django-based API calculates the best **fuel stops** along a route in the USA, ensuring cost-effective refueling based on fuel prices. The API fetches optimized routes using OpenRouteService and calculates total fuel costs based on fuel efficiency.

## **🌟 Features**
✔️ Takes start and finish locations (longitude, latitude) within the USA.  
✔️ Fetches the **optimal route** using OpenRouteService API.  
✔️ Identifies **cost-effective fuel stops** along the way.  
✔️ Ensures refueling within a **500-mile range** limit.  
✔️ Calculates **total fuel cost**, assuming a vehicle efficiency of **10 miles per gallon**.  
✔️ Returns the **full mapped route** in GeoJSON format.  

---

## **📂 Project Setup & Installation**

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/FuelOptimizer.git
cd FuelOptimizer
```

### **2️⃣ Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Apply Migrations**
```bash
python manage.py migrate
```

### **5️⃣ Sign Up for OpenRouteService API**
- Create an account at **[OpenRouteService](https://openrouteservice.org/)**
- Generate a **new API token** and copy it.

### **6️⃣ Add API Key to Django Settings**
In `settings.py`, add:
```python
ORS_API_KEY = "your_api_token_here"
```

### **7️⃣ Run the Server**
```bash
python manage.py runserver
```

---

## **🚀 API Usage**

### **📌 Endpoint:** `/optimize/`
**Base URL:** `http://127.0.0.1:8000/optimize/`

### **🔹 Request Format**
```http
GET /optimize/?start=-74.0060,40.7128&finish=-118.2437,34.0522
```
| Parameter  | Description                          | Example |
|------------|--------------------------------------|---------|
| `start`    | Starting location (lon, lat)        | `-74.0060,40.7128` (New York) |
| `finish`   | Destination location (lon, lat)     | `-118.2437,34.0522` (Los Angeles) |

---

### **🔹 Sample Response**
```json
{
    "total_distance_miles": 2793.02,
    "total_duration_hours": 44.79,
    "total_fuel_cost_usd": 697.97,
    "fuel_stops": [
        {
            "coordinates": [-84.16625, 41.591677],
            "distance_to_stop": 756.85,
            "fuel_price": 3.459,
            "state": "Ohio"
        },
        {
            "coordinates": [-104.909402, 39.86192],
            "distance_to_stop": 1592.06,
            "fuel_price": 3.149,
            "state": "Colorado"
        }
    ],
    ...,
  
    "route": {
        "type": "FeatureCollection",
        "bbox": [
            -118.243564,
            34.051518,
            -74.005612,
            41.756919
        ],
        "features": [
            {
                "bbox": [
                    -118.243564,
                    34.051518,
                    -74.005612,
                    41.756919
                ],
                "type": "Feature",
                "properties": {
                    "segments": [
                        {
                            "distance": 4494923.6,
                            "duration": 161258.3,
                            "steps": [
                                {
                                    "distance": 386.3,
                                    "duration": 88.2,
                                    "type": 11,
                                    "instruction": "Head southwest on Centre Street",
                                    "name": "Centre Street",
                                    "way_points": [
                                        0,
                                        12
                                    ]
                                },
                                {
                                    "distance": 350.6,
                                    "duration": 74.5,
                                    "type": 1,
                                    "instruction": "Turn right onto Church Street",
                                    "name": "Church Street",
                                    "way_points": [
                                        12,
                                        23
                                    ]
                                },
                                "way_points": [
                        0,
                        21326
                    ],
                    "summary": {
                        "distance": 4494923.6,
                        "duration": 161258.3
                    }
                },
                "geometry": {
                    "coordinates": [
                        [
                            -74.005612,
                            40.712158
                        ],
                        [
                            -74.005693,
                            40.71213
                        ],
                       ...
                    ],
                    "type": "LineString"
                }
            }
        ],
        "metadata": {
            "attribution": "openrouteservice.org | OpenStreetMap contributors",
            "service": "routing",
            "timestamp": 1738149811599,
            "query": {
                "coordinates": [
                    [
                        -74.006,
                        40.7128
                    ],
                    [
                        -118.2437,
                        34.0522
                    ]
                ],
                "profile": "driving-car",
                "profileName": "driving-car",
                "format": "geojson"
            },
            "engine": {
                "version": "9.0.0",
                "build_date": "2024-12-02T11:09:21Z",
                "graph_date": "2025-01-21T09:49:30Z"
            }
        }
    }
}
}
```

---

## **💡 How It Works**
1️⃣ The API fetches the route between `start` and `finish` using OpenRouteService.  
2️⃣ It identifies the **best fuel stops** based on state-wise fuel prices.  
3️⃣ Calculates total fuel cost based on **10 MPG efficiency** and fuel price at each stop.  
4️⃣ Returns:
   - 🚗 **Total Distance (miles)**
   - ⏳ **Total Duration (hours)**
   - ⛽ **Total Fuel Cost (USD)**
   - 🗺️ **List of Fuel Stops** (coordinates, fuel price, state)
   - 📌 **Full Route Map (GeoJSON)**  

---

## **📁 Project Structure**
```
FuelOptimizer/
│── route_optimizer/
│   ├── __init__.py
│   ├── views.py
│   ├── urls.py
│   ├── utils.py
│   ├── states_abb.py
│   ├── fuel_prices.csv
│── FuelOptimizer/
│   ├── settings.py
│   ├── urls.py
│── requirements.txt
│── manage.py
```

---

## **🛠 Technologies Used**
✅ **Django 3.2.23** - Backend framework  
✅ **OpenRouteService API** - Route calculation  
✅ **Nominatim API** - Reverse geocoding  
✅ **Postman** - API testing  

---

## **🎥 Demo**
🔹 **[Watch Loom Video](your-loom-video-link-here)** (5 min walkthrough of API usage)

---

## **📜 License**
License by **Sawera Khadium**

---

