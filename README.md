# 🏛️ NSI Booking App

A **Hall Booking Web Application** built with **FastAPI** and **Streamlit**, enabling users to register and reserve hourly time slots in a seamless, real-time interface.

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-High--Performance-brightgreen)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-orange)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---

## 📌 Features

- 🔐 **User Registration** with username, email, and password  
- 📅 **Real-Time Slot Booking** (9AM to 5PM, one-hour slots)  
- 📦 **FastAPI Backend API** with SQLite database  
- 🎨 **Streamlit Frontend** for an interactive user interface  
- ⚙️ **Input Validation** for time, slots, and user data  
- 🌐 **Cross-Origin Enabled** (CORS)

---

## 🚀 Demo

### 🖥️ Backend (`FastAPI`):
Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

![FastAPI Demo](https://user-images.githubusercontent.com/your-screenshot-link.png)

### 🌐 Frontend (`Streamlit`):

```bash
streamlit run frontend.py

```
## 📁 Folder Structure
```
NSI-Booking-App/
│
├── main.py             # FastAPI backend
├── frontend.py         # Streamlit frontend
├── requirements.txt    # All required packages
└── hall_booking.db     # (ignored) SQLite DB file
```
##📦 Installation & Setup
```
# Clone the repo
git clone https://github.com/MUSTAFAOP29/NSI-BOOKING-APP.git
cd NSI-BOOKING-APP

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run Backend
uvicorn main:app --reload

# Run Frontend
streamlit run frontend.py
```

##⚠️ Important Notes
Database file hall_booking.db is excluded from GitHub for security & storage reasons.
The backend must be running before accessing the Streamlit frontend.

## 🧠 Tech Stack
| Component  | Technology |
| ---------- | ---------- |
| Backend    | FastAPI    |
| Frontend   | Streamlit  |
| Database   | SQLite     |
| Validation | Pydantic   |
| API Docs   | Swagger UI |


✍️ Author
Syed Mustafa
B.Tech AI & Data Science | Developer & Startup Enthusiast

## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](www.linkedin.com/in/syedmustafa29)


