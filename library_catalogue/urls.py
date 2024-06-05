from django.urls import path
from . import views

urlpatterns = [
    path('', views.LibraryCatalogueListView.as_view(), name='index'),
    path('library_catalogue/add', views.LibraryCatalogueCreateView.as_view()),
    path('library_catalogue/update', views.LibraryCatalogueUpdateView.as_view()),
    path('library_catalogue', views.LibraryCatalogueListView.as_view()),
    path('library_catalogue/<int:pk>/', views.LibraryCatalogueDetailView.as_view()),
    path('resource_type/add', views.ResourceTypeCreateView.as_view()),
    path('resource_type/update', views.ResourceTypeUpdateView.as_view()),
    path('resource_type', views.ResourceTypeListView.as_view()),
    path('resource_type/<int:pk>/', views.ResourceTypeDetailView.as_view()),
    path('book/add', views.BookCreateView.as_view()),
    path('book/update', views.BookUpdateView.as_view()),
    path('book', views.BookListView.as_view()),
    path('book/<str:pk>/', views.BookDetailView.as_view()),
    path('article/add', views.ArticleCreateView.as_view()),
    path('article/update', views.ArticleUpdateView.as_view()),
    path('article', views.ArticleListView.as_view()),
    path('article/<int:pk>/', views.ArticleDetailView.as_view()),
    path('newspaper/add', views.NewspaperCreateView.as_view()),
    path('newspaper/update', views.NewspaperUpdateView.as_view()),
    path('newspaper', views.NewspaperListView.as_view()),
    path('newspaper/<int:pk>/', views.NewspaperDetailView.as_view()),
    path('membership/add', views.MembershipCreateView.as_view()),
    path('membership/update', views.MembershipUpdateView.as_view()),
    path('membership', views.MembershipListView.as_view()),
    path('membership/<int:pk>/', views.MembershipDetailView.as_view()),
    path('membership_status/add', views.MembershipCreateView.as_view()),
    path('membership_status/update', views.MembershipUpdateView.as_view()),
    path('membership_status', views.MembershipListView.as_view()),
    path('membership_status/<int:pk>/', views.MembershipDetailView.as_view()),
    path('membership_status/pending/<int:role_id>/<int:membership_status_id>/', views.GetMembershipsPerStatusView.as_view()),
    path('membership_status/change_status', views.ChangeMembershipStatusView.as_view()),
    path('lending_behaviour/add', views.LendingBehaviourCreateView.as_view()),
    path('lending_behaviour/update', views.LendingBehaviourUpdateView.as_view()),
    path('lending_behaviour', views.LendingBehaviourListView.as_view()),
    path('lending_behaviour/<int:pk>/', views.LendingBehaviourDetailView.as_view()),
    path('lending_preference/add', views.LendingPreferenceCreateView.as_view()),
    path('lending_preference/update', views.LendingPreferenceUpdateView.as_view()),
    path('lending_preference', views.LendingPreferenceListView.as_view()),
    path('lending_preference/<int:pk>/', views.LendingPreferenceDetailView.as_view()),
    path('member_lending_preference/add', views.MemberLendingPreferenceCreateView.as_view()),
    path('member_lending_preference/update', views.MemberLendingPreferenceUpdateView.as_view()),
    path('member_lending_preference', views.MemberLendingPreferenceListView.as_view()),
    path('member_lending_preference/<int:pk>/', views.MemberLendingPreferenceDetailView.as_view()),
    path('member_lending_behaviour/add', views.MemberLendingBehaviourCreateView.as_view()),
    path('member_lending_behaviour/update', views.MemberLendingBehaviourUpdateView.as_view()),
    path('member_lending_behaviour', views.MemberLendingBehaviourListView.as_view()),
    path('member_lending_behaviour/<int:pk>/', views.MemberLendingBehaviourDetailView.as_view()),
    path('borrowing_state/add', views.BorrowingStateCreateView.as_view()),
    path('borrowing_state/update', views.BorrowingStateUpdateView.as_view()),
    path('borrowing_state', views.BorrowingStateListView.as_view()),
    path('borrowing_state/<int:pk>/', views.BorrowingStateDetailView.as_view()),
    path('user_catalogue/add', views.UserCatalogueCreateView.as_view()),
    path('user_catalogue/update', views.UserCatalogueUpdateView.as_view()),
    path('user_catalogue', views.UserCatalogueListView.as_view()),
    path('user_catalogue/<int:pk>/', views.UserCatalogueDetailView.as_view()),
    path('user_catalogue/user_catalogue/<int:user_id>/', views.GetCataloguePerUserView.as_view()),
    path('user_catalogue/change_catalogue_status', views.ChangeUserCatalogueStatusView.as_view()),
    path('user_catalogue/catalogue_status/<int:lending_status_id>/', views.GetUserCataloguesPerStatusView.as_view()),
    path('user_catalogue/return_resource', views.ReturnResourceView.as_view()),
    path('user_catalogue/returned_resources', views.GetReturnedResourcesView.as_view()),
    path('user_catalogue/close_lending_activity', views.CloseLendingActivityView.as_view()),
    path('user_catalogue/preferences_behaviour', views.GetPreferencesBehaviourView.as_view()),
    path('user_catalogue/user_preferences_behaviour/<int:user_id>/', views.GetUserPreferencesBehaviourView.as_view()),
    path('reports/library_resources_categories', views.GetResourcesPerCategoryView.as_view()),
    path('reports/library_resources_month', views.GetResourcesPerMonthView.as_view()),
    path('reports/enrolled_members', views.GetEnrolledMembersView.as_view()),
    path('reports/borrowed_resources', views.GetBorrowedResourcesView.as_view()),
]
