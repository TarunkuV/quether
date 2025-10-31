import requests #pip install requests
import random
from tkinter import * # pi pinstall tkinter 
from tkinter import messagebox
from PIL import Image, ImageTk  # You need Pillow installed 

# -----------------------------
# CONFIGURATION
# -----------------------------
API_KEY = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
CITY_FILE = "cities.txt"
NUM_ROUNDS = 10
TEMP_RANGE = (-10, 45)

# -----------------------------
# GAME VARIABLES
# -----------------------------
current_round = 1
current_player = 1
scores = [0, 0]
city_list = []
city_label = None
result_label = None
player_label = None
slider = None

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def load_cities():
    global city_list
    try:
        with open(CITY_FILE, "r") as f:
            city_list = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{CITY_FILE}' not found!")
        root.destroy()

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
    if not city_list:
        load_cities()
    current_city = random.choice(city_list)
    city_label.config(text=f"🌆 Guess the temperature in {current_city}")

def submit_guess():
    global current_round, current_player

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

    current_round += 1
    if current_round > NUM_ROUNDS:
        end_game()
    else:
        current_player = 2 if current_player == 1 else 1
        player_label.config(text=f"👤 Player {current_player}'s turn")
        load_city()

def end_game():
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

    if scores[0] > scores[1]:
        winner = "🎉 Player 1 wins!"
    elif scores[1] > scores[0]:
        winner = "🎉 Player 2 wins!"
    else:
        winner = "🤝 It’s a tie!"

    Label(
        root,
        text=winner,
        font=("Segoe UI", 13, "bold"),
        bg="#EAF4F4",
        fg="#E67E22",
    ).pack(pady=(10, 30))

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
    global current_round, current_player, scores
    current_round = 1
    current_player = 1
    scores = [0, 0]
    show_game_ui()

# -----------------------------
# UI BUILDING
# -----------------------------
def build_game_ui():
    global city_label, result_label, player_label, slider

    root.configure(bg="#EAF4F4")

    # Header
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

    # Player label
    player_label = Label(
        root,
        text=f"👤 Player {current_player}'s turn",
        font=("Segoe UI", 13, "bold"),
        bg="#EAF4F4",
        fg="#333",
    )
    player_label.pack(pady=5)

    # City label
    city_label = Label(
        root,
        text="🌆 Guess the temperature...",
        font=("Segoe UI", 14, "bold"),
        bg="#EAF4F4",
        fg="#0077B6",
    )
    city_label.pack(pady=10)

    # Slider
    slider_frame = Frame(root, bg="#EAF4F4")
    slider_frame.pack(pady=15)

# --- Label above the slider ---
    Label(
        slider_frame,
        text="🌡️ Select your temperature guess (°C):",
        font=("Segoe UI", 10, "bold"),
        bg="#EAF4F4",
        fg="#005F73",
    ).pack(pady=(0, 5))

# --- Styled Slider ---
    slider = Scale(
    slider_frame,
    from_=TEMP_RANGE[0],
    to=TEMP_RANGE[1],
    orient=HORIZONTAL,
    length=320,
    tickinterval=10,
    bg="#EAF4F4",
    troughcolor="#A9DEF9",     # lighter sky blue groove
    highlightthickness=0,
    fg="#1A1A1A",
    font=("Segoe UI", 9),
    sliderrelief="flat",
)

# Make the slider handle (“knob”) stand out a bit
    slider.config(
        bd=0,
        activebackground="#0077B6",  # handle color when dragging
    )

    slider.pack(pady=(0, 5))

    # Submit button
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

    # Result label
    result_label = Label(
        root,
        text="",
        font=("Segoe UI", 12),
        bg="#EAF4F4",
        fg="#444",
    )
    result_label.pack(pady=10)

    # Footer
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

    # --- Title at top ---
    Label(
        root,
        text="🌦️Quether    🌍",
        font=("Poppins", 35, "bold"),
        bg="#D6F0FF",
        fg="#1A1A1A",
    ).pack(pady=(30, 10))  # 30px from top

    # --- Outer container for centered content ---
    container = Frame(root, bg="#D6F0FF")
    container.pack(expand=True)

    # --- Subtitle text ---
    Label(
        container,
        text="Guess the temperature of random cities!\nPlay with a friend and test your intuition 🔥",
        font=("Georgia", 11, "italic"),
        bg="#D6F0FF",
        fg="#333",
        justify="center",
        wraplength=350,
    ).pack(pady=(0, 15))

    # --- Button frame ---
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

    # --- Footer ---
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
root.geometry("450x450")
root.resizable(False, False)
root.configure(bg="#EAF4F4")


start_screen()
root.mainloop()


