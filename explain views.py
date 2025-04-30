"""
This file contains all the view functions for the Portfolio Builder application.
Views are Python functions that handle web requests and return web responses.
They contain the business logic of the application and connect the database (models) with the UI (templates).

Here's a breakdown of how Django views work:
1. A request comes in from a user's browser
2. Django's URL router determines which view function should handle it
3. The view function processes the request
4. The view returns a response (usually by rendering a template with data)
"""

# Import necessary modules and functions from Django
from django.shortcuts import render, redirect, get_object_or_404  # Functions for rendering templates and redirecting users
from django.http import HttpResponse  # Class for returning HTTP responses
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout  # Authentication functions
from django.contrib.auth.models import User  # Django's built-in User model
from django.contrib.auth.decorators import login_required  # Decorator to restrict views to logged-in users
from django.template.loader import render_to_string, get_template  # Functions for working with templates
from django.conf import settings  # Access to Django settings
from django.contrib import messages  # System for displaying one-time notification messages
import os  # Python's built-in module for interacting with the operating system
from .models import Portfolio, Template, Project  # Our custom database models
from .forms import PortfolioForm, ProjectForm, UserProfileForm  # Our custom forms
from django.template import TemplateDoesNotExist  # Exception raised when a template can't be found

def index(request):
    """
    Home page view - shows the landing page to visitors.
    
    The 'request' parameter contains information about the HTTP request
    that triggered this view, like user session, GET/POST data, etc.
    """
    # render() takes a request, a template path, and optional context data
    # and returns an HttpResponse with the rendered template
    return render(request, "portfolio/home.html") 

def login(request):
    """
    User login view - handles authentication of existing users.
    
    This function:
    1. Checks if the user is already logged in
    2. If not, shows a login form (on GET request)
    3. Processes the form submission (on POST request)
    4. Authenticates the user and creates a session
    5. Redirects to the dashboard or requested page
    """
    # If user is already logged in, redirect to dashboard
    # request.user is the current user (either authenticated or AnonymousUser)
    if request.user.is_authenticated:
        return redirect("dashboard")  # redirect() takes a URL name or path and returns an HttpResponseRedirect
    
    # Get next parameter from URL if it exists
    # This is used to redirect users back to the page they were trying to access
    # request.GET is a dictionary-like object containing all GET parameters
    next_url = request.GET.get('next', '')  # get() returns '' if 'next' parameter doesn't exist
    
    # Security check: make sure 'next' URL isn't malicious
    if next_url and (next_url.startswith('//') or ':' in next_url or '%' in next_url):
        next_url = ''  # Reset to empty if it looks suspicious
        
    # Check if this is a form submission
    # request.method tells us if this is a GET, POST, etc. request
    if request.method == "POST":
        # Extract form data
        # request.POST is a dictionary-like object containing all POST parameters
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Try to authenticate the user with the provided credentials
        # If successful, authenticate() returns a User object; if not, it returns None
        user = authenticate(username=username, password=password)
        
        # If authentication failed, show an error message
        if not user:
            # Render the login template again with an error message
            return render(request, "portfolio/login.html", {"error_message": "Invalid credentials", "next": next_url})
        
        # If authentication succeeded, log the user in
        # This creates a session for the user that persists across requests
        auth_login(request, user)
        
        # Get next URL from form submission (it might be different from URL parameter)
        next_url = request.POST.get('next', '')
        
        # Security check on 'next' URL
        if next_url and not (next_url.startswith('//') or ':' in next_url or '%' in next_url):
            # Only redirect to internal paths (starting with /)
            if next_url.startswith('/'):
                return redirect(next_url)
            else:
                try:
                    # Try to resolve the URL by name
                    return redirect(next_url)
                except:
                    # If URL resolution fails, go to dashboard
                    return redirect("dashboard")
        
        # Default redirect if no valid 'next' URL was provided
        return redirect("dashboard")
    else:
        # For GET requests, just show the login form
        return render(request, "portfolio/login.html", {"next": next_url})

def signup(request):
    """
    User registration view - handles creation of new user accounts.
    
    This function:
    1. Checks if the user is already logged in
    2. If not, shows a registration form (on GET request)
    3. Processes the form submission (on POST request)
    4. Validates user input and creates a new user account
    5. Logs the user in and redirects to the dashboard
    """
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    # Get and validate 'next' parameter (same as in login view)
    next_url = request.GET.get('next', '')
    if next_url and (next_url.startswith('//') or ':' in next_url or '%' in next_url):
        next_url = ''
        
    # Handle form submission
    if request.method == "POST":
        # Extract form data
        firstname = request.POST.get("firstname")
        lastname  = request.POST.get("lastname")
        username  = request.POST.get("username")
        email     = request.POST.get("email")
        password  = request.POST.get("password")
        
        # Basic validation: check if all required fields are filled
        # all() returns True only if all elements in the list are True/truthy
        # An empty string is considered False in Python
        if not all([firstname, lastname, username, email, password]):
            return render(request, "portfolio/signup.html", {
                "error_message": "All fields are required", 
                "next": next_url
            })
            
        # Check if username already exists in database
        # User.objects gives us access to the User model's database manager
        # filter() returns a QuerySet of matching records
        # exists() returns True if the QuerySet contains any records
        if User.objects.filter(username=username).exists():
            return render(request, "portfolio/signup.html", {
                "error_message": "Username already exists",
                "next": next_url
            })
        
        # Create the user
        # create_user() is a helper method that properly hashes the password
        user = User.objects.create_user(
            username=username, 
            password=password, 
            email=email,
            first_name=firstname, 
            last_name=lastname
        )
        
        # Log the user in automatically
        auth_login(request, user)
        
        # Handle 'next' URL redirection (same as in login view)
        next_url = request.POST.get('next', '')
        
        if next_url and not (next_url.startswith('//') or ':' in next_url or '%' in next_url):
            if next_url.startswith('/'):
                return redirect(next_url)
            else:
                try:
                    return redirect(next_url)
                except:
                    return redirect("dashboard")
        
        # Default redirect
        return redirect("dashboard")
    else:
        # For GET requests, just show the signup form
        return render(request, "portfolio/signup.html", {"next": next_url})
    
def logout(request):
    """
    User logout view - handles ending user sessions.
    
    This function:
    1. Logs the user out by clearing their session
    2. Redirects to the home page
    """
    # auth_logout() clears the user's session data
    auth_logout(request)
    # Redirect to the home page
    return redirect("index")

@login_required  # This decorator prevents non-logged-in users from accessing this view
def dashboard(request):
    """
    Dashboard view - shows the user's portfolios and options.
    
    This is the main landing page after login, showing all portfolios
    the user has created. The @login_required decorator makes sure
    only authenticated users can access this view.
    """
    # Get all portfolios belonging to the current user
    # filter() returns a QuerySet matching the given criteria
    # order_by() sorts the results - the '-' means descending order (newest first)
    portfolios = Portfolio.objects.filter(user=request.user).order_by('-created_at')
    
    # Render the dashboard template with the portfolios as context data
    # The dictionary {'portfolios': portfolios} is the "context" -
    # it contains variables that will be available in the template
    return render(request, 'portfolio/dashboard.html', {'portfolios': portfolios})

@login_required
def template_selection(request):
    """
    Template selection view - shows available portfolio templates.
    
    This view displays all active templates that users can choose for their portfolios.
    """
    # Get all active templates from the database
    templates = Template.objects.filter(is_active=True)
    
    # Render the template selection page
    return render(request, 'portfolio/template_selection.html', {'templates': templates})

@login_required
def preview_template(request, template_id):
    """
    Template preview view - shows how a template looks with sample data.
    
    This view:
    1. Gets the requested template
    2. Creates sample data (portfolio and projects)
    3. Renders the template with this sample data
    
    The template_id parameter comes from the URL and is passed by the URL router.
    """
    # Get the requested template or return 404 if not found
    # get_object_or_404 is a shortcut function that raises Http404 if the object doesn't exist
    template = get_object_or_404(Template, id=template_id)
    
    # Create a sample portfolio with dummy data for preview
    # This is just a dictionary with example values
    sample_portfolio = {
        'title': 'John Doe',
        'about_me': 'I am a software developer with experience in web development, mobile applications, and machine learning. I am passionate about creating efficient and user-friendly applications.',
        'contact_email': 'john.doe@example.com',
        'linkedin_url': 'https://linkedin.com/in/johndoe',
        'github_url': 'https://github.com/johndoe',
    }
    
    # Create sample projects for the preview
    # First, define a custom class to mimic Project objects
    class SampleProject:
        """
        A class that mimics the Project model for template preview.
        This lets us create sample projects without saving to the database.
        """
        def __init__(self, title, description, project_url, github_url, technologies, completion_date):
            # Store all the project attributes
            self.title = title
            self.description = description
            self.project_url = project_url
            self.github_url = github_url
            self.technologies = technologies
            self.completion_date = completion_date
            
        # Property decorator makes this method accessible as if it were an attribute
        # This mimics the real Project model's behavior
        @property
        def technologies_list(self):
            # Split the comma-separated technologies string into a list
            # The list comprehension:
            # 1. Split the string by commas
            # 2. For each item, strip whitespace
            # 3. Only include non-empty items
            return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
    
    # Create a list of sample project objects
    sample_projects = [
        SampleProject(
            title='E-commerce Website',
            description='A full-featured e-commerce platform with product catalog, shopping cart, and payment processing.',
            project_url='https://example.com/ecommerce',
            github_url='https://github.com/johndoe/ecommerce',
            technologies='Python, Django, JavaScript, React, PostgreSQL',
            completion_date='2023-05-15',
        ),
        SampleProject(
            title='Task Management App',
            description='A mobile application for managing tasks, deadlines, and team collaboration.',
            project_url='https://example.com/taskapp',
            github_url='https://github.com/johndoe/taskapp',
            technologies='React Native, Firebase, Redux',
            completion_date='2023-02-20',
        ),
        SampleProject(
            title='Machine Learning Project',
            description='An image classification system using deep learning techniques.',
            project_url='https://example.com/imgclassify',
            github_url='https://github.com/johndoe/imgclassify',
            technologies='Python, TensorFlow, Keras, NumPy',
            completion_date='2022-11-10',
        )
    ]
    
    # Create a Portfolio-like object for the template
    # This is another custom class to mimic the Portfolio model
    class SamplePortfolio:
        """
        A class that mimics the Portfolio model for template preview.
        This lets us create a sample portfolio without saving to the database.
        """
        def __init__(self, title, about_me, contact_email, linkedin_url, github_url):
            # Set up all the necessary portfolio attributes
            self.id = 1
            self.title = title
            self.about_me = about_me
            self.contact_email = contact_email
            self.linkedin_url = linkedin_url
            self.github_url = github_url
            self.slug = 'sample-portfolio'
            self.user = request.user
            
    # Create an instance of the SamplePortfolio class with our sample data        
    portfolio_obj = SamplePortfolio(
        title=sample_portfolio['title'],
        about_me=sample_portfolio['about_me'],
        contact_email=sample_portfolio['contact_email'],
        linkedin_url=sample_portfolio['linkedin_url'],
        github_url=sample_portfolio['github_url']
    )
    
    # Map template names to their corresponding template files
    # This dictionary links the template name (e.g., "Dark Mode") to its file path
    template_map = {
        'Dark Mode': 'portfolio/templates/dark_mode.html',
        'Gradient': 'portfolio/templates/gradient.html',
        'Minimalist': 'portfolio/templates/minimalist.html',
        'Modern': 'portfolio/templates/modern/modern.html',  # Note the subdirectory for this one
    }
    
    # Get the appropriate template file or fall back to default
    if template.name in template_map:
        template_file = template_map[template.name]
    else:
        template_file = 'portfolio/template_preview.html'
    
    # Check if the template file actually exists
    try:
        # Try to load the template
        get_template(template_file)
    except TemplateDoesNotExist:
        # If template doesn't exist, use default and show warning
        template_file = 'portfolio/template_preview.html'
        # Add a message that will be displayed to the user
        # This uses Django's messages framework to show a one-time notification
        messages.warning(request, "The selected template could not be found. Using default template instead.")
    
    # Render the template with our sample data
    # The third argument is the context dictionary containing data for the template
    return render(request, template_file, {
        'template': template,
        'portfolio': portfolio_obj,
        'projects': sample_projects
    })

@login_required
def create_portfolio(request):
    """
    Portfolio creation view - handles creating new portfolios.
    
    This view:
    1. Gets a template ID from URL parameters (if provided)
    2. Shows a portfolio creation form (on GET request)
    3. Processes the form submission (on POST request)
    4. Creates a new portfolio in the database
    """
    # Get template ID from URL parameters if provided
    template_id = request.GET.get('template')
    # Get the template object or 404 if it doesn't exist
    # The ternary operator says: if template_id exists, get the template, otherwise set to None
    selected_template = get_object_or_404(Template, id=template_id) if template_id else None
    
    # Handle form submission
    if request.method == 'POST':
        # Create form instance with submitted data and files
        # request.FILES contains uploaded files (like images)
        form = PortfolioForm(request.POST, request.FILES)
        
        # Check if form data is valid according to the form's validation rules
        if form.is_valid():
            # Create portfolio object but don't save to database yet (commit=False)
            # This lets us modify it before saving
            portfolio = form.save(commit=False)
            # Set the user to current user
            portfolio.user = request.user
            # Set template if not already set in the form
            if not portfolio.template and selected_template:
                portfolio.template = selected_template
            # Save the portfolio to the database
            portfolio.save()
            
            # Show success message and redirect to edit page
            messages.success(request, "Portfolio created successfully!")
            return redirect('edit_portfolio', portfolio_id=portfolio.id)
    else:
        # For GET requests, create an empty form
        # If template was selected, pre-fill that field (initial data)
        initial_data = {'template': selected_template.id} if selected_template else {}
        form = PortfolioForm(initial=initial_data)
    
    # Render the creation form
    return render(request, 'portfolio/create_portfolio.html', {
        'form': form,
        'selected_template': selected_template
    })

@login_required
def edit_portfolio(request, portfolio_id):
    """
    Portfolio editing view - handles updating existing portfolios.
    
    This view:
    1. Gets the portfolio by ID
    2. Ensures the current user owns the portfolio (security)
    3. Shows an edit form with current portfolio data (on GET request)
    4. Processes the form submission (on POST request)
    5. Updates the portfolio in the database
    
    The portfolio_id parameter comes from the URL.
    """
    # Get the portfolio or 404 if not found
    # Also checks that the current user owns this portfolio for security
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    
    # Handle form submission
    if request.method == 'POST':
        # Create form with submitted data, files, and the existing portfolio instance
        # The instance parameter tells the form to update the existing object
        # rather than create a new one
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            # Save changes to database
            form.save()
            # Show success message and redirect to dashboard
            messages.success(request, "Portfolio updated successfully!")
            return redirect('dashboard')
    else:
        # For GET requests, create form with existing portfolio data
        # This pre-fills the form with the current values
        form = PortfolioForm(instance=portfolio)
    
    # Get all projects belonging to this portfolio for display
    projects = Project.objects.filter(portfolio=portfolio).order_by('order')
    
    # Render the edit form with portfolio and projects
    return render(request, 'portfolio/edit_portfolio.html', {
        'form': form,
        'portfolio': portfolio,
        'projects': projects
    })

@login_required
def view_portfolio(request, portfolio_slug):
    """
    Portfolio view - shows the public/preview view of a portfolio.
    
    This view:
    1. Gets the portfolio by its slug (URL-friendly identifier)
    2. Checks if the user has permission to view it
    3. Gets all projects for this portfolio
    4. Renders the portfolio with the selected template
    
    The portfolio_slug parameter comes from the URL.
    """
    # Get the portfolio by slug (URL-friendly identifier)
    portfolio = get_object_or_404(Portfolio, slug=portfolio_slug)
    
    # Check if user is authorized to view (either owner or portfolio is published)
    if not (request.user == portfolio.user or portfolio.published):
        # If not authorized, show warning and redirect
        messages.warning(request, "You don't have permission to view this portfolio.")
        return redirect('dashboard')
    
    # Get all projects for this portfolio, ordered by their display order
    projects = Project.objects.filter(portfolio=portfolio).order_by('order')
    
    # Map template names to their corresponding template files (same as in preview_template)
    template_map = {
        'Dark Mode': 'portfolio/templates/dark_mode.html',
        'Gradient': 'portfolio/templates/gradient.html',
        'Minimalist': 'portfolio/templates/minimalist.html',
        'Modern': 'portfolio/templates/modern/modern.html',
    }
    
    # Get the appropriate template file or fall back to default
    if portfolio.template and portfolio.template.name in template_map:
        template_file = template_map[portfolio.template.name]
    else:
        template_file = 'portfolio/view_portfolio.html'
    
    # Check if the template exists
    try:
        get_template(template_file)
    except TemplateDoesNotExist:
        # If template doesn't exist, use default and show warning
        template_file = 'portfolio/view_portfolio.html'
        messages.warning(request, "Template not found. Using default template.")
    
    # Render the portfolio with the selected template
    return render(request, template_file, {
        'portfolio': portfolio,
        'projects': projects
    })

@login_required
def delete_portfolio(request, portfolio_id):
    """
    Portfolio deletion view - handles removing portfolios.
    
    This view:
    1. Gets the portfolio by ID
    2. Ensures the current user owns it (security)
    3. Deletes the portfolio from the database
    4. Redirects to the dashboard with a success message
    
    Note: When a Portfolio is deleted, all its Projects are also deleted
    automatically because of the CASCADE setting in the foreign key.
    """
    # Get the portfolio or 404 if not found, ensure user owns it
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    
    # Delete the portfolio from database
    # This also deletes all associated projects due to the CASCADE setting
    portfolio.delete()
    
    # Show success message and redirect to dashboard
    messages.success(request, "Portfolio deleted successfully!")
    return redirect('dashboard')

@login_required
def add_project(request, portfolio_id):
    """
    Project creation view - handles adding new projects to a portfolio.
    
    This view:
    1. Gets the portfolio by ID
    2. Ensures the current user owns it (security)
    3. Shows a project creation form (on GET request)
    4. Processes the form submission (on POST request)
    5. Creates a new project in the database
    
    The portfolio_id parameter comes from the URL.
    """
    # Get the portfolio or 404, ensure user owns it
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    
    # Handle form submission
    if request.method == 'POST':
        # Create form with submitted data and files
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # Create project but don't save yet
            project = form.save(commit=False)
            # Set the portfolio relationship
            project.portfolio = portfolio
            # Save to database
            project.save()
            
            # Show success message and redirect to portfolio edit page
            messages.success(request, "Project added successfully!")
            return redirect('edit_portfolio', portfolio_id=portfolio.id)
    else:
        # For GET requests, create an empty form
        form = ProjectForm()
    
    # Render the project creation form
    return render(request, 'portfolio/add_project.html', {
        'form': form,
        'portfolio': portfolio
    })

@login_required
def edit_project(request, project_id):
    """
    Project editing view - handles updating existing projects.
    
    This view:
    1. Gets the project by ID
    2. Ensures the current user owns the portfolio it belongs to (security)
    3. Shows an edit form with current project data (on GET request)
    4. Processes the form submission (on POST request)
    5. Updates the project in the database
    
    The project_id parameter comes from the URL.
    """
    # Get the project or 404 if not found
    project = get_object_or_404(Project, id=project_id)
    
    # Ensure user owns the portfolio this project belongs to
    # This is a security check to prevent unauthorized edits
    if project.portfolio.user != request.user:
        messages.warning(request, "You don't have permission to edit this project.")
        return redirect('dashboard')
    
    # Handle form submission
    if request.method == 'POST':
        # Create form with submitted data, files, and existing project
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            # Save changes to database
            form.save()
            
            # Show success message and redirect to portfolio edit page
            messages.success(request, "Project updated successfully!")
            return redirect('edit_portfolio', portfolio_id=project.portfolio.id)
    else:
        # For GET requests, create form with existing project data
        form = ProjectForm(instance=project)
    
    # Render the project edit form
    return render(request, 'portfolio/edit_project.html', {
        'form': form,
        'project': project,
        'portfolio': project.portfolio
    })

@login_required
def delete_project(request, project_id):
    """
    Project deletion view - handles removing projects.
    
    This view:
    1. Gets the project by ID
    2. Ensures the current user owns the portfolio it belongs to (security)
    3. Deletes the project from the database
    4. Redirects back to the portfolio edit page
    """
    # Get the project or 404 if not found
    project = get_object_or_404(Project, id=project_id)
    
    # Ensure user owns the portfolio this project belongs to
    # Security check to prevent unauthorized deletion
    if project.portfolio.user != request.user:
        messages.warning(request, "You don't have permission to delete this project.")
        return redirect('dashboard')
    
    # Store portfolio ID for redirection after deletion
    portfolio_id = project.portfolio.id
    
    # Delete the project from database
    project.delete()
    
    # Show success message and redirect to portfolio edit page
    messages.success(request, "Project deleted successfully!")
    return redirect('edit_portfolio', portfolio_id=portfolio_id)

@login_required
def edit_profile(request):
    """
    User profile editing view - handles updating user information.
    
    This view:
    1. Gets the current user's information
    2. Shows an edit form with current user data (on GET request)
    3. Processes the form submission (on POST request)
    4. Updates the user in the database
    
    Note: This edits the Django User model, not the Portfolio model.
    """
    # Get the current user
    user = request.user
    
    # Handle form submission
    if request.method == 'POST':
        # Create form with submitted data and existing user
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            # Save changes to database
            form.save()
            
            # Show success message and redirect to dashboard
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
    else:
        # For GET requests, create form with existing user data
        form = UserProfileForm(instance=user)
    
    # Render the profile edit form
    return render(request, 'portfolio/edit_profile.html', {'form': form})

# Remove unused views for pages that don't have templates
# If you need these pages in the future, uncomment and create
# the corresponding templates

"""
def features(request):
    return render(request, 'portfolio/features.html')

def pricing(request):
    return render(request, 'portfolio/pricing.html')

def about(request):
    return render(request, 'portfolio/about.html')

def blog(request):
    return render(request, 'portfolio/blog.html')

def tutorials(request):
    return render(request, 'portfolio/tutorials.html')

def examples(request):
    return render(request, 'portfolio/examples.html')

def faq(request):
    return render(request, 'portfolio/faq.html')

def privacy(request):
    return render(request, 'portfolio/privacy.html')

def terms(request):
    return render(request, 'portfolio/terms.html')

def cookies(request):
    return render(request, 'portfolio/cookies.html')

def contact(request):
    return render(request, 'portfolio/contact.html')
"""