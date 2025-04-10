from django.urls import path 
from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    
    # Dashboard URL
    path("dashboard/", views.dashboard, name="dashboard"),
    
    # Portfolio management URLs
    path("templates/", views.template_selection, name="templates"),
    path("templates/<int:template_id>/preview/", views.preview_template, name="preview_template"),
    path("portfolio/create/", views.create_portfolio, name="create_portfolio"),
    path("portfolio/<int:portfolio_id>/edit/", views.edit_portfolio, name="edit_portfolio"),
    path("portfolio/<slug:portfolio_slug>/", views.view_portfolio, name="view_portfolio"),
    path("portfolio/<int:portfolio_id>/delete/", views.delete_portfolio, name="delete_portfolio"),
    path("portfolio/<int:portfolio_id>/projects/add/", views.add_project, name="add_project"),
    path("portfolio/project/<int:project_id>/edit/", views.edit_project, name="edit_project"),
    path("portfolio/project/<int:project_id>/delete/", views.delete_project, name="delete_project"),
    
    # User profile
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    
    # Additional pages
    path("features/", views.features, name="features"),
    path("pricing/", views.pricing, name="pricing"),
    path("about/", views.about, name="about"),
    path("blog/", views.blog, name="blog"),
    path("tutorials/", views.tutorials, name="tutorials"),
    path("examples/", views.examples, name="examples"),
    path("faq/", views.faq, name="faq"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("cookies/", views.cookies, name="cookies"),
    path("contact/", views.contact, name="contact"),
]