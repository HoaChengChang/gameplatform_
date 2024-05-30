from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'gameApp'
urlpatterns = [
    path("game/", views.Index.as_view(), name = "game_list"),
    path("game/<int:id>", views.GameDetail.as_view(), name = "game_detail"),
    path("about/", views.AboutUs.as_view(), name = "about"),
    path("contact/", views.ContactUs.as_view(), name = "contact"),
    path("games/", views.Games.as_view(), name = "games"),
    path("trendsgame/", views.TrendsGame.as_view(), name = "trendsgame"),
    path("like/<int:commend_id>/<int:game_id>/", views.CommentLike.as_view(), name = "commentlike"),
    path("signin/", views.Signin.as_view(), name = "signin"),
    path("register/", views.Register.as_view(), name = "register"),
    path("commentarea/", views.CommentArea.as_view(), name = "commentarea"),
    path("user/", views.UserSpace.as_view(), name="user"),
    path("emailverify/", views.EmailVerify.as_view(), name="emailverify"),
]

# if settings.DEBUG is False:  不要開 不使用這個的話會抓不到media路徑!!
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)