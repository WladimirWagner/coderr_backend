from rest_framework import permissions


class IsProfileOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a profile to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Lesen ist für alle authentifizierten Benutzer erlaubt
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Schreiben ist nur für den Profilbesitzer erlaubt
        return obj.username == request.user


class IsAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsBusinessUser(permissions.BasePermission):
    """
    Custom permission to only allow business users to create offers.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            profile = request.user.profile
            return profile.type == 'business'
        except:
            return False


class IsOfferOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an offer to edit/delete it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Lesen ist für alle authentifizierten Benutzer erlaubt
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Schreiben ist nur für den Offer-Besitzer erlaubt
        return obj.user.username == request.user


class IsCustomerUser(permissions.BasePermission):
    """
    Custom permission to only allow customer users to create orders.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            profile = request.user.profile
            return profile.type == 'customer'
        except:
            return False


class IsOrderParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of an order to view it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Benutzer muss entweder Kunde oder Business-User der Order sein
        return (obj.customer_user.username == request.user or 
                obj.business_user.username == request.user)


class IsBusinessOrderOwner(permissions.BasePermission):
    """
    Custom permission to only allow business users to update order status.
    """
    
    def has_object_permission(self, request, view, obj):
        # Nur Business-User der Order kann den Status aktualisieren
        return obj.business_user.username == request.user


class IsStaffUser(permissions.BasePermission):
    """
    Custom permission to only allow staff users to delete orders.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class IsReviewOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a review to edit/delete it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Lesen ist für alle authentifizierten Benutzer erlaubt
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Schreiben ist nur für den Review-Ersteller erlaubt
        return obj.reviewer.username == request.user
