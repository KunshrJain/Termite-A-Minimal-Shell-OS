# 🔧 Mcu Live RAM Usage Monitor via Serial

Track your Mcu’s real-time **RAM usage** as a percentage via serial communication. Designed for embedded devs to visualize memory consumption every second, in real-time.

---

## 📦 Features

| Feature                         | Description                                        |
|-------------------------------|----------------------------------------------------|
| 💾 RAM Usage Monitor          | Prints `used RAM`, `free RAM`, and `% used`       |
| 🔁 Real-Time Updates           | Sends updates every 1000ms                         |
| 🎮 Serial Activation           | Starts on user input `'p'`                         |
| 🔍 Easy Debug Integration      | Add your code inside `runMain()` for tracking     |
| ⚡ Zero Library Dependency     | Pure C with no bloat                               |

---

## 🖥️ Serial Output Example

Connected to COM6 successfully.
Arduino 32256 367
ram-6
ram-14
ram-26
ram-39


---

## 🚀 Getting Started

### ✅ Requirements

| Tool            | Version / Info                |
|-----------------|-------------------------------|
| Arduino IDE     | v1.8+ or 2.x                  |
| Arduino Board   | UNO / Nano / ATmega328-based |
| USB Cable       | Standard USB/TTL              |
| Serial Monitor  | Arduino Serial / PuTTY        |

---

## 📂 Project Structure

├── Arduino_RAM_Monitor.ino # Main sketch
├── README.md # This file


---

## 🔧 Installation & Upload

git clone https://github.com/yourusername/arduino-ram-monitor.git

---

## 🔧 Installation & Upload

Clone repo 
upload code to MCU
run DesktopSide -> Main.py

---

| Step | Action                               |
| ---- | ------------------------------------ |
| 1    | Open Serial Monitor after upload     |
| 2    | Send `p` to begin monitoring         |
| 3    | RAM stats appear every 1 second      |
| 4    | Your program runs inside `runMain()` |



---

Let me know if you want a matching `requirements.txt` or `.ino` template to auto-link from GitHub, or a Python script to visualize the data on a live dashboard.
