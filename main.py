# ============================================================
# NOTEPAD WEB APP - main.py
# Built with FastAPI + MongoDB + Jinja2 Templates
# ============================================================
# LEARNING NOTE:
#   This file is the heart of the app.
#   It handles ALL routes (URLs), reads data from MongoDB,
#   and renders HTML pages using Jinja2 templates.
# ============================================================

from fastapi import FastAPI, Request, Form  # pyrefly: ignore 
from fastapi.responses import RedirectResponse  # pyrefly: ignore 
from fastapi.templating import Jinja2Templates  # pyrefly: ignore 
from fastapi.staticfiles import StaticFiles  # pyrefly: ignore 
from starlette.middleware.sessions import SessionMiddleware  # pyrefly: ignore 
from pymongo import MongoClient  # pyrefly: ignore 
from bson import ObjectId  # pyrefly: ignore 
from datetime import datetime  # pyrefly: ignore 
import hashlib  # pyrefly: ignore 
from pymongo.server_api import ServerApi   # pyrefly: ignore 
from dotenv import load_dotenv  # pyrefly: ignore 
import os  # pyrefly: ignore 
import certifi  # pyrefly: ignore 
from openai import OpenAI  # pyrefly: ignore 

load_dotenv() 

# Password hashing functions using bcrypt. ===================

def hash(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()

# ============================================================

clientAI = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)

def AI_text(user_note):

    messages = [

        {
            "role": "system",
            "content": """
You are an incredibly energetic, fun, and highly capable daily task organizer AI! 🚀✨

Your job is to:
- Convert messy daily notes into structured, exciting checklists
- Fix all grammar and spelling mistakes perfectly
- Keep the original meaning but make it sound incredibly motivating!
- Add appropriate and fun emojis naturally! 🎉
- IMPORTANT: You must output ONLY raw HTML (Do NOT use Markdown).
- For the title, use a <div style="font-size: 1.2rem; font-weight: bold; line-height: 30px; margin: 0;"> tag.
- For EACH task, you MUST use this exact HTML structure:
  <div style="display: flex; align-items: flex-start; gap: 8px;"><input type="checkbox" class="task-checkbox" style="width: 18px; height: 18px; cursor: pointer; margin-top: 6px;"><span class="task-text" style="line-height: 30px;">Your exciting task here!</span></div>
- Do NOT wrap the response in ```html markdown blocks. Output pure HTML.
"""
        },

        # Few-shot example 1
        {
            "role": "user",
            "content": "i have to go to gym then study maths and then eat dinner"
        },

        {
            "role": "assistant",
            "content": """
<div style="font-size: 1.2rem; font-weight: bold; line-height: 30px; margin: 0;">📋 My Awesome Tasks for Today! 🌟</div>
<div style="display: flex; align-items: flex-start; gap: 8px;"><input type="checkbox" class="task-checkbox" style="width: 18px; height: 18px; cursor: pointer; margin-top: 6px;"><span class="task-text" style="line-height: 30px;">💪 Crush it at the gym!</span></div>
<div style="display: flex; align-items: flex-start; gap: 8px;"><input type="checkbox" class="task-checkbox" style="width: 18px; height: 18px; cursor: pointer; margin-top: 6px;"><span class="task-text" style="line-height: 30px;">📚 Study Mathematics like a genius</span></div>
<div style="display: flex; align-items: flex-start; gap: 8px;"><input type="checkbox" class="task-checkbox" style="width: 18px; height: 18px; cursor: pointer; margin-top: 6px;"><span class="task-text" style="line-height: 30px;">🍽️ Enjoy a well-deserved dinner</span></div>
"""
        },

        # Few-shot example 2
        {
            "role": "user",
            "content": "complete python project and call rahul after coming home"
        },

        {
            "role": "assistant",
            "content": """
<div style="font-size: 1.2rem; font-weight: bold; line-height: 30px; margin: 0;">📋 Let's Get Things Done! 🚀</div>
<div style="display: flex; align-items: flex-start; gap: 8px;"><input type="checkbox" class="task-checkbox" style="width: 18px; height: 18px; cursor: pointer; margin-top: 6px;"><span class="task-text" style="line-height: 30px;">💻 Complete the amazing Python project</span></div>
<div style="display: flex; align-items: flex-start; gap: 8px;"><input type="checkbox" class="task-checkbox" style="width: 18px; height: 18px; cursor: pointer; margin-top: 6px;"><span class="task-text" style="line-height: 30px;">📞 Catch up with Rahul after coming home</span></div>
"""
        },

        # Actual user input
        {
            "role": "user",
            "content": user_note
        }

    ]

    response = clientAI.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.5
    )

    return response.choices[0].message.content 


# ============================================================
# APP INITIALIZATION
# ============================================================
# FastAPI() creates the main application object.
# Every route (URL) will be registered to this object.
app = FastAPI()


# ============================================================
# SESSION MIDDLEWARE
# ============================================================
# Sessions allow us to remember who is logged in.
# When a user logs in, we store their username in the session.
# The session is stored in a cookie on the user's browser.
# "secret_key" is used to sign/encrypt the cookie so it can't be tampered with.
#
# IMPORTANT: Use a long, random secret key in real apps!
app.add_middleware(SessionMiddleware, secret_key="super-secret-notepad-key-change-in-production")


# ============================================================
# STATIC FILES
# ============================================================
# This tells FastAPI: "For any URL starting with /static,
# look for the file in the ./static folder."
# So style.css will be at: http://localhost:8000/static/style.css
app.mount("/static", StaticFiles(directory="static"), name="static")


# ============================================================
# JINJA2 TEMPLATES
# ============================================================
# Jinja2Templates tells FastAPI where our HTML files live.
# We can then call templates.TemplateResponse("login.html", {...})
# to render and return an HTML page.
templates = Jinja2Templates(directory="templates")


# ============================================================
# MONGODB CONNECTION
# ============================================================
# MongoClient connects to a running MongoDB server.
# By default, MongoDB runs on localhost (your computer) at port 27017.
#
# HOW TO START MONGODB:
#   - Windows: Run "mongod" in your terminal
#   - Mac:     Run "brew services start mongodb-community"
#   - Linux:   Run "sudo systemctl start mongod"

uri = os.getenv("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(uri, tlsCAFile=certifi.where())
  

# Select (or create) the database named "notepad_db"
# MongoDB creates it automatically when you first insert data
db = client["notepad_db"]

# Collections are like tables in SQL.
# "users" stores user accounts.
# "notes" stores notes.
users_collection = db["users"]
notes_collection = db["notes"]


# ============================================================
# HELPER FUNCTION: Get the currently logged-in user
# ============================================================
# Sessions in Starlette/FastAPI work like a dictionary.
# When the user logs in, we do: request.session["username"] = "john"
# Later, we can read it with: request.session.get("username")
# If nobody is logged in, it returns None.

def get_current_user(request: Request):
    # request.session is the session dictionary for this user
    # .get("username") returns the value, or None if not found
    return request.session.get("username")


# ============================================================
# ROUTE: Home page (redirect to dashboard or login)
# ============================================================
# @app.get("/") means: when the user visits the root URL "/"
# run the function below and return its result.
#
# RedirectResponse sends the user to a different URL.
# status_code=302 is the standard "temporary redirect" code.

@app.get("/")
def home(request: Request):
    user = get_current_user(request)
    if user:
        # User is logged in → send them to the dashboard
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        # Not logged in → send them to login page
        return RedirectResponse(url="/login", status_code=302)


# ============================================================
# ROUTE: Register (GET) - Show the registration form
# ============================================================
# GET requests are used to "get" a page (just viewing it).
# We return the register.html template.
# "request" is always passed because Jinja2 needs it.
# "error=None" means no error to display yet.

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "register.html", 
        context = {
            "request": request,
            "error": None
        }
    )


# ============================================================
# ROUTE: Register (POST) - Handle the submitted form
# ============================================================
# POST requests carry form data (username, password, etc.)
# FastAPI reads form fields using: Form(...)
# The "..." means the field is required.

@app.post("/register")
def register(
    request: Request,
    username: str = Form(...),        # reads "username" field from the form
    password: str = Form(...),        # reads "password" field from the form
    confirm_password: str = Form(...) # reads "confirm_password" from the form
):
    # --- Validate: passwords must match ---
    if password != confirm_password:
        return templates.TemplateResponse(
            request = request,
            name = "register.html",
            context = {
                "request": request,
                "error": "Passwords do not match!"
            }
        )

    # --- Validate: username must not already exist ---
    # find_one() searches MongoDB for a document matching the filter.
    # {"username": username} means: find a user where username equals the given value.
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        return templates.TemplateResponse(
            request = request,
            name = "register.html",
            context = {
                "request": request,
                "error": "Username already taken. Try a different one."
            }
        )

    # --- Save the new user to MongoDB ---
    # IMPORTANT SECURITY NOTE:
    #   We are storing the password as plain text here.
    #   This is ONLY for learning purposes.
    #   In a real production app, you should NEVER store plain passwords.
    #   Instead, use a library like "passlib" or "bcrypt" to hash the password:
    #   Example: hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    #   Then store hashed_password instead of password.
    #
    # MongoDB insert_one() adds a new document (like a row in SQL) to the collection.
    users_collection.insert_one({
        "username": username,
        "password": str(hash(password)),       # ⚠ PLAIN TEXT - only for learning!
        "created_at": datetime.now()
    })

    # After successful registration, redirect to login page
    return RedirectResponse(url="/login", status_code=302)


# ============================================================
# ROUTE: Login (GET) - Show the login form
# ============================================================

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "login.html",
        context = {
            "request": request,
            "error": None
        }
    )


# ============================================================
# ROUTE: Login (POST) - Handle login form submission
# ============================================================

@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    # --- Find the user in MongoDB ---
    # We search for a user where BOTH username AND password match.
    # SECURITY NOTE:
    #   In production, you'd fetch user by username only, then
    #   compare the hashed password using bcrypt.checkpw().
    user = users_collection.find_one({
        "username": username,
        "password": str(hash(password))  # ⚠ PLAIN TEXT check - only for learning!
    })

    if not user:
        # Wrong username or password
        return templates.TemplateResponse(
            request = request,
            name = "login.html",
            context = {
                "request": request,
                "error": "Invalid username or password."
            }
        )

    # --- Store the username in the session ---
    # This is how we "remember" that this user is logged in.
    # The session data is stored in an encrypted cookie on the browser.
    # Every future request from this browser will include this session.
    request.session["username"] = username

    # Redirect to dashboard after successful login
    return RedirectResponse(url="/dashboard", status_code=302)


# ============================================================
# ROUTE: Dashboard - Show all notes for the logged-in user
# ============================================================

@app.get("/dashboard")
def dashboard(request: Request):
    # Check if user is logged in
    user = get_current_user(request)
    if not user:
        # Not logged in → kick them to login page
        return RedirectResponse(url="/login", status_code=302)

    # --- Fetch all notes belonging to this user ---
    # find() returns ALL documents matching the filter.
    # {"owner": user} means: get all notes where owner equals the logged-in username.
    # We convert to a list so we can loop over it in the template.
    notes = list(notes_collection.find({"owner": user}))

    # MongoDB stores IDs as ObjectId objects (e.g., ObjectId("abc123..."))
    # HTML/Jinja2 templates can't use ObjectId directly — they need plain strings.
    # So we convert each note's _id to a string.
    for note in notes:
        note["_id"] = str(note["_id"])

    return templates.TemplateResponse(
        request = request,
        name = "dashboard.html",
        context = {
            "request": request,
            "username": user,
            "notes": notes     # Pass the list of notes to the template
        }
    )


# ============================================================
# ROUTE: New Note (GET) - Show the empty note editor
# ============================================================

@app.get("/note/new")
def new_note_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    # Render the editor with empty fields (no note yet)
    return templates.TemplateResponse(
        request = request,
        name = "editor.html",
        context = {
            "request": request,
            "note": None,       # No existing note — this is a new one
            "username": user
        }
    )


# ============================================================
# ROUTE: Create Note (POST) - Save a new note to MongoDB
# ============================================================
# LEARNING NOTE (HTTP Methods):
#   We use @app.post here instead of @app.get. 
#   GET requests are just for "reading" or "viewing" data.
#   POST requests are used to safely send data (like a form) 
#   to CREATE or UPDATE something on the server.
#
#   The form data is automatically extracted using FastAPI's Form(...)

@app.post("/note/new")
def create_note(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    color: str = Form("#FFFDF9")
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    # --- Insert the new note into MongoDB ---
    # LEARNING NOTE (MongoDB):
    #   insert_one() takes a Python dictionary and stores it as a 
    #   JSON-like document in the database.
    #   Each note stores:
    #     owner    → which user it belongs to (links note to user)
    #     title    → the note title
    #     content  → the note body (HTML string)
    #     color    → background color of the note
    #     created  → when it was created (formatted nicely for display)
    notes_collection.insert_one({
        "owner": user,
        "title": title,
        "content": content,
        "color": color,
        "created": datetime.now().strftime("%d %b %Y, %I:%M %p")
        # Example output: "24 Jul 2025, 03:45 PM"
    })

    return RedirectResponse(url="/dashboard", status_code=302) 


# ============================================================
# ROUTE: Edit Note (GET) - Show editor with existing note data
# ============================================================
# {note_id} in the URL is a "path parameter".
# If the URL is /note/edit/abc123, then note_id = "abc123"
# FastAPI automatically extracts it for us.

@app.get("/note/edit/{note_id}")
def edit_note_page(request: Request, note_id: str):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    # --- Fetch the specific note from MongoDB ---
    # ObjectId() converts the string ID back to MongoDB's ObjectId format.
    # MongoDB stores _id as ObjectId, not as a plain string.
    note = notes_collection.find_one({"_id": ObjectId(note_id)})

    if not note:
        # Note doesn't exist → go back to dashboard
        return RedirectResponse(url="/dashboard", status_code=302)

    # Security check: make sure this note belongs to the logged-in user.
    # We don't want User A to edit User B's notes!
    if note["owner"] != user:
        return RedirectResponse(url="/dashboard", status_code=302)

    # Convert ObjectId to string for the template
    note["_id"] = str(note["_id"])

    return templates.TemplateResponse(
        request = request,
        name = "editor.html",
        context = {
            "request": request,
            "note": note,       # Pass the existing note data to pre-fill the form
            "username": user
        }
    )


# ============================================================
# ROUTE: Update Note (POST) - Save edits to an existing note
# ============================================================

@app.post("/note/edit/{note_id}")
def update_note(
    request: Request,
    note_id: str,
    title: str = Form(...),
    content: str = Form(...),
    color: str = Form("#FFFDF9")
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    # --- Update the note in MongoDB ---
    # LEARNING NOTE (MongoDB Updates):
    #   update_one() finds ONE document matching the filter and updates it.
    #   First argument: the filter (which document to update)
    #     {"_id": ObjectId(note_id), "owner": user}
    #   Second argument: the update operation
    #     "$set" is a special MongoDB operator that means: 
    #     "set these specific fields, but leave the rest of the document untouched!"
    notes_collection.update_one(
        {"_id": ObjectId(note_id), "owner": user},  # filter
        {"$set": {                                   # update
            "title": title,
            "content": content,
            "color": color
        }}
    )

    return RedirectResponse(url="/dashboard", status_code=302)


# AI Text feature ============================================

@app.post("/note/ai_text")
def ai_text(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    note_id: str = Form(None),
    color: str = Form("#FFFDF9")
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    ai_response = AI_text(content)

    note_data = {"title": title, "color": color}
    if note_id:
        note_data["_id"] = note_id

    return templates.TemplateResponse(
        request = request,
        name = "editor.html",
        context = {
            "request": request,
            "username": user,
            "note": note_data,
            "ai_response": ai_response
        }
    )



# ============================================================
# ROUTE: Delete Note (POST)
# ============================================================
# We use POST (not GET) for delete because:
# - GET requests can be triggered by just visiting a URL (unsafe for deletion)
# - POST requires a form submission (more intentional)

@app.post("/note/delete/{note_id}")
def delete_note(request: Request, note_id: str):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    # --- Delete the note from MongoDB ---
    # LEARNING NOTE (MongoDB Deletion):
    #   delete_one() permanently removes the first document matching the filter.
    #   We include "owner": user as a crucial security check!
    #   If an attacker tries to guess someone else's note_id, the deletion 
    #   will fail because the "owner" won't match their username.
    notes_collection.delete_one({
        "_id": ObjectId(note_id),
        "owner": user   # Security: can't delete someone else's note
    })

    return RedirectResponse(url="/dashboard", status_code=302)


# ============================================================
# ROUTE: Logout
# ============================================================

@app.get("/logout")
def logout(request: Request):
    # Clear the session — this removes the stored username.
    # The user's browser cookie becomes empty/invalid.
    # They will be treated as "not logged in" on the next request.
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)


# ============================================================
# RUN THE APP (only when running this file directly)
# ============================================================
# This block runs only if you do: python main.py
# (Not when imported as a module)
# Uvicorn is the ASGI server that runs FastAPI apps.
# host="0.0.0.0" means accessible from any network interface.
# port=8000 is the default FastAPI port.
# reload=True means the server restarts when you save changes (great for development!)

if __name__ == "__main__":
    # pyrefly: ignore [missing-import]
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# This is the end of the main.py file. The app is now complete and ready to run!





# some code




























































































