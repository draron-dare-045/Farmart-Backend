from rest_framework import permissions

class IsFarmerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_authenticated and request.user.user_type == 'FARMER'

class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if hasattr(obj, 'buyer'):
            return obj.buyer == request.user
            
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        return False

class IsOrderFarmerOrBuyerOrAdmin(permissions.BasePermission):

    message = "You do not have permission to perform this action on this order."
 
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if obj.buyer == request.user:
            return True
        
        if request.user.user_type == 'FARMER':
            return obj.items.filter(animal__farmer=request.user).exists()

        return False
