from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserAccount, UserProfile, TransactionTicket


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


class UserSerializer (serializers.ModelSerializer):
    useraccount = UserAccountSerializer()
    userprofile = UserProfileSerializer()
    transactionticket_set = TransactionTicketSerializer(
        many=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'useraccount', 'userprofile', 'last_login', 'is_superuser', 'is_active', 'transactionticket_set')

    def create(self, validated_data):
        useraccount_data = validated_data.pop('useraccount')
        userprofile_data = validated_data.pop('userprofile')

        transaction_tickets_data = validated_data.pop(
            'transactionticket_set', [])

        user = User.objects.create(**validated_data)

        UserAccount.objects.create(user=user, **useraccount_data)
        UserProfile.objects.create(user=user, **userprofile_data)

        if not transaction_tickets_data:
            TransactionTicket.objects.create(user=user)

        return user

    def update(self, instance, validated_data):
        useraccount_data = validated_data.pop('useraccount', {})

        if not hasattr(instance, 'useraccount'):
            if useraccount_data:
                useraccount = UserAccount.objects.create(
                    user=instance, **useraccount_data)
                instance.useraccount = useraccount

        useraccount_serializer = UserAccountSerializer(
            instance.useraccount, data=useraccount_data, partial=True)
        if useraccount_serializer.is_valid():
            useraccount = useraccount_serializer.save()
            validated_data['useraccount'] = useraccount

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
