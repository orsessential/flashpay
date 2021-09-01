from rest_framework.fields import BooleanField
from .models import Wallet
from rest_framework import permissions

class WalletPermision(permissions.BasePermission):
    def has_permission(self, request, view):
        wallet = Wallet.objects.filter(user=request.user).first()
        if wallet.get_status_display() == "enable":
            if request.method == "PATCH":
                access = True
            else:
                access = True
        elif wallet.get_status_display() == "disable":
            if request.method == "POST":
                access = True
            else:
                access = False
        return access
    