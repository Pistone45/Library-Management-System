from rest_framework import serializers
from library_catalogue.models import *


class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = '__all__'


class LibraryCatalogueSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryCatalogue
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class NewspaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newspaper
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class MembershipStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipStatus
        fields = '__all__'


class LendingBehaviourSerializer(serializers.ModelSerializer):
    class Meta:
        model = LendingBehaviour
        fields = '__all__'


class LendingPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LendingPreference
        fields = "__all__"


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"


class MemberLendingPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberLendingPreference
        fields = "__all__"


class MemberLendingBehaviourSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberLendingBehaviour
        fields = "__all__"


class BorrowingStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowingState
        fields = "__all__"


class UserCatalogueSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCatalogue
        fields = "__all__"
