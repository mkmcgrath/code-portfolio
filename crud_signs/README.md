📘 CRUD Signs
CRUD Signs is a proof-of-concept terminal-based tool for managing orders and client information for a fictional sign company. It demonstrates how you might build a real-world database interface using Python and FastAPI.

🚀 Getting Started
Clone the repository and set up a virtual environment:

bash

# clone this repo using git clone

cd crud-signs

# create the virtual environment
python -m venv crud_venv

source crud_venv/bin/activate  # or use .\\crud_venv\\Scripts\\activate on Windows

pip install -r requirements.txt


▶️ Running the Application
First, run the FastAPI backend:

bash
Copy
uvicorn api.main:app --reload
Then, launch the terminal interface:

bash
Copy
python tui_interface.py
Log in with:

Username: admin

Password: secret

🛠️ Features
🔐 JWT-authenticated login

🧾 Create, view, update, and delete clients and orders

🔍 Search for clients by name

⚙️ FastAPI + SQLite backend

🧑‍💻 Clean and simple Python terminal UI frontend

🧱 Development Environment
OS: Arch Linux

Language: Python 3.13

Editor: VSCode

Frameworks & Libraries:

FastAPI

SQLAlchemy

Requests

Python-JOSE (JWT)

🔮 Future Development
Planned enhancements:

CSV export

Notes/attachments on orders

Pagination, sorting, and filtering

Role-based user access

Web frontend (e.g., React or Svelte)

🤝 Contributing
Pull requests welcome! Fork this repo and make your own changse, or feel free to get in touch.

📬 Contact: mkmcgrath.dev@gmail.com

