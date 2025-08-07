from rest_framework import serializers
from coderr_app.models import Profile, Offer, OfferDetail, Order, Review
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer für Profile mit allen Feldern für GET und PATCH Operationen.
    """
    user = serializers.ReadOnlyField(source='username.id')
    username = serializers.ReadOnlyField(source='username.username')
    
    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file', 
            'location', 'tel', 'description', 'working_hours', 
            'type', 'email', 'created_at'
        ]
        read_only_fields = ['user', 'username', 'type', 'created_at']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer für PATCH Operationen - erlaubt nur bestimmte Felder zu aktualisieren.
    """
    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'file', 'location', 
            'tel', 'description', 'working_hours', 'email'
        ]

    def validate_email(self, value):
        """
        Validiert, dass die E-Mail-Adresse eindeutig ist (außer für den aktuellen Benutzer).
        """
        user = self.context['request'].user
        if Profile.objects.filter(email=value).exclude(username=user).exists():
            raise serializers.ValidationError("Diese E-Mail-Adresse wird bereits verwendet.")
        return value


class BusinessProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer für die Liste der Business-Profile.
    """
    user = serializers.ReadOnlyField(source='username.id')
    username = serializers.ReadOnlyField(source='username.username')
    
    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file', 
            'location', 'tel', 'description', 'working_hours', 'type'
        ]


class CustomerProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer für die Liste der Customer-Profile.
    """
    user = serializers.ReadOnlyField(source='username.id')
    username = serializers.ReadOnlyField(source='username.username')
    
    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file', 
            'location', 'tel', 'description', 'working_hours', 'type'
        ]


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer für OfferDetail mit allen Feldern.
    """
    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days', 
            'price', 'features', 'offer_type'
        ]


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    """
    Serializer für die Erstellung von OfferDetails.
    """
    class Meta:
        model = OfferDetail
        fields = [
            'title', 'revisions', 'delivery_time_in_days', 
            'price', 'features', 'offer_type'
        ]


class OfferDetailUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer für die Aktualisierung von OfferDetails.
    """
    class Meta:
        model = OfferDetail
        fields = [
            'title', 'revisions', 'delivery_time_in_days', 
            'price', 'features', 'offer_type'
        ]


class OfferDetailListSerializer(serializers.ModelSerializer):
    """
    Serializer für die Liste von OfferDetails (nur ID und URL).
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/offerdetails/{obj.id}/')
        return f'/api/offerdetails/{obj.id}/'


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer für Benutzerdetails in Offer-Listen.
    """
    first_name = serializers.CharField(source='profile.first_name', allow_blank=True, default='')
    last_name = serializers.CharField(source='profile.last_name', allow_blank=True, default='')
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
    
    def to_representation(self, instance):
        """
        Überschreibt die Darstellung um sicherzustellen, dass immer gültige Werte zurückgegeben werden.
        """
        try:
            return super().to_representation(instance)
        except Exception:
            # Fallback wenn Profile nicht existiert
            return {
                'first_name': getattr(instance.profile, 'first_name', '') if hasattr(instance, 'profile') and instance.profile else '',
                'last_name': getattr(instance.profile, 'last_name', '') if hasattr(instance, 'profile') and instance.profile else '',
                'username': instance.username
            }


class OfferListSerializer(serializers.ModelSerializer):
    """
    Serializer für die Liste von Offers mit minimalen Informationen.
    """
    user = serializers.ReadOnlyField(source='user.username.id')
    details = OfferDetailListSerializer(many=True, read_only=True)
    user_details = UserDetailsSerializer(source='user.username', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at', 
            'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details'
        ]
    
    def to_representation(self, instance):
        """
        Überschreibt die Darstellung um sicherzustellen, dass immer gültige Werte zurückgegeben werden.
        """
        try:
            return super().to_representation(instance)
        except Exception as e:
            # Fallback bei Fehlern
            return {
                'id': getattr(instance, 'id', None),
                'user': getattr(instance.user.username, 'id', None) if instance.user and hasattr(instance.user, 'username') else None,
                'title': getattr(instance, 'title', ''),
                'image': getattr(instance, 'image', None),
                'description': getattr(instance, 'description', ''),
                'created_at': getattr(instance, 'created_at', None),
                'updated_at': getattr(instance, 'updated_at', None),
                'details': [],
                'min_price': getattr(instance, 'min_price', 0),
                'min_delivery_time': getattr(instance, 'min_delivery_time', 0),
                'user_details': {
                    'first_name': '',
                    'last_name': '',
                    'username': getattr(instance.user.username, 'username', '') if instance.user and hasattr(instance.user, 'username') else ''
                }
            }


class OfferDetailViewSerializer(serializers.ModelSerializer):
    """
    Serializer für ein einzelnes Offer mit allen Details.
    """
    user = serializers.ReadOnlyField(source='user.username.id')
    details = OfferDetailListSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at', 
            'updated_at', 'details', 'min_price', 'min_delivery_time'
        ]


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer für die Erstellung von Offers mit Details.
    """
    details = OfferDetailCreateSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']

    def validate_details(self, value):
        """
        Validiert, dass mindestens 3 Details vorhanden sind.
        """
        if len(value) < 3:
            raise serializers.ValidationError("Ein Angebot muss mindestens 3 Details haben.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user
        profile = Profile.objects.get(username=user)
        
        offer = Offer.objects.create(user=profile, **validated_data)
        
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        
        return offer


class OfferUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer für die Aktualisierung von Offers.
    """
    details = OfferDetailUpdateSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        
        # Update Offer fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update details if provided
        if details_data is not None:
            # Delete existing details
            instance.details.all().delete()
            
            # Create new details
            for detail_data in details_data:
                OfferDetail.objects.create(offer=instance, **detail_data)
        
        return instance


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer für Orders mit allen Feldern.
    """
    customer_user = serializers.ReadOnlyField(source='customer_user.username.id')
    business_user = serializers.ReadOnlyField(source='business_user.username.id')

    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'title', 'revisions',
            'delivery_time_in_days', 'price', 'features', 'offer_type',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'customer_user', 'business_user', 'title', 'revisions',
            'delivery_time_in_days', 'price', 'features', 'offer_type',
            'created_at', 'updated_at'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer für die Erstellung von Orders.
    """
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['offer_detail_id']

    def validate_offer_detail_id(self, value):
        """
        Validiert, dass das OfferDetail existiert.
        """
        try:
            OfferDetail.objects.get(id=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError("Das angegebene Angebotsdetail existiert nicht.")
        return value

    def create(self, validated_data):
        offer_detail_id = validated_data.pop('offer_detail_id')
        offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        
        user = self.context['request'].user
        customer_profile = Profile.objects.get(username=user)
        
        order = Order.objects.create(
            customer_user=customer_profile,
            offer_detail=offer_detail,
            **validated_data
        )
        
        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer für die Aktualisierung von Orders (nur Status).
    """
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        """
        Validiert, dass der Status gültig ist.
        """
        valid_statuses = ['in_progress', 'completed', 'cancelled']
        if value not in valid_statuses:
            raise serializers.ValidationError("Ungültiger Status.")
        return value


class OrderCountSerializer(serializers.Serializer):
    """
    Serializer für Order-Count-Endpunkte.
    """
    order_count = serializers.IntegerField()


class CompletedOrderCountSerializer(serializers.Serializer):
    """
    Serializer für Completed-Order-Count-Endpunkte.
    """
    completed_order_count = serializers.IntegerField()


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer für Reviews mit allen Feldern.
    """
    business_user = serializers.ReadOnlyField(source='business_user.username.id')
    reviewer = serializers.ReadOnlyField(source='reviewer.username.id')

    class Meta:
        model = Review
        fields = [
            'id', 'business_user', 'reviewer', 'rating', 'description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['business_user', 'reviewer', 'created_at', 'updated_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer für die Erstellung von Reviews.
    """
    business_user = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['business_user', 'rating', 'description']

    def validate_business_user(self, value):
        """
        Validiert, dass der Business-User existiert und vom Typ 'business' ist.
        """
        try:
            business_user = User.objects.get(id=value)
            profile = Profile.objects.get(username=business_user, type='business')
        except (User.DoesNotExist, Profile.DoesNotExist):
            raise serializers.ValidationError("Der angegebene Business-User existiert nicht.")
        return value

    def validate(self, data):
        """
        Validiert, dass der Reviewer nur eine Bewertung pro Business-User abgeben kann.
        """
        user = self.context['request'].user
        reviewer_profile = Profile.objects.get(username=user)
        business_user_id = data['business_user']
        business_user = User.objects.get(id=business_user_id)
        business_profile = Profile.objects.get(username=business_user, type='business')
        
        # Prüfe, ob bereits eine Bewertung existiert
        if Review.objects.filter(reviewer=reviewer_profile, business_user=business_profile).exists():
            raise serializers.ValidationError("Sie haben bereits eine Bewertung für diesen Business-User abgegeben.")
        
        return data

    def create(self, validated_data):
        business_user_id = validated_data.pop('business_user')
        business_user = User.objects.get(id=business_user_id)
        business_profile = Profile.objects.get(username=business_user, type='business')
        
        user = self.context['request'].user
        reviewer_profile = Profile.objects.get(username=user)
        
        review = Review.objects.create(
            business_user=business_profile,
            reviewer=reviewer_profile,
            **validated_data
        )
        
        return review


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer für die Aktualisierung von Reviews (nur rating und description).
    """
    class Meta:
        model = Review
        fields = ['rating', 'description']

    def validate_rating(self, value):
        """
        Validiert, dass die Bewertung zwischen 1 und 5 liegt.
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("Die Bewertung muss zwischen 1 und 5 liegen.")
        return value


class BaseInfoSerializer(serializers.Serializer):
    """
    Serializer für die Basis-Informationen der Plattform.
    """
    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    business_profile_count = serializers.IntegerField()
    offer_count = serializers.IntegerField()
