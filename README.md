# Welcome to the Python Pantry!

The Python Pantry app uses Python 3.11+ and Kivy 2.31. 

The purpose of this app is to provide a way for users to interact with the Python Pantry. This includes checking the pantry's inventory, donating goods, volunteering to pick up donations, and selecting food for them to pick up if they are in need. 

Leaving the name and password blank will sign you into the guest account, which will let you see the entire app, but will not allow you to interact with certain features. This includes saving allergens, changing settings, ordering food, or volunteering to pick up donations. To have access to these things, the user must create an account.

# Python Pantry - Local Run

To run locally:

1. Create a Python 3.11+ venv and install dependencies:

MAC:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

WINDOWS:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

NOTE: if above does not work on windows, try:
```bash
py -m venv .venv
```

If these steps do not work, ensure you are in the correct directory before creating the virtual environment

2. Run the app:

```bash
python3 app.py
```

NOTE: if above does not work on windows, try:
```bash
py app.py
```

If the UI fails to load, check the terminal for tracebacks.
