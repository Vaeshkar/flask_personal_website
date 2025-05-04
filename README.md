# 🖥️ Flask Personal Website

---

## 🧠 Project Overview

This project is a **personal portfolio website** built using the **Flask** web framework.  
It allows for **dynamic management of content** through an admin interface.

The goal was not only to build the frontend, but also to **plan and architect** the entire backend structure — from database design to user flows.

---

## 🔗 URL
https://flask-personal-website.onrender.com/

---

## 📂 Features

- Home page displaying personal information and projects.
- Admin login/logout functionality (authentication).
- Admin dashboard to update:
  - Personal bio information
  - Project listings
- Dynamic database-driven site (no hardcoded content).
- Secure handling of admin credentials.

---

## 🔥 Key Concepts Practiced

- Web application architecture (frontend ↔ backend communication)
- Flask route planning and HTTP method design (GET, POST)
- Database schema design (tables for user info, projects, authentication)
- Templating with Jinja2
- User authentication (login system)
- CRUD operations via the Flask backend
- Separation of concerns (frontend vs backend logic)

---

## 🚀 Technologies Used

- Python 3
- Flask
- Jinja2 Templates
- SQLite (or PostgreSQL if upgraded)
- HTML5, CSS3 (static files)

---

## 🗺️ Planned App Structure

| Endpoint | HTTP Method | Purpose |
|:---------|:------------|:--------|
| `/` | GET | Home page displaying public information |
| `/login` | GET, POST | Admin login form and login process |
| `/logout` | GET | Log out the admin |
| `/settings` | GET, POST | Admin dashboard to update profile and project info |
| `/project/add` | GET, POST | Add a new project (if implemented) |
| `/project/delete` | POST | Delete a project (if implemented) |

---

## 🛠️ Database Schema Overview

| Table | Fields |
|:------|:-------|
| **admin** | id, username, password_hash |
| **personal_info** | id, name, bio, contact_email, (etc.) |
| **projects** | id, title, description, link |

Constraints ensure consistency and data integrity across the app.

---

## 📜 License

This project is part of my coursework at **WBS Coding School**.  
It is intended for educational purposes and personal portfolio building.

---
