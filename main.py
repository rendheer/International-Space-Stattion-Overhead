import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 37.662571
MY_LONG = -77.485130

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    print(f"ISS Lat {iss_latitude}")
    print(f"ISS Lng {iss_longitude}")
    print(f"My Lat {MY_LAT}")
    print(f"My Lng {MY_LONG}")

    if MY_LAT-5 <= iss_latitude >= 5 and MY_LONG <= iss_longitude >= 5:
        return True


#Your position is within +5 or -5 degrees of the ISS position.

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    print(f"Sunrise {sunrise}")
    print(f"Sunset {sunset}")

    time_now = datetime.now()
    current_hour = time_now.hour
    print(f"Current Hour {current_hour}")
    if current_hour <= sunrise or current_hour >= sunset:
        return True


def send_letter(name, message_to_send):
    my_email = "rendheer_joshy@yahoo.com"
    password = "toxjwadamcckymbh"
    with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="jrendheer@gmail.com",
            msg=f"Subject:Look Up - International Space Station - {name}\n\n{message_to_send}"
        )

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        print("Time to see the station")
        send_letter(name="Joshy", message_to_send="The International Space Station can be see above you now")
    else:
        print("Too early to see the station")





