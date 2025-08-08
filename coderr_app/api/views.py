from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    OfferWithDetailsSerializer,
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
    Retrieve and partially update a specific profile.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """
        Resolve profile by user id from the URL path.
        """
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, username=user)
        return profile
    
    def get_serializer_class(self):
        """
        Use different serializers for GET and PATCH.
        """
        if self.request.method == 'PATCH':
            return ProfileUpdateSerializer
        return ProfileSerializer

    def get_permissions(self):
        """
        GET: any authenticated user can view profiles.
        PATCH/PUT: only the profile owner can update.
        """
        if self.request.method in ['PATCH', 'PUT']:
            return [IsAuthenticated(), IsProfileOwner()]
        return [IsAuthenticated()]
    
    def patch(self, request, *args, **kwargs):
        """
        Partially update profile and return the full representation.
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
    List all business profiles.
    """
    serializer_class = BusinessProfileListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only business profiles.
        """
        return Profile.objects.filter(type='business')
    
    def list(self, request, *args, **kwargs):
        """
        Always return an array (empty on errors) for consistency.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # On error return an empty array
            return Response([], status=status.HTTP_200_OK)


class CustomerProfileListView(generics.ListAPIView):
    """
    List all customer profiles.
    """
    serializer_class = CustomerProfileListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only customer profiles.
        """
        return Profile.objects.filter(type='customer')
    
    def list(self, request, *args, **kwargs):
        """
        Always return an array (empty on errors) for consistency.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # On error return an empty array
            return Response([], status=status.HTTP_200_OK)


class OfferPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class OfferListView(generics.ListCreateAPIView):
    """
    List offers (public) and create offers (business users).
    """
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user__username__id']
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['-updated_at']
    
    def get_paginated_response(self, data):
        """
        Ensure a consistent paginated structure in the response.
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
            # Für Erstellung nehmen wir den Create-Serializer für Validierung,
            # aber wir werden die Response mit OfferWithDetailsSerializer bauen
            return OfferCreateSerializer
        return OfferListSerializer

    def get_queryset(self):
        queryset = Offer.objects.all()
        
        # Filter by creator_id
        creator_id = self.request.query_params.get('creator_id')
        if creator_id and creator_id.strip() and creator_id != "":
            try:
                creator_id_int = int(creator_id)
                queryset = queryset.filter(user__username__id=creator_id_int)
            except (ValueError, TypeError):
                # Ignore filter if conversion fails
                pass
        
        # Filter by min_price
        min_price = self.request.query_params.get('min_price')
        if min_price and min_price.strip() and min_price != "":
            try:
                min_price_decimal = Decimal(min_price)
                queryset = queryset.filter(details__price__gte=min_price_decimal).distinct()
            except (ValueError, TypeError):
                # Ignore filter if conversion fails
                pass
        
        # Filter by max_delivery_time
        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time and max_delivery_time.strip() and max_delivery_time != "":
            try:
                max_delivery_time_int = int(max_delivery_time)
                queryset = queryset.filter(details__delivery_time_in_days__lte=max_delivery_time_int).distinct()
            except (ValueError, TypeError):
                # Ignore filter if conversion fails
                pass
        
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsBusinessUser()]
        # GET, HEAD, OPTIONS do not require authentication
        return [AllowAny()]
    
    def list(self, request, *args, **kwargs):
        """
        Return paginated response or a consistent results envelope.
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
            # Fallback on error
            return Response({
                'count': 0,
                'next': None,
                'previous': None,
                'results': []
            }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create an offer and return the full offer with details (including IDs) with HTTP 201.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Neu erstelltes Offer abrufen
        offer_instance = serializer.instance
        response_serializer = OfferWithDetailsSerializer(offer_instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific offer.
    """
    
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return OfferUpdateSerializer
        return OfferDetailViewSerializer

    def get_queryset(self):
        return Offer.objects.all()

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [IsAuthenticated(), IsOfferOwner()]
        # GET requires authentication per documentation
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        """
        Partially or fully update an offer using OfferUpdateSerializer,
        then return the full offer payload (including id and details with ids).
        """
        partial = request.method.lower() == 'patch'
        instance = self.get_object()
        serializer = OfferUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_serializer = OfferWithDetailsSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class OfferDetailDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific OfferDetail.
    """
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = OfferDetail.objects.all()


class OrderListView(generics.ListCreateAPIView):
    """
    List orders for the current user and create new orders.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        """
        Return only orders related to the authenticated user.
        """
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user__username=user) | Q(business_user__username=user)
        )

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]
    
    def list(self, request, *args, **kwargs):
        """
        Always return an array (empty on errors) for consistency.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # On error return an empty array
            return Response([], status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create an order from offer_detail_id and return the full order object with HTTP 201.
        Return 404 if the offer_detail_id does not exist.
        """
        # Vorab 404 prüfen, damit der korrekte Statuscode zurückkommt
        offer_detail_id = request.data.get('offer_detail_id')
        if offer_detail_id is None:
            return Response({'offer_detail_id': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
        try:
            offer_detail_id_int = int(offer_detail_id)
        except (TypeError, ValueError):
            return Response({'offer_detail_id': ['A valid integer is required.']}, status=status.HTTP_400_BAD_REQUEST)

        if not OfferDetail.objects.filter(id=offer_detail_id_int).exists():
            return Response({'detail': 'OfferDetail not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        order_instance = serializer.instance
        response_serializer = OrderSerializer(order_instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific order.
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
            return [IsAuthenticated(), IsStaffUser()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        """
        Update order status using OrderUpdateSerializer and
        return the full order payload (including id and timestamps).
        """
        partial = request.method.lower() == 'patch'
        instance = self.get_object()
        serializer = OrderUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_serializer = OrderSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class OrderCountView(generics.RetrieveAPIView):
    """
    Return number of in-progress orders for a given business user.
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
    Return number of completed orders for a given business user.
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
    List reviews (with filtering and ordering) and create new reviews.
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
        
        # Filter by business_user_id
        business_user_id = self.request.query_params.get('business_user_id')
        if business_user_id and business_user_id.strip():
            try:
                business_user_id_int = int(business_user_id)
                queryset = queryset.filter(business_user__username__id=business_user_id_int)
            except (ValueError, TypeError):
                pass
        
        # Filter by reviewer_id
        reviewer_id = self.request.query_params.get('reviewer_id')
        if reviewer_id and reviewer_id.strip():
            try:
                reviewer_id_int = int(reviewer_id)
                queryset = queryset.filter(reviewer__username__id=reviewer_id_int)
            except (ValueError, TypeError):
                pass
        
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]
    
    def list(self, request, *args, **kwargs):
        """
        Always return an array (empty on errors) for consistency.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Bei Fehlern geben wir ein leeres Array zurück
            return Response([], status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create a review and return the full review (id, business_user, reviewer, rating, description, created_at, updated_at) with HTTP 201.
        """
        create_serializer = ReviewCreateSerializer(data=request.data, context={'request': request})
        create_serializer.is_valid(raise_exception=True)
        self.perform_create(create_serializer)

        review_instance = create_serializer.instance
        response_serializer = ReviewSerializer(review_instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific review.
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

    def update(self, request, *args, **kwargs):
        """
        Update a review (rating/description) and return the full review payload
        including id, business_user, reviewer, timestamps.
        """
        partial = request.method.lower() == 'patch'
        instance = self.get_object()
        serializer = ReviewUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_serializer = ReviewSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class BaseInfoView(generics.RetrieveAPIView):
    """
    Return platform base information and aggregates.
    """
    serializer_class = BaseInfoSerializer
    permission_classes = []  # Keine Authentifizierung erforderlich

    def get_object(self):
        """
        Compute and return platform aggregates.
        """
        # Number of reviews
        review_count = Review.objects.count()
        
        # Average rating rounded to one decimal
        avg_rating_result = Review.objects.aggregate(avg_rating=Avg('rating'))
        average_rating = avg_rating_result['avg_rating']
        if average_rating is not None:
            # Round to one decimal place
            average_rating = round(float(average_rating), 1)
        else:
            average_rating = 0.0
        
        # Number of business profiles
        business_profile_count = Profile.objects.filter(type='business').count()
        
        # Number of offers
        offer_count = Offer.objects.count()
        
        return {
            'review_count': review_count,
            'average_rating': average_rating,
            'business_profile_count': business_profile_count,
            'offer_count': offer_count
        }
