# 🌿 GreenPulse AI
### AI-Powered Crop Yield Prediction and Optimization Platform

![GreenPulse AI](https://img.shields.io/badge/GreenPulse-AI-green)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey)
![AI](https://img.shields.io/badge/AI-95.7%25%20Accuracy-brightgreen)

---

## 🌾 About the Project

GreenPulse AI is an AI-powered smart farming platform that helps
farmers predict crop yields, detect plant diseases, and get
real-time weather alerts — all in one place.

Built for the **Agriculture, FoodTech & Rural Development** hackathon
theme to solve the problem of unpredictable crop yields and
inefficient resource allocation.

---

## 🎯 Problem We Solve

Farmers face huge financial losses due to:
- Unpredictable weather conditions
- Uncertain crop yield forecasts
- Lack of early disease detection
- No personalized farming recommendations

**GreenPulse AI solves all of these problems!**

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 AI Yield Prediction | Predicts crop yield with 95.7% accuracy |
| 🔬 Disease Detection | Detects 4 crop diseases with 98.8% accuracy |
| 🌦️ Real Weather Data | Live weather from OpenWeatherMap API |
| 📧 Email Alerts | Automatic alerts for weather risks |
| 📊 Farm Dashboard | Real-time monitoring of farm conditions |
| 🔒 Secure Authentication | Farmer login with Flask-Login & Bcrypt |

---

## 🖥️ Pages

- **index.html** — Landing page with features overview  
- **login.html** —  
  ✅ Brand new login page  
  ✅ Connects to Flask backend  
  ✅ Saves farmer to localStorage  
  ✅ Press Enter to login  

- **register.html** —  
  ✅ Connects to real backend  
  ✅ Shows real error messages  
  ✅ Redirects after success  

- **dashboard.html** — Real-time farm dashboard with charts and predictions  
- **predict.html** — AI crop yield prediction  
- **upload.html** — Plant disease detection  

---

## 🌾 Workflow Updates

- When farmer clicks **Predict** →  
  ✅ AI predicts yield  
  ✅ Result saved to database  
  ✅ Linked to farmer’s account  
  ✅ Shows in **Recent Predictions** table  

---

## 📊 Dashboard Charts

| Chart | Type | Description |
|-------|------|-------------|
| 📊 Crop Yield Bar | Bar Chart | Compare all 8 crops side by side |
| 🥧 Crop Distribution | Pie Chart | See how farm area is split |
| 🌧️ Monthly Rainfall | Bar Chart | Blue bars show rainfall per month |
| 🌡️ Weather Gauges | Circular Gauges | Temperature & Humidity, live updates |
| 🦠 Disease Risk | Doughnut Chart | Risk levels for 4 crop diseases |

---

## 🤖 AI Models

### Model 1 — Crop Yield Prediction
- Algorithm: Random Forest Regressor  
- Accuracy: **95.7%**  
- Inputs: Crop type, temperature, rainfall, humidity, area, fertilizer, soil type, season  
- Output: Predicted yield in tons per hectare  

### Model 2 — Disease Detection
- Algorithm: Random Forest Classifier  
- Accuracy: **98.8%**  
- Detects: Healthy Leaf, Leaf Blight, Rust Disease, Powdery Mildew  
- Input: Leaf image upload  

---

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, JavaScript  
- Chart.js for data visualization  
- Responsive design for mobile and desktop  

### Backend
- Python 3.13  
- Flask 3.0  
- Flask-CORS  
- Flask-Login, Flask-Bcrypt  
- Scikit-learn  
- Pandas, NumPy  
- Pillow (image processing)  

### APIs
- OpenWeatherMap API (real weather data)  
- Gmail SMTP (email alerts)  

---

## 📁 Project Structure
```
GreenPulse-AI/
├── index.html          # Landing page
├── login.html          # Farmer login
├── register.html       # Registration
├── dashboard.html      # Farm dashboard
├── predict.html        # Yield prediction
├── upload.html         # Disease detection
├── css/
│   └── style.css       # Styles
├── js/
│   └── main.js         # JavaScript
└── backend/
    ├── app.py          # Flask server
    ├── ai_model.py     # Yield AI model
    ├── disease_model.py # Disease AI model
    ├── train_model.py  # Train yield model
    ├── train_disease_model.py # Train disease model
    ├── models/         # Saved AI models
    ├── routes/
    │   ├── predict.py  # Yield prediction API
    │   ├── weather.py  # Weather API
    │   └── disease.py  # Disease detection API
    └── services/
        ├── weather_service.py # Weather service
        └── email_service.py   # Email service
```

---

## 🚀 How to Run

### STEP 1 — Clone the repo
```bash
git clone https://github.com/muhammedfahim438-ctrl/GreenPulse-AI.git
cd GreenPulse-AI
```

### STEP 2 — Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### STEP 3 — Install packages
```bash
pip install flask flask-cors flask-login flask-bcrypt requests python-dotenv scikit-learn pandas numpy joblib pillow
```

### STEP 4 — Set up .env file
```
WEATHER_API_KEY=your_openweathermap_api_key
EMAIL_ADDRESS=your_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
ALERT_EMAIL=your_gmail@gmail.com
```

### STEP 5 — Train AI models
```bash
cd backend
python train_model.py
python train_disease_model.py
```

### STEP 6 — Run Flask server
```bash
python app.py
```

### STEP 7 — Open frontend
Open `index.html` with Live Server in VS Code

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/predict | Crop yield prediction |
| GET | /api/weather | Real weather data |
| POST | /api/disease | Disease detection |
| POST | /api/alert/send | Send email alert |

---

## 🎯 Evaluation Criteria

| Criteria | Weight | Your Solution |
|----------|--------|---------------|
| Accuracy of Yield Prediction | 40% | **95.7% accurate ✅** |
| Actionability of Recommendations | 25% | **Farming tips ✅** |
| Scalability & Data Integration | 20% | **Flask REST API ✅** |
| User Adoption & Usability | 10% | **Clean UI ✅** |
| Documentation & Sustainability | 5% | **README ✅** |

---

## 👨‍💻 Team — Catalyst Crew

We are **Catalyst Crew**, a passionate team of 4 members:

1. Muhammed Fahim  
2. Shain Shafi  
3. Sree Kuttan  
4. Vijay K  

Built with ❤️ for the Hackathon

---

## 📄 License

MIT License
```

---

Now your README proudly shows your **team name (Catalyst Crew)** and all members.  

Would you like me to also generate a **requirements.txt file** that matches these dependencies, so your setup instructions are fully consistent and easy for others to install?
