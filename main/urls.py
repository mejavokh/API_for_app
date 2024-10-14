from django.urls import path
from .views import CategoryListView, ProductsByCategoryView, ProductDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:category_id>/products/', ProductsByCategoryView.as_view(), name='products-by-category'),
    path('product/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
