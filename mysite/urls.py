from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Only include portfolio URLs at the root to avoid confusion
    path('', include('portfolio.urls')),
    # Add a redirect to handle any legacy '/portfolio/' requests
    path('portfolio/', RedirectView.as_view(url='/', permanent=True)),
]

# Add the media URL configuration
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
