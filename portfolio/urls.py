from django.urls import path 
from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    
    # Dashboard URL
    path("dashboard/", views.dashboard, name="dashboard"),
    
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    
    # Portfolio management URLs
    path("templates/", views.template_selection, name="templates"),
    path("templates/<int:template_id>/preview/", views.preview_template, name="preview_template"),
    path("create/", views.create_portfolio, name="create_portfolio"),
    path("<int:portfolio_id>/edit/", views.edit_portfolio, name="edit_portfolio"),
    path("<slug:portfolio_slug>/", views.view_portfolio, name="view_portfolio"),
    path("<int:portfolio_id>/delete/", views.delete_portfolio, name="delete_portfolio"),
    path("<int:portfolio_id>/projects/add/", views.add_project, name="add_project"),
    path("project/<int:project_id>/edit/", views.edit_project, name="edit_project"),
    path("project/<int:project_id>/delete/", views.delete_project, name="delete_project"),
    
   
]