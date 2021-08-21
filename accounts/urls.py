from django.urls import path
from .views import (signup_view, login_view, logout_view,
 account_view, update_view, deactivate_view, delete_view, account_view,
 post_upvote, post_downvote, account_bookmark_add)

app_name = 'accounts'

urlpatterns = [
    path('accounts/signup/', signup_view, name='accounts_signup'),
    path('accounts/login/', login_view, name='accounts_login'),
    path('accounts/logout/', logout_view, name='accounts_logout'),
    path('accounts/view/', account_view, name='accounts_view'),
    path('accounts/edit/', update_view, name='accounts_update'),
    path('accounts/deactivate/', deactivate_view, name='accounts_deactivate'),
    path('accounts/delete/', delete_view, name='accounts_delete'),
    path('accounts/upvote/<id>/', post_upvote, name='post_upvote'),
    path('accounts/downvote/<id>/', post_downvote, name='post_downvote'),
    path('accounts/bookmark/<id>/', account_bookmark_add, name='account_bookmark_add'),

]
