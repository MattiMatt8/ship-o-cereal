from django.urls import path
from . import views
#from views import CategoryView

urlpatterns = [
    path("<int:id>", views.product_details, name="product-details"),
    path('<str:category_name>', views.product_category, name='product-category'),
]