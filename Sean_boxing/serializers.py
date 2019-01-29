<<<<<<< HEAD
from rest_framework import serializers

from .models import Anchor, CandidateInfo, Box, QBQ, Frame
=======
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Anchor, CandidateInfo, Box, QBQ, Frame, Project
>>>>>>> Add user management and API


class CurrentFrameDefault(object):
    """
    현재의 Frame Default입니다.
    """
    def set_context(self, serializer_field):
        self.frame = serializer_field.context['frame']

    def __call__(self):
        return Frame.objects.get(pk=self.frame)

class CurrentQBQDefault(object):
    """
    현재의 QBQ Default입니다.
    """
    def set_context(self, serializer_field):
        self.QBQ = serializer_field.context['qbq_source']

    def __call__(self):
        return QBQ.objects.get(pk=self.QBQ)


class AnchorWriteSerializer(serializers.ModelSerializer):
    left = serializers.DecimalField(max_digits=51, decimal_places=50)
    top = serializers.DecimalField(max_digits=51, decimal_places=50)
    right = serializers.DecimalField(max_digits=51, decimal_places=50)
    bottom = serializers.DecimalField(max_digits=51, decimal_places=50)
<<<<<<< HEAD
    work_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
=======
    # work_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
>>>>>>> Add user management and API
    QBQ_source = serializers.HiddenField(default=CurrentQBQDefault())

    class Meta:
        model = Anchor
<<<<<<< HEAD
        fields = ['id', 'QBQ_source', 'left', 'top', 'right', 'bottom', 'work_user']
=======
        fields = ['id', 'QBQ_source', 'left', 'top', 'right', 'bottom']
>>>>>>> Add user management and API

    def create(self, validated_data):
        QBQ = validated_data['QBQ_source']
        return Anchor.objects.create(
        left = validated_data['left'],
        top = validated_data['top'],
        right = validated_data['right'],
        bottom = validated_data['bottom'],
        QBQ_source = QBQ,
<<<<<<< HEAD
        work_user = validated_data['work_user']
=======
        # work_user = validated_data['work_user']
>>>>>>> Add user management and API
        )


class AnchorReadSerializer(serializers.ModelSerializer):
    left = serializers.FloatField()
    top = serializers.FloatField()
    right = serializers.FloatField()
    bottom = serializers.FloatField()

    class Meta:
        model = Anchor
        fields = ['id', 'left', 'top', 'right', 'bottom']


class BoxWriteSerializer(serializers.ModelSerializer):
    left = serializers.DecimalField(max_digits=51, decimal_places=50)
    top = serializers.DecimalField(max_digits=51, decimal_places=50)
    right = serializers.DecimalField(max_digits=51, decimal_places=50)
    bottom = serializers.DecimalField(max_digits=51, decimal_places=50)
    work_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    frame_source = serializers.HiddenField(default=CurrentFrameDefault())

    class Meta:
        model = Box
        fields = ['id', 'frame_source', 'left', 'top', 'right', 'bottom', 'work_user']

    def create(self, validated_data):
        frame = validated_data['frame_source']
        return Box.objects.create(
        left = validated_data['left'],
        top = validated_data['top'],
        right = validated_data['right'],
        bottom = validated_data['bottom'],
        frame_source = frame,
        work_user = validated_data['work_user']
        )


class BoxReadSerializer(serializers.ModelSerializer):
    left = serializers.FloatField()
    top = serializers.FloatField()
    right = serializers.FloatField()
    bottom = serializers.FloatField()

    class Meta:
        model = Box
        fields = ['id', 'left', 'top', 'right', 'bottom']


<<<<<<< HEAD
class CandidateSerializer(serializers.ModelSerializer):
    boxes = BoxReadSerializer(read_only=True, many=True)
=======
class BoxCandiReadSerializer(serializers.ModelSerializer):
    left = serializers.FloatField()
    top = serializers.FloatField()
    right = serializers.FloatField()
    bottom = serializers.FloatField()

    class Meta:
        model = Box
        fields = ['left', 'top', 'right', 'bottom']


class CandidateSerializer(serializers.ModelSerializer):
>>>>>>> Add user management and API

    class Meta:
        model = CandidateInfo
        fields = (
<<<<<<< HEAD
            'id', 'image_url', 'boxes',
=======
            'rotation_image_url','rotation_angle',
        )


class FrameSerializer(serializers.ModelSerializer):
    box = serializers.SerializerMethodField('get_valid_box')
    candidate_info = serializers.SerializerMethodField('get_valid_candidate')

    def get_valid_candidate(self, frame):
        qs=CandidateInfo.objects.filter(frame_from_candidate=frame)
        # print(qs)
        serializer = CandidateSerializer(instance=qs, many=True)
        return serializer.data

    def get_valid_box(self, frame):
        qs=Box.objects.filter(frame_source=frame)
        # print(qs)
        serializer = BoxReadSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Frame
        fields = (
            'id',
            'candidate_info',
            'box',
>>>>>>> Add user management and API
        )


class AnchorSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    boxes = BoxReadSerializer(read_only=True, many=True)
=======
    frame = serializers.SerializerMethodField('get_valid_frame')

    def get_valid_frame(self, anchor):
        user=User.objects.get(username='minjun')
        qs=Frame.objects.filter(box_from_frame__isnull=False, box_from_frame__work_user=user ,anchor_source=anchor)
        # print(qs)
        serializer = FrameSerializer(instance=qs, many=True)
        return serializer.data
>>>>>>> Add user management and API

    class Meta:
        model = Anchor
        fields = (
<<<<<<< HEAD
            'id', 'image_url', 'boxes', 'QBQ_source', 'anchor_group'
        )


class QBQSerializer(serializers.ModelSerializer):
    anchors = AnchorReadSerializer(read_only=True, many=True)
=======
            'id', 'anchor_image_url',
            'frame',
        )


class QBQReadSerializer(serializers.ModelSerializer):
    anchor = AnchorSerializer(read_only=True, many=True)

    # def get_valid_anchor(self, qbq):
    #     # user=User.objects.get(username='minjun')
    #     qs=Anchor.objects.filter(box_from_frame__isnull=False ,QBQ_source=qbq)
    #     print(qs)
    #     serializer = FrameSerializer(instance=qs, many=True)
    #     return serializer.data

    class Meta:
        model = QBQ
        fields = (
            'id', 'image_url', 'anchor'
        )


#box 저장할때 사용
class QBQSerializer(serializers.ModelSerializer):
    anchor = AnchorReadSerializer(read_only=True, many=True)
>>>>>>> Add user management and API

    class Meta:
        model = QBQ
        fields = (
<<<<<<< HEAD
            'id', 'image_url', 'anchors', 'book_title', 'book_id'
=======
            'id', 'image_url', 'anchor', 'book_title', 'book_id'
>>>>>>> Add user management and API
        )


class CandidateReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateInfo
<<<<<<< HEAD
        fields = '__all__'
=======
        fields = '__all__'


class ProjectMakeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        valid_anchor = validated_data['valid_anchor']
        print(valid_anchor)
        user = validated_data['user']
        print(user)
        # valid_anchor = Anchor.objects.filter(valid=None).order_by('pk').first()
        return Project.objects.create(
            assigned_anchor=valid_anchor,
            assigned_user=user
        )
>>>>>>> Add user management and API
