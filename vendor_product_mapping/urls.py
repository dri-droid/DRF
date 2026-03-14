from django.urls import path
from .views import VendorProductMappingListCreateAPIView, VendorProductMappingDetailAPIView

urlpatterns = [

    path('vendor-product-mappings/', VendorProductMappingListCreateAPIView.as_view()),
    path('vendor-product-mappings/<int:pk>/', VendorProductMappingDetailAPIView.as_view()),

]