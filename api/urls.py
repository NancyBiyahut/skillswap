from django.urls import path
from .views import *

urlpatterns = [
    path('create-user/', create_user, name='create_user'),
    path('login/', user_login, name='user_login'),
    path('create-learner/', create_learner, name='create_learner'),
    path('create-educator/', create_educator, name='create_educator'),
    path('make-session-request/', make_session_request, name='make_session_request'),
    path('educator-sessions/', get_educator_sessions, name='get_educator_sessions'),
    path('learner-sessions/', get_learner_sessions, name='get_learner_sessions'),
    path('update-session-status/<int:session_id>/', update_session_status, name='update_session_status'),
    path('delete-session/<int:session_id>/', delete_session, name='delete_session'),
    path('educator-sessions-and-reviews/<int:educator_id>/', list_educator_sessions_and_reviews, name='list_educator_sessions_and_reviews'),
    path('list-learners/', list_learners, name='list_learners'),
    path('list-educators/', list_educators, name='list_educators'),
    path('list-tags/' , list_tags , name = 'list-tags'),
    path('add-review/' , add_review , name='add_review'),
    path('scheduled-sessions/' , scheduled_sessions , name="schedules_session"),
    path('session-history/' , session_history , name='session-history'),
]