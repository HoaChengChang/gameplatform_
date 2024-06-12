from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'gameApp'
urlpatterns = [
    #首頁
    path("", views.Index.as_view(), name = "game_list"),
    #個別遊戲
    path("game/<int:id>", views.GameDetail.as_view(), name = "game_detail"),
    #聯繫平台的網頁
    path("contactus/", views.ContactUs.as_view(), name = "contact"),
    #介紹遊戲的頁面
    path("games/", views.Games.as_view(), name = "games"),
    #該種類的所有遊戲
    path("trendsgame/", views.TrendsGame.as_view(), name = "trendsgame"),
    #登入
    path("signin/", views.Signin.as_view(), name = "signin"),
    #註冊
    path("register/", views.Register.as_view(), name = "register"),
    #評論區
    path("commentarea/", views.CommentSite.as_view(), name = "commentarea"),
    #評論區點讚功能
    path("commentarea/<int:comment_id>", views.CommentAreaLike.as_view(), name = "commentarea_like"),
    #評論各別留言的點讚功能
    path("commentarea/<int:comment_id>/<int:pk>/", views.CommentAreaReviewLike.as_view(), name = "commentarea_review_like"),
    #個別遊戲留言的點讚功能
    path("like/<int:comment_id>/<int:game_id>/", views.CommentLike.as_view(), name = "comment_like"),
    #針對留言的評論
    path("commentarea/<int:pk>/", views.CommentReview.as_view(), name = "comment_review"),
    #使用者資訊頁面
    path("user/", views.UserSpace.as_view(), name="user"),
    #信件認證功能
    path("emailverify/", views.EmailVerify.as_view(), name="emailverify"),
]

# if settings.DEBUG is False:  不要開 不使用這個的話會抓不到media路徑!!
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
