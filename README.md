# Invisibility Cloak Web App

This is a Flask-based web application that simulates the invisibility effect using OpenCV. The project allows users to experience the invisibility cloak effect inspired by Harry Potter.

## 🚀 Live UI Preview

You can check out the **UI of the web app** here: 🔗 [Invisibility Cloak UI](https://invisibility-cloak-pjpz.onrender.com/)

⚠ **Note:** Since Render does not support direct webcam access, the invisibility effect will only work when you run the app locally.

## 🖥️ Running Locally

To use the invisibility effect, you need to run the app on your own computer.

### **1️⃣ Clone the Repository**

```sh
git clone https://github.com/lilypandey/Invisibility-Cloak.git
cd Invisibility-Cloak
```

### **2️⃣ Install Dependencies**

Ensure you have Python installed, then run:

```sh
pip install -r requirements.txt
```

### **3️⃣ Run the Application**

Change `app.run(host="0.0.0.0", port=10000)` to:

```python
app.run(debug=True)
```

Then, start the app with:

```sh
python app.py
```

By default, the app runs on `http://127.0.0.1:5000/`. Open it in your browser.

## 📂 Project Structure

```
Invisibility-Cloak/
│-- static/
│   ├── css/
│   │   ├── index.css
│   │   ├── camera.css
│   ├── images/
│   │   ├── castle-of-hogwarts.jpg
│-- templates/
│   ├── index.html
│   ├── camera.html
│-- app.py
│-- requirements.txt
│-- README.md
```

## ⚙️ Features

- Automatic HSV calibration for cloak detection 🎭
- Real-time invisibility effect using OpenCV 🪄
- Flask-based web interface 🌐

## 📌 Notes

- Ensure your **camera is working** before running the script.
- The background is captured at the start, so make sure **no one is in the frame** for the first few seconds.
- Click **Back** to stop the webcam before exiting.

## 🛠️ Technologies Used

- **Python** (Flask, OpenCV, NumPy)
- **HTML, CSS, JavaScript** for frontend
- **Render** for deployment (UI preview) (no webcam support)