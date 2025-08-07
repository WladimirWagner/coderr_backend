from django.urls import path
from . import views

urlpatterns = [
    # Base Info View - Plattform-Statistiken
    path('base-info/', views.BaseInfoView.as_view(), name='base-info'),
    
    # Profile Detail View - GET und PATCH für spezifisches Profil
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    
    # Profile List Views - GET für Business und Customer Profile
    path('profiles/business/', views.BusinessProfileListView.as_view(), name='business-profiles'),
    path('profiles/customer/', views.CustomerProfileListView.as_view(), name='customer-profiles'),
    
    # Offer Views - CRUD für Offers
    path('offers/', views.OfferListView.as_view(), name='offer-list'),
    path('offers/<int:pk>/', views.OfferDetailView.as_view(), name='offer-detail'),
    
    # OfferDetail View - GET für spezifisches OfferDetail
    path('offerdetails/<int:pk>/', views.OfferDetailDetailView.as_view(), name='offerdetail-detail'),
    
    # Order Views - CRUD für Orders
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    
    # Order Count Views - Statistiken für Business-User
    path('order-count/<int:business_user_id>/', views.OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/', views.CompletedOrderCountView.as_view(), name='completed-order-count'),
    
    # Review Views - CRUD für Reviews
    path('reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
]