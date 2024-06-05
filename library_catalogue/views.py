import json
from datetime import timedelta, datetime

from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import generics, permissions, status
from library_catalogue.serializers import *
from rest_framework.response import Response

from users.models import Role


# Book Views
class BookCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                library_catalogue = LibraryCatalogue(title=request.data['book_name'],
                                                     publication_date=request.data['publication_date'],
                                                     current_condition=request.data['current_condition'],
                                                     resource_type_id=request.data['resource_type_id'],
                                                     genre_id=request.data['genre_id'],
                                                     format_id=request.data['format_id'])
                library_catalogue.save()

                # Create book based on catalogue
                book = Book(isbn=request.data['isbn'], book_name=request.data['book_name'],
                            author=request.data['author'],
                            number_of_copies=request.data['number_of_copies'],
                            publication_date=request.data['publication_date'],
                            library_catalogue_id=library_catalogue.library_catalogue_id)
                book.save()
                data = Book.objects.filter(pk=book.pk).values()

                # Commit the changes
                transaction.savepoint_commit(sid)
                return Response(data[0], status=status.HTTP_201_CREATED)

            except Exception as e:
                transaction.savepoint_rollback(sid)
                data = {"code": status.HTTP_400_BAD_REQUEST, "message": "Failed to create Book"}
                return JsonResponse(data, safe=False)


class BookListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        books = list(Book.objects.annotate(
            genre_id=F('library_catalogue__genre__genre_id'),
            genre=F('library_catalogue__genre__genre'),
            format_id=F('library_catalogue__format__format_id'),
            format=F('library_catalogue__format__format'),
        ).values(
            'isbn',
            'book_name',
            'author',
            'number_of_copies',
            'publication_date',
            'library_catalogue_id',
            'genre_id',
            'genre',
            'format_id',
            'format'
        ))
        return Response(data=books, status=status.HTTP_200_OK)


class BookDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Article Views
class ArticleCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                library_catalogue = LibraryCatalogue(title=request.data['title'],
                                                     publication_date=request.data['publication_date'],
                                                     current_condition=request.data['current_condition'],
                                                     resource_type_id=request.data['resource_type_id'])
                library_catalogue.save()

                # Create article based on catalogue
                article = Article(author=request.data['author'], publication_date=request.data['publication_date'],
                                  content=request.data['content'], url=request.data['url'],
                                  library_catalogue_id=library_catalogue.library_catalogue_id)
                article.save()
                data = Article.objects.filter(pk=article.pk).values()

                # Commit the changes
                transaction.savepoint_commit(sid)
                return Response(data[0], status=status.HTTP_201_CREATED)

            except Exception as e:
                transaction.savepoint_rollback(sid)
                data = {"code": status.HTTP_400_BAD_REQUEST, "message": "Failed to create Article"}
                return JsonResponse(data, safe=False)


class ArticleListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        articles = list(Article.objects.annotate(
            genre_id=F('library_catalogue__genre__genre_id'),
            genre=F('library_catalogue__genre__genre'),
            format_id=F('library_catalogue__format__format_id'),
            format=F('library_catalogue__format__format'),
        ).values(
            'article_id',
            'author',
            'publication_date',
            'content',
            'library_catalogue_id',
            'url',
            'genre_id',
            'genre',
            'format_id',
            'format'
        ))
        return Response(data=articles, status=status.HTTP_200_OK)


class ArticleDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


# Newspaper Views
class NewspaperCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Newspaper.objects.all()
    serializer_class = NewspaperSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                library_catalogue = LibraryCatalogue(title=request.data['title'],
                                                     publication_date=request.data['publication_date'],
                                                     current_condition=request.data['current_condition'],
                                                     resource_type_id=request.data['resource_type_id'])
                library_catalogue.save()

                # Create newspaper based on catalogue
                newspaper = Newspaper(url=request.data['url'], content=request.data['content'],
                                      publication_date=request.data['publication_date'], source=request.data['source'],
                                      library_catalogue_id=library_catalogue.library_catalogue_id)
                newspaper.save()
                data = Newspaper.objects.filter(pk=newspaper.pk).values()

                # Commit the changes
                transaction.savepoint_commit(sid)
                return Response(data[0], status=status.HTTP_201_CREATED)

            except Exception as e:
                transaction.savepoint_rollback(sid)
                data = {"code": status.HTTP_400_BAD_REQUEST, "message": "Failed to create Newspaper"}
                return JsonResponse(data, safe=False)


class NewspaperListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Newspaper.objects.all()
    serializer_class = NewspaperSerializer

    def get(self, request, *args, **kwargs):
        newspapers = list(Newspaper.objects.annotate(
            genre_id=F('library_catalogue__genre__genre_id'),
            genre=F('library_catalogue__genre__genre'),
            format_id=F('library_catalogue__format__format_id'),
            format=F('library_catalogue__format__format'),
        ).values(
            'newspaper_id',
            'publication_date',
            'source',
            'url',
            'content',
            'library_catalogue_id',
            'genre_id',
            'genre',
            'format_id',
            'format'
        ))
        return Response(data=newspapers, status=status.HTTP_200_OK)


class NewspaperDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Newspaper.objects.all()
    serializer_class = NewspaperSerializer


class NewspaperUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Newspaper.objects.all()
    serializer_class = NewspaperSerializer


class NewspaperDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Newspaper.objects.all()
    serializer_class = NewspaperSerializer


# Library Catalogue Views
class LibraryCatalogueCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LibraryCatalogue.objects.all()
    serializer_class = LibraryCatalogueSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LibraryCatalogueListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LibraryCatalogue.objects.all()
    serializer_class = LibraryCatalogueSerializer


class LibraryCatalogueDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LibraryCatalogue.objects.all()
    serializer_class = LibraryCatalogueSerializer


class LibraryCatalogueUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LibraryCatalogue.objects.all()
    serializer_class = LibraryCatalogueSerializer


class LibraryCatalogueDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LibraryCatalogue.objects.all()
    serializer_class = LibraryCatalogueSerializer


# Resource Type Views
class ResourceTypeCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ResourceTypeListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer


class ResourceTypeDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer


class ResourceTypeUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer


class ResourceTypeDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer


# Membership Views
class MembershipCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MembershipListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class MembershipDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class MembershipUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class MembershipDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


# Membership Status Views
class MembershipStatusCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MembershipStatus.objects.all()
    serializer_class = MembershipStatusSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MembershipStatusListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MembershipStatus.objects.all()
    serializer_class = MembershipStatusSerializer


class MembershipStatusDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MembershipStatus.objects.all()
    serializer_class = MembershipStatusSerializer


class MembershipStatusUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MembershipStatus.objects.all()
    serializer_class = MembershipStatusSerializer


class GetMembershipsPerStatusView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        role_id = kwargs['role_id']
        membership_status_id = kwargs['membership_status_id']

        # Check if role is admin
        role = Role.objects.get(pk=role_id)
        if role.role_name == "Admin":
            memberships = list(Membership.objects.filter(membership_status_id=membership_status_id).annotate(
                first_name=F('user__user__first_name'),
                last_name=F('user__user__last_name'),
                middle_name=F('user__middle_name'),
                membership_status_name=F('membership_status__membership_status_name'),
            ).values(
                'membership_id',
                'user_id',
                'date_enrolled',
                'membership_status_id',
                'membership_status_name',
                'first_name',
                'last_name',
                'middle_name'
            ))
            return Response(memberships, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class ChangeMembershipStatusView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        role_id = request.data['role_id']
        membership_id = request.data['membership_id']
        membership_status_id = request.data['membership_status_id']

        # Check if role is admin
        role = Role.objects.get(pk=role_id)
        if role.role_name == "Admin":
            membership = Membership.objects.get(pk=membership_id)
            membership.membership_status_id = membership_status_id
            membership.save()
            data = {"message": f"Successfully updated {membership.membership_status.membership_status_name} membership"}
            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class MembershipStatusDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MembershipStatus.objects.all()
    serializer_class = MembershipStatusSerializer


# Lending Behaviour Views
class LendingBehaviourCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LendingBehaviour.objects.all()
    serializer_class = LendingBehaviourSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LendingBehaviourListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LendingBehaviour.objects.all()
    serializer_class = LendingBehaviourSerializer


class LendingBehaviourDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LendingBehaviour.objects.all()
    serializer_class = LendingBehaviourSerializer


class LendingBehaviourUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LendingBehaviour.objects.all()
    serializer_class = LendingBehaviourSerializer


class LendingBehaviourDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LendingBehaviour.objects.all()
    serializer_class = LendingBehaviourSerializer


# Lending Preference Views
class LendingPreferenceCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LendingPreference.objects.all()
    serializer_class = LendingPreferenceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LendingPreferenceListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LendingPreference.objects.all()
    serializer_class = LendingPreferenceSerializer


class LendingPreferenceDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LendingPreference.objects.all()
    serializer_class = LendingPreferenceSerializer


class LendingPreferenceUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LendingPreference.objects.all()
    serializer_class = LendingPreferenceSerializer


class LendingPreferenceDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LendingPreference.objects.all()
    serializer_class = LendingPreferenceSerializer


# Member Lending Preference Views
class MemberLendingPreferenceCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MemberLendingPreference.objects.all()
    serializer_class = MemberLendingPreferenceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MemberLendingPreferenceListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MemberLendingPreference.objects.all()
    serializer_class = MemberLendingPreferenceSerializer


class MemberLendingPreferenceDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MemberLendingPreference.objects.all()
    serializer_class = MemberLendingPreferenceSerializer


class MemberLendingPreferenceUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MemberLendingPreference.objects.all()
    serializer_class = MemberLendingPreferenceSerializer


class MemberLendingPreferenceDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MemberLendingPreference.objects.all()
    serializer_class = MemberLendingPreferenceSerializer


# Member Lending Behaviour Views
class MemberLendingBehaviourCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MemberLendingBehaviour.objects.all()
    serializer_class = MemberLendingBehaviourSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MemberLendingBehaviourListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MemberLendingBehaviour.objects.all()
    serializer_class = MemberLendingBehaviourSerializer


class MemberLendingBehaviourDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MemberLendingBehaviour.objects.all()
    serializer_class = MemberLendingBehaviourSerializer


class MemberLendingBehaviourUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MemberLendingBehaviour.objects.all()
    serializer_class = MemberLendingBehaviourSerializer


class MemberLendingBehaviourDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = MemberLendingBehaviour.objects.all()
    serializer_class = MemberLendingBehaviourSerializer


# Borrowing State Views
class BorrowingStateCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = BorrowingState.objects.all()
    serializer_class = BorrowingStateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BorrowingStateListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = BorrowingState.objects.all()
    serializer_class = BorrowingStateSerializer


class BorrowingStateDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = BorrowingState.objects.all()
    serializer_class = BorrowingStateSerializer


class BorrowingStateUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = BorrowingState.objects.all()
    serializer_class = BorrowingStateSerializer


class BorrowingStateDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = BorrowingState.objects.all()
    serializer_class = BorrowingStateSerializer


# User Catalogue Views
class UserCatalogueCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = UserCatalogue.objects.all()
    serializer_class = UserCatalogueSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                # Check if membership is active
                membership = Membership.objects.get(pk=request.data["membership_id"])
                if membership.membership_status_id == 1:  # Active
                    # Check for resource type
                    catalogue = LibraryCatalogue.objects.get(pk=request.data["library_catalogue_id"])
                    resource_type_name = catalogue.resource_type.resource_type_name
                    duration = request.data["duration_in_days"]
                    if resource_type_name == "Newspaper":
                        if request.data["duration_in_days"] > 1:
                            data = {"code": status.HTTP_400_BAD_REQUEST, "message": "Failed. Newspaper is only "
                                                                                    "allowed for a maximum of 1 Day"}
                            return JsonResponse(data, safe=False)

                    elif resource_type_name == "Book":
                        book = Book.objects.get(library_catalogue_id=request.data["library_catalogue_id"])
                        if book.number_of_copies < 1:
                            data = {"code": status.HTTP_400_BAD_REQUEST,
                                    "message": "Failed. This book is not available"}
                            return JsonResponse(data, safe=False)

                        elif book.number_of_copies > 10:
                            data = {"code": status.HTTP_400_BAD_REQUEST,
                                    "message": "Failed. Book is only allowed for a maximum of 10 days"}
                            return JsonResponse(data, safe=False)

                        else:
                            if book.library_catalogue.genre.genre == "Non-Fiction":
                                # Borrow for 5 days only
                                duration = 5

                        # Update copies
                        book.number_of_copies = -1
                        book.save()

                    user_catalogue = UserCatalogue(user_id=request.data["user_id"],
                                                   library_catalogue_id=request.data["library_catalogue_id"],
                                                   borrow_state_id=request.data["borrow_state"],
                                                   duration_in_days=duration,
                                                   lending_status_id=request.data["lending_status_id"])
                    user_catalogue.save()

                    data = {
                        "catalogue_id": user_catalogue.user_catalogue_id,
                        "membership_id": request.data["membership_id"],
                        "date_lent": user_catalogue.date_lent,
                        "date_returned": user_catalogue.date_returned,
                        "duration_in_days": user_catalogue.duration_in_days,
                        "transaction": user_catalogue.transaction,
                        "user": {"user_id": user_catalogue.user.user_id,
                                 "first_name": user_catalogue.user.user.first_name,
                                 "last_name": user_catalogue.user.user.last_name},
                        "borrowing_state": {"borrow_state_id": user_catalogue.borrow_state.borrowing_state_id,
                                            "borrow_state": user_catalogue.borrow_state.borrowing_state},
                        "lending_status": {"lending_status_id": user_catalogue.lending_status.lending_status_id,
                                           "lending_status": user_catalogue.lending_status.lending_status},
                    }

                    # Record lending behaviour
                    # Get member ID
                    membership = Membership.objects.get(user_id=request.data["user_id"])
                    self.record_lending_preferences(user_catalogue.library_catalogue.genre.genre,
                                                    request.data["user_id"],
                                                    membership.membership_id)

                    # Commit the changes
                    transaction.savepoint_commit(sid)
                    return JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)

                else:
                    data = {"code": status.HTTP_403_FORBIDDEN,
                            "message": f"Failed. Your membership is {membership.membership_status.membership_status_name}"}
                    return JsonResponse(data, safe=False)

            except Exception as e:
                transaction.savepoint_rollback(sid)
                data = {"code": status.HTTP_400_BAD_REQUEST, "message": "Failed to create Article"}
                return JsonResponse(data, safe=False)

    @staticmethod
    def record_lending_preferences(genre, user_id, membership_id):
        try:
            # Getting lending preference
            lending_preference = (LendingPreference.objects.
                                  get(lending_preference=genre,
                                      memberlendingpreference__member_id=membership_id))
            lending_preference.occurrence = lending_preference.occurrence + 1
            lending_preference.save()

        # Preference does not exist
        except LendingPreference.DoesNotExist:
            preference = LendingPreference(lending_preference=genre, occurrence=1)
            preference.save()
            MemberLendingPreference(member_id=membership_id,
                                    lending_preference_id=preference.lending_preference_id).save()


class ReturnResourceView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            user_catalogue = UserCatalogue.objects.get(pk=request.data['user_catalogue_id'])

            # Check for overdue
            if self.is_overdue(user_catalogue):
                self.record_lending_behavior("Overdue", request.data['user_id'], request.data['membership_id'])

            user_catalogue.date_returned = datetime.now()
            user_catalogue.save()
            return Response({"message": "Successfully returned the resource"}, status=status.HTTP_200_OK)

        except Exception as e:
            data = {"code": status.HTTP_400_BAD_REQUEST, "message": "Failed to return the resource"}
            return JsonResponse(data, safe=False)

    # Checking for due date
    @staticmethod
    def is_overdue(user_catalogue):
        due_date = user_catalogue.date_lent + timedelta(days=user_catalogue.duration_in_days)
        return timezone.now() > due_date

    @staticmethod
    def record_lending_behavior(behaviour, user_id, membership_id):
        try:
            # Getting lending behaviour
            lending_behavior = (LendingBehaviour.objects.
                                get(lending_behaviour=behaviour,
                                    memberlendingbehaviour__member__membership_id=membership_id))
            lending_behavior.occurrence = lending_behavior.occurrence + 1
            lending_behavior.save()

        # Behaviour does not exist
        except LendingBehaviour.DoesNotExist:
            lending_behaviour = LendingBehaviour(lending_behaviour=behaviour, occurrence=1)
            lending_behaviour.save()
            MemberLendingBehaviour(member_id=membership_id,
                                   lending_behaviour_id=lending_behaviour.lending_behaviour_id).save()

# Get all uncompleted library resources
class GetReturnedResourcesView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        user_catalogue = list(UserCatalogue.objects.filter(transaction__isnull=True, date_returned__isnull=False).values())
        return Response(user_catalogue, status=status.HTTP_200_OK)


class CloseLendingActivityView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        # Get return state
        return_state = BorrowingState.objects.get(pk=request.data['return_state_id'])

        user_catalogue = UserCatalogue.objects.get(pk=request.data['user_catalogue_id'])
        user_catalogue.return_state = return_state
        user_catalogue.transaction = "Completed"
        user_catalogue.save()

        # Check for Book resource
        catalogue = LibraryCatalogue.objects.get(pk=request.data['library_catalogue_id'])
        if catalogue.resource_type.resource_type_name == "Book":
            # Update copies
            book = Book.objects.get(library_catalogue_id=request.data['library_catalogue_id'])
            book.number_of_copies = book.number_of_copies + 1
            book.save()

        return Response({"message": "Successfully closed the lending activity"}, status=status.HTTP_200_OK)


class GetPreferencesBehaviourView(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        users = list(User.objects.filter(role__role_name="Member").annotate(
            first_name=F('user__first_name'),
            last_name=F('user__last_name'),
            email=F('user__email')
        ).values(
            'user_id',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'postal_address',
            'physical_address',
            'role_id'
        ))
        data = users
        for user in data:
            membership_id = Membership.objects.get(user_id=user['user_id']).membership_id
            # get preferences and behaviours
            preferences = list(LendingPreference.objects.filter(memberlendingpreference__member_id=membership_id).values())
            behaviours = list(LendingBehaviour.objects.filter(memberlendingbehaviour__member_id=membership_id).values())
            user['preferences'] = preferences
            user['behaviours'] = behaviours

        return Response(data, status=status.HTTP_200_OK)


class GetUserPreferencesBehaviourView(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        user = list(User.objects.filter(user_id=user_id, role__role_name="Member").annotate(
            first_name=F('user__first_name'),
            last_name=F('user__last_name'),
            email=F('user__email')
        ).values(
            'user_id',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'postal_address',
            'physical_address',
            'role_id'
        ))
        membership_id = Membership.objects.get(user_id=user_id).membership_id
        # get preferences and behaviours
        preferences = list(LendingPreference.objects.filter(memberlendingpreference__member_id=membership_id).values())
        behaviours = list(LendingBehaviour.objects.filter(memberlendingbehaviour__member_id=membership_id).values())
        user[0]['preferences'] = preferences
        user[0]['behaviours'] = behaviours

        return Response(user[0], status=status.HTTP_200_OK)


class UserCatalogueListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = UserCatalogue.objects.all()
    serializer_class = UserCatalogueSerializer


class UserCatalogueDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = UserCatalogue.objects.all()
    serializer_class = UserCatalogueSerializer


class UserCatalogueUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = UserCatalogue.objects.all()
    serializer_class = UserCatalogueSerializer


class UserCatalogueDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = UserCatalogue.objects.all()
    serializer_class = UserCatalogueSerializer


class ChangeUserCatalogueStatusView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            user_catalogue = UserCatalogue.objects.get(pk=request.data['user_catalogue_id'])
            user_catalogue.lending_status_id = request.data['lending_status_id']
            user_catalogue.save()

            return Response({"message": "Successfully updated status"}, status=status.HTTP_200_OK)

        except Exception as e:
            data = {"code": status.HTTP_400_BAD_REQUEST, "message": "Failed to change status"}
            return JsonResponse(data, safe=False)


class GetUserCataloguesPerStatusView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        lending_status_id = kwargs['lending_status_id']
        catalogues = list(UserCatalogue.objects.filter(lending_status__lending_status_id=lending_status_id).values())
        return JsonResponse(catalogues, safe=False)


class GetCataloguePerUserView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        try:
            data = []
            user_catalogues = list(UserCatalogue.objects.filter(user_id=user_id).values())
            for user_catalogue in user_catalogues:
                catalogue = UserCatalogue.objects.get(pk=user_catalogue['user_catalogue_id'])

                # Get the resource
                resource_type_name = catalogue.library_catalogue.resource_type.resource_type_name
                resource = None
                if resource_type_name == "Book":
                    resource = list(Book.objects.filter(
                        library_catalogue_id=catalogue.library_catalogue.library_catalogue_id).values())

                elif resource_type_name == "Article":
                    resource = list(Article.objects.filter(
                        library_catalogue_id=catalogue.library_catalogue.library_catalogue_id).values())

                elif resource_type_name == "Newspaper":
                    resource = list(Newspaper.objects.filter(
                        library_catalogue_id=catalogue.library_catalogue.library_catalogue_id).values())

                data.append({
                    "catalogue_id": catalogue.user_catalogue_id,
                    "date_lent": catalogue.date_lent,
                    "date_returned": catalogue.date_returned,
                    "duration_in_days": catalogue.duration_in_days,
                    "transaction": catalogue.transaction,
                    "user": {"user_id": catalogue.user.user_id,
                             "first_name": catalogue.user.user.first_name,
                             "last_name": catalogue.user.user.last_name},
                    "borrowing_state": {"borrow_state_id": catalogue.borrow_state.borrowing_state_id,
                                        "borrow_state": catalogue.borrow_state.borrowing_state},
                    "lending_status": {"lending_status_id": catalogue.lending_status.lending_status_id,
                                       "lending_status": catalogue.lending_status.lending_status},
                    "resource": resource[0]
                })

            return JsonResponse(data, safe=False)

        except Exception as e:
            data = {"code": status.HTTP_400_BAD_REQUEST, "message": "Failed to get catalogues"}
            return JsonResponse(data, safe=False)


# Reports views
# Total No of resources per category
class GetResourcesPerCategoryView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        resource_types = list(ResourceType.objects.values())
        for resource_type in resource_types:
            resource_type['count'] = len(LibraryCatalogue.objects.filter(resource_type_id=resource_type['resource_type_id']))
        return Response(resource_types, status=status.HTTP_200_OK)


# Total No of resources added on the current month
class GetResourcesPerMonthView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        # Current month
        current_month = timezone.now().month

        resource_types = list(ResourceType.objects.values())
        for resource_type in resource_types:
            resource_type['count'] = len(LibraryCatalogue.objects.filter(resource_type_id=resource_type['resource_type_id'],  date_added__month=current_month))
        return Response(resource_types, status=status.HTTP_200_OK)


# Total No of enrolled members
class GetEnrolledMembersView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        members = list(Membership.objects.filter().annotate(
            membership_status_name=F('membership_status__membership_status_name'),
            first_name=F('user__user__first_name'),
            last_name=F('user__user__last_name'),
            middle_name=F('user__middle_name'),
            email=F('user__user__email')
        ).values(
            'membership_id',
            'membership_status_id',
            'user_id',
            'membership_status_name',
            'first_name',
            'last_name',
            'middle_name',
            'email'
        ))
        data = [{"total_members": len(members)}]
        data[0]['members'] = members
        return Response(data, status=status.HTTP_200_OK)


# Total No of resources borrowed
class GetBorrowedResourcesView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        # Current month
        current_month = timezone.now().month

        resources = list(UserCatalogue.objects.filter(date_lent__month=current_month).values())
        data = [{"total_borrowed_library_resources": len(resources)}]
        data[0]['library_resources'] = resources
        return Response(data, status=status.HTTP_200_OK)
