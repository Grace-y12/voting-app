# 🗳️ Secure Voting App
A secure web-based voting system built with Django that uses RSA encryption and multi-committee member authentication for vote decryption to ensure vote integrity and controlled access to results

##  🚀 Features
-  RSA-based key authentication for committee members
-  Multi-user login approval for admin access
-  Digital signatures for vote decryption
-  Voter registration and authentication
-  Secure vote casting and vote encryption
-  Session-based login control (expires on browser close)
-  Facial recognition for identity validation (optional)

##  📂 Project Structure
voting_app/
├── vote/ # Main Django app
│ ├── templates/ # HTML templates
│ ├── static/ # CSS, JS files
│ ├── views.py # Application logic
│ ├── models.py # Database models
│ ├── forms.py # Login & registration forms
│ └── urls.py # App URLs
├── voting_system/ # Django project settings
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── db.sqlite3 # SQLite database
├── manage.py # Django management script
└── requirements.txt # Python dependencies

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Grace-y12/voting-app.git
cd voting-app

###  2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Apply Migrations
python manage.py makemigrations
python manage.py migrate

### 5. Run the Server
python manage.py runserver

### 6. Open in Browser
Go to http://127.0.0.1:8000/ in your browser.

🧪 Committee Member Login
Committee members must log in using their username and RSA key pair. Access to the admin dashboard is only granted when all three members have successfully authenticated.
##

## 📌 Technologies Used
1. Django (Python)

2.SQLite

3.Bootstrap (for UI)

4.RSA Encryption (rsa library)

5.Session Middleware
