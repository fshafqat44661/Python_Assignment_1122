from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Your API Documentation')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),
    path('api/', include('user.urls')),
    path('docs/', schema_view),
]
