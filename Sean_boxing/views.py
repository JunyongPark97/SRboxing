<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .serializers import CandidateSerializer, BoxWriteSerializer, AnchorWriteSerializer, QBQSerializer
from .models import CandidateInfo, Anchor, Box, QBQ, Frame



def index(request):
    return render(request, 'Sean_boxing/index.html')


@method_decorator(login_required, name='dispatch')
class CandidateDetailView(DetailView):
    model = CandidateInfo


@method_decorator(login_required, name='dispatch')
class AnchorDetailView(DetailView):
    model = Anchor
=======
import django_filters
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, TemplateView, ListView
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Sean_boxing.filters import BoxFilter
from .serializers import CandidateSerializer, BoxWriteSerializer, AnchorWriteSerializer, QBQSerializer, \
    QBQReadSerializer, AnchorSerializer
from .models import CandidateInfo, Anchor, Box, QBQ, Frame, Project


class HomeView(TemplateView):
    """
    본인의 Home을 보여주는 클래스입니다.
    """
    template_name = 'Sean_boxing/index.html'
    permission_classes = (IsAuthenticated,)

    def get_context_data(self,**kwargs):
        context = super(HomeView, self).get_context_data()
        user=self.request.user
        box_counts = Box.objects.filter(work_user=user).count()
        anchor_counts = Project.objects.filter(assigned_user=user).count()
        project_first = Project.objects.filter(assigned_user=user).filter(valid=None).order_by('pk').first()
        if project_first:
            anchor_first = project_first.assigned_anchor
        else:
            anchor_first = None
        context['box_count'] = box_counts
        context['anchor_count'] = anchor_counts
        context['anchor'] = anchor_first
        context['valid_project'] = Project.objects.filter(assigned_user=user).filter(valid=True).count()
        return context


class ProjectView(TemplateView):
    template_name = 'Sean_boxing/project_detail.html'
    permission_classes = (IsAuthenticated,)

    def get_context_data(self, pk, pk2):
        if self.request.user.is_authenticated:
            context = super(ProjectView, self).get_context_data()
            anchor = Anchor.objects.get(id=pk)
            id_list=[]
            user = self.request.user
            frames_id = anchor.frame_from_anchor.values('id')
            project_list = Project.objects.filter(assigned_user=user)

            prev_project = project_list.filter(valid=None).filter(assigned_user=user).filter(assigned_anchor_id__lt=pk).order_by('pk').last()
            next_project = project_list.filter(valid=None).filter(assigned_user=user).filter(assigned_anchor_id__gt=pk).order_by('pk').first()

            if prev_project:
                prev_anchor = prev_project.assigned_anchor
            else:
                prev_anchor = None
            if next_project:
                next_anchor = next_project.assigned_anchor
            else:
                next_anchor = None

            frame = anchor.frame_from_anchor.get(id=pk2)
            """
            anchor를 변경했을 때 prev,next가 없는 anchor들을 필터링 합니다.
            """
            if prev_anchor:
                prev_frame = prev_anchor.frame_from_anchor.all().last()
            else:
                prev_frame = None

            if next_anchor:
                next_frame = next_anchor.frame_from_anchor.all().first()
            else:
                next_frame = None

            """
            한 anchor당 속해있는 frames를 제한하기 위한 id를 얻습니다.
            """
            for frame_id in frames_id:
                id_list.append(frame_id['id'])

            context['anchor'] = anchor
            context['frame_list'] = id_list
            context['frame'] = frame
            context['p_frame'] = prev_frame
            context['n_frame'] = next_frame
            context['box_count'] = anchor.frame_from_anchor.filter(box_from_frame__isnull=False).count()
            context['frame_count'] = id_list.index(pk2)+1
            context['total_frames'] = len(id_list)
            context['all_anchors'] = anchor.QBQ_source.anchor.all()
            context['first_frame'] = id_list[0]
            context['last_frame'] = id_list[-1]
            context['prev_anchor'] = prev_anchor
            context['next_anchor'] = next_anchor
            return context

#
# @method_decorator(login_required, name='dispatch')
# class CandidateDetailView(DetailView):
#     model = CandidateInfo
#
#
# @method_decorator(login_required, name='dispatch')
# class AnchorDetailView(DetailView):
#     model = Anchor
>>>>>>> Add user management and API


@method_decorator(login_required, name='dispatch')
class QBQDetailView(DetailView):
    model = QBQ


@method_decorator(login_required, name='dispatch')
class FrameDetailView(DetailView):
    model = Frame


class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxWriteSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        qdict = self.request.data
        qdict = qdict.dict()
        return {'request': self.request, 'frame': qdict['frame']}

<<<<<<< HEAD

=======
#사용안함
>>>>>>> Add user management and API
class CandidateViewSet(viewsets.ModelViewSet):
    queryset = CandidateInfo.objects.all()
    serializer_class = CandidateSerializer
    pagination_class = LimitOffsetPagination


class AnchorViewSet(viewsets.ModelViewSet):
    queryset = Anchor.objects.all()
    serializer_class = AnchorWriteSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_context(self):
        qdict = self.request.data
        qdict = qdict.dict()
        return {'request': self.request, 'qbq_source': qdict['source']}


class QBQViewSet(viewsets.ModelViewSet):
    queryset = QBQ.objects.all()
    serializer_class = QBQSerializer
    pagination_class = LimitOffsetPagination


class AnchorFrameView(TemplateView):
    template_name = 'Sean_boxing/anchor_detail.html'

    def get_context_data(self, pk, pk2):
<<<<<<< HEAD
=======
        global frame_next, frame_prev
>>>>>>> Add user management and API
        context = super(AnchorFrameView, self).get_context_data()
        anchor = Anchor.objects.get(id=pk)
        id_list=[]
        frames_id = anchor.frame_from_anchor.values('id')
        prev_anchor = anchor.prev
        next_anchor = anchor.next
<<<<<<< HEAD
=======
        frame = anchor.frame_from_anchor.get(id=pk2)
>>>>>>> Add user management and API
        """
        anchor를 변경했을 때 prev,next가 없는 anchor들을 필터링 합니다.
        """
        if prev_anchor:
            prev_frame = prev_anchor.frame_from_anchor.all().last()
        else:
            prev_frame = None

        if next_anchor:
            next_frame = next_anchor.frame_from_anchor.all().first()
        else:
            next_frame = None
<<<<<<< HEAD
=======

>>>>>>> Add user management and API
        """
        한 anchor당 속해있는 frames를 제한하기 위한 id를 얻습니다.
        """
        for frame_id in frames_id:
            id_list.append(frame_id['id'])

        context['anchor'] = anchor
<<<<<<< HEAD
        context['frame_limit'] = id_list
        context['frame'] = anchor.frame_from_anchor.get(id=pk2)
        context['p_frame'] = prev_frame
        context['n_frame'] = next_frame
        context['box_count'] = anchor.frame_from_anchor.filter(box_from_frame__isnull=False).count()
        return context
=======
        context['frame_list'] = id_list
        context['frame'] = frame
        context['p_frame'] = prev_frame
        context['n_frame'] = next_frame
        context['box_count'] = anchor.frame_from_anchor.filter(box_from_frame__isnull=False).count()
        context['frame_count'] = id_list.index(pk2)+1
        context['total_frames'] = len(id_list)
        context['all_anchors'] = anchor.QBQ_source.anchor.all()
        context['first_frame'] = id_list[0]
        context['last_frame'] = id_list[-1]
        return context


@csrf_protect
def project_anchor(request):
    if request.method == "POST":
        user = request.user
        valid_anchor = Anchor.objects.filter(valid=None).order_by('pk').first()
        valid_anchor.valid = True
        valid_anchor.save()
        return Project.objects.create(assigned_user=user, assigned_anchor=valid_anchor)
    else:
        pass
    return redirect("main")


def make_anchor_valid(request,pk,pk2):
    anchor = Anchor.objects.get(id=pk)
    anchor.valid = True
    anchor.save()
    return redirect('finalboxing-detail', pk=pk, pk2=pk2)


def make_project_valid(request,pk,pk2):
    project = Project.objects.get(assigned_anchor_id=pk)
    project.valid = True
    project.save()
    return redirect('project-detail', pk=pk, pk2=pk2)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'registration/logged_out.html')
    return HttpResponse('error')


class ManageUserList(ListView):
    template_name = 'registration/manage.html'
    context_object_name = 'users'
    permission_classes = (IsAuthenticated,)


    def get_queryset(self): # 컨텍스트 오버라이딩
      return User.objects.filter(project__isnull=False).distinct()


class ManageUserDetailView(DetailView):
    model = User
    template_name = 'registration/manage-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.kwargs['pk']를 통해서 url에서 pk값을 받을 수 있습니다.
        # url은 `path('<pk>/', PhotoView.as_view())으로 구현되어있어서 해당 pk 부분을 받아옵니다.`
        user = User.objects.get(id=self.kwargs['pk'])
        projects = Project.objects.filter(assigned_user=user)

        #프로젝트 기준으로 생성된 box를 찾습니다.
        boxes = []
        for prj in projects:
            frames = prj.assigned_anchor.frame_from_anchor.all()
            for frame in frames:
                try:
                    boxes.append(frame.box_from_frame)
                except:
                    pass

        ##box의 생성일을 계산합니다.
        box_dates = []
        for box in boxes:
            box_dates.append(box.created_at.date().day)
            box_dates = list(set(box_dates))

        ## 생성일과 생성일에 해당하는 box를 저장합니다.
        box_info = {}
        for box in boxes:
            if box.created_at.date().day in box_info:
                box_info[box.created_at.date().day].append(box)
            else:
                box_info[box.created_at.date().day] = [box]

        ## dict에서 날짜당 box 갯수 반환합니다.
        box_info_count = {}
        for x, v in box_info.items():
            box_info_count[x] = len(v)

        ## project 에서 각 project마다 anchor의 frame중 valid=True를 찾습니다.
        valid_frame = []
        for prj in projects:
            valid_frame.append(prj.assigned_anchor.frame_from_anchor.filter(valid=True))

        ## frame 쿼리셋을 합칩니다.
        valid_frames = []
        for i in valid_frame:
            valid_frames += (list(i))

        ##valid 인 frame 날짜별로 계산합니다.
        valid_frame_info={}
        for fram in valid_frames:
            try:
                if fram.valid_updated_at.date().day in valid_frame_info:
                    valid_frame_info[fram.valid_updated_at.date().day].append(fram)
                else:
                    valid_frame_info[fram.valid_updated_at.date().day] = [fram]
            except:
                pass

        ##valid_frame_info에 대해 날짜당 갯수 계산합니다.
        valid_frame_info_count = {}
        for x, v in valid_frame_info.items():
            valid_frame_info_count[x] = len(v)

        from itertools import chain
        from collections import defaultdict
        all_info = defaultdict(list)
        for k, v in chain(box_info_count.items(), valid_frame_info_count.items()):
            all_info[k].append(v)

        context['boxes'] = box_dates
        context['all_info'] = dict(all_info)
        return context


#/search로 접속할 수 있으며, 검색을 구현하였습니다. (오래걸려서 쓰지 않음)
def search(request):
    box_list = Box.objects.all()
    box_filter = BoxFilter(request.GET, queryset=box_list)
    return render(request, 'search/box_list.html', {'filter': box_filter})


#api/box으로 접속 가능하며 user가 작업한 작업 결과를 확인할 수 있는 API를 생성합니다.
class AnchorReadViewset(viewsets.ModelViewSet):
    queryset = Anchor.objects.all()
    serializer_class = AnchorSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # filter_class = BoxTypeFilter

    def get_queryset(self):
        user = User.objects.get(username='minjun')
        frames = Frame.objects.filter(box_from_frame__isnull=False, box_from_frame__work_user=user)

        if 'pk' in self.kwargs:
            print(self.kwargs['pk'])
            valid_anchor = self.queryset.filter(frame_from_anchor__in=frames).distinct()
            valid_anchor = valid_anchor[:float(self.kwargs['pk'])]
            return HttpResponse('ee')
        else:
            valid_anchor = self.queryset.filter(frame_from_anchor__in=frames).distinct()[:100]
        return valid_anchor


    @classmethod
    def get_extra_actions(cls):
        return []

>>>>>>> Add user management and API
