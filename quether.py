import requests
import random
from tkinter import *
from tkinter import messagebox

# -----------------------------
# CONFIGURATION
# -----------------------------
API_KEY = "YOUR_API_KEY_HERE"  # <-- Replace with your OpenWeatherMap API key
CITY_FILE = "cities.txt"
NUM_ROUNDS = 10  # 5 per player
TEMP_RANGE = (-20, 50)  # in °C
ROUND_POINTS = 100  # base points

# -----------------------------
# FUNCTIONS
# -----------------------------

def get_temperature(city):
    """Fetch real-time temperature from OpenWeatherMap."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data.get("cod") != 200:
        return None
    return data["main"]["temp"]

def calculate_points(guess, actual):
    """Score based on accuracy."""
    difference = abs(guess - actual)
    return max(0, ROUND_POINTS - int(difference * 5))  # -5 points per °C off

def next_round():
    """Proceed to next city/turn or finish the game."""
    global current_round, current_player

    current_round += 1
    if current_round >= NUM_ROUNDS:
        end_game()
    else:
        # Alternate players each round
        current_player = 1 if current_player == 2 else 2
        load_city()

def load_city():
    """Load next city and reset UI."""
    global current_city, actual_temp
    current_city = cities[current_round]
    actual_temp = get_temperature(current_city)
    if actual_temp is None:
        # Skip city if API fails
        next_round()
        return

    city_label.config(text=f"🌆 Guess the temperature in {current_city}")
    result_label.config(text="")
    slider.set(0)
    player_label.config(text=f"👤 Player {current_player}'s turn")

def submit_guess():
    """Handle player's guess."""
    global scores
    guess = slider.get()
    points = calculate_points(guess, actual_temp)
    scores[current_player] += points

    result_label.config(
        text=f"Actual: {actual_temp:.1f}°C | You scored {points} pts!"
    )
    root.after(2000, next_round)  # wait 2 seconds, then move on

def end_game():
    """Show final scores and winner."""
    winner_text = ""
    if scores[1] > scores[2]:
        winner_text = "🏆 Player 1 Wins!"
    elif scores[2] > scores[1]:
        winner_text = "🏆 Player 2 Wins!"
    else:
        winner_text = "🤝 It's a Tie!"

    msg = f"Final Scores:\n\nPlayer 1: {scores[1]} pts\nPlayer 2: {scores[2]} pts\n\n{winner_text}"
    messagebox.showinfo("Game Over", msg)
    root.destroy()

# -----------------------------
# MAIN PROGRAM
# -----------------------------

# Load random cities
with open(CITY_FILE, "r") as f:
    cities = [line.strip() for line in f if line.strip()]
cities = random.sample(cities, NUM_ROUNDS)

# Initialize state
current_round = 0
current_player = 1
scores = {1: 0, 2: 0}
current_city = ""
actual_temp = 0.0

# -----------------------------
# TKINTER UI SETUP
# -----------------------------
root = Tk()
root.title("🌍 Quether - Guess the Weather")
root.geometry("400x350")
root.resizable(False, False)

player_label = Label(root, text=f"👤 Player {current_player}'s turn", font=("Arial", 13))
player_label.pack(pady=10)

city_label = Label(root, text="", font=("Arial", 14, "bold"))
city_label.pack(pady=10)

slider = Scale(
    root,
    from_=TEMP_RANGE[0],
    to=TEMP_RANGE[1],
    orient=HORIZONTAL,
    length=300,
    tickinterval=10,
)
slider.pack(pady=10)

submit_btn = Button(root, text="✅ Submit Guess", command=submit_guess, font=("Arial", 12))
submit_btn.pack(pady=10)

result_label = Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Start the game
load_city()
root.mainloop()
