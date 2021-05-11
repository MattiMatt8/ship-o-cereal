"""ShipOCereal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
git puExamples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from products.views import ProductSearchView
from . import views, settings
from django.conf.urls.static import static

handler400 = "ShipOCereal.views.bad_request"
handler403 = "ShipOCereal.views.permission_denied"
handler404 = "ShipOCereal.views.page_not_found"
handler500 = "ShipOCereal.views.server_error"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="index"),
    path("", include("users.urls"), name="users"),
    path("", include("orders.urls"), name="orders"),
    path("products/", include("products.urls"), name="products"),
    path("admin/", admin.site.urls),
    path("search/<str:search_str>/", ProductSearchView.as_view(), name="search"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
