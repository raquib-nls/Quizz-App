# 🧠 Flask Quiz Application

A fully functional **quiz web application** built using **Flask**, supporting category-wise questions, user login, administrator controls, and instant result evaluation.  
Deployed on **Render**, with a cloud-hosted PostgreSQL database.

---
## 📖 Project Description

**Flask Quiz Application** is a fully functional, category-based quiz platform built using the Flask framework. 
It enables users to register, log in, and take quizzes filtered by categories and subcategories — with instant result evaluation including score, percentage, grade, and detailed question review.

The application includes a secure admin panel for managing quiz content, supporting bulk JSON uploads and individual question add. 
It uses PostgreSQL for database management, bcrypt for password hashing, and follows environment variable practices for secure deployment on **Render**.

This project highlights strong full-stack development capabilities, showcasing both backend logic, database handling, and frontend user interaction in a production-ready environment.

---

## 🚀 Features

### 👥 Users
- 🔐 Secure registration and login
- 📚 Attempt quizzes by category & subcategory
- 🧾 Get instant feedback with:
  - Score
  - Percentage
  - Grade
  - Per-question correct/incorrect review

### 🔐 Admin
- ✨ Clean admin login (with password hashing)
- 📤 Upload questions via JSON
- ➕ Add or 🗑️ delete individual questions
- 📂 Filter questions by category and subcategory

---

## 🛠 Tech Stack

- **Frontend:** HTML, CSS, Jinja2
- **Backend:** Python, Flask
- **Database:** MySQL (cloud-hosted on db4free.net)
- **Security:** bcrypt password hashing
- **Hosting:** Render

---

## 🗂 Project Structure

```
quiz-app/
├── static/                  # CSS/static files
├── templates/               # HTML pages (Jinja2)
├── .env                     # Hidden file for DB and secrets (not pushed)
├── app.py                   # Main Flask application
├── db.py                    # Database connection helper
├── admin.py                 # Admin logic (uses env vars; keep sensitive parts secure)
├── requirements.txt         # Python dependencies
├── uploads/                 # json file(s)
└── README.md                # This file
```

---

## 🔐 Environment Variables

Create a `.env` file in your project folder and add sensitive configs like database info, Flask secret key, and admin login credentials.

> ⚠️ **Never upload your `.env` to GitHub.** Be sure to add it to `.gitignore`.

Example `.gitignore`:
```
.env
__pycache__/
*.pyc
instance/
```

---

## 💻 Installation (Local Testing)(Optional)
This step is only needed if you want to run the project locally instead of using the deployed Render version.

### ✅ Requirements
- Python 3.x
- pip (Python package manager)

### ⚙️ Setup Steps

```bash
git clone https://github.com/your-username/quiz-app.git
cd quiz-app
pip install -r requirements.txt
```

Create a `.env` file and set your environment variables:

```
DB_HOST=your_postgres_host
DB_PORT=5432
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_NAME=your_postgres_database_name
SECRET_KEY=your_flask_secret_key
ADMIN_EMAIL=your_admin_email
ADMIN_PASSWORD=your_admin_password (bcrypt hashed)
```

Then run the app:

```bash
python app.py
```

Open your browser and go to:  
📍 `http://127.0.0.1:5000`

## 🧾 Sample JSON Format for Question Upload

```json
{
  "categories": {
    "Sports": {
      "Cricket": {
        "sub_id": 1,
        "questions": [
          {
            "question": "Which country won the first Cricket World Cup in 1975?",
            "option1": "India",
            "option2": "Australia",
            "option3": "West Indies",
            "option4": "England",
            "correct_option": "c"
          }
        ]
      }
    }
  }
}
```
> ✅ Make sure the `correct_option` is one of `"a"`, `"b"`, `"c"`, or `"d"` corresponding to option1–4.

---

## 🌐 Live App

🔗 **Live Demo:** [https://quiz-app-q7v3.onrender.com](https://quizz-app-q7v3.onrender.com)  


---

## 🏁 Future Improvements

- Leaderboard system
- User quiz history
- Mobile app version (React Native / Flutter)
- AI-generated questions

---

## 🙌 Credits

Made with ❤️ by [**Mohd Raquib Hussain**](https://github.com/raquib-nls)  
🎓 Third-Year B.Tech Student | Artificial Intelligence & Machine Learning 
Connect with me on [LinkedIn](https://www.linkedin.com/in/mohd-raquib-hussain-nls108)
---
## 🙏 Acknowledgments

- [Bootstrap](https://getbootstrap.com/) – for responsive frontend components
- [Flask Documentation](https://flask.palletsprojects.com/) – for backend routing & session handling
- Various online communities, tutorials, and blogs for helping implement secure login, session management, and JSON parsing logic

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).
