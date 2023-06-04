from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from django.contrib.auth.models import User
from .models import UserAccount, UserProfile, TransactionTicket, UserWallet, UserTransactions
from .serializers import UserSerializer, UserAccountSerializer, UserProfileSerializer, TransactionTicketSerializer, UserWalletSerializer, UserTransactionsSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.db import transaction
from django.db.models import Q
import requests


bankUrl = "http://127.0.0.1:1213"
headersList = {
    "Accept": "*/*",
    "Authorization": "Token 88075057772ea79caa679a1e2c1fe138d25cc8db",
    "Content-Type": "application/json"
}


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        token['is_active'] = user.is_active
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def getUsers(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def getUserInfo(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getTickets(request):
    if request.method == 'GET':
        ticket = TransactionTicket.objects.all()
        serializer = TransactionTicketSerializer(
            ticket, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TransactionTicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def getTicket(request, reference_id):
    try:
        ticket = TransactionTicket.objects.get(reference_id=reference_id)
    except TransactionTicket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TransactionTicketSerializer(ticket)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def getUserAccount(request, id):
    card_num = request.data.get('card_num')
    card_pin = request.data.get('card_pin')

    try:
        useraccount_set = UserAccount.objects.filter(user=id)
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if card_num and card_pin:
            account = UserAccount.objects.get(user=id,
                                              card_num=card_num, card_pin=card_pin)
            serializer = UserAccountSerializer(account)
            return Response(serializer.data)

        serializer = UserAccountSerializer(useraccount_set, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data.copy()
        data['card_num'] = data.get('card_num')
        data['card_pin'] = data.get('card_pin')
        data['user'] = id

        exist = UserAccount.objects.filter(user=id,
                                           card_num=card_num, card_pin=card_pin).exists()

        response = requests.get(
            f'{bankUrl}/api/accounts/verify', json=data, headers=headersList)
        if response.status_code == 200 and not exist:
            if data['card_num'][:3] == '456':
                data['brand'] = 'FortBank'
            else:
                data['brand'] = 'bank'
            serializer = UserAccountSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif response.status_code == 404:
            return Response({"message": "Card number/pin does not exist"}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'an error occured in the server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'PUT':
        account = UserAccount.objects.get(card_num=card_num, card_pin=card_pin)
        serializer = UserAccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        account = UserAccount.objects.get(card_num=card_num, card_pin=card_pin)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def getUserProfile(request, id):
    try:
        userProfile = UserProfile.objects.get(user=id)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserProfileSerializer(userProfile)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(userProfile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        userProfile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBalance(request, id):
    try:
        userwallet = UserWallet.objects.get(user=id)
    except UserWallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserWalletSerializer(userwallet)
        return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def updateBalance(request, id):
    try:
        userwallet = UserWallet.objects.get(user=id)
    except UserWallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserWalletSerializer(userwallet)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserWalletSerializer(
            userwallet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@transaction.atomic
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Payment(request):
    if request.method == 'POST':
        user1_id = request.data.get('user1')
        user2_id = request.data.get('user2')
        amount = request.data.get('amount')

        user1 = User.objects.get(id=user1_id)
        user2 = User.objects.get(id=user2_id)
        if user1 and user2:
            sender = UserWallet.objects.get(user=user1)
            sender_history = UserTransactions(
                user=user1,
                sent_to=user2.username,
                amount=amount,
                previous_balance=sender.balance,
                transaction_type='Pay'
            )
            sender_history.save()
            sender.balance -= amount
            sender.save()

            receiver = UserWallet.objects.get(user=user2)
            receiver_history = UserTransactions(
                user=user2,
                sent_to=user1.username,
                amount=amount,
                previous_balance=receiver.balance,
                transaction_type='Receive Payment'
            )
            receiver_history.save()
            receiver.balance += amount
            receiver.save()

            serializer = UserWalletSerializer(sender)

            return Response(serializer.data)
        return Response({'message': 'invalid'})


@transaction.atomic
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def AddFunds(request):
    if request.method == 'PUT':
        user = request.data.get('user')
        amount = request.data.get('amount')
        card_num = request.data.get('card_num')
        card_pin = request.data.get('card_pin')

        if user:
            data = {
                "card_num": card_num,
                "card_pin": card_pin
            }

            response = requests.get(
                f'{bankUrl}/api/accounts/update_balance', json=data, headers=headersList)
            bank_details = response.json()
            prev_balance = bank_details['balance']

            if prev_balance < amount:
                return Response({"message": "Account insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

            data = {
                "card_num": card_num,
                "card_pin": card_pin,
                "balance": prev_balance - amount
            }
            requests.put(
                f'{bankUrl}/api/accounts/update_balance', json=data, headers=headersList)

            receiver = UserWallet.objects.get(user=user)
            receiverUser = User.objects.get(id=user)
            addfunds_history = UserTransactions(
                user=receiverUser,
                sent_to=card_num,
                amount=amount,
                previous_balance=receiver.balance,
                transaction_type='Add funds'
            )
            addfunds_history.save()
            receiver.balance += amount
            receiver.save()

            serializer = UserWalletSerializer(receiver)

            return Response(serializer.data)


@transaction.atomic
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def CashOutFunds(request):
    if request.method == 'PUT':
        user = request.data.get('user')
        amount = request.data.get('amount')
        card_num = request.data.get('card_num')
        card_pin = request.data.get('card_pin')
        if user:
            data = {
                "card_num": card_num,
                "card_pin": card_pin
            }

            response = requests.get(
                f'{bankUrl}/api/accounts/update_balance', json=data, headers=headersList)
            bank_details = response.json()
            prev_balance = bank_details['balance']

            data = {
                "card_num": card_num,
                "card_pin": card_pin,
                "balance": prev_balance + amount
            }
            requests.put(
                f'{bankUrl}/api/accounts/update_balance', json=data, headers=headersList)

            sender = UserWallet.objects.get(user=user)
            if sender.balance < amount:
                return Response({"message": "wallet insufficient balance"})
            senderUser = User.objects.get(id=user)
            cashoutfunds_history = UserTransactions(
                user=senderUser,
                sent_to=bank_details['card_num'],
                amount=amount,
                previous_balance=sender.balance,
                transaction_type='Transfer to bank'
            )
            cashoutfunds_history.save()
            sender.balance -= amount
            sender.save()

            serializer = UserWalletSerializer(sender)

            return Response(serializer.data)


@transaction.atomic
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def TransacHistory(request, id):
    try:
        history = UserTransactions.objects.filter(user=id)
    except UserTransactions.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserTransactionsSerializer(history, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data.copy()
        data['sender'] = data.get('sender')
        data['receiver'] = data.get('receiver')
        data['amount'] = data.get('amount')
        data['transaction_type'] = data.get('type')

        serializer = TransactionTicketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
