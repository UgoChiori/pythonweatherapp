from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")

@app.route('/weather', methods=['GET'])
def get_weather():
    # Get city from query parameter or use the default
    city = request.args.get('city', os.getenv("CITY"))

    # Build the URL for the OpenWeatherMap API request
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    # Fetch the weather data from the API
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temperature = data["main"]["temp"]
            weather_message = determine_weather_message(temperature)

            # Return the data as JSON
            return jsonify({
                "city": city,
                "temperature": temperature,
                "message": weather_message
            }), 200
        else:
            return jsonify({"error": "Could not fetch weather data"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def determine_weather_message(temperature):
    name = "Ugo!"
    if temperature > 30:
        return f"It's a hot day, {name} please, stay hydrated, and wear sunscreen."
    elif temperature > 20:
        return f"It's a cooooool day, {name} Go out and have fun, but first, grab a coffee!"
    elif temperature < 10:
        return f"It's a cold day, {name} please, stay warm."
    else:
        return f"The weather is moderate today, {name}. Have a great day!"

if __name__ == '__main__':
    app.run(debug=True)
