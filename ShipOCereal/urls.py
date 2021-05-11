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
