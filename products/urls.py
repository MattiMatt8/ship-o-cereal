from django.urls import path
from . import views
#from views import CategoryView

urlpatterns = [
    path("<int:id>", views.product_details, name="product-details"),
    path("<str:category_name>", views.ProductCategory.as_view(), name="product-category"),
]