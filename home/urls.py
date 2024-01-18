from django.utils.decorators import method_decorator
from django.urls import path
from home.views import SignUpView, IndexView, LoginView, PostView, LogoutView, DetailView,EditsView ,DeletesView

urlpatterns = [
    path('', IndexView.as_view(), name="homepage"),
    path('signup', SignUpView.as_view(), name="signup"),
    path('log_in', LoginView.as_view(), name="log_in"),
    path('log_out', LogoutView.as_view(), name="log_out"),
    path('posts', PostView.as_view(), name="posts"),
    # path('select', Select.as_view(), name="select"),
    # path('sort', Sort.as_view(), name="sort"),
    
    path('details', DetailView.as_view(), name="details"),
    path('<int:id>/delete', DeletesView.as_view(), name='delete'),
    path('<int:id>/edit', EditsView.as_view(), name='edit'),
    
]