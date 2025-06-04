# """
# URL configuration for mexTex project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.conf import settings
# from django.conf.urls.static import static
# from django.urls import path, include
# from django.conf.urls.i18n import i18n_patterns
# from django.views.i18n import set_language
# from blog.views import HomePagesViews  # Asosiy sahifa uchun view

# urlpatterns = [
#     path("i18n/setlang/", set_language, name="set_language"),  # Tilni o‘zgartirish uchun URL
# ]

# urlpatterns += i18n_patterns(
#     path("", HomePagesViews.as_view(), name="home"),  # Asosiy sahifa (ichida bo‘lishi kerak)
#     path("admin/", admin.site.urls),
#     path('accounts/',include('accounts.urls')),
#     path('accounts/',include('django.contrib.auth.urls')),
#     path("blog/", include("blog.urls")),
#     path("mextexbaza/", include("mextexbaza.urls")),
#     path("boglanish/", include("boglanish.urls")),
# )

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from blog.views import HomePagesViews  # Asosiy sahifa uchun view
from django.shortcuts import redirect  # 🔁 redirect qilish uchun kerak

urlpatterns = [
    # Root URL: / => /uz/ ga yo‘naltirish
    path('', lambda request: redirect('/uz/')),

    # Tilni o‘zgartirish uchun URL
    path("i18n/setlang/", set_language, name="set_language"),
]

urlpatterns += i18n_patterns(
    path("", HomePagesViews.as_view(), name="home"),  # Asosiy sahifa
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("blog/", include("blog.urls")),
    path("mextexbaza/", include("mextexbaza.urls")),
    path("boglanish/", include("boglanish.urls")),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
