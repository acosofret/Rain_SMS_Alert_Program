import requests
from twilio.rest import Client
from my_vars import *

# Go to https://openweathermap.org/api?ref=apilist.fun and read the documentation,
# then get your API Key
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = OPENWEATHERMAP_API_KEY # this is hidden for security. Update with your own API Key.
# Then go to https://www.twilio.com/, sign-up for a free account and read the documentation.
# Get your 'account sid' and your 'authentication token', the copy them in the variables below:
twilio_account_sid = TWILIO_ACC_SID # this is hidden for security. Update with your own 'account sid'.
twilio_auth_token = TWILIO_AUTH_TOKEN # this is hidden for security. Update with your own 'authentication token'.

weather_params = {
	"lat": 51.400459,
	"lon": -1.321850,
	"appid": api_key,
	"cnt": 4,
}

# Pull weather data from our Openweather Endpoint, in json format:
response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

today_codes = []
# codes is a specific parameter in the weather data that refers to the chances of rain at a specific time
# read the openweather documentation for full details

# we code in the rules, as if the "code" is <700 (high chance of rain), an action is made (send SMS using Twilio):
codes_score = 0
for item in weather_data["list"]:
	code = item["weather"][0]["id"]
	today_codes.append(code)

for code in today_codes:
	if int(code) < 700:
		codes_score += int(code)
if codes_score > 0:
	# If condition for high-probability rain is met, then we send SMS via Twilio service
	# (read documentation for full details)
	client = Client(twilio_account_sid, twilio_auth_token)
	message = client.messages \
		.create(
		body="It may rain today. Remember to bring an umbrella.☂️", # you can customise this message
		from_=MY_TWILIO_NUMBER, # Number shown in your own Twilio account.
		to=MY_NUMBER # Here, enter your own phone number.
	)
	print(message.status)