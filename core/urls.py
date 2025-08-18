from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("apps.blog.urls")),
    path("admin/", admin.site.urls),
    path("account/", include("apps.users.urls")),
]
