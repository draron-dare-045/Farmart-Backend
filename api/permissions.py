from rest_framework import permissions

class IsFarmerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow farmers to edit objects.
    Read-only access for everyone else.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_authenticated and request.user.user_type == 'FARMER'

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if hasattr(obj, 'buyer'):
            return obj.buyer == request.user
            
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        return False

class IsOrderFarmerOrBuyerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow a user to interact with an order if they are:
    1. The buyer of the order.
    2. A farmer whose animal is included in the order.
    3. An admin/staff user.
    """
    message = "You do not have permission to perform this action on this order."
 
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if obj.buyer == request.user:
            return True
        
        if request.user.user_type == 'FARMER':
            return obj.items.filter(animal__farmer=request.user).exists()

        return False