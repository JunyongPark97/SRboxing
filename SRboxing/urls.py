from django.contrib import admin
<<<<<<< HEAD
=======
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
>>>>>>> Add user management and API
from django.urls import path, include
from Sean_boxing import views as seanboxing_views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'anchor-boxing/box', seanboxing_views.BoxViewSet)
router.register(r'anchor-making/anchor', seanboxing_views.AnchorViewSet)
router.register(r'anchor-making', seanboxing_views.QBQViewSet)
router.register(r'anchor-frame/box', seanboxing_views.BoxViewSet)
<<<<<<< HEAD

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', seanboxing_views.index, name="main"),
    path('sean-boxing/source/<int:pk>/<int:pk2>', seanboxing_views.AnchorFrameView.as_view(), name='finalboxing-detail'),
    path('sean-boxing/qbq/<int:pk>', seanboxing_views.QBQDetailView.as_view(), name='qbqboxing-detail'),
    path('sean-boxing/frame/<int:pk>', seanboxing_views.FrameDetailView.as_view(), name='frameboxing-detail'),
=======
router.register(r'box', seanboxing_views.AnchorReadViewset),

# router.register(r'project-making/anchor', seanboxing_views.MakeProject)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(seanboxing_views.HomeView.as_view()), name="main"),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('manage/', seanboxing_views.ManageUserList.as_view(), name='manage'),
    path('manage/<int:pk>', seanboxing_views.ManageUserDetailView.as_view(), name='manage-detail'),
    path('search', seanboxing_views.search, name='search'),
    # path('box', seanboxing_views.TestView.as_view(), name='box'),

    path('sean-boxing/anchor/<int:pk>/<int:pk2>', seanboxing_views.make_anchor_valid, name='edit-anchor'),
    path('sean-boxing/project/anchor/<int:pk>/<int:pk2>', seanboxing_views.make_project_valid, name='edit-project'),
    path('sean-boxing/source/<int:pk>/<int:pk2>', seanboxing_views.AnchorFrameView.as_view(), name='finalboxing-detail'),
    path('sean-boxing/project/<int:pk>/<int:pk2>', seanboxing_views.ProjectView.as_view(), name='project-detail'),
    path('sean-boxing/qbq/<int:pk>', seanboxing_views.QBQDetailView.as_view(), name='qbqboxing-detail'),
    path('sean-boxing/frame/<int:pk>', seanboxing_views.FrameDetailView.as_view(), name='frameboxing-detail'),
    path('sean-boxing/project', seanboxing_views.project_anchor, name='make-project'),
>>>>>>> Add user management and API
    path('api/', include(router.urls)),
]
