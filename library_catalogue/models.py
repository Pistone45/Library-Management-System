from django.db import models

from users.models import User


# Create your models here.


class ResourceType(models.Model):
    resource_type_id = models.AutoField(primary_key=True)
    resource_type_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'resource_type'
        managed = True

    def __str__(self):
        return f"{self.resource_type_id} - {self.resource_type_name}"


class Genres(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=255)

    class Meta:
        db_table = 'genres'
        managed = True

    def __str__(self):
        return f"{self.genre_id} - {self.genre}"


class Format(models.Model):
    format_id = models.AutoField(primary_key=True)
    format = models.CharField(max_length=255)

    class Meta:
        db_table = 'format'
        managed = True

    def __str__(self):
        return f"{self.format_id} - {self.format}"


class LibraryCatalogue(models.Model):
    library_catalogue_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    publication_date = models.DateTimeField()
    current_condition = models.CharField(max_length=255)
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE, null=True, blank=True)
    format = models.ForeignKey(Format, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'library_catalogue'
        managed = True

    def __str__(self):
        return f"{self.library_catalogue_id} - {self.title}"


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=255)
    publication_date = models.DateTimeField()
    content = models.TextField()
    url = models.TextField(null=True, blank=True)
    library_catalogue = models.ForeignKey(LibraryCatalogue, on_delete=models.CASCADE)

    class Meta:
        db_table = 'article'
        managed = True

    def __str__(self):
        return f"{self.article_id} - {self.author}"


class Newspaper(models.Model):
    newspaper_id = models.AutoField(primary_key=True)
    publication_date = models.DateTimeField()
    source = models.CharField(max_length=255)
    url = models.TextField()
    content = models.TextField(null=True, blank=True)
    library_catalogue = models.ForeignKey(LibraryCatalogue, on_delete=models.CASCADE)

    class Meta:
        db_table = 'newspaper'
        managed = True

    def __str__(self):
        return f"{self.newspaper_id} - {self.source}"


class Book(models.Model):
    isbn = models.CharField(primary_key=True, max_length=255)
    book_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    number_of_copies = models.IntegerField()
    publication_date = models.DateTimeField()
    library_catalogue = models.ForeignKey(LibraryCatalogue, on_delete=models.CASCADE)

    class Meta:
        db_table = 'book'
        managed = True

    def __str__(self):
        return f"{self.isbn} - {self.book_name}"


class MembershipStatus(models.Model):
    membership_status_id = models.AutoField(primary_key=True)
    membership_status_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'membership_status'
        managed = True

    def __str__(self):
        return f"{self.membership_status_id} - {self.membership_status_name}"


class LendingBehaviour(models.Model):
    lending_behaviour_id = models.AutoField(primary_key=True)
    lending_behaviour = models.CharField(max_length=255)
    occurrence = models.IntegerField()

    class Meta:
        db_table = 'lending_behaviour'
        managed = True

    def __str__(self):
        return f"{self.lending_behaviour} - {self.lending_behaviour}"


class LendingPreference(models.Model):
    lending_preference_id = models.AutoField(primary_key=True)
    lending_preference = models.CharField(max_length=255)
    occurrence = models.IntegerField()

    class Meta:
        db_table = 'lending_preferences'
        managed = True

    def __str__(self):
        return f"{self.lending_preference_id} - {self.lending_preference}"


class Membership(models.Model):
    membership_id = models.AutoField(primary_key=True)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    membership_status = models.ForeignKey(MembershipStatus, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'membership'
        managed = True

    def __str__(self):
        return f"{self.membership_id} - {self.user.user.username}"


class MemberLendingPreference(models.Model):
    member_lending_preference_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Membership, on_delete=models.CASCADE)
    lending_preference = models.ForeignKey(LendingPreference, on_delete=models.CASCADE)

    class Meta:
        db_table = 'member_lending_preferences'
        managed = True

    def __str__(self):
        return f"{self.member_lending_preference_id} - {self.member.membership_id} - {self.member.user.user.username}"


class MemberLendingBehaviour(models.Model):
    member_lending_behaviour_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Membership, on_delete=models.CASCADE)
    lending_behaviour = models.ForeignKey(LendingBehaviour, on_delete=models.CASCADE)

    class Meta:
        db_table = 'member_lending_behaviour'
        managed = True

    def __str__(self):
        return f"{self.member_lending_behaviour_id} - {self.member.membership_id} - {self.member.user.user.username}"


class BorrowingState(models.Model):
    borrowing_state_id = models.AutoField(primary_key=True)
    borrowing_state = models.CharField(max_length=255)

    class Meta:
        db_table = 'borrowing_states'
        managed = True

    def __str__(self):
        return f"{self.borrowing_state_id} - {self.borrowing_state}"


class LendingStatus(models.Model):
    lending_status_id = models.AutoField(primary_key=True)
    lending_status = models.CharField(max_length=255)

    class Meta:
        db_table = 'lending_status'
        managed = True

    def __str__(self):
        return f"{self.lending_status_id} - {self.lending_status}"


class UserCatalogue(models.Model):
    user_catalogue_id = models.AutoField(primary_key=True)
    date_lent = models.DateTimeField(auto_now_add=True)
    date_returned = models.DateTimeField(null=True, blank=True)
    return_state = models.ForeignKey(BorrowingState, on_delete=models.CASCADE, related_name='return_state',
                                     blank=True, null=True)
    borrow_state = models.ForeignKey(BorrowingState, on_delete=models.CASCADE, related_name='borrow_state',
                                     blank=True, null=True)
    duration_in_days = models.IntegerField()
    transaction = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    library_catalogue = models.ForeignKey(LibraryCatalogue, on_delete=models.CASCADE)
    lending_status = models.ForeignKey(LendingStatus, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'user_catalogue'
        managed = True

    def __str__(self):
        return f"{self.user_catalogue_id} - {self.user.user.username}"
