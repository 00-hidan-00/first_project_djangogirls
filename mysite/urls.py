from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounts/login/', views.LoginView.as_view(), name='login'),
                  path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
                  path('', include('blog.urls')),
                  path('cms/', include(wagtailadmin_urls)),
                  path('pages/', include(wagtail_urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
