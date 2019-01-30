from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Anchor, CandidateInfo, Box, QBQ, Frame, Project


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
    QBQ_source = serializers.HiddenField(default=CurrentQBQDefault())

    class Meta:
        model = Anchor
        fields = ['id', 'QBQ_source', 'left', 'top', 'right', 'bottom']

    def create(self, validated_data):
        QBQ = validated_data['QBQ_source']
        return Anchor.objects.create(
        left = validated_data['left'],
        top = validated_data['top'],
        right = validated_data['right'],
        bottom = validated_data['bottom'],
        QBQ_source = QBQ,
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


class BoxCandiReadSerializer(serializers.ModelSerializer):
    left = serializers.FloatField()
    top = serializers.FloatField()
    right = serializers.FloatField()
    bottom = serializers.FloatField()

    class Meta:
        model = Box
        fields = ['left', 'top', 'right', 'bottom']


class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateInfo
        fields = (
            'rotation_image_url','rotation_angle',
        )


class FrameSerializer(serializers.ModelSerializer):
    box = serializers.SerializerMethodField('get_valid_box')
    candidate_info = serializers.SerializerMethodField('get_valid_candidate')

    def get_valid_candidate(self, frame):
        qs=CandidateInfo.objects.filter(frame_from_candidate=frame)
        serializer = CandidateSerializer(instance=qs, many=True)
        return serializer.data

    def get_valid_box(self, frame):
        qs=Box.objects.filter(frame_source=frame)
        serializer = BoxReadSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Frame
        fields = (
            'id',
            'candidate_info',
            'box',
        )


class AnchorSerializer(serializers.ModelSerializer):
    frame = serializers.SerializerMethodField('get_valid_frame')

    def get_valid_frame(self, anchor):
        user=User.objects.get(username='minjun')
        qs=Frame.objects.filter(box_from_frame__isnull=False, box_from_frame__work_user=user ,anchor_source=anchor)
        serializer = FrameSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Anchor
        fields = (
            'id', 'anchor_image_url',
            'frame',
        )


class QBQReadSerializer(serializers.ModelSerializer):
    anchor = AnchorSerializer(read_only=True, many=True)

    class Meta:
        model = QBQ
        fields = (
            'id', 'image_url', 'anchor'
        )


#box 저장할때 사용
class QBQSerializer(serializers.ModelSerializer):
    anchor = AnchorReadSerializer(read_only=True, many=True)

    class Meta:
        model = QBQ
        fields = (
            'id', 'image_url', 'anchor', 'book_title', 'book_id'
        )


class CandidateReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateInfo
        fields = '__all__'


class ProjectMakeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        valid_anchor = validated_data['valid_anchor']
        user = validated_data['user']
        return Project.objects.create(
            assigned_anchor=valid_anchor,
            assigned_user=user
        )