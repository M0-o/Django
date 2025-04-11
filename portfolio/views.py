from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Portfolio, Template, Project
from .forms import PortfolioForm, ProjectForm, UserProfileForm

def index(request):
    return render(request, "portfolio/home.html") 

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return render(request, "login.html", {"error_message": "Invalid credentials"})
        auth_login(request, user)
        return redirect("dashboard")
    else:
        return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname  = request.POST.get("lastname")
        username  = request.POST.get("username")
        email     = request.POST.get("email")
        password  = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error_message": "Username already exists"})
        
        user = User.objects.create_user(username=username, password=password, email=email,
                                        first_name=firstname, last_name=lastname)
        auth_login(request, user)
        return redirect("dashboard")
    else:
        return render(request, "signup.html")
    
def logout(request):
    auth_logout(request)
    return redirect("index")

@login_required
def dashboard(request):
    """Dashboard view to display user's portfolios"""
    portfolios = Portfolio.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'portfolio/dashboard.html', {'portfolios': portfolios})

@login_required
def template_selection(request):
    templates = Template.objects.filter(is_active=True)
    print(templates)
    return render(request, 'portfolio/template_selection.html', {'templates': templates})

@login_required
def preview_template(request, template_id):
    """Preview a template before selecting it"""
    template = get_object_or_404(Template, id=template_id)
    
    # Create a sample portfolio with dummy data for preview
    sample_portfolio = {
        'title': 'John Doe',
        'about_me': 'I am a software developer with experience in web development, mobile applications, and machine learning. I am passionate about creating efficient and user-friendly applications.',
        'contact_email': 'john.doe@example.com',
        'linkedin_url': 'https://linkedin.com/in/johndoe',
        'github_url': 'https://github.com/johndoe',
    }
    
    # Create sample projects for the preview
    class SampleProject:
        def __init__(self, title, description, project_url, github_url, technologies, completion_date):
            self.title = title
            self.description = description
            self.project_url = project_url
            self.github_url = github_url
            self.technologies = technologies
            self.completion_date = completion_date
            
        @property
        def technologies_list(self):
            return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
    
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
    class SamplePortfolio:
        def __init__(self, title, about_me, contact_email, linkedin_url, github_url):
            self.id = 1
            self.title = title
            self.about_me = about_me
            self.contact_email = contact_email
            self.linkedin_url = linkedin_url
            self.github_url = github_url
            self.slug = 'sample-portfolio'
            self.user = request.user
            
    portfolio_obj = SamplePortfolio(
        title=sample_portfolio['title'],
        about_me=sample_portfolio['about_me'],
        contact_email=sample_portfolio['contact_email'],
        linkedin_url=sample_portfolio['linkedin_url'],
        github_url=sample_portfolio['github_url']
    )
    
    # Map template names to template files
    template_map = {
        'Dark Mode': 'portfolio/templates/dark_mode.html',
        'Gradient': 'portfolio/templates/gradient.html',
        'Minimalist': 'portfolio/templates/minimalist.html',
        
    }
    
    # Default to the generic preview template if the specific template is not found
    template_file = template_map.get(template.name, 'portfolio/template_preview.html')
    
    return render(request, template_file, {
        'template': template,
        'portfolio': portfolio_obj,
        'projects': sample_projects
    })

@login_required
def create_portfolio(request):
    template_id = request.GET.get('template')
    selected_template = get_object_or_404(Template, id=template_id) if template_id else None
    
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            if not portfolio.template and selected_template:
                portfolio.template = selected_template
            portfolio.save()
            messages.success(request, "Portfolio created successfully!")
            return redirect('edit_portfolio', portfolio_id=portfolio.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        initial_data = {}
        if selected_template:
            initial_data['template'] = selected_template
        form = PortfolioForm(initial=initial_data)
    
    context = {
        'form': form,
        'selected_template': selected_template,
    }
    return render(request, 'portfolio/create_portfolio.html', context)

@login_required
def edit_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    projects = portfolio.projects.all().order_by('order')
    
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            form.save()
            messages.success(request, "Portfolio updated successfully!")
            return redirect('edit_portfolio', portfolio_id=portfolio.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PortfolioForm(instance=portfolio)
    
    return render(request, 'portfolio/edit_portfolio.html', {
        'form': form, 
        'portfolio': portfolio, 
        'projects': projects
    })

@login_required
def view_portfolio(request, portfolio_slug):
    portfolio = get_object_or_404(Portfolio, slug=portfolio_slug)
    projects = portfolio.projects.all().order_by('order')
    
    # Map template names to template files
    template_map = {
        'Dark Mode': 'portfolio/templates/dark_mode.html',
        'Gradient': 'portfolio/templates/gradient.html',
        'Minimalist': 'portfolio/templates/minimalist.html',
    }
    
    # Use the selected template or fall back to default
    template_name = template_map.get(portfolio.template.name, 'portfolio/view_portfolio.html')
    
    return render(request, template_name, {
        'portfolio': portfolio,
        'projects': projects
    })

@login_required
def delete_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    
    if request.method == 'POST':
        portfolio.delete()
        messages.success(request, "Portfolio deleted successfully!")
        return redirect('dashboard')
    
    return redirect('edit_portfolio', portfolio_id=portfolio_id)

@login_required
def add_project(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.portfolio = portfolio
            project.save()
            messages.success(request, "Project added successfully!")
            return redirect('edit_portfolio', portfolio_id=portfolio.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProjectForm()
    
    context = {
        'form': form, 
        'portfolio_id': portfolio.id,
        'portfolio_slug': portfolio.slug
    }
    return render(request, 'portfolio/create_project.html', context)

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    portfolio = project.portfolio
    
    # Ensure the user owns this project
    if portfolio.user != request.user:
        messages.error(request, "You don't have permission to edit this project.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect('edit_portfolio', portfolio_id=portfolio.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProjectForm(instance=project)
    
    context = {
        'form': form,
        'project': project
    }
    return render(request, 'portfolio/edit_project.html', context)

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    portfolio = project.portfolio
    
    # Ensure the user owns this project
    if portfolio.user != request.user:
        messages.error(request, "You don't have permission to delete this project.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully!")
    
    return redirect('edit_portfolio', portfolio_id=portfolio.id)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'edit_profile.html', {'form': form})

