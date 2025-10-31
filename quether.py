import requests  # pip install requests
import random
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # pip install pillow
import numpy as np  # pip install numpy
import pandas as pd  # pip install pandas
import os

# -----------------------------
# CONFIGURATION
# -----------------------------
API_KEY = "091e71f0f2974ea55abd5c80c4c0f3a0"  # Replace with your OpenWeatherMap API key
NUM_ROUNDS = 10
TEMP_RANGE = (-10, 45)

# Leaderboard file path
LEADERBOARD_FILE = "quether_leaderboard.csv"

# -----------------------------
# GAME VARIABLES
# -----------------------------
current_round = 1
current_player = 1
scores = [0, 0]
city_label = None
result_label = None
player_label = None
slider = None
current_city = None
player1_guess = None
player1_points = None

results_df = pd.DataFrame(columns=[
    "Round", "City", "Actual Temp (°C)",
    "Player 1 Guess", "Player 2 Guess",
    "P1 Points", "P2 Points"
])

# Use NumPy array for cities
cities = np.array([
    "New York", "London", "Paris", "Tokyo", "Dubai", "Singapore", "Sydney",
    "Los Angeles", "Rome", "Berlin", "Toronto", "Hong Kong", "Madrid",
    "Istanbul", "Moscow", "Bangkok", "Beijing", "Shanghai", "Seoul",
    "Cape Town", "Rio de Janeiro", "São Paulo", "Mexico City", "Cairo",
    "Nairobi", "Athens", "Zurich", "Amsterdam", "Kuala Lumpur", "Vienna",
    "San Francisco", "Chicago", "Barcelona", "Prague", "Milan", "Doha",
    "Jakarta", "Vancouver", "Melbourne", "Mumbai", "Bangalore", "Vellore",
    "Chennai", "Delhi", "Navi Mumbai","Miami", "Boston", "Washington D.C.", 
    "Las Vegas", "Houston", "Dallas","Atlanta", "Montreal", "Ottawa",
    "Philadelphia", "San Diego","Denver", "Pune", "Cancun"
])


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def get_temperature(city):
    """Fetch current temperature (°C) from OpenWeatherMap API"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()
        return data["main"]["temp"]
    except Exception:
        return None


def load_city():
    global current_city
    current_city = np.random.choice(cities)
    city_label.config(text=f"🌆 Guess the temperature in {current_city}")


def submit_guess():
    global current_round, current_player, results_df
    global player1_guess, player1_points  # ✅ declare before usage

    guess = slider.get()
    actual_temp = get_temperature(current_city)

    if actual_temp is None:
        messagebox.showerror("Error", "Could not fetch weather data. Check your API key or internet.")
        return

    diff = abs(actual_temp - guess)
    points = max(0, 10 - int(diff))
    scores[current_player - 1] += points

    result_label.config(
        text=f"Actual: {actual_temp:.1f}°C | Your guess: {guess}°C | "
             f"Diff: {diff:.1f}°C | +{points} points"
    )

    if current_player == 1:
        player1_guess = guess
        player1_points = points
        current_player = 2
        player_label.config(text=f"👤 Player {current_player}'s turn")

    else:
        results_df.loc[len(results_df)] = [
            current_round, current_city, actual_temp,
            player1_guess, guess,
            player1_points, points
        ]
        current_round += 1
        current_player = 1
        player_label.config(text=f"👤 Player {current_player}'s turn")

    if current_round > NUM_ROUNDS:
        end_game()
    else:
        load_city()


def update_leaderboard(winner_name, points):
    """Create or update the persistent leaderboard CSV"""
    if os.path.exists(LEADERBOARD_FILE):
        leaderboard = pd.read_csv(LEADERBOARD_FILE)
    else:
        leaderboard = pd.DataFrame(columns=["Winner", "Points"])

    # Append new record
    leaderboard.loc[len(leaderboard)] = [winner_name, points]

    # Save back
    leaderboard.to_csv(LEADERBOARD_FILE, index=False)


def get_high_score():
    """Return the highest score and corresponding winner name"""
    if os.path.exists(LEADERBOARD_FILE):
        leaderboard = pd.read_csv(LEADERBOARD_FILE)
        if not leaderboard.empty:
            top_row = leaderboard.loc[leaderboard["Points"].idxmax()]
            return top_row["Winner"], top_row["Points"]
    return None, None


def end_game():
    global results_df

    for widget in root.winfo_children():
        widget.destroy()

    Label(
        root,
        text="🏆 Game Over! 🏆",
        font=("Poppins", 20, "bold"),
        bg="#EAF4F4",
        fg="#1A1A1A"
    ).pack(pady=(30, 10))

    Label(
        root,
        text=f"Player 1: {scores[0]} points\nPlayer 2: {scores[1]} points",
        font=("Segoe UI", 13, "bold"),
        bg="#EAF4F4",
        fg="#0077B6",
    ).pack(pady=10)

    # Determine winner
    if scores[0] > scores[1]:
        winner = "Player 1"
        winner_text = "🎉 Player 1 wins!"
        winning_points = scores[0]
    elif scores[1] > scores[0]:
        winner = "Player 2"
        winner_text = "🎉 Player 2 wins!"
        winning_points = scores[1]
    else:
        winner = "Tie"
        winner_text = "🤝 It’s a tie!"
        winning_points = max(scores)

    # Update leaderboard if not a tie
    if winner != "Tie":
        update_leaderboard(winner, winning_points)

    Label(
        root,
        text=winner_text,
        font=("Segoe UI", 13, "bold"),
        bg="#EAF4F4",
        fg="#E67E22",
    ).pack(pady=(10, 30))

    # 🧾 Show results table in console
    print("\n================ GAME RESULTS ================")
    print(results_df.to_string(index=False))
    print("=============================================\n")

    results_df.to_csv("quether_results.csv", index=False)

    # 🔝 Show high score at bottom
    top_player, top_score = get_high_score()
    if top_player:
        Label(
            root,
            text=f"🌟 High Score: {top_player} - {top_score} points",
            font=("Segoe UI", 11, "bold"),
            bg="#EAF4F4",
            fg="#0096C7",
        ).pack(pady=(0, 20))

    btn_frame = Frame(root, bg="#EAF4F4")
    btn_frame.pack(pady=10)

    Button(
        btn_frame,
        text="🔁 Play Again",
        font=("Segoe UI", 12, "bold"),
        bg="#0077B6",
        fg="white",
        activebackground="#00B4D8",
        relief="flat",
        padx=10,
        pady=5,
        command=restart_game,
        cursor="hand2",
    ).grid(row=0, column=0, padx=50)

    Button(
        btn_frame,
        text="❌ Exit",
        font=("Segoe UI", 12, "bold"),
        bg="#E74C3C",
        fg="white",
        activebackground="#FF6B6B",
        relief="flat",
        padx=10,
        pady=5,
        command=root.destroy,
        cursor="hand2",
    ).grid(row=0, column=1, padx=50)


def restart_game():
    global current_round, current_player, scores, results_df
    global player1_guess, player1_points
    current_round = 1
    current_player = 1
    scores = [0, 0]
    player1_guess = None
    player1_points = None
    results_df = pd.DataFrame(columns=[
        "Round", "City", "Actual Temp (°C)",
        "Player 1 Guess", "Player 2 Guess",
        "P1 Points", "P2 Points"
    ])
    show_game_ui()

# -----------------------------
# UI BUILDING
# -----------------------------
def build_game_ui():
    global city_label, result_label, player_label, slider

    root.configure(bg="#EAF4F4")

    Label(
        root,
        text="🌦️Quether    🌍",
        font=("Poppins", 20, "bold"),
        bg="#99D7EA",
        fg="#1A1A1A",
        relief="ridge",
        bd=2,
        padx=10,
        pady=5,
    ).pack(fill=X, pady=(0, 10))

    player_label = Label(
        root,
        text=f"👤 Player {current_player}'s turn",
        font=("Segoe UI", 13, "bold"),
        bg="#EAF4F4",
        fg="#333",
    )
    player_label.pack(pady=5)

    city_label = Label(
        root,
        text="🌆 Guess the temperature...",
        font=("Segoe UI", 14, "bold"),
        bg="#EAF4F4",
        fg="#0077B6",
    )
    city_label.pack(pady=10)

    slider_frame = Frame(root, bg="#EAF4F4")
    slider_frame.pack(pady=15)

    Label(
        slider_frame,
        text="🌡️ Select your temperature guess (°C):",
        font=("Segoe UI", 10, "bold"),
        bg="#EAF4F4",
        fg="#005F73",
    ).pack(pady=(0, 5))

    slider = Scale(
        slider_frame,
        from_=TEMP_RANGE[0],
        to=TEMP_RANGE[1],
        orient=HORIZONTAL,
        length=320,
        tickinterval=10,
        bg="#EAF4F4",
        troughcolor="#A9DEF9",
        highlightthickness=0,
        fg="#1A1A1A",
        font=("Segoe UI", 9),
        sliderrelief="flat",
    )
    slider.config(bd=0, activebackground="#0077B6")
    slider.pack(pady=(0, 5))

    Button(
        root,
        text="✅ Submit Guess",
        command=submit_guess,
        font=("Segoe UI", 12, "bold"),
        bg="#0077B6",
        fg="white",
        activebackground="#00B4D8",
        activeforeground="white",
        padx=15,
        pady=8,
        relief="flat",
        cursor="hand2",
    ).pack(pady=15)

    result_label = Label(
        root,
        text="",
        font=("Segoe UI", 12),
        bg="#EAF4F4",
        fg="#444",
    )
    result_label.pack(pady=10)

    Label(
        root,
        text="☁️ Powered by OpenWeatherMap",
        font=("Segoe UI", 9, "italic"),
        bg="#EAF4F4",
        fg="#666",
    ).pack(side="bottom", pady=5)

# -----------------------------
# SCREENS
# -----------------------------
def start_screen():
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#D6F0FF")

    Label(
        root,
        text="🌦️Quether    🌍",
        font=("Poppins", 35, "bold"),
        bg="#D6F0FF",
        fg="#1A1A1A",
    ).pack(pady=(30, 10))

    container = Frame(root, bg="#D6F0FF")
    container.pack(expand=True)

    Label(
        container,
        text="Guess the temperature of random cities!\nPlay with a friend and test your intuition 🔥",
        font=("Georgia", 11, "italic"),
        bg="#D6F0FF",
        fg="#333",
        justify="center",
        wraplength=350,
    ).pack(pady=(0, 15))

    btn_frame = Frame(container, bg="#D6F0FF")
    btn_frame.pack(pady=(5, 0))

    Button(
        btn_frame,
        text="▶ Start Game",
        font=("Segoe UI", 10, "bold"),
        bg="#0077B6",
        fg="white",
        activebackground="#00B4D8",
        relief="flat",
        padx=10,
        pady=5,
        cursor="hand2",
        command=show_game_ui,
        width=12
    ).grid(row=0, column=0, padx=8)

    Button(
        btn_frame,
        text="❌ Exit",
        font=("Segoe UI", 10, "bold"),
        bg="#E74C3C",
        fg="white",
        activebackground="#FF6B6B",
        relief="flat",
        padx=10,
        pady=5,
        cursor="hand2",
        command=root.destroy,
        width=12
    ).grid(row=0, column=1, padx=8)

    Label(
        root,
        text="☁️ Powered by OpenWeatherMap",
        font=("Segoe UI", 8, "italic"),
        bg="#D6F0FF",
        fg="#666",
    ).pack(side="bottom", pady=5)


def show_game_ui():
    for widget in root.winfo_children():
        widget.destroy()
    build_game_ui()
    load_city()

# -----------------------------
# TKINTER UI SETUP
# -----------------------------
root = Tk()
root.title("🌍 Quether - Guess the Weather")
root.geometry("450x480")
root.resizable(False, False)
root.configure(bg="#EAF4F4")

start_screen()
root.mainloop()
