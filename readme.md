# Django Portfolio Builder

A web application that allows users to create and manage their professional portfolios online. Users can showcase their projects, skills, and contact information using different design templates.

## Project Structure

```
.
├── manage.py                  # Django command-line utility
├── db.sqlite3                 # SQLite database
├── mysite/                    # Project configuration
│   ├── settings.py            # Main settings file
│   ├── urls.py                # Project-level URL routing
│   └── wsgi.py                # WSGI deployment configuration
├── portfolio/                 # Main application
│   ├── admin.py               # Admin configuration
│   ├── forms.py               # Form definitions
│   ├── models.py              # Database models
│   ├── urls.py                # App-level URL routing
│   ├── views.py               # View functions
│   ├── management/            # Management commands
│   │   └── commands/
│   │       └── add_templates.py  # Command to add templates
│   ├── static/                # Static files
│   │   └── css/               # CSS files
│   │       └── styles.css     # Main styles
│   └── templates/             # HTML templates
│       ├── base.html          # Base template with layout
│       ├── login.html         # Login page
│       ├── signup.html        # Signup page
│       └── portfolio/         # App templates
│           ├── home.html                # Landing page
│           ├── dashboard.html           # User dashboard
│           ├── template_selection.html  # Template selection
│           ├── edit_profile.html        # Edit user profile
│           ├── edit_portfolio.html      # Edit portfolio details
│           ├── view_portfolio.html      # Default portfolio view
│           ├── create_portfolio.html    # Create new portfolio
│           ├── add_project.html         # Add new project
│           ├── edit_project.html        # Edit project
│           ├── template_preview.html    # Preview template
│           └── templates/               # Portfolio templates
│               ├── dark_mode.html       # Dark mode template
│               ├── gradient.html        # Gradient template
│               ├── minimalist.html      # Minimalist template
│               └── modern/              # Modern template
│                   ├── modern.html      # Modern template
│                   └── style.css        # Modern template styles
├── media/                     # User uploaded media
│   ├── portfolios/            # Portfolio media files
│   └── templates/             # Template images
├── project_explanation.txt    # General project documentation
└── project_code_structure.txt # Technical documentation
```

## Features

- User Authentication (Login/Signup)
- Portfolio Creation and Management
- Project Management
- Multiple Template Designs:
  - Dark Mode: A sleek dark-themed template
  - Gradient: Beautiful gradient color scheme
  - Minimalist: Clean, minimal design
  - Modern: Contemporary professional look

## Core Functions

1. **Template Selection**: Users can choose from multiple portfolio templates
2. **Portfolio Management**: Create, edit, view and delete portfolios
3. **Project Management**: Add and manage projects in each portfolio
4. **User Profile**: Update personal information

## Running the Project

This project requires Python 3. The `python` command on your system might point to Python 2, which won't work with this project. 

### Setup Instructions

1. Clone the repository
2. Navigate to the project directory: `cd /path/to/Django`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate the virtual environment:
   - On macOS/Linux: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Apply migrations: `python3 manage.py migrate`
7. Create template thumbnails: `python3 manage.py add_templates`
8. Run the server: `python3 manage.py runserver`

The site should now be accessible at http://127.0.0.1:8000/

### Important Notes

- Always use `python3` instead of `python` to ensure you're using Python 3
- If you encounter template errors, run `python3 check_templates.py` to diagnose the issue
- After making changes to models, run migrations: 
  ```
  python3 manage.py makemigrations
  python3 manage.py migrate
  ```

## Project Documentation

For detailed documentation about the project structure and implementation:
- See project_code_structure.txt for technical details
- See project_explanation.txt for general explanation



