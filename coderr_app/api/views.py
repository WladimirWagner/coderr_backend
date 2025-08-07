from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q, Avg, Count
from decimal import Decimal

from coderr_app.models import Profile, Offer, OfferDetail, Order, Review
from coderr_app.api.serializers import (
    ProfileSerializer, 
    ProfileUpdateSerializer,
    BusinessProfileListSerializer,
    CustomerProfileListSerializer,
    OfferListSerializer,
    OfferDetailViewSerializer,
    OfferCreateSerializer,
    OfferUpdateSerializer,
    OfferDetailSerializer,
    OrderSerializer,
    OrderCreateSerializer,
    OrderUpdateSerializer,
    OrderCountSerializer,
    CompletedOrderCountSerializer,
    ReviewSerializer,
    ReviewCreateSerializer,
    ReviewUpdateSerializer,
    BaseInfoSerializer
)
from coderr_app.api.permissions import (
    IsProfileOwner, IsBusinessUser, IsOfferOwner, 
    IsCustomerUser, IsOrderParticipant, IsBusinessOrderOwner, IsStaffUser,
    IsReviewOwner
)


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    View für GET und PATCH Operationen auf einem spezifischen Profil.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]
    
    def get_object(self):
        """
        Holt das Profil basierend auf der User-ID aus der URL.
        """
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, username=user)
        return profile
    
    def get_serializer_class(self):
        """
        Verwendet unterschiedliche Serializer für GET und PATCH.
        """
        if self.request.method == 'PATCH':
            return ProfileUpdateSerializer
        return ProfileSerializer
    
    def patch(self, request, *args, **kwargs):
        """
        PATCH Operation für Profilaktualisierung.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            # Verwende den vollständigen Serializer für die Antwort
            full_serializer = ProfileSerializer(instance)
            return Response(full_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessProfileListView(generics.ListAPIView):
    """
    View für die Liste aller Business-Profile.
    """
    serializer_class = BusinessProfileListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtert nur Business-Profile.
        """
        return Profile.objects.filter(type='business')


class CustomerProfileListView(generics.ListAPIView):
    """
    View für die Liste aller Customer-Profile.
    """
    serializer_class = CustomerProfileListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtert nur Customer-Profile.
        """
        return Profile.objects.filter(type='customer')


class OfferListView(generics.ListCreateAPIView):
    """
    View für die Liste und Erstellung von Offers.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user__username__id']
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['-updated_at']
    
    def get_paginated_response(self, data):
        """
        Überschreibt die Standard-Pagination-Antwort um sicherzustellen,
        dass immer eine korrekte Struktur zurückgegeben wird.
        """
        paginator = self.paginator
        return Response({
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': data
        })

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer

    def get_queryset(self):
        queryset = Offer.objects.all()
        
        # Filter nach creator_id
        creator_id = self.request.query_params.get('creator_id')
        if creator_id and creator_id.strip() and creator_id != "":
            try:
                creator_id_int = int(creator_id)
                queryset = queryset.filter(user__username__id=creator_id_int)
            except (ValueError, TypeError):
                # Wenn creator_id nicht konvertiert werden kann, ignoriere den Filter
                pass
        
        # Filter nach min_price
        min_price = self.request.query_params.get('min_price')
        if min_price and min_price.strip() and min_price != "":
            try:
                min_price_decimal = Decimal(min_price)
                queryset = queryset.filter(details__price__gte=min_price_decimal).distinct()
            except (ValueError, TypeError):
                # Wenn min_price nicht konvertiert werden kann, ignoriere den Filter
                pass
        
        # Filter nach max_delivery_time
        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time and max_delivery_time.strip() and max_delivery_time != "":
            try:
                max_delivery_time_int = int(max_delivery_time)
                queryset = queryset.filter(details__delivery_time_in_days__lte=max_delivery_time_int).distinct()
            except (ValueError, TypeError):
                # Wenn max_delivery_time nicht konvertiert werden kann, ignoriere den Filter
                pass
        
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsBusinessUser()]
        return [IsAuthenticated()]
    
    def list(self, request, *args, **kwargs):
        """
        Überschreibt die list-Methode um sicherzustellen, dass immer eine korrekte Antwort zurückgegeben wird.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'count': len(serializer.data),
                'next': None,
                'previous': None,
                'results': serializer.data
            })
        except Exception as e:
            # Fallback bei Fehlern
            return Response({
                'count': 0,
                'next': None,
                'previous': None,
                'results': []
            }, status=status.HTTP_200_OK)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View für GET, PATCH und DELETE Operationen auf einem spezifischen Offer.
    """
    permission_classes = [IsAuthenticated, IsOfferOwner]
    
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return OfferUpdateSerializer
        return OfferDetailViewSerializer

    def get_queryset(self):
        return Offer.objects.all()

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [IsAuthenticated(), IsOfferOwner()]
        return [IsAuthenticated()]


class OfferDetailDetailView(generics.RetrieveAPIView):
    """
    View für GET Operationen auf einem spezifischen OfferDetail.
    """
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = OfferDetail.objects.all()


class OrderListView(generics.ListCreateAPIView):
    """
    View für die Liste und Erstellung von Orders.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        """
        Gibt nur Orders zurück, die mit dem angemeldeten Benutzer verbunden sind.
        """
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user__username=user) | Q(business_user__username=user)
        )

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCustomerUser()]
        return [IsAuthenticated()]


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View für GET, PATCH und DELETE Operationen auf einem spezifischen Order.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return OrderUpdateSerializer
        return OrderSerializer

    def get_queryset(self):
        return Order.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsOrderParticipant()]
        elif self.request.method in ['PATCH', 'PUT']:
            return [IsAuthenticated(), IsBusinessOrderOwner()]
        elif self.request.method == 'DELETE':
            return [IsStaffUser()]
        return [IsAuthenticated()]


class OrderCountView(generics.RetrieveAPIView):
    """
    View für die Anzahl der laufenden Bestellungen eines Business-Users.
    """
    serializer_class = OrderCountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        business_user_id = self.kwargs.get('business_user_id')
        business_user = get_object_or_404(User, id=business_user_id)
        profile = get_object_or_404(Profile, username=business_user, type='business')
        
        order_count = Order.objects.filter(
            business_user=profile,
            status='in_progress'
        ).count()
        
        return {'order_count': order_count}


class CompletedOrderCountView(generics.RetrieveAPIView):
    """
    View für die Anzahl der abgeschlossenen Bestellungen eines Business-Users.
    """
    serializer_class = CompletedOrderCountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        business_user_id = self.kwargs.get('business_user_id')
        business_user = get_object_or_404(User, id=business_user_id)
        profile = get_object_or_404(Profile, username=business_user, type='business')
        
        completed_order_count = Order.objects.filter(
            business_user=profile,
            status='completed'
        ).count()
        
        return {'completed_order_count': completed_order_count}


class ReviewListView(generics.ListCreateAPIView):
    """
    View für die Liste und Erstellung von Reviews.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['business_user__username__id', 'reviewer__username__id']
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.all()
        
        # Filter nach business_user_id
        business_user_id = self.request.query_params.get('business_user_id')
        if business_user_id:
            queryset = queryset.filter(business_user__username__id=business_user_id)
        
        # Filter nach reviewer_id
        reviewer_id = self.request.query_params.get('reviewer_id')
        if reviewer_id:
            queryset = queryset.filter(reviewer__username__id=reviewer_id)
        
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCustomerUser()]
        return [IsAuthenticated()]


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View für GET, PATCH und DELETE Operationen auf einem spezifischen Review.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewOwner]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return ReviewUpdateSerializer
        return ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [IsAuthenticated(), IsReviewOwner()]
        return [IsAuthenticated()]


class BaseInfoView(generics.RetrieveAPIView):
    """
    View für die Basis-Informationen der Plattform.
    """
    serializer_class = BaseInfoSerializer
    permission_classes = []  # Keine Authentifizierung erforderlich

    def get_object(self):
        """
        Berechnet aggregierende Informationen über die Plattform.
        """
        # Anzahl der Reviews
        review_count = Review.objects.count()
        
        # Durchschnittliche Bewertung (auf eine Dezimalstelle gerundet)
        avg_rating_result = Review.objects.aggregate(avg_rating=Avg('rating'))
        average_rating = avg_rating_result['avg_rating']
        if average_rating is not None:
            # Runde auf eine Dezimalstelle
            average_rating = round(float(average_rating), 1)
        else:
            average_rating = 0.0
        
        # Anzahl der Business-Profile
        business_profile_count = Profile.objects.filter(type='business').count()
        
        # Anzahl der Offers
        offer_count = Offer.objects.count()
        
        return {
            'review_count': review_count,
            'average_rating': average_rating,
            'business_profile_count': business_profile_count,
            'offer_count': offer_count
        }
