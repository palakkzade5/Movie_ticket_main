from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ShowListView, BookingView, BookingHistoryView
from .admin_views import ShowListAdminView, ShowCreateView, ShowEditView, ShowDeleteView, BookingListAdminView
from django.urls import path

app_name = 'booking'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', ShowListView.as_view(), name='show_list'),
    path('booking/<int:show_id>/', BookingView.as_view(), name='booking'),
    path('booking/history/', BookingHistoryView.as_view(), name='booking_history'),

    # Admin URLs
    path('admin/shows/', ShowListAdminView.as_view(), name='admin_show_list'),
    path('admin/shows/create/', ShowCreateView.as_view(), name='admin_show_create'),
    path('admin/shows/edit/<int:show_id>/', ShowEditView.as_view(), name='admin_show_edit'),
    path('admin/shows/delete/<int:show_id>/', ShowDeleteView.as_view(), name='admin_show_delete'),
    path('admin/bookings/', BookingListAdminView.as_view(), name='admin_booking_list'),
]
