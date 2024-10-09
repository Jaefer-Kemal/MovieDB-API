from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def had_permission(self,view,request):
        admin_permission = bool(request.user and request.user.is_staff)
        # return request.method == 'GET' or admin_permission
        # super() provide value bool(request.user and request.user.is_staff)
        return request.method in permissions.SAFE_METHODS or admin_permission
    
    
class IsReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.review_user == request.user