from rest_framework import serializers
from .models import Wallet
        
class WalletDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Wallet
        fields = ('uuid', 'status', 'created', 'updated', 'balance')
