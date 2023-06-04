from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserWallet, UserAccount, UserProfile, TransactionTicket, UserTransactions


class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = '__all__'


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class TransactionTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionTicket
        fields = '__all__'


class UserTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTransactions
        fields = '__all__'


class UserSerializer (serializers.ModelSerializer):
    userwallet = UserWalletSerializer()
    userprofile = UserProfileSerializer()
    useraccount_set = UserAccountSerializer(many=True, required=False)
    transactionticket_set = TransactionTicketSerializer(
        many=True, required=False)
    transactionhistory_set = UserTransactionsSerializer(
        many=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'userwallet', 'useraccount_set', 'userprofile', 'last_login', 'is_superuser', 'is_active', 'transactionticket_set', 'transactionhistory_set')

    def create(self, validated_data):
        userwallet_data = validated_data.pop('userwallet')
        userprofile_data = validated_data.pop('userprofile')
        transaction_tickets_data = validated_data.pop(
            'transactionticket_set', [])

        user = User.objects.create(**validated_data)

        UserWallet.objects.create(user=user, **userwallet_data)
        UserProfile.objects.create(user=user, **userprofile_data)

        if not transaction_tickets_data:
            TransactionTicket.objects.create(user=user)

        return user

    def update(self, instance, validated_data):
        userwallet_data = validated_data.pop('userwallet', {})
        if not hasattr(instance, 'userwallet'):
            if userwallet_data:
                userwallet = UserWallet.objects.create(
                    user=instance, **userwallet_data)
                instance.userwallet = userwallet

        userwallet_serializer = UserWalletSerializer(
            instance.userwallet, data=userwallet_data, partial=True)
        if userwallet_serializer.is_valid():
            userwallet = userwallet_serializer.save()
            validated_data['userwallet'] = userwallet

        useraccount_data = validated_data.pop('useraccount_set', [])

        # if not hasattr(instance, 'useraccount_set'):
        #     if useraccount_data:
        #         useraccount = UserAccount.objects.create(
        #             user=instance, **useraccount_data)
        #         instance.useraccount = useraccount

        useraccount_serializer = UserAccountSerializer(
            instance.useraccount_set, data=useraccount_data, partial=True)
        if useraccount_serializer.is_valid():
            useraccount = useraccount_serializer.save()
            validated_data['useraccount_set'] = useraccount

        userprofile_data = validated_data.pop('userprofile', {})

        if not hasattr(instance, 'userprofile'):
            if userprofile_data:
                userprofile = UserProfile.objects.create(
                    user=instance, **userprofile_data)
                instance.userprofile = userprofile

        userprofile_serializer = UserProfileSerializer(
            instance.userprofile, data=userprofile_data, partial=True)
        if userprofile_serializer.is_valid():
            userprofile = userprofile_serializer.save()
            validated_data['userprofile'] = userprofile

        return super().update(instance, validated_data)
