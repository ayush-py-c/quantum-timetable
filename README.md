
![image](https://github.com/user-attachments/assets/d00643c2-33ff-4607-9d4b-6556fe6f4b85)

#  Quantum Timetable System

**Quantum Timetable System** is an advanced scheduling application designed to manage course allocations with precision and clarity. Built with Flask and styled using Tailwind CSS, this system allows users to dynamically manage and view timetable entries.

![Quantum Timetable UI](https://via.placeholder.com/1000x500?text=Project+Screenshot)  
*A clean and futuristic UI for managing scheduling data.*

---

## 🧠 Features

- 🔄 Dynamic entry of timetable slots
- 🧑‍🎓 User-based course and teacher assignment
- 🕒 Clear display of schedule with date and time
- 💅 Sleek futuristic UI using Tailwind CSS
- ☁️ Deployed on Render with MySQL backend
- ➕ Modal popup for adding new entries
- 📅 Sortable and neatly formatted data table

---

## 📦 Tech Stack

| Layer       | Technology       |
|------------|------------------|
| Backend     | Flask (Python)   |
| Frontend    | HTML + Tailwind CSS |
| Database    | MySQL            |
| Deployment  | Render           |

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ayush-py-c/quantum-timetable.git
cd quantum-timetable
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Update your `.env` file (create one if not existing) with:

```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=quantum_timetable
```

Then initialize your MySQL database and run the schema script (if any).

### 5. Run the App

```bash
flask run
```

The app will be live at `http://127.0.0.1:5000/`

---

## 🖼️ UI Overview

- **Home Page**: Lists all active timetable entries
- **Add Entry Modal**: Pop-up form to create a new timetable entry
- **Responsive Table**: Displays `user_id`, `course_id`, `teacher_id`, and `datetime`

---

## 📸 Screenshots

<details>
<summary>📅 Main Dashboard</summary>

![Main Dashboard Screenshot](https://via.placeholder.com/800x400?text=Main+Dashboard)
</details>

---

## 🌐 Deployment

This app is deployed using [Render](https://render.com/):

- **Web Service** for Flask backend
- **MySQL Database** connected via private networking
- Environment variables managed via Render dashboard

---

## 📁 File Structure

```
quantum-timetable/
│
├── static/             # Tailwind CSS and assets
├── templates/          # HTML templates
├── app.py              # Main Flask app
├── requirements.txt    # Python dependencies
├── .env                # Environment config
└── README.md           # Project documentation
```

---

## 🙌 Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Render](https://render.com/)
- Iconography from [Lucide](https://lucide.dev/)

---

## 📄 License

MIT License. See `LICENSE` file for more details.
