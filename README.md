# Flask-Blogging-Website-1

Here is your **complete Flask Blogging App README in a single script** — including a `requirements.txt`, how to run, setup DB, and all instructions:

---

### 📦 `README.md` (Single-Script Style for GitHub)

```markdown
# 📝 Flask Blogging App

A role-based blogging platform built using Flask, WTForms, and SQLAlchemy. Users can register, login, publish posts, comment, and like posts. Includes Admin, Publisher, and Visitor roles.

---

## 🚀 Features

- 🔐 Register/Login with email
- 📧 Email format validation
- 🧑‍💼 Role-based access (Admin, Publisher, Visitor)
- ✍️ Create/Edit/Delete posts (Admin & Publisher)
- 📥 Upload media (image, audio, video)
- 💬 Commenting system
- ❤️ Like/Unlike functionality
- 🔍 Search posts
- 📄 Pagination

---

## 📁 Project Structure

```

flask-blog/
│
├── app.py
├── config.py
├── extensions.py
│
├── models/
│   ├── user.py
│   ├── post.py
│   ├── comment.py
│   └── reaction.py
│
├── controllers/
├── routes/
├── forms/
│
├── templates/
│   ├── auth/
│   ├── posts/
│   └── base.html
│
├── static/
│
├── requirements.txt
└── README.md

````

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/flask-blog.git
cd flask-blog
````

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate         # Windows
# or
source venv/bin/activate      # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

If using raw SQLAlchemy:

```bash
python
>>> from app import create_app
>>> from extensions import db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

(Optional if using Flask-Migrate):

```bash
flask db init
flask db migrate -m "Initial"
flask db upgrade
```

---

## 🏃 Run the App

```bash
flask run
```

Visit: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Default User Roles

| Role      | Capabilities                        |
| --------- | ----------------------------------- |
| ADMIN     | Full access, edit/delete any post   |
| PUBLISHER | Create/manage their own posts       |
| VISITOR   | View posts, comment, and like posts |

---

## 📌 requirements.txt

```txt
Flask==3.1.1
Flask-WTF==1.2.1
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
email-validator==2.1.1
Werkzeug==3.0.1
```

---

## 🙋 Contribution

Pull requests are welcome. For major changes, please open an issue to discuss improvements.

---

---
```
