from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django import forms

from .models import Anchor, Box, get_box_filename, QBQ, Frame
from .utils import *


class SourceForm(forms.ModelForm):
    grade = forms.ChoiceField(choices=((i, i) for i in range(1,7)))


class CsvImportForm(forms.Form):
    csv_file = forms.FileField(widget=forms.FileInput(attrs={'accept': ".csv"}))


class BoxInline(admin.TabularInline):
    model = Box
    fields = ['left', 'top', 'right', 'bottom', 'frame_source', 'work_user']
    readonly_fields = ['frame_source', 'work_user']


class AnchorBoxInline(admin.TabularInline):
    model = Anchor
<<<<<<< HEAD
    fields = ['get_image', 'left', 'right', 'top', 'bottom', 'work_user', 'anchor_group']
    readonly_fields = ['get_image', 'work_user']
=======
    fields = ['get_image', 'left', 'right', 'top', 'bottom', 'anchor_group']
    readonly_fields = ['get_image']
>>>>>>> Add user management and API

    def get_image(self, anchor):
        return mark_safe('<img src="%s" style="max-width:200px;" />' % anchor.anchor_image.url)


class IsFrameBoxNullFilter(admin.SimpleListFilter):
    """
    Frame에서 작업시 box가 없는 것들을 찾가 위한 필터입니다.
    """
    title = 'is_box_null'
    parameter_name = 'is_box_null'

    def lookups(self, request, model_admin):
        return [
            (None, '전체'),
            ('true', '박스가 없음'),
            ('false', '박스가 있음'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'true':
            queryset = queryset.filter(box_from_frame__isnull=True)#fliter로 먹히는지 확인필요
        elif self.value() == 'false':
            queryset = queryset.filter(box_from_frame__isnull=False)
        return queryset


class IsRotatedImagedNullFilter(admin.SimpleListFilter):
    title = 'is_rotated_img_null'
    parameter_name = 'is_rotated_img_null'

    def lookups(self, request, model_admin):
        return [
            (None, '전체'),
            ('true', 's3 이미지 없음'),
            ('false', 's3 이미지 있음'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'true':
            queryset = queryset.filter(rotated_image='')
        elif self.value() == 'false':
            queryset = queryset.exclude(rotated_image='')
        return queryset


class QBQAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ['id', 'QBaseQuestion_id', 'get_image_url', 'anchor_count', 'book_title', 'book_id',
=======
    list_display = ['id', 'QBaseQuestion_id', 'get_image_url', 'candidate_count','anchor_count', 'book_title', 'book_id',
>>>>>>> Add user management and API
                    ]
    change_list_template = 'Sean_boxing/admin/QBQ_change_list.html'
    change_form_template = 'Sean_boxing/admin/QBQ_change_form.html'
    inlines = [AnchorBoxInline, ]
    actions = ()

    def get_image_url(self, QBQ):
        return mark_safe('<img src="%s" width=200px "/>' % QBQ.image_url)
    get_image_url.short_description = 'image'

    def anchor_count(self, QBQ):
<<<<<<< HEAD
        anchors = QBQ.anchor.all()
        anchor_counts=[]
        if anchors.exists():
            for anchor in anchors:
                anchor_counts.append(anchor)
            return len(anchor_counts)
        else:
            return 0


class AnchorAdmin(admin.ModelAdmin):# 추후 같은 anchor끼리 그룹 묶는 작업할 수 있도록 바꿔야함
    list_display = ['id', 'get_image_url','get_QBQ_image_url','count_saved_boxes', 'work_user'
=======
        anchors = QBQ.anchor.all().count()
        return anchors

    def candidate_count(self, QBQ):
        return QBQ.candidates.all().count()


class AnchorAdmin(admin.ModelAdmin):# 추후 같은 anchor끼리 그룹 묶는 작업할 수 있도록 바꿔야함
    list_display = ['id', 'get_image_url','get_QBQ_image_url','anchor_group', 'count_saved_boxes','get_assigend_user', 'valid'
>>>>>>> Add user management and API
                    ]
    change_list_template = 'Sean_boxing/admin/final_boxing_list.html'
    change_form_template = 'Sean_boxing/admin/final_boxing_form.html'
    list_filter = []
<<<<<<< HEAD
    actions = (
=======
    actions = ('make_frames','make_anchor_group'
>>>>>>> Add user management and API
    )
#
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        """
        admin url 에 object를 전달하기 위한 render_change_form입니다.

        """
        context.update({'object': self.get_object(request, object_id=context['object_id'])})
        return super(AnchorAdmin, self).render_change_form(request, context, add, change, form_url, obj)

    def get_image_url(self, anchor):
<<<<<<< HEAD
        return mark_safe('<img src="%s" width=200px "/>' % anchor.anchor_image.url)
=======
        try:
            return mark_safe('<img src="%s" width=200px "/>' % anchor.anchor_image.url)
        except:
            return None
>>>>>>> Add user management and API
    get_image_url.short_description = 'anchor 이미지'

    def get_QBQ_image_url(self, anchor):
        if anchor.__dict__['QBQ_source_id'] is not '':
            return mark_safe('<img src="%s" width=200px "/>' % anchor.QBQ_source.image_url)
        else:
            return '-'
    get_QBQ_image_url.short_description = '원본 이미지'

<<<<<<< HEAD
=======
    def get_assigend_user(self, anchor):
        user = anchor.project.assigned_user
        # if user:
        return user
        # else:
        #     return '-'
    get_assigend_user.short_description = '할당자'

>>>>>>> Add user management and API
    def count_saved_boxes(self, anchor):
        return anchor.frame_from_anchor.all().filter(box_from_frame__isnull=False).count()
    count_saved_boxes.short_description = 'box 갯수'

<<<<<<< HEAD
=======
    def _make_anchor_group(self, request, queryset): #수정해야함
        valid_queryset = queryset.filter(rotated_image='')
        if valid_queryset.count() > 100:
            self.message_user(request,
                              "ERROR: Cannot Finish Requests (Requests Count: {})".format(valid_queryset.count()),
                              level=messages.ERROR)
        else:
            for candidate in valid_queryset:
                candidate._save_rotation_image()
            self.message_user(request, "Finish {} Requests Successfully".format(valid_queryset.count()))

    def make_frames(self, request, queryset):
        for anchor in queryset:
            candidates = anchor.QBQ_source.candidates.all()
            for candidate in candidates:
                Frame.objects.get_or_create(anchor_source=anchor, candidate_info=candidate)

    def make_anchor_group(self, request, queryset):
        anchor_group_exists = queryset.filter(anchor_group__isnull=False)
        anchor_group_not_exists = queryset.filter(anchor_group__isnull=True).distinct()
        anchor_first = anchor_group_exists.first()

        try:
            self._add_exists_anchor_group(anchor_group_exists)
        except:
            pass

        try:
            self._add_or_create_anchor_group(anchor_group_not_exists,anchor_first)
        except:
            pass

    def _add_exists_anchor_group(self, queryset):
        for anchor in queryset:
            anchors = anchor.anchor_group.anchors.all()
            for each_anchor in anchors:
                each_anchor.anchor_group = queryset.first().anchor_group
                each_anchor.save()

    def _add_or_create_anchor_group(self, queryset, first_anchor):
        if first_anchor:
            for anchor in queryset:
                anchor.anchor_group = first_anchor.anchor_group
                anchor.save()
        else:
            anchor_group = AnchorGroup.objects.create()
            for anchor in queryset:
                anchor.anchor_group = anchor_group
                anchor.save()

>>>>>>> Add user management and API

class CandidateAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_rotated_img', 'rotation_angle', 'get_QBQ_image_url',
                    ]
    actions = (
        'update_rotation_image',
    )

    def get_rotated_img(self, candidate):
        if candidate.rotated_image:
            return mark_safe('<img src="%s" width=200px "/>' % candidate.rotated_image.url)
        else:
            '-'

    def get_QBQ_image_url(self, candidate):
        return mark_safe('<img src="%s" width=200px "/>' % candidate.QBQ_source.image_url)
    get_QBQ_image_url.short_description = 'QBQ 이미지'

<<<<<<< HEAD
    def update_rotation_image(self, request, queryset): #추후 QBQ에 대한 candi 생성 action으로 바꿀수도..?
=======
    def update_rotation_image(self, request, queryset):
>>>>>>> Add user management and API
        valid_queryset = queryset.filter(rotated_image='')
        if valid_queryset.count() > 100:
            self.message_user(request,
                              "ERROR: Cannot Finish Requests (Requests Count: {})".format(valid_queryset.count()),
                              level=messages.ERROR)
        else:
            for candidate in valid_queryset:
                candidate._save_rotation_image()
            self.message_user(request, "Finish {} Requests Successfully".format(valid_queryset.count()))


class IsValidFilter(admin.SimpleListFilter):
    title = 'is_valid'
    parameter_name = 'is_valid'
    def lookups(self, request, model_admin):
        return [
            (None, '전체'),
            ('true', '한번 이상 본 것'),
            ('false', '한번도 안 본 것'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'true':
            queryset = queryset.filter(valid=True)
        elif self.value() == 'false':
            queryset = queryset.exclude(valid=True)
        return queryset

class IsBoxFilter(admin.SimpleListFilter):
    title = 'check_box'
    parameter_name = 'check_box'
    def lookups(self, request, model_admin):
        return [
            (None, '전체'),
            ('true', 'box 없음'),
            ('false', 'box 있음'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'true':
            queryset = queryset.filter(box_from_frame__isnull=True)
        elif self.value() == 'false':
            queryset = queryset.filter(box_from_frame__isnull=False)
        return queryset

<<<<<<< HEAD
class FrameAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_anchor_image', 'get_QBQ_image','get_candidate_image','get_check_box', 'valid']
=======

class FrameAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_anchor_image', 'get_QBQ_image','get_candidate_image','get_check_box','valid_updated_at', 'valid']
>>>>>>> Add user management and API
    list_filter = [IsValidFilter, IsBoxFilter]
    actions = []

    def get_anchor_image(self, frame):
        return mark_safe('<img src="%s" width=200px "/>' % frame.anchor_source.anchor_image.url)
    get_anchor_image.short_description = 'anchor image'

    def get_QBQ_image(self, frame):
        QBQ = frame.anchor_source.QBQ_source
        return mark_safe('<img src="%s" width=200px "/>' % QBQ.image_url)
    get_QBQ_image.short_description = 'QBQ image'

    def get_candidate_image(self, frame):
        if frame.candidate_info.rotated_image:
            return mark_safe('<img src="%s" width=200px "/>' % frame.candidate_info.rotated_image.url)
        else:
            '-'
    get_candidate_image.short_description = 'candidate image'

    def get_check_box(self, frame):
        if frame.box_from_frame:
            box =  1
        else:
            box = 0
        return box


class BoxAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_anchor_image_url', 'get_candidate_image', 'left','right','top','bottom', 'work_user']
    actions = []

    def get_anchor_image_url(self, box):
        anchor = box.frame_source.anchor_source
        return mark_safe('<img src="%s" width=200px "/>' % anchor.anchor_image.url)
    get_anchor_image_url.short_description = 'anchor image'

    def get_candidate_image(self, box):
        candidate = box.frame_source.candidate_info
        return mark_safe('<img src="%s" width=200px "/>' % candidate.rotated_image.url)
    get_candidate_image.short_description = 'candidate image'


<<<<<<< HEAD
=======
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'assigned_user', 'assigned_anchor', 'valid']
    actions = ['delete_model']

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        for prj in obj:
            print(prj.assigned_anchor, prj.assigned_anchor.valid)
            try:
                prj.assigned_anchor.valid=None
                prj.assigned_anchor.save()
                print(prj.assigned_anchor.valid)
            except:
                pass
        obj.delete()


>>>>>>> Add user management and API
admin.site.register(QBQ, QBQAdmin)
admin.site.register(Anchor, AnchorAdmin)
admin.site.register(CandidateInfo, CandidateAdmin)
admin.site.register(Box, BoxAdmin)
admin.site.register(Frame, FrameAdmin)
<<<<<<< HEAD
=======
admin.site.register(Project, ProjectAdmin)
>>>>>>> Add user management and API
