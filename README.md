# 📓 Interactive Notepad Web App

Welcome to the **Interactive Notepad App**! This project is designed not just as a functional application, but as a **learning resource** for beginners. 

If you are new to web development, this codebase is filled with `LEARNING NOTE:` comments scattered throughout the files. This `README.md` will serve as your high-level textbook to understand how everything pieces together!

---

## 🛠️ Tech Stack Overview

This app is built using a modern, lightweight, and incredibly fast stack:

1. **FastAPI (Python)**: The backend web framework that handles all the logic, routing, and requests.
2. **MongoDB**: A NoSQL database where all our users and notes are permanently saved.
3. **Jinja2**: A templating engine that allows us to inject dynamic Python data directly into our HTML files.
4. **HTML/CSS/JS**: Plain vanilla frontend technologies to keep things simple, fast, and dependency-free.
5. **Groq (Llama 3)**: An AI integration used for the "AI Formatter" feature to intelligently organize task lists.

---

## 📚 Core Concepts to Learn

### 1. HTTP Methods (GET vs POST)
In web development, the way your browser talks to the server is via HTTP requests. The two most common methods you will see in `main.py` are:

- **`GET`**: Used to *request* data from the server. Whenever you type a URL into your browser or click a standard link, you are making a `GET` request. 
  - *Example:* `@app.get("/dashboard")` simply fetches the HTML page and displays your notes.
- **`POST`**: Used to *send* data to the server to create or modify something. Forms (like login, register, or creating a new note) use `POST` because they carry sensitive or large amounts of data in the background.
  - *Example:* `@app.post("/note/new")` securely sends your typed note to the server so it can be saved in the database.

### 2. FastAPI Routing
In `main.py`, you will see functions decorated with `@app.get(...)` or `@app.post(...)`. These are called **Routes**. 
They act as traffic cops. When a user visits `/login`, FastAPI looks for the exact function associated with that route and executes it!

### 3. MongoDB (NoSQL Database)
Unlike traditional SQL databases (which use rigid tables and columns), MongoDB stores data in flexible, JSON-like "documents".
- **Collections**: Think of these like folders. We have a `users` collection and a `notes` collection.
- **Documents**: Think of these like files inside the folder. Each note is a separate document containing its title, content, color, and owner.

**Key MongoDB Commands used in this project:**
- `insert_one({...})`: Creates a brand new document in the database.
- `find({...})`: Searches the database for all documents matching a specific condition (e.g., all notes owned by "John").
- `find_one({...})`: Searches for the *first* document that matches a condition.
- `update_one({...})`: Finds a specific document and updates specific fields using the `$set` operator without destroying the rest of the document.
- `delete_one({...})`: Permanently removes a document.

### 4. Jinja2 Templating
If you look inside the `templates/` folder, you'll see files ending in `.html`. However, they have special Python-like syntax inside them, like `{{ note.title }}` or `{% for note in notes %}`.

This is **Jinja2**. It allows us to pass variables from `main.py` directly into the HTML before sending it to the user's browser. 
- `{{ variable }}` prints the value of the variable.
- `{% logic %}` executes loops, if-statements, and formatting logic.

---

## 📂 Project Structure

- `main.py`: The brain of the application. All backend logic, AI integration, and database queries live here.
- `templates/`: Contains all the HTML files (`login.html`, `dashboard.html`, `editor.html`).
- `static/`: Contains `style.css` which makes the app look beautiful with a custom notebook grid design.

## 🚀 How to Run the App

1. Ensure you have Python installed.
2. Install the required dependencies: `pip install fastapi uvicorn pymongo python-dotenv jinja2 starlette certifi openai`
3. Set up your environment variables by creating a `.env` file in the root directory:
   ```env
   MONGO_URI="your_mongodb_connection_string"
   GROQ_API_KEY="your_groq_api_key"
   ```
4. Run the server using Uvicorn:
   ```bash
   python main.py
   ```
5. Open your browser and visit `http://localhost:8000`

Happy Learning and Coding! 🎉
