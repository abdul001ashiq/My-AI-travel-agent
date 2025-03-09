from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, load_tool, tool, FinalAnswerTool
from tools.final_answer import MemoryStep, final_answer
import datetime
import requests
import pytz
import yaml
import json
import os
import time
from dotenv import load_dotenv
from Gradio_UI import GradioUI


load_dotenv()

# Get Hugging Face API token from environment variable
HUGGING_FACE_TOKEN = os.getenv('HUGGING_FACE_TOKEN')
if not HUGGING_FACE_TOKEN:
    raise ValueError("Please set HUGGING_FACE_TOKEN in your environment variables or .env file")

# Set the token as an environment variable for the Hugging Face library
os.environ["HUGGINGFACE_TOKEN"] = HUGGING_FACE_TOKEN
os.environ["HF_TOKEN"] = HUGGING_FACE_TOKEN
os.environ["HUGGINGFACE_HUB_TOKEN"] = HUGGING_FACE_TOKEN  # This is the most common environment variable name
os.environ["HF_API_TOKEN"] = HUGGING_FACE_TOKEN

# Current time in timezone tool
@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """Get the current local time in a specified US timezone.

    Args:
        timezone: A string representing a valid US timezone (e.g., 'America/New_York', 'America/Chicago').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"

# Weather information tool with alert capabilities
@tool
def get_weather_forecast(location: str) -> str:
    """Fetches current weather, forecast, and any weather alerts for a US location.

    Args:
        location: A string representing a US city or place (e.g., 'New York, NY', 'Austin, TX')
    """
    # In production: Use a weather API like OpenWeatherMap, Weather.gov (NWS), or AccuWeather
    # This is a mock implementation for demonstration
    try:
        # Check if there are any mock alerts for this location
        weather_alerts = {
            "miami": "Hurricane Warning: Category 2 hurricane approaching. Prepare for evacuation.",
            "new orleans": "Flood Warning: Heavy rainfall expected over the next 48 hours.",
            "los angeles": "Heat Advisory: Temperatures expected to reach 100°F over the next 3 days."
        }

        # Mock weather data
        weather_data = {
            "new york": {
                "current": {"temp": 72, "condition": "Partly Cloudy", "humidity": 65},
                "forecast": [
                    {"day": "Tomorrow", "temp": 75, "condition": "Sunny"},
                    {"day": "Day 2", "temp": 70, "condition": "Light Rain"},
                    {"day": "Day 3", "temp": 68, "condition": "Cloudy"}
                ]
            },
            "austin": {
                "current": {"temp": 85, "condition": "Sunny", "humidity": 45},
                "forecast": [
                    {"day": "Tomorrow", "temp": 88, "condition": "Sunny"},
                    {"day": "Day 2", "temp": 90, "condition": "Clear"},
                    {"day": "Day 3", "temp": 89, "condition": "Partly Cloudy"}
                ]
            },
            "chicago": {
                "current": {"temp": 65, "condition": "Windy", "humidity": 55},
                "forecast": [
                    {"day": "Tomorrow", "temp": 63, "condition": "Partly Cloudy"},
                    {"day": "Day 2", "temp": 58, "condition": "Rain"},
                    {"day": "Day 3", "temp": 60, "condition": "Partly Cloudy"}
                ]
            }
        }

        # Normalize location
        location_key = location.lower().split(",")[0].strip()

        # Format response
        response = f"Weather information for {location}:\n\n"

        # Check for alerts first
        if location_key in weather_alerts:
            response += f"ALERT: {weather_alerts[location_key]}\n\n"

        # Add weather data if available
        if location_key in weather_data:
            current = weather_data[location_key]["current"]
            response += f"Current: {current['temp']}°F, {current['condition']}, {current['humidity']}% humidity\n\nForecast:\n"

            for day in weather_data[location_key]["forecast"]:
                response += f"- {day['day']}: {day['temp']}°F, {day['condition']}\n"
        else:
            response += "Detailed weather data not available. In a real implementation, this would connect to a weather API."

        return response
    except Exception as e:
        return f"Error fetching weather for '{location}': {str(e)}"

# Budget estimation tool
@tool
def estimate_travel_budget(destination: str, num_people: int, num_days: int, accommodation_type: str = "budget") -> str:
    """Estimates a comprehensive travel budget for a US destination.

    Args:
        destination: US city (e.g., 'New York', 'Austin')
        num_people: Number of travelers
        num_days: Length of stay in days
        accommodation_type: Type of accommodation ('budget', 'mid-range', 'luxury')
    """
    try:
        # Mock budget data for common US destinations
        budget_data = {
            "new york": {
                "accommodation": {
                    "budget": 150,    # Price per room per night
                    "mid-range": 250,
                    "luxury": 450
                },
                "food": {
                    "budget": 40,     # Price per person per day
                    "mid-range": 80,
                    "luxury": 150
                },
                "local_transport": 15,  # Per person per day
                "attractions": 25       # Per person per day
            },
            "los angeles": {
                "accommodation": {
                    "budget": 130,
                    "mid-range": 230,
                    "luxury": 400
                },
                "food": {
                    "budget": 40,
                    "mid-range": 75,
                    "luxury": 140
                },
                "local_transport": 20,
                "attractions": 30
            },
            "chicago": {
                "accommodation": {
                    "budget": 120,
                    "mid-range": 220,
                    "luxury": 350
                },
                "food": {
                    "budget": 35,
                    "mid-range": 70,
                    "luxury": 130
                },
                "local_transport": 14,
                "attractions": 22
            },
            "miami": {
                "accommodation": {
                    "budget": 130,
                    "mid-range": 240,
                    "luxury": 420
                },
                "food": {
                    "budget": 38,
                    "mid-range": 75,
                    "luxury": 140
                },
                "local_transport": 16,
                "attractions": 28
            },
            "austin": {
                "accommodation": {
                    "budget": 100,
                    "mid-range": 180,
                    "luxury": 320
                },
                "food": {
                    "budget": 30,
                    "mid-range": 65,
                    "luxury": 120
                },
                "local_transport": 12,
                "attractions": 20
            },
            "san francisco": {
                "accommodation": {
                    "budget": 160,
                    "mid-range": 260,
                    "luxury": 450
                },
                "food": {
                    "budget": 45,
                    "mid-range": 85,
                    "luxury": 160
                },
                "local_transport": 18,
                "attractions": 28
            },
            "nashville": {
                "accommodation": {
                    "budget": 110,
                    "mid-range": 190,
                    "luxury": 340
                },
                "food": {
                    "budget": 35,
                    "mid-range": 70,
                    "luxury": 130
                },
                "local_transport": 12,
                "attractions": 22
            },
            "new orleans": {
                "accommodation": {
                    "budget": 105,
                    "mid-range": 185,
                    "luxury": 330
                },
                "food": {
                    "budget": 40,
                    "mid-range": 75,
                    "luxury": 140
                },
                "local_transport": 12,
                "attractions": 20
            }
        }

        # Normalize destination
        destination_key = destination.lower().split(",")[0].strip()

        if destination_key not in budget_data:
            # Provide a generic budget if specific city isn't found
            return f"Specific budget data not available for {destination}. As a general estimate for a US city:\n\n" + \
                   f"For {num_people} people for {num_days} days with {accommodation_type} accommodations:\n" + \
                   f"- Accommodation: ${100 * num_days} - ${300 * num_days} (varies widely by city)\n" + \
                   f"- Food: ${35 * num_people * num_days} - ${75 * num_people * num_days}\n" + \
                   f"- Local transportation: ${15 * num_people * num_days}\n" + \
                   f"- Attractions: ${20 * num_people * num_days}\n\n" + \
                   f"Estimated total: ${(100 + 35 * num_people + 15 * num_people + 20 * num_people) * num_days} - " + \
                   f"${(300 + 75 * num_people + 15 * num_people + 20 * num_people) * num_days}"

        # Calculate accommodation cost (assumes 2 people per room)
        rooms_needed = (num_people + 1) // 2  # Round up division
        accommodation_cost = budget_data[destination_key]["accommodation"][accommodation_type] * rooms_needed * num_days

        # Calculate food cost
        food_cost = budget_data[destination_key]["food"][accommodation_type] * num_people * num_days

        # Calculate transportation and attractions costs
        transport_cost = budget_data[destination_key]["local_transport"] * num_people * num_days
        attractions_cost = budget_data[destination_key]["attractions"] * num_people * num_days

        # Calculate total cost
        total_cost = accommodation_cost + food_cost + transport_cost + attractions_cost

        # Format the response
        response = f"Estimated Budget for {num_people} people in {destination} for {num_days} days ({accommodation_type} level):\n\n"
        response += f"🏨 Accommodation: ${accommodation_cost} (${budget_data[destination_key]['accommodation'][accommodation_type]} per room × {rooms_needed} room(s) × {num_days} nights)\n\n"
        response += f"🍽️ Food: ${food_cost} (${budget_data[destination_key]['food'][accommodation_type]} per person per day × {num_people} people × {num_days} days)\n\n"
        response += f"🚌 Local Transportation: ${transport_cost} (${budget_data[destination_key]['local_transport']} per person per day × {num_people} people × {num_days} days)\n\n"
        response += f"🎟️ Attractions: ${attractions_cost} (${budget_data[destination_key]['attractions']} per person per day × {num_people} people × {num_days} days)\n\n"
        response += f"💰 Total Estimated Cost: ${total_cost}\n\n"
        response += "Note: This is a base estimate. Actual costs may vary based on season, specific accommodations, dining preferences, and activities chosen."

        return response
    except Exception as e:
        return f"Error calculating budget: {str(e)}"

# Hotel recommendation tool
@tool
def find_hotels(location: str, check_in: str, check_out: str, num_people: int, budget_level: str, preferences: str = "") -> str:
    """Finds hotel accommodations based on traveler preferences.

    Args:
        location: US city (e.g., 'Chicago, IL')
        check_in: Check-in date (YYYY-MM-DD)
        check_out: Check-out date (YYYY-MM-DD)
        num_people: Number of guests
        budget_level: 'budget', 'mid-range', or 'luxury'
        preferences: String of comma-separated preferences (e.g., 'breakfast,pet-friendly,pool')
    """
    try:
        # Parse preferences
        pref_list = [p.strip().lower() for p in preferences.split(",") if p.strip()]

        # Mock hotel database
        hotel_db = {
            "new york": [
                {
                    "name": "Budget Inn NYC",
                    "level": "budget",
                    "price": 129,
                    "rating": 3.5,
                    "features": ["wifi", "air conditioning"],
                    "breakfast": False,
                    "pet_friendly": False,
                    "check_in": "3:00 PM",
                    "check_out": "11:00 AM",
                    "deposit": "First night's stay",
                    "cancellation": "24 hours before check-in",
                    "address": "123 Budget St, New York, NY",
                    "room_types": ["Queen", "Double Twin"]
                },
                {
                    "name": "Midtown Comfort Hotel",
                    "level": "mid-range",
                    "price": 229,
                    "rating": 4.2,
                    "features": ["wifi", "gym", "air conditioning"],
                    "breakfast": True,
                    "pet_friendly": True,
                    "pet_fee": 50,
                    "check_in": "4:00 PM",
                    "check_out": "12:00 PM",
                    "deposit": "First night's stay",
                    "cancellation": "48 hours before check-in",
                    "address": "456 Midtown Ave, New York, NY",
                    "room_types": ["Queen", "King", "Double Queen"]
                },
                {
                    "name": "Grand Manhattan Hotel",
                    "level": "luxury",
                    "price": 450,
                    "rating": 4.8,
                    "features": ["wifi", "spa", "gym", "pool", "concierge", "room service"],
                    "breakfast": True,
                    "pet_friendly": True,
                    "pet_fee": 100,
                    "check_in": "3:00 PM",
                    "check_out": "12:00 PM",
                    "deposit": "First night's stay",
                    "cancellation": "72 hours before check-in",
                    "address": "789 Luxury Blvd, New York, NY",
                    "room_types": ["King", "Junior Suite", "Executive Suite"]
                }
            ],
            "chicago": [
                {
                    "name": "Windy City Budget Stay",
                    "level": "budget",
                    "price": 99,
                    "rating": 3.6,
                    "features": ["wifi", "air conditioning"],
                    "breakfast": False,
                    "pet_friendly": False,
                    "check_in": "3:00 PM",
                    "check_out": "11:00 AM",
                    "deposit": "First night's stay",
                    "cancellation": "24 hours before check-in",
                    "address": "123 Economy Ave, Chicago, IL",
                    "room_types": ["Queen", "Double Twin"]
                },
                {
                    "name": "Lakeside Inn",
                    "level": "mid-range",
                    "price": 189,
                    "rating": 4.3,
                    "features": ["wifi", "gym", "air conditioning", "restaurant"],
                    "breakfast": True,
                    "pet_friendly": True,
                    "pet_fee": 40,
                    "check_in": "3:00 PM",
                    "check_out": "12:00 PM",
                    "deposit": "First night's stay",
                    "cancellation": "48 hours before check-in",
                    "address": "456 Lakeview Dr, Chicago, IL",
                    "room_types": ["Queen", "King", "Double Queen"]
                },
                {
                    "name": "The Chicago Grand Hotel",
                    "level": "luxury",
                    "price": 350,
                    "rating": 4.7,
                    "features": ["wifi", "spa", "gym", "pool", "concierge", "room service"],
                    "breakfast": True,
                    "pet_friendly": True,
                    "pet_fee": 75,
                    "check_in": "4:00 PM",
                    "check_out": "12:00 PM",
                    "deposit": "First night's stay",
                    "cancellation": "72 hours before check-in",
                    "address": "789 Magnificent Mile, Chicago, IL",
                    "room_types": ["King", "Junior Suite", "Executive Suite"]
                }
            ],
            "austin": [
                {
                    "name": "Austin Budget Inn",
                    "level": "budget",
                    "price": 89,
                    "rating": 3.4,
                    "features": ["wifi", "air conditioning", "free parking"],
                    "breakfast": False,
                    "pet_friendly": True,
                    "pet_fee": 25,
                    "check_in": "3:00 PM",
                    "check_out": "11:00 AM",
                    "deposit": "First night's stay",
                    "cancellation": "24 hours before check-in",
                    "address": "123 Budget Ln, Austin, TX",
                    "room_types": ["Queen", "Double Twin"]
                },
                {
                    "name": "Riverside Hotel Austin",
                    "level": "mid-range",
                    "price": 169,
                    "rating": 4.3,
                    "features": ["wifi", "pool", "gym", "air conditioning", "restaurant"],
                    "breakfast": True,
                    "pet_friendly": True,
                    "pet_fee": 35,
                    "check_in": "3:00 PM",
                    "check_out": "12:00 PM",
                    "deposit": "First night's stay",
                    "cancellation": "48 hours before check-in",
                    "address": "456 Riverside Dr, Austin, TX",
                    "room_types": ["Queen", "King", "Double Queen"]
                },
                {
                    "name": "Austin Luxury Resort",
                    "level": "luxury",
                    "price": 320,
                    "rating": 4.6,
                    "features": ["wifi", "spa", "gym", "pool", "concierge", "room service", "golf"],
                    "breakfast": True,
                    "pet_friendly": True,
                    "pet_fee": 50,
                    "check_in": "4:00 PM",
                    "check_out": "11:00 AM",
                    "deposit": "50% of total stay",
                    "cancellation": "72 hours before check-in",
                    "address": "789 Luxury Way, Austin, TX",
                    "room_types": ["King", "Junior Suite", "Executive Suite"]
                }
            ]
        }

        # Normalize location
        location_key = location.lower().split(",")[0].strip()

        if location_key not in hotel_db:
            return f"Hotel information not available for {location}. In a real implementation, this would connect to a hotel API."

        # Filter hotels by budget level
        matching_hotels = [h for h in hotel_db[location_key] if h["level"] == budget_level]

        # Filter by preferences if provided
        if "breakfast" in pref_list:
            matching_hotels = [h for h in matching_hotels if h.get("breakfast", False)]

        if "pet-friendly" in pref_list:
            matching_hotels = [h for h in matching_hotels if h.get("pet_friendly", False)]

        if "pool" in pref_list:
            matching_hotels = [h for h in matching_hotels if "pool" in h.get("features", [])]

        # Prepare response
        if not matching_hotels:
            return f"No hotels found in {location} matching your criteria. Try adjusting your preferences or budget level."

        # Format response
        response = f"Hotels in {location} ({budget_level}):\n\n"

        for hotel in matching_hotels:
            response += f"🏨 {hotel['name']} - ${hotel['price']} per night\n"
            response += f"⭐ Rating: {hotel['rating']}/5\n"
            response += f"📍 Address: {hotel['address']}\n"

            features_str = ", ".join(hotel['features'])
            response += f"✨ Features: {features_str}\n"

            room_types_str = ", ".join(hotel['room_types'])
            response += f"🛏️ Room Types: {room_types_str}\n"

            response += f"🕒 Check-in: {hotel['check_in']}, Check-out: {hotel['check_out']}\n"

            if hotel.get("breakfast", False):
                response += "🍳 Breakfast included\n"

            if hotel.get("pet_friendly", False):
                response += f"🐾 Pet-friendly (Fee: ${hotel.get('pet_fee', 0)})\n"

            response += f"💰 Deposit: {hotel['deposit']}\n"
            response += f"❌ Cancellation: {hotel['cancellation']}\n"

            response += "\n"

        return response
    except Exception as e:
        return f"Error finding hotels: {str(e)}"

# Restaurant recommendation tool
@tool
def find_restaurants(location: str, cuisine_type: str = "", dietary_preferences: str = "", price_range: str = "", near_address: str = "") -> str:
    """Finds restaurants based on location and dining preferences.

    Args:
        location: US city or neighborhood (e.g., 'Miami, FL')
        cuisine_type: Type of cuisine (e.g., 'Italian', 'Chinese', 'Indian')
        dietary_preferences: Dietary restrictions (e.g., 'vegetarian', 'halal', 'gluten-free')
        price_range: Budget level ('$', '$$', '$$$', '$$$$')
        near_address: Optional address to find nearby restaurants
    """
    try:
        # Mock restaurant database
        restaurant_db = {
            "new york": [
                {
                    "name": "Little Italy Pizzeria",
                    "cuisine": "Italian",
                    "price_range": "$$",
                    "rating": 4.3,
                    "dietary_options": ["vegetarian"],
                    "signature_dish": "Margherita Pizza",
                    "address": "123 Little Italy St, New York, NY",
                    "hours": "11:00 AM - 10:00 PM"
                },
                {
                    "name": "Golden Dragon",
                    "cuisine": "Chinese",
                    "price_range": "$$",
                    "rating": 4.1,
                    "dietary_options": ["vegetarian"],
                    "signature_dish": "Peking Duck",
                    "address": "456 Chinatown Ave, New York, NY",
                    "hours": "11:30 AM - 11:00 PM"
                },
                {
                    "name": "Taj Mahal",
                    "cuisine": "Indian",
                    "price_range": "$$",
                    "rating": 4.4,
                    "dietary_options": ["vegetarian", "halal"],
                    "signature_dish": "Butter Chicken",
                    "address": "789 Curry Row, New York, NY",
                    "hours": "12:00 PM - 10:30 PM"
                },
                {
                    "name": "Le Bernardin",
                    "cuisine": "French",
                    "price_range": "$$$$",
                    "rating": 4.8,
                    "dietary_options": [],
                    "signature_dish": "Seafood Tasting Menu",
                    "address": "155 W 51st St, New York, NY",
                    "hours": "5:00 PM - 10:00 PM"
                },
                {
                    "name": "Green Garden",
                    "cuisine": "Vegan",
                    "price_range": "$$",
                    "rating": 4.2,
                    "dietary_options": ["vegetarian", "vegan", "gluten-free"],
                    "signature_dish": "Buddha Bowl",
                    "address": "321 Healthy Ave, New York, NY",
                    "hours": "10:00 AM - 9:00 PM"
                }
            ],
            "austin": [
                {
                    "name": "Texas BBQ House",
                    "cuisine": "American",
                    "price_range": "$$",
                    "rating": 4.5,
                    "dietary_options": [],
                    "signature_dish": "Beef Brisket",
                    "address": "123 BBQ Lane, Austin, TX",
                    "hours": "11:00 AM - 10:00 PM"
                },
                {
                    "name": "Taco Heaven",
                    "cuisine": "Mexican",
                    "price_range": "$",
                    "rating": 4.4,
                    "dietary_options": ["vegetarian"],
                    "signature_dish": "Street Tacos",
                    "address": "456 Taco St, Austin, TX",
                    "hours": "10:00 AM - 11:00 PM"
                },
                {
                    "name": "Sushi Ko",
                    "cuisine": "Japanese",
                    "price_range": "$$$",
                    "rating": 4.6,
                    "dietary_options": ["gluten-free"],
                    "signature_dish": "Omakase",
                    "address": "789 Sushi Blvd, Austin, TX",
                    "hours": "12:00 PM - 10:30 PM"
                },
                {
                    "name": "Veggie Paradise",
                    "cuisine": "Vegetarian",
                    "price_range": "$$",
                    "rating": 4.2,
                    "dietary_options": ["vegetarian", "vegan", "gluten-free"],
                    "signature_dish": "Impossible Burger",
                    "address": "101 Green St, Austin, TX",
                    "hours": "11:00 AM - 9:00 PM"
                },
                {
                    "name": "Halal Grill",
                    "cuisine": "Middle Eastern",
                    "price_range": "$$",
                    "rating": 4.3,
                    "dietary_options": ["halal"],
                    "signature_dish": "Lamb Kebab",
                    "address": "202 Halal Way, Austin, TX",
                    "hours": "11:00 AM - 10:00 PM"
                }
            ],
            "chicago": [
                {
                    "name": "Deep Dish Heaven",
                    "cuisine": "American",
                    "price_range": "$$",
                    "rating": 4.6,
                    "dietary_options": ["vegetarian"],
                    "signature_dish": "Chicago Deep Dish Pizza",
                    "address": "123 Pizza Ave, Chicago, IL",
                    "hours": "11:00 AM - 11:00 PM"
                },
                {
                    "name": "Windy City Steakhouse",
                    "cuisine": "American",
                    "price_range": "$$$$",
                    "rating": 4.7,
                    "dietary_options": [],
                    "signature_dish": "Dry-aged Ribeye",
                    "address": "456 Steak Blvd, Chicago, IL",
                    "hours": "5:00 PM - 10:30 PM"
                },
                {
                    "name": "Little Saigon",
                    "cuisine": "Vietnamese",
                    "price_range": "$$",
                    "rating": 4.4,
                    "dietary_options": ["gluten-free"],
                    "signature_dish": "Pho",
                    "address": "789 Vietnam St, Chicago, IL",
                    "hours": "11:00 AM - 10:00 PM"
                },
                {
                    "name": "Taste of India",
                    "cuisine": "Indian",
                    "price_range": "$$",
                    "rating": 4.3,
                    "dietary_options": ["vegetarian", "halal"],
                    "signature_dish": "Chicken Tikka Masala",
                    "address": "101 Curry Lane, Chicago, IL",
                    "hours": "12:00 PM - 10:00 PM"
                },
                {
                    "name": "Green Leaf",
                    "cuisine": "Vegan",
                    "price_range": "$$",
                    "rating": 4.2,
                    "dietary_options": ["vegetarian", "vegan", "gluten-free"],
                    "signature_dish": "Vegan Chicago Dog",
                    "address": "202 Healthy Way, Chicago, IL",
                    "hours": "10:00 AM - 9:00 PM"
                }
            ]
        }

        # Normalize location
        location_key = location.lower().split(",")[0].strip()

        if location_key not in restaurant_db:
            return f"Restaurant information not available for {location}. In a real implementation, this would connect to a restaurant API."

        # Get all restaurants in the location
        restaurants = restaurant_db[location_key]

        # Apply filters
        if cuisine_type:
            cuisine_list = [c.strip().lower() for c in cuisine_type.split(",")]
            filtered_restaurants = []
            for restaurant in restaurants:
                if restaurant["cuisine"].lower() in cuisine_list:
                    filtered_restaurants.append(restaurant)
            restaurants = filtered_restaurants

        if dietary_preferences:
            dietary_list = [d.strip().lower() for d in dietary_preferences.split(",")]
            filtered_restaurants = []
            for restaurant in restaurants:
                if any(diet in [opt.lower() for opt in restaurant["dietary_options"]] for diet in dietary_list):
                    filtered_restaurants.append(restaurant)
            restaurants = filtered_restaurants

        if price_range:
            restaurants = [r for r in restaurants if r["price_range"] == price_range]

        # Prepare response
        if not restaurants:
            return f"No restaurants found in {location} matching your criteria. Try adjusting your preferences."

        # Format response
        response = f"Restaurants in {location}:\n\n"

        for restaurant in restaurants:
            response += f"🍽️ {restaurant['name']} - {restaurant['price_range']}\n"
            response += f"⭐ Rating: {restaurant['rating']}/5\n"
            response += f"🍳 Cuisine: {restaurant['cuisine']}\n"
            response += f"🏆 Signature Dish: {restaurant['signature_dish']}\n"
            response += f"📍 Address: {restaurant['address']}\n"
            response += f"🕒 Hours: {restaurant['hours']}\n"

            if restaurant["dietary_options"]:
                dietary_str = ", ".join(restaurant["dietary_options"])
                response += f"🥗 Dietary options: {dietary_str}\n"

            response += "\n"

        return response
    except Exception as e:
        return f"Error finding restaurants: {str(e)}"

# Fast food/chain restaurant finder
@tool
def find_nearby_food_chains(location: str, chain_name: str = "", near_address: str = "") -> str:
    """Finds nearby food chains and fast food restaurants.

    Args:
        location: US city or neighborhood (e.g., 'Las Vegas, NV')
        chain_name: Specific chain to search for (e.g., 'McDonald's', 'Starbucks')
        near_address: Address or hotel name to find nearby options
    """
    try:
        # Mock food chain database
        chain_db = {
            "new york": {
                "McDonald's": ["123 Broadway, New York, NY", "456 5th Ave, New York, NY", "789 Times Square, New York, NY"],
                "Starbucks": ["111 Park Ave, New York, NY", "222 Broadway, New York, NY", "333 7th Ave, New York, NY"],
                "Chipotle": ["444 8th Ave, New York, NY", "555 Broadway, New York, NY"],
                "Subway": ["666 6th Ave, New York, NY", "777 Broadway, New York, NY"],
                "Panda Express": ["888 Canal St, New York, NY"]
            },
            "chicago": {
                "McDonald's": ["123 Michigan Ave, Chicago, IL", "456 State St, Chicago, IL"],
                "Starbucks": ["111 Wacker Dr, Chicago, IL", "222 Michigan Ave, Chicago, IL"],
                "Chipotle": ["444 State St, Chicago, IL"],
                "Subway": ["666 Clark St, Chicago, IL", "777 Michigan Ave, Chicago, IL"],
                "Portillo's": ["888 Clark St, Chicago, IL"]
            },
            "austin": {
                "McDonald's": ["123 Congress Ave, Austin, TX", "456 Lamar Blvd, Austin, TX"],
                "Starbucks": ["111 6th St, Austin, TX", "222 Congress Ave, Austin, TX"],
                "Chipotle": ["444 Lamar Blvd, Austin, TX"],
                "Subway": ["666 Congress Ave, Austin, TX"],
                "Whataburger": ["888 Lamar Blvd, Austin, TX", "999 Congress Ave, Austin, TX"]
            }
        }

        # Normalize location
        location_key = location.lower().split(",")[0].strip()

        if location_key not in chain_db:
            return f"Food chain information not available for {location}. In a real implementation, this would connect to a location API."

        # Filter by chain name if provided
        if chain_name:
            chain_name = chain_name.strip()
            if chain_name not in chain_db[location_key]:
                return f"{chain_name} locations not found in {location}."

            chains = {chain_name: chain_db[location_key][chain_name]}
        else:
            chains = chain_db[location_key]

        # Format response
        response = f"Food chains in {location}:\n\n"

        for chain, locations in chains.items():
            response += f"🍔 {chain}\n"
            for loc in locations:
                response += f"  📍 {loc}\n"
            response += "\n"

        return response
    except Exception as e:
        return f"Error finding food chains: {str(e)}"

# US Attractions finder based on traveler profile and interests
@tool
def find_attractions(location: str, traveler_profile: str, interests: str = "") -> str:
    """Finds tourist attractions based on traveler profile and interests.

    Args:
        location: US city (e.g., 'Orlando, FL')
        traveler_profile: Type of travelers ('single', 'couple', 'family_with_kids', 'seniors')
        interests: Comma-separated list of interests (e.g., 'adventure,history,nature')
    """
    try:
        # Parse interests
        interest_list = [i.strip().lower() for i in interests.split(",") if i.strip()]

        # Mock attractions database
        attractions_db = {
            "new york": {
                "popular": ["Times Square", "Statue of Liberty", "Empire State Building", "Central Park", "Metropolitan Museum of Art"],
                "history": ["Ellis Island", "9/11 Memorial & Museum", "American Museum of Natural History", "Tenement Museum"],
                "culture": ["Broadway", "Metropolitan Opera", "Museum of Modern Art (MoMA)", "The High Line"],
                "adventure": ["Hudson River Kayaking", "Coney Island", "Hell's Kitchen Food Tour"],
                "nature": ["Central Park", "Brooklyn Botanic Garden", "Prospect Park"],
                "romantic": ["Top of the Rock at sunset", "Central Park carriage ride", "Dinner cruise on Hudson River"],
                "family": ["Central Park Zoo", "American Museum of Natural History", "Bronx Zoo", "Intrepid Sea, Air & Space Museum"],
                "nightlife": ["Rooftop bars in Manhattan", "Comedy clubs", "Jazz clubs in Harlem", "Clubs in Meatpacking District"],
                "shopping": ["Fifth Avenue", "SoHo", "Chelsea Market"]
            },
            "chicago": {
                "popular": ["Millennium Park & Cloud Gate", "Navy Pier", "The Art Institute of Chicago", "Willis Tower Skydeck"],
                "history": ["Chicago History Museum", "Field Museum", "Architecture River Cruise"],
                "culture": ["The Art Institute of Chicago", "Symphony Center", "Chicago Theatre"],
                "adventure": ["Lakefront Trail biking", "Chicago River kayaking", "Willis Tower Skydeck"],
                "nature": ["Lincoln Park", "Garfield Park Conservatory", "Chicago Botanic Garden"],
                "romantic": ["Navy Pier Ferris Wheel", "Signature Room at sunset", "Architecture River Cruise"],
                "family": ["Shedd Aquarium", "Museum of Science and Industry", "Lincoln Park Zoo", "Navy Pier"],
                "nightlife": ["River North bars", "Comedy clubs", "Jazz clubs", "Blue Chicago"],
                "shopping": ["Magnificent Mile", "State Street", "Wicker Park boutiques"]
            },
            "miami": {
                "popular": ["South Beach", "Art Deco Historic District", "Bayside Marketplace", "Wynwood Walls"],
                "history": ["Vizcaya Museum & Gardens", "Freedom Tower", "Ancient Spanish Monastery"],
                "culture": ["Pérez Art Museum", "Wynwood Walls", "Little Havana"],
                "adventure": ["Everglades airboat tour", "Deep sea fishing", "Jet skiing", "Parasailing"],
                "nature": ["Everglades National Park", "Biscayne National Park", "Miami Beach Botanical Garden"],
                "romantic": ["South Beach sunset walk", "Dinner cruise on Biscayne Bay", "Vizcaya Gardens"],
                "family": ["Miami Seaquarium", "Jungle Island", "Zoo Miami", "Miami Children's Museum"],
                "nightlife": ["South Beach clubs", "Wynwood bars", "Ball & Chain in Little Havana"],
                "shopping": ["Bayside Marketplace", "Aventura Mall", "Dolphin Mall"]
            },
            "austin": {
                "popular": ["Texas State Capitol", "Lady Bird Lake", "Zilker Park", "South Congress Avenue"],
                "history": ["Texas State Capitol", "Bullock Texas State History Museum", "LBJ Presidential Library"],
                "culture": ["Austin City Limits Live", "The Contemporary Austin", "Live music on 6th Street"],
                "adventure": ["Barton Springs Pool", "Lake Travis Zipline Adventures", "Paddleboarding on Lady Bird Lake"],
                "nature": ["Zilker Park", "Lady Bird Johnson Wildflower Center", "Hamilton Pool Preserve"],
                "romantic": ["Mount Bonnell at sunset", "Lake Austin dinner cruise", "Moonlight towers"],
                "family": ["Thinkery Children's Museum", "Zilker Park Playground", "Austin Aquarium", "Texas Memorial Museum"],
                "nightlife": ["6th Street bars", "Rainey Street", "Continental Club", "Antone's"],
                "shopping": ["South Congress Avenue", "The Domain", "2nd Street District"]
            },
            "las vegas": {
                "popular": ["The Strip", "Bellagio Fountains", "Fremont Street Experience", "High Roller Observation Wheel"],
                "history": ["The Mob Museum", "Neon Museum", "Springs Preserve"],
                "culture": ["Cirque du Soleil shows", "Bellagio Gallery of Fine Art", "Smith Center for the Performing Arts"],
                "adventure": ["Grand Canyon helicopter tour", "Zip line on Fremont Street", "Dune buggy desert tour"],
                "nature": ["Red Rock Canyon", "Valley of Fire State Park", "Hoover Dam"],
                "romantic": ["Gondola ride at The Venetian", "Eiffel Tower viewing deck", "Bellagio Fountains at night"],
                "family": ["Adventuredome at Circus Circus", "Shark Reef at Mandalay Bay", "Tournament of Kings"],
                "nightlife": ["Casino nightclubs", "Fremont Street bars", "Rooftop lounges", "Magic shows"],
                "shopping": ["The Forum Shops at Caesars", "Grand Canal Shoppes", "Las Vegas North Premium Outlets"]
            }
        }

        # Normalize location
        location_key = location.lower().split(",")[0].strip()

        if location_key not in attractions_db:
            return f"Attraction information not available for {location}. In a real implementation, this would connect to a tourism API."

        # Map traveler profile to interest categories
        profile_to_interests = {
            "single": ["popular", "adventure", "nightlife", "culture"],
            "couple": ["romantic", "culture", "popular", "nightlife"],
            "family_with_kids": ["family", "popular", "nature", "adventure"],
            "seniors": ["history", "culture", "popular", "nature"]
        }

        # Determine which categories to show based on profile
        selected_categories = []

        # Add profile-based categories
        if traveler_profile in profile_to_interests:
            selected_categories.extend(profile_to_interests[traveler_profile])

        # Add specific interest categories if provided
        for interest in interest_list:
            if interest in attractions_db[location_key] and interest not in selected_categories:
                selected_categories.append(interest)

        # Deduplicate and ensure "popular" is included
        if "popular" not in selected_categories:
            selected_categories.append("popular")

        # Format response
        response = f"Recommended attractions in {location} for {traveler_profile.replace('_', ' ')}:\n\n"

        for category in selected_categories:
            if category in attractions_db[location_key]:
                response += f"--- {category.capitalize()} Attractions ---\n"
                for attraction in attractions_db[location_key][category]:
                    response += f"• {attraction}\n"
                response += "\n"

        return response
    except Exception as e:
        return f"Error finding attractions: {str(e)}"

# Transportation route planner
@tool
def plan_transportation(from_city: str, to_city: str, transport_mode: str = "all") -> str:
    """Plans transportation between US cities with multiple options.

    Args:
        from_city: Starting city (e.g., 'Austin, TX')
        to_city: Destination city (e.g., 'New York, NY')
        transport_mode: Type of transportation ('air', 'train', 'bus', 'car', or 'all')
    """
    try:
        # Mock transportation database
        transport_db = {
            "austin-new york": {
                "air": [
                    {"airline": "American Airlines", "duration": "3h 50m", "price_range": "$200-450", "direct": True},
                    {"airline": "Delta", "duration": "3h 45m", "price_range": "$220-480", "direct": True},
                    {"airline": "United", "duration": "5h 30m", "price_range": "$180-350", "direct": False}
                ],
                "train": [
                    {"operator": "Amtrak", "duration": "2d 5h", "price_range": "$280-450", "transfers": 2}
                ],
                "bus": [
                    {"operator": "Greyhound", "duration": "1d 18h", "price_range": "$180-250", "transfers": 2}
                ],
                "car": {
                    "distance": "1,742 miles",
                    "duration": "26h (non-stop)",
                    "estimated_fuel": "$230-290",
                    "route": "I-35 N, I-40 E, I-81 N, I-78 E"
                }
            },
            "new york-chicago": {
                "air": [
                    {"airline": "United", "duration": "2h 20m", "price_range": "$150-300", "direct": True},
                    {"airline": "American Airlines", "duration": "2h 25m", "price_range": "$160-320", "direct": True}
                ],
                "train": [
                    {"operator": "Amtrak", "duration": "19h 30m", "price_range": "$120-210", "transfers": 0}
                ],
                "bus": [
                    {"operator": "Greyhound", "duration": "18h", "price_range": "$90-150", "transfers": 0},
                    {"operator": "Megabus", "duration": "17h 30m", "price_range": "$80-140", "transfers": 0}
                ],
                "car": {
                    "distance": "790 miles",
                    "duration": "12h (non-stop)",
                    "estimated_fuel": "$100-130",
                    "route": "I-80 W, I-90 W"
                }
            },
            "los angeles-las vegas": {
                "air": [
                    {"airline": "Southwest", "duration": "1h 10m", "price_range": "$80-180", "direct": True},
                    {"airline": "Spirit", "duration": "1h 15m", "price_range": "$60-150", "direct": True}
                ],
                "train": [],  # No direct train service
                "bus": [
                    {"operator": "Greyhound", "duration": "5h 30m", "price_range": "$30-60", "transfers": 0},
                    {"operator": "Megabus", "duration": "5h 45m", "price_range": "$25-55", "transfers": 0},
                    {"operator": "Flixbus", "duration": "5h", "price_range": "$20-50", "transfers": 0}
                ],
                "car": {
                    "distance": "270 miles",
                    "duration": "4h (non-stop)",
                    "estimated_fuel": "$35-45",
                    "route": "I-15 N"
                }
            }
        }

        # Normalize city names and create route key
        from_key = from_city.lower().split(",")[0].strip()
        to_key = to_city.lower().split(",")[0].strip()
        route_key = f"{from_key}-{to_key}"

        # Check if route exists
        if route_key not in transport_db:
            # Try reverse route
            route_key = f"{to_key}-{from_key}"
            if route_key not in transport_db:
                return f"Transportation information not available for route between {from_city} and {to_city}. In a real implementation, this would connect to transportation APIs."

        # Filter by transport mode
        if transport_mode != "all" and transport_mode not in ["air", "train", "bus", "car"]:
            return f"Invalid transport mode. Please choose from 'air', 'train', 'bus', 'car', or 'all'."

        # Format response
        response = f"Transportation options from {from_city} to {to_city}:\n\n"

        modes_to_show = [transport_mode] if transport_mode != "all" else ["air", "train", "bus", "car"]

        for mode in modes_to_show:
            if mode == "car":
                car_info = transport_db[route_key]["car"]
                response += f"🚗 By Car:\n"
                response += f"  • Distance: {car_info['distance']}\n"
                response += f"  • Driving time: {car_info['duration']}\n"
                response += f"  • Estimated fuel cost: {car_info['estimated_fuel']}\n"
                response += f"  • Suggested route: {car_info['route']}\n\n"
            else:
                options = transport_db[route_key].get(mode, [])

                if not options:
                    response += f"No direct {mode} service available for this route.\n\n"
                    continue

                if mode == "air":
                    response += f"✈️ By Air:\n"
                elif mode == "train":
                    response += f"🚄 By Train:\n"
                elif mode == "bus":
                    response += f"🚌 By Bus:\n"

                for option in options:
                    if mode == "air":
                        response += f"  • {option['airline']} - {option['duration']} "
                        response += f"({'Direct' if option['direct'] else 'Connecting'})\n"
                        response += f"    Price range: {option['price_range']}\n"
                    elif mode in ["train", "bus"]:
                        response += f"  • {option['operator']} - {option['duration']} "
                        if option['transfers'] > 0:
                            response += f"({option['transfers']} transfer{'s' if option['transfers'] > 1 else ''})\n"
                        else:
                            response += "(Direct)\n"
                        response += f"    Price range: {option['price_range']}\n"

                response += "\n"

        return response
    except Exception as e:
        return f"Error planning transportation: {str(e)}"

# Local transportation options
@tool
def get_local_transportation(city: str, from_location: str = "", to_location: str = "", transport_type: str = "") -> str:
    """Provides information about local transportation options within a US city.

    Args:
        city: US city (e.g., 'Boston, MA')
        from_location: Starting point or address (optional)
        to_location: Destination point or address (optional)
        transport_type: Type of transportation ('subway', 'bus', 'rideshare', 'taxi', 'rental')
    """
    try:
        # Mock local transportation database
        transport_info = {
            "new york": {
                "subway": {
                    "name": "New York City Subway",
                    "fare": "$2.75 per ride",
                    "pass_options": ["Day Pass: $13", "Week Pass: $33", "Month Pass: $127"],
                    "hours": "24/7 service with late-night changes",
                    "coverage": "Most parts of Manhattan, Brooklyn, Queens, and The Bronx",
                    "app": "NYC Subway Map or Google Maps",
                    "tips": "Subway is often the fastest way to move around Manhattan and between boroughs."
                },
                "bus": {
                    "name": "MTA Bus",
                    "fare": "$2.75 per ride",
                    "pass_options": ["Same as subway passes"],
                    "hours": "Varies by route, many run 24/7",
                    "coverage": "All five boroughs",
                    "app": "MTA Bus Time or Google Maps",
                    "tips": "Buses are good for crosstown travel in Manhattan where subway options are limited."
                },
                "rideshare": {
                    "options": ["Uber", "Lyft", "Via"],
                    "estimated_cost": "$20-40 for most Manhattan rides",
                    "availability": "Widely available 24/7",
                    "tips": "Can be expensive during rush hour or bad weather. Shared rides available for lower costs."
                },
                "taxi": {
                    "name": "Yellow Cab (in Manhattan) or Green Cab (outer boroughs)",
                    "fare_structure": "Base fare $2.50 + $0.50 per 1/5 mile or per 60 seconds in slow traffic",
                    "availability": "Abundant in Manhattan, less common in outer boroughs",
                    "tips": "Hail on street or use Curb app. 15-20% tip expected."
                },
                "rental": {
                    "car": ["Enterprise", "Hertz", "Avis", "Zipcar"],
                    "bike": ["Citi Bike: $3.50 per 30-minute ride or $15/day pass"],
                    "scooter": ["Lime", "Bird"],
                    "tips": "Car rental not recommended due to traffic and expensive parking. Citi Bike is great for short trips."
                },
                "routes": {
                    "times square-empire state building": {
                        "subway": "Take the N, Q, R, or W train from Times Square to Herald Square, then walk east.",
                        "bus": "Take the M42 crosstown bus east, then transfer to M5 southbound.",
                        "walking": "20-minute walk (0.8 miles) down Broadway or 7th Avenue."
                    },
                    "central park-brooklyn bridge": {
                        "subway": "Take the 4/5/6 train from 59th St-Lexington Ave to Brooklyn Bridge-City Hall.",
                        "bus": "Take the M5 bus southbound.",
                        "walking": "Long walk (4.5 miles) down 5th Avenue and Broadway."
                    }
                }
            },
            "chicago": {
                "subway": {
                    "name": "Chicago 'L' Train",
                    "fare": "$2.50 per ride",
                    "pass_options": ["Day Pass: $10", "3-Day Pass: $20", "Week Pass: $28"],
                    "hours": "Varies by line, some 24/7",
                    "coverage": "Downtown and many neighborhoods, airport connections",
                    "app": "Ventra app or Google Maps",
                    "tips": "The 'L' is great for travel to/from downtown and the airports."
                },
                "bus": {
                    "name": "CTA Bus",
                    "fare": "$2.25 per ride",
                    "pass_options": ["Same as 'L' passes"],
                    "hours": "Varies by route",
                    "coverage": "Extensive coverage throughout the city",
                    "app": "CTA Bus Tracker or Google Maps",
                    "tips": "Buses fill gaps in the 'L' network and are good for east-west travel."
                },
                "rideshare": {
                    "options": ["Uber", "Lyft"],
                    "estimated_cost": "$15-30 for most city rides",
                    "availability": "Widely available 24/7",
                    "tips": "Good option during non-rush hour times."
                },
                "taxi": {
                    "name": "Chicago Taxi",
                    "fare_structure": "Base fare $3.25 + $2.25 per mile",
                    "availability": "Common in downtown and near hotels",
                    "tips": "Hail on street or use Curb app. 15-20% tip expected."
                },
                "rental": {
                    "car": ["Enterprise", "Hertz", "Avis", "Zipcar"],
                    "bike": ["Divvy Bikes: $3.30 per 30-minute ride or $15/day pass"],
                    "scooter": ["Lime", "Bird"],
                    "tips": "Divvy bikes are great for lakefront trail and neighborhoods."
                }
            },
            "san francisco": {
                "subway": {
                    "name": "BART (regional) and Muni Metro (city)",
                    "fare": "BART: $2-12 depending on distance, Muni: $2.50 per ride",
                    "pass_options": ["Muni Day Pass: $5", "Clipper Card for all systems"],
                    "hours": "BART: 5am-midnight, Muni varies by line",
                    "coverage": "BART connects to East Bay and airport, Muni serves city neighborhoods",
                    "app": "BART app, Muni app, or Google Maps",
                    "tips": "BART for longer trips, Muni for within city travel."
                },
                "bus": {
                    "name": "Muni Bus",
                    "fare": "$2.50 per ride",
                    "pass_options": ["Muni Day Pass: $5", "Muni Monthly Pass: $81"],
                    "hours": "Varies by route, some 24/7 routes",
                    "coverage": "Extensive city coverage",
                    "app": "Muni Mobile or Google Maps",
                    "tips": "Buses go where BART and Muni Metro don't."
                },
                "rideshare": {
                    "options": ["Uber", "Lyft"],
                    "estimated_cost": "$15-35 for most city rides",
                    "availability": "Widely available 24/7",
                    "tips": "Can be expensive during peak times, but convenient for hills."
                },
                "taxi": {
                    "name": "SF Taxi",
                    "fare_structure": "Base fare $3.50 + $3.00 per mile",
                    "availability": "Common downtown and in tourist areas",
                    "tips": "Hail on street or use Flywheel app. 15-20% tip expected."
                },
                "rental": {
                    "car": ["Enterprise", "Hertz", "Avis", "Zipcar"],
                    "bike": ["Bay Wheels: $3.49 per 30-minute ride or $15/day pass"],
                    "scooter": ["Lime", "Spin", "Bird"],
                    "tips": "Car rental challenging due to hills and parking. Consider bike for Golden Gate Park and waterfront."
                }
            }
        }

        # Normalize city
        city_key = city.lower().split(",")[0].strip()

        if city_key not in transport_info:
            return f"Local transportation information not available for {city}. In a real implementation, this would connect to local transit APIs."

        # Format response
        if from_location and to_location:
            # Normalize locations
            from_location_key = from_location.lower().strip()
            to_location_key = to_location.lower().strip()
            route_key = f"{from_location_key}-{to_location_key}"

            # Check if we have specific route information
            if "routes" in transport_info[city_key] and route_key in transport_info[city_key]["routes"]:
                route_info = transport_info[city_key]["routes"][route_key]

                response = f"How to get from {from_location} to {to_location} in {city}:\n\n"

                for mode, instruction in route_info.items():
                    if mode == "subway":
                        response += f"🚇 By Subway: {instruction}\n\n"
                    elif mode == "bus":
                        response += f"🚌 By Bus: {instruction}\n\n"
                    elif mode == "walking":
                        response += f"🚶 Walking: {instruction}\n\n"

                return response
            else:
                # If specific route not found, provide general transportation info
                response = f"Specific route information from {from_location} to {to_location} not available. Here are the general transportation options in {city}:\n\n"
                transport_type = ""  # Show all options since specific route not found
        else:
            response = f"Local transportation options in {city}:\n\n"

        # Filter by transport type if specified
        transport_types = [transport_type] if transport_type else ["subway", "bus", "rideshare", "taxi", "rental"]

        for t_type in transport_types:
            if t_type in transport_info[city_key]:
                info = transport_info[city_key][t_type]

                if t_type == "subway":
                    response += f"🚇 Subway/Metro: {info['name']}\n"
                    response += f"  • Fare: {info['fare']}\n"
                    response += f"  • Pass options: {', '.join(info['pass_options'])}\n"
                    response += f"  • Hours: {info['hours']}\n"
                    response += f"  • Coverage: {info['coverage']}\n"
                    response += f"  • Recommended app: {info['app']}\n"
                    response += f"  • Tip: {info['tips']}\n\n"

                elif t_type == "bus":
                    response += f"🚌 Bus: {info['name']}\n"
                    response += f"  • Fare: {info['fare']}\n"
                    response += f"  • Pass options: {', '.join(info['pass_options'])}\n"
                    response += f"  • Hours: {info['hours']}\n"
                    response += f"  • Coverage: {info['coverage']}\n"
                    response += f"  • Recommended app: {info['app']}\n"
                    response += f"  • Tip: {info['tips']}\n\n"

                elif t_type == "rideshare":
                    response += f"🚗 Rideshare Services:\n"
                    response += f"  • Available options: {', '.join(info['options'])}\n"
                    response += f"  • Estimated cost: {info['estimated_cost']}\n"
                    response += f"  • Availability: {info['availability']}\n"
                    response += f"  • Tip: {info['tips']}\n\n"

                elif t_type == "taxi":
                    response += f"🚕 Taxi: {info['name']}\n"
                    response += f"  • Fare structure: {info['fare_structure']}\n"
                    response += f"  • Availability: {info['availability']}\n"
                    response += f"  • Tip: {info['tips']}\n\n"

                elif t_type == "rental":
                    response += f"🚲 Rental Options:\n"
                    response += f"  • Car rental: {', '.join(info['car'])}\n"
                    response += f"  • Bike sharing: {', '.join(info['bike'])}\n"
                    response += f"  • Scooter sharing: {', '.join(info['scooter'])}\n"
                    response += f"  • Tip: {info['tips']}\n\n"

        return response
    except Exception as e:
        return f"Error getting local transportation information: {str(e)}"

# Crime and safety alerts
@tool
def get_safety_information(city: str) -> str:
    """Provides safety information and crime alerts for a US city.

    Args:
        city: US city (e.g., 'Miami, FL')
    """
    try:
        # Mock safety database
        safety_db = {
            "new york": {
                "safety_rating": "Good",
                "current_alerts": [
                    "Increased pickpocketing in popular tourist areas",
                    "Construction on Broadway between 42nd and 50th Streets"
                ],
                "safe_areas": ["Most of Manhattan", "Much of Brooklyn Heights", "Park Slope"],
                "caution_areas": ["Parts of the Bronx at night", "Parts of East Harlem late at night"],
                "emergency_numbers": {
                    "police": "911",
                    "tourist_police": "646-610-6655"
                },
                "tips": [
                    "Be aware of your surroundings in crowded tourist areas",
                    "Keep wallets and phones secure, especially on subway",
                    "Use licensed yellow or green taxis, or reputable rideshare apps",
                    "Be cautious with your belongings in Times Square and on the subway"
                ]
            },
            "chicago": {
                "safety_rating": "Good in tourist areas, variable elsewhere",
                "current_alerts": [
                    "Increased car break-ins in downtown parking garages",
                    "Pickpocketing along Magnificent Mile"
                ],
                "safe_areas": ["Downtown/Loop", "North Michigan Ave", "Lincoln Park", "Lakeview"],
                "caution_areas": ["Some South and West Side neighborhoods, especially at night"],
                "emergency_numbers": {
                    "police": "911",
                    "non-emergency": "311"
                },
                "tips": [
                    "Stay in well-lit, busy areas at night",
                    "Use caution when using public transit late at night",
                    "Keep valuables out of sight in parked cars",
                    "Be aware of surroundings when using ATMs"
                ]
            },
            "miami": {
                "safety_rating": "Generally good in tourist areas",
                "current_alerts": [
                    "Increased vehicle break-ins in South Beach parking areas",
                    "Be alert for hurricane warnings during season (June-November)"
                ],
                "safe_areas": ["South Beach (daytime)", "Downtown Miami", "Coral Gables", "Coconut Grove"],
                "caution_areas": ["Liberty City", "Overtown", "Some areas of Little Haiti at night"],
                "emergency_numbers": {
                    "police": "911",
                    "miami beach visitor center": "305-673-7400"
                },
                "tips": [
                    "Be cautious of scooter rental scams",
                    "Use hotel safes for valuables",
                    "Be aware of rip currents at beaches",
                    "Lock vehicles and don't leave valuables visible",
                    "Stay hydrated in hot weather"
                ]
            },
            "las vegas": {
                "safety_rating": "Good on Strip and tourist areas",
                "current_alerts": [
                    "Street performers may be aggressive in soliciting tips",
                    "Drink spiking incidents reported in some clubs"
                ],
                "safe_areas": ["The Strip", "Downtown (Fremont St)", "Most casino properties"],
                "caution_areas": ["Areas north and east of downtown", "Some parts of North Las Vegas"],
                "emergency_numbers": {
                    "police": "911",
                    "tourist safety hotline": "702-229-3111"
                },
                "tips": [
                    "Stay hydrated and use sunscreen in hot weather",
                    "Be cautious of 'card slappers' offering adult services",
                    "Watch your drink at all times in bars and clubs",
                    "Use casino ATMs rather than those on side streets",
                    "Be wary of 'friendly strangers' offering deals or special access"
                ]
            }
        }

        # Normalize city
        city_key = city.lower().split(",")[0].strip()

        if city_key not in safety_db:
            return f"Safety information not available for {city}. In a real implementation, this would connect to safety and crime data APIs."

        # Get safety info
        info = safety_db[city_key]

        # Format response
        response = f"⚠️ Safety Information for {city} ⚠️\n\n"
        response += f"Overall safety rating: {info['safety_rating']}\n\n"

        response += "Current alerts:\n"
        for alert in info['current_alerts']:
            response += f"• {alert}\n"
        response += "\n"

        response += "Generally safe areas:\n"
        for area in info['safe_areas']:
            response += f"• {area}\n"
        response += "\n"

        response += "Areas to use caution:\n"
        for area in info['caution_areas']:
            response += f"• {area}\n"
        response += "\n"

        response += "Emergency numbers:\n"
        for service, number in info['emergency_numbers'].items():
            response += f"• {service.title()}: {number}\n"
        response += "\n"

        response += "Safety tips:\n"
        for tip in info['tips']:
            response += f"• {tip}\n"

        return response
    except Exception as e:
        return f"Error retrieving safety information: {str(e)}"

# Image generation for attractions
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

# Create a custom DuckDuckGo search tool with rate limit handling
class RateLimitHandledDuckDuckGoSearchTool(DuckDuckGoSearchTool):
    def __call__(self, search_term: str) -> str:
        try:
            return super().__call__(search_term)
        except Exception as e:
            if "202 Ratelimit" in str(e):
                # Add a delay and retry once
                time.sleep(2)
                try:
                    return super().__call__(search_term)
                except Exception:
                    return f"Sorry, I couldn't perform the web search for '{search_term}' because of rate limiting. Please try again in a few minutes or try a different search term."
            return f"Error performing search for '{search_term}': {str(e)}"

# Add the DuckDuckGo search tool for up-to-date tourist information
search_tool = RateLimitHandledDuckDuckGoSearchTool()

# Create a wrapper for the search_tool that accepts a query parameter
@tool
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo.

    Args:
        query: The search query to look up on the web.

    Returns:
        str: Search results as text.
    """
    return search_tool(search_term=query)

# Using the final_answer function imported from tools.final_answer
# Not creating a FinalAnswerTool instance to avoid confusion

# Add a simple mock model class as fallback
class MockModel:
    """A simple mock model that doesn't require API calls"""
    
    def __init__(self, model_id="mock-model"):
        self.model_id = model_id
        self.memory = type('obj', (object,), {
            'steps': [],
            'reset': lambda: None
        })
        
    def run(self, prompt, additional_args=None):
        """Simple mock implementation that returns a fixed response"""
        # Create a mock step
        step = type('obj', (object,), {
            'step_number': 1,
            'model_output': f"I received your prompt: {prompt}",
            'tool_calls': None,
            'observations': "Processing the request locally without API calls.",
            'error': None,
            'input_token_count': 10,
            'output_token_count': 20,
            'duration': 0.5
        })
        
        # Add step to memory
        self.memory.steps.append(step)
        
        # Set final answer
        self.final_answer = "This is a mock response since we're having issues with the Hugging Face API. Please check your API token and model settings."
        
        return self.final_answer

# Try to use HfApiModel, but fall back to MockModel if it fails
try:
    # Set up the model with appropriate parameters for a tourist agent
    model = HfApiModel(
        max_tokens=1024,
        temperature=0.7,
        model_id='Qwen/Qwen2.5-Coder-32B-Instruct',  # Using the Qwen model with 32B parameters
        token=HUGGING_FACE_TOKEN  # Ensure the token is set correctly
        # Removed is_chat_model parameter as it's not supported
    )
    
    # Skip direct testing of the model as HfApiModel doesn't have a run method
    # The model will be tested when used through the CodeAgent
    print(f"Model initialized with: {model.model_id}")
    
except Exception as e:
    print(f"Error with HfApiModel: {str(e)}")
    print("Falling back to mock model for demonstration purposes")
    model = MockModel()

# Load prompt templates
with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

# Add customized greeting handling to the prompt templates
prompt_templates["system_prompt"] = prompt_templates.get("system_prompt", "") + "\n\nWhen a user simply greets you (with messages like 'hi', 'hello', etc.), respond with a friendly greeting and offer to help with travel planning. For all other queries, first check if there's a specific tool that can help answer the query directly. Only use web search if no specialized tool exists for the task."

# Add a safe Python interpreter with limited imports
@tool
def python_interpreter(answer: str) -> str:
    """Execute Python code with restricted imports for safety.

    Args:
        answer: Python code to execute
    """
    import re
    import io
    import sys
    from contextlib import redirect_stdout

    # List of allowed imports for security
    allowed_imports = [
        'statistics', 'random', 'collections', 'unicodedata',
        'stat', 'math', 'itertools', 'time', 're', 'datetime', 'queue'
    ]

    # Check for unauthorized imports
    import_pattern = re.compile(r'(?:from|import)\s+([a-zA-Z0-9_.]+)')
    imports = import_pattern.findall(answer)

    # Extract the base module name (before any dots)
    base_imports = [imp.split('.')[0] for imp in imports]

    # Find unauthorized imports
    unauthorized = [imp for imp in base_imports if imp not in allowed_imports]

    if unauthorized:
        return f"Import from {', '.join(unauthorized)} is not allowed. Authorized imports are: {', '.join(allowed_imports)}"

    # If imports are okay, execute the code
    f = io.StringIO()
    try:
        with redirect_stdout(f):
            exec(answer)
        output = f.getvalue()
        if output:
            return output
        else:
            return "Code executed successfully with no output."
    except Exception as e:
        return f"Error: {str(e)}"

# Create the agent with all tourism-related tools
agent = CodeAgent(
    model=model,
    tools=[
        get_current_time_in_timezone,
        get_weather_forecast,
        estimate_travel_budget,
        find_hotels,
        find_restaurants,
        find_nearby_food_chains,
        find_attractions,
        plan_transportation,
        get_local_transportation,
        get_safety_information,
        python_interpreter,
        web_search,
        image_generation_tool,
        final_answer  # Use the imported final_answer function, not final_answer_tool
    ],
    max_steps=8,  # Increased steps for more complex tourist queries
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name="USATourGuide",
    description="An AI travel assistant that helps tourists plan trips and navigate destinations within the United States.",
    prompt_templates=prompt_templates
)

# Launch the Gradio UI
if __name__ == "__main__":
    print("Starting USA Travel Guide Agent...")
    print(f"Using model: {model.model_id}")
    
    # Verify if token is available
    if HUGGING_FACE_TOKEN:
        print(f"Using Hugging Face token: {HUGGING_FACE_TOKEN[:4]}...{HUGGING_FACE_TOKEN[-4:] if len(HUGGING_FACE_TOKEN) > 8 else ''}")
    else:
        print("Warning: No Hugging Face token provided. Some models may not work correctly.")
    
    # List all available tools for debugging
    print("\nAvailable tools:")
    for i, tool_func in enumerate(agent.tools):
        if hasattr(tool_func, '__name__'):
            tool_name = tool_func.__name__
        elif hasattr(tool_func, 'name'):
            tool_name = tool_func.name
        else:
            tool_name = str(tool_func)
        print(f"  {i+1}. {tool_name}")
    
    print("\nVerifying agent configuration...")
    # Check if final_answer function is properly configured
    if any(getattr(tool, '__name__', '') == 'final_answer' for tool in agent.tools):
        print("✅ final_answer function is properly configured")
    else:
        print("⚠️ Warning: final_answer function might not be properly configured")
    
    print("\nInitializing Gradio UI...")
    try:
        GradioUI(agent).launch(share=False)  # Set share=True if you want to create a public link
        print("Gradio UI launched successfully!")
    except Exception as e:
        print(f"Error launching Gradio UI: {str(e)}")
        import traceback
        traceback.print_exc()