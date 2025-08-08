from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Profile model for platform users.
    
    Extends Django's User with profile type (business/customer), contact
    information, and working hours.
    """
    
    TYPE_CHOICES = [
        ('business', 'Business'),
        ('customer', 'Customer'),
    ]

    username = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    file = models.FileField(upload_to='files/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, default='')
    tel = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(max_length=255, blank=True, default='')
    working_hours = models.CharField(max_length=255, blank=True, default='')
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the profile."""
        return f"{self.username.username} - {self.type}"


class Offer(models.Model):
    """
    Offer model for services.
    
    Represents a service offering by a business user. Each offer can have
    multiple details (basic, standard, premium).
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the offer."""
        return f"{self.title} by {self.user.username.username}"

    @property
    def min_price(self):
        """
        Compute minimal price across all offer details.
        
        Returns:
            Decimal: Lowest price among details or 0 if none exist
        """
        details = self.details.all()
        if details.exists():
            return min(detail.price for detail in details)
        return 0

    @property
    def min_delivery_time(self):
        """
        Compute shortest delivery time across all offer details.
        
        Returns:
            int: Shortest delivery time in days or 0 if none exist
        """
        details = self.details.all()
        if details.exists():
            return min(detail.delivery_time_in_days for detail in details)
        return 0


class OfferDetail(models.Model):
    """
    Offer detail model.
    
    Each offer can have multiple detail tiers (basic, standard, premium)
    with different prices, delivery times and features.
    """
    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES)

    def __str__(self):
        """String representation of the offer detail."""
        return f"{self.title} - {self.offer_type}"


class Order(models.Model):
    """
    Order model.
    
    Represents a customer's order for a specific offer detail provided by a
    business user.
    """
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders_as_customer')
    business_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders_as_business')
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE, related_name='orders')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=20, choices=OfferDetail.OFFER_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the order."""
        return f"Order {self.id} - {self.title} ({self.status})"

    def save(self, *args, **kwargs):
        """
        Override save to copy fields from the referenced offer detail on creation.
        """
        if not self.pk and self.offer_detail:
            self.title = self.offer_detail.title
            self.revisions = self.offer_detail.revisions
            self.delivery_time_in_days = self.offer_detail.delivery_time_in_days
            self.price = self.offer_detail.price
            self.features = self.offer_detail.features
            self.offer_type = self.offer_detail.offer_type
            self.business_user = self.offer_detail.offer.user
        super().save(*args, **kwargs)


class Review(models.Model):
    """
    Review model.
    
    Allows customers to review business users after orders.
    """
    business_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews_received')
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews_given')
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the review."""
        return f"Review by {self.reviewer} for {self.business_user}"

