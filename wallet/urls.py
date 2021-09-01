from django.urls import path
from django.conf.urls import include
from .views import WalletInitial, WalletView, DepositAmount, WithdrawalWallet

urlpatterns = [

    path('api/v1/', include([
        path('init', WalletInitial.as_view(), name='initial-wallet'),
        path('wallet', WalletView.as_view(), name='wallet-view'),
        path('wallet/withdrawls', WithdrawalWallet.as_view(), name='wallet-withdraw'),
        path('wallet/deposits', DepositAmount.as_view(), name='wallet-deposit')
    ])),
]
