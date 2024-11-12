from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")


@app.route('/')
def home():
    # Redirect to the /weather endpoint
    return redirect(url_for('get_weather'))

@app.route('/weather', methods=['GET'])
def get_weather():
    # Get city from query parameter or use the default
    city = request.args.get('city', os.getenv("CITY"))

    if not city:
        return render_template('weather.html')

    # Build the URL for the OpenWeatherMap API request
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    # Fetch the weather data from the API
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temperature = data["main"]["temp"]
            weather_message = determine_weather_message(temperature)

            # Render the HTML page with weather data
            return render_template('weather.html', city=city, temperature=temperature, message=weather_message)
        else:
            error_message = "Could not fetch weather data"
            return render_template('weather.html', message=error_message)

    except Exception as e:
        error_message = f"Error: {e}"
        return render_template('weather.html', message=error_message)

def determine_weather_message(temperature):
    # name = "Ugo!"
    if temperature > 30:
        return f"It's a hot day🥵🔥♨️🪭 please, stay hydrated, and wear sunscreen."
    elif temperature > 20:
        return f"It's a cooooool day!🚤🍹🏖️😎  Go out and have fun, but first, grab a coffee!"
    elif temperature < 10:
        return f"It's a cold day 🥶❄️ Please, stay warm."
    else:
        return f"The weather is moderate today. Have a great day!"

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True, port=5001)
