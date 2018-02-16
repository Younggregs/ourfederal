from django.conf.urls import url

from . import views
app_name = 'federal'

urlpatterns = [
    #thefederal/
    url(r'^$',views.HomeView.as_view(), name = 'home'),

    #thefederal/index
    url(r'^index/$',views.index, name = 'index'),

    #thefederal/sign_up
    url(r'^sign_up/$',views.SignupView.as_view() , name='signup'),

    #thefederal/sign_in
    url(r'^sign_in/$',views.SigninView.as_view() , name='signin'),

    #thefederal/signout
    url(r'logout/', views.logout, name='logout'),

    #thefederal/pk/comment
    url(r'^(?P<context_id>[0-9]+)/comment/$', views.CommentView.as_view(), name='comment'),

    #thefederal/pk/reply
    url(r'^(?P<context_id>[0-9]+)/reply/$', views.ReplyView.as_view(), name='reply'),

    #thefederal/ajax/validate_username
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),

    #thefederal/ajax/threadfavorited
    url(r'^ajax/t_favorited/$', views.t_favorited, name='t_favorited'),

    #thefederal/ajax/threadunfavorited
    url(r'^ajax/t_unfavorited/$', views.t_unfavorited, name='t_unfavorited'),

    #thefederal/ajax/commentfavorited
    url(r'^ajax/c_favorited/$', views.c_favorited, name='c_favorited'),

    #thefederal/ajax/commentunfavorited
    url(r'^ajax/c_unfavorited/$', views.c_unfavorited, name='c_unfavorited'),

    #thefederal/ajax/replyfavorited
    url(r'^ajax/r_favorited/$', views.r_favorited, name='r_favorited'),

    #thefederal/ajax/replyunfavorited
    url(r'^ajax/r_unfavorited/$', views.r_unfavorited, name='r_unfavorited'),

    #thefederal/favorites
    url(r'^favorites/$', views.favorites, name='favorites'),

    #thefederal/threadfavorite
    url(r'^threadfavorite/$', views.ThreadfavoriteView.as_view(), name='threadfavorite'),

    #thefederal/commentfavorite
    url(r'^commentfavorite/$', views.CommentfavoriteView.as_view(), name='commentfavorite'),

    #thefederal/replyfavorite
    url(r'^replyfavorite/$', views.ReplyfavoriteView.as_view(), name='replyfavorite'),

    #thefederal/profile
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),

    #thefederal/feedback
    url(r'^feedback/$', views.FeedbackView.as_view(), name='feedback'),

    #thefederal/about
    url(r'^about/$', views.about, name='about'),

    #thefederal/terms
    url(r'^terms/$', views.terms, name='terms'),

    #thefederal/respect_policy
    url(r'^respect_policy/$', views.respect_policy, name='respect_policy'),

    #thefederal/content_policy
    url(r'^content_policy/$', views.content_policy, name='content_policy'),

    #thefederal/forgot_password
    url(r'^forgotpassword/$', views.ForgotPasswordView.as_view(), name='forgotpassword'),




]
