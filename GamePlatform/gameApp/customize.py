from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from uuid import uuid4
import os

# 用戶上傳頭像重命名
def icon_rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('media/icon', filename)

# 用於個別遊戲頁留言功能登入重定向以及保留已輸入信息
def save_message_to_session(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated and request.method == 'POST':
            request.session['saved_message'] = request.POST.get('Message')
            request.session['saved_score'] = request.POST.get('score')
            return redirect(f"{reverse('gameApp:signin')}?next={request.path}")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

