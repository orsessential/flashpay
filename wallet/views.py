from accounts.models import UserWallet
import uuid

from decimal import Context
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework import exceptions
from django.http.response import JsonResponse
from django.conf import settings
from rest_framework.response import Response

from .models import Wallet
from .utils import WalletPermision
from rest_framework.authtoken.models import Token

class DepositAmount(APIView):
    # API to deposit an amount to user's wallet.

    permission_classes = (IsAuthenticated, WalletPermision)
    def post(self, request):
        success, data = False, {}
        amount = request.data.get('amount', None)
        user = request.user
        
        if user:
            if (not amount) or (amount <= 0):
                success = False
            else:
                wallet = Wallet.objects.filter(user=user).first()
                if wallet.get_status_display() == "enable":
                    current_balance = wallet.balance
                    wallet.balance = current_balance + amount
                    wallet.save()
                    success = True
                else:
                    success = False
            
        if success:
            data = {"deposit": {"id": wallet.uuid,
                                "deposit_by": user.owned_by,
                                "status": wallet.get_status_display(),
                                "deposit_at": wallet.updated,
                                "amount": wallet.balance,
                                "reference_id":str(uuid.uuid4())}}
              
        return JsonResponse({'status': "success" if success else "fail",
                             'data': data},
                            status=201 if success else 
                            status.HTTP_400_BAD_REQUEST)


class WithdrawalWallet(APIView):
    # API to withdraw amount from user's wallet.

    permission_classes = (IsAuthenticated, WalletPermision)
    def post(self, request):
        success, data = False, {}
        amount = request.data.get('amount', None)
        user = request.user   
                
        if user:
            wallet = Wallet.objects.filter(user=user).first()
            if (not amount) or (amount > wallet.balance) or (amount <= 0):
                success = False
            else:
                current_balance = wallet.balance
                wallet.balance = current_balance - amount
                wallet.save()
                success = True
            
        if success:
            data = {"withdrawal": {"id": wallet.uuid,
                                   "withdrawn_by": user.owned_by,
                                   "status": wallet.get_status_display(),
                                   "withdrawn_at": wallet.updated,
                                   "amount": wallet.balance,
                                   "reference_id":str(uuid.uuid4())}}
              
        return JsonResponse({'status': "success" if success else "fail",
                             'data': data},
                            status=201 if success else 
                            status.HTTP_400_BAD_REQUEST)


class WalletView(APIView):
    permission_classes = (IsAuthenticated, WalletPermision)
    
    def get(self, request):
        '''
            this function used to get wallet balance of authenticated user.
            access will be denied if wallet status is 'disable'
        '''
        success, data = False, {}
        user = request.user
        
        if user:
            wallet = Wallet.objects.filter(user=user).first()
            data = {"wallet": {"id": wallet.uuid,
                               "owned_by": wallet.user.owned_by,
                               "status": wallet.get_status_display(),
                               "enable_at": wallet.created, 
                               "balance": wallet.balance}}
            success = True
        else:
            data ={"error": "Disable"}
            
            
        return JsonResponse({'status': "success" if success else "fail",
                             'data': data},
                            status=200 if success else
                            status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        '''
            this function used to ENABLE to user's wallet when wallet status "disable".
            after di status enable, we can deposit, view, or withdrawal our wallet again.
            if wallet already "enable" this method return 400 response
        '''
        success, data = False, {}
        user = request.user
        
        if user:
            wallet = Wallet.objects.filter(user=user).first()
            if wallet.get_status_display() == "enable":
                success = False
            else:
                wallet.status = wallet.STATUS.enable
                wallet.save()
                success = True
            
        if success:
            data = {"wallet": {"id": wallet.uuid,
                               "owned_by": wallet.user.owned_by,
                               "status": wallet.get_status_display(),
                               "enabled_at": wallet.updated, 
                               "balance": wallet.balance}}
              
        return JsonResponse({'status': "success" if success else "fail",
                             'data': data}, status=201 if success else 
                            status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        '''
            this function used to DISABLE to user's wallet when wallet status "enable".
            after di status disable, we can not deposit, view, or withdrawal our wallet.
            if status wallet already "disable" we cannot access this one. we need to enable.
            
        '''
        success, data = False, {}
        user = request.user
        
        if user:
            wallet = Wallet.objects.filter(user=user).first()
            wallet.status = wallet.STATUS.disable
            wallet.save()
            success = True
            
        if success:
            data = {"wallet": {"id": wallet.uuid,
                               "owned_by": wallet.user.owned_by,
                               "status": wallet.get_status_display(),
                               "disable_at": wallet.updated, 
                               "balance": wallet.balance}}
              
        return JsonResponse({'status': "success" if success else "fail",
                             'data': data}, status=200 if success else 
                            status.HTTP_400_BAD_REQUEST)


class WalletInitial(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        '''
            this function normally used to initialize user's wallet using customer_xid existing user.
            if user not found in UserWallet model. return 400.
        '''
        success, data = False, {}
        user = UserWallet.objects.filter(owned_by=request.data.get('customer_xid')).first()
        if user:
            wallet_exist = Wallet.objects.filter(user=user).first()
            if wallet_exist is None:
                obj = Wallet.objects.create(user=user)
                obj.save()
                token = Token.objects.create(user=user)
                data = {
                    "token": token.key
                }
                success = True

        return JsonResponse({'status': "success" if success else "fail",
                                'data': data}, status=201 if success else 
                                status.HTTP_400_BAD_REQUEST)
            