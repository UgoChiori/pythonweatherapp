import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
city = os.getenv("city")

# Define the URL for the API request
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

try:
    # Make a request to the weather API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Check if "main" exists in the response data
        if "main" in data:
            temperature = data["main"]["temp"]
            name = "Ugo!"

            # Conditional messages based on temperature
            if temperature > 30:
                print(f"It's a hot day, {name} please, stay hydrated, and wear sunscreen.")
            elif temperature > 20:
                print(f"It's a cooooool day, {name} Go out and have fun, but first, grab a coffee!")
            elif temperature < 10:
                print(f"It's a cold day, {name} please, stay warm.")
            else:
                print(f"The weather is moderate today, {name}. Have a great day!")
        else:
            print("Error: 'main' data not found in the response.")
            print("Response received:", data)  # Print full response for debugging

    else:
        print(f"Error fetching weather data. Status code: {response.status_code}")
        print("Response received:", response.json())  # Print error details

except Exception as e:
    print("There was an error fetching the weather data:", e)
