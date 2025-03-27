from django.contrib import admin
from django.urls import include , path

urlpatterns = [
    path("portfolio/", include("portfolio.urls")),
    path('admin/', admin.site.urls),
]
