from django.urls import path
from website import views

urlpatterns = [
    # GET
    path('', views.homepage, name="homepage"),
    path('board/<str:name>', views.board, name="get-board"),
    path('board/<str:name>/<str:owner>', views.board, name="get-other-board"),
    path('register', views.register_request, name="register"),
    path('login', views.login_request, name="login"),
    path('profile', views.profile, name="profile"),
    path('logout', views.logout_request, name="logout"),

    path('notification/<int:notification_pk>/board/<str:board_name>', views.BoardNotification.as_view(),
         name='board-notification'),
    path('notification/<int:notification_pk>/card/<int:card_id>', views.CardNotification.as_view(),
         name='card-notification'),

    path('join-board/<str:name>/<str:owner>', views.JoinBoard.as_view(), name='join-board'),

    # POST
    path('create_board', views.create_board, name='make-board'),
    path('delete_board', views.delete_board, name='delete-board'),
    path('edit_board', views.edit_board, name="edit-board"),

    path('create_board_content', views.create_board_content, name='create-board-content'),
    path('delete_board_content', views.delete_board_content, name='delete-board-content'),
    path('edit_board_content', views.edit_board_content, name='edit-board-content'),
    path('move_cards', views.move_cards, name='move-cards'),

    path('create_category', views.create_category, name='create-category'),
    path('delete_category', views.delete_category, name='delete-category'),
    path('rename_category', views.rename_category, name='rename-category'),

    path('edit_password', views.change_password, name='edit-password'),
    path('manage_board_user', views.ManageBoardUser.as_view(), name="manage-board-user"),
    path('manage_card_assignee', views.ManageCardAssignee.as_view(), name="manage-card-assignee")
]
