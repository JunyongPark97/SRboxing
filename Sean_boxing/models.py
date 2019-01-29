import random
import string
<<<<<<< HEAD
=======
import json
import logging
from datetime import datetime
>>>>>>> Add user management and API
from io import BytesIO

import requests
from django.contrib.auth.base_user import AbstractBaseUser
<<<<<<< HEAD
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
=======
from django.contrib.auth.models import User, AbstractUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from munch import munchify
>>>>>>> Add user management and API

from qanda.ocr.models import OCRSearchRequest
from qbase.models import QBaseQuestion
from django import template
<<<<<<< HEAD

register = template.Library()


PRECISION = 4
THRESHOLD = 0.1 ** PRECISION
=======
# import user

register = template.Library()

logger = logging.getLogger('test')

PRECISION = 4
THRESHOLD = 0.1 ** PRECISION
CANDIDATES_COUNT = 100
>>>>>>> Add user management and API

book_lst = \
    [
        '개념원리RPM중22학기',
        '개념원리RPM수학2',
        '개념원리RPM중3하2016',
        '개념SSEN중등수학1하2016',
        'SSEN중등수학3하',
        '라이트SSEN중등수학2하',
        '라이트SSEN중등수학3하',
        'SSEN중등수학1하',
        'SSEN중등수학2하',
        '개념SSEN중등수학3하2016',
        '개념SSEN중등수학2하2016',
        '라이트SSEN중등수학1하',
    ]

def get_box_filename():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12)) + '.jpg'


def equals(f1, f2):
    return abs(f1 - f2) < THRESHOLD


class AnchorGroup(models.Model):
    pass


class QBQ(models.Model):
    QBaseQuestion_id = models.IntegerField()
<<<<<<< HEAD
    image_url = models.URLField(max_length=200)## 이전 자료 보고 uuid or image_url property 확인
=======
    image_url = models.URLField(max_length=200)
>>>>>>> Add user management and API
    book_title = models.CharField(max_length=50)
    book_id = models.IntegerField()

    def get_image_extension(self):
        return 'jpeg'

    @property
    def prev(self):
        return QBQ.objects.filter(pk__lt=self.pk).order_by('pk').last()

    @property
    def next(self):
        return QBQ.objects.filter(pk__gt=self.pk).order_by('pk').first()

    def save(self, *args, **kwargs):
        super(QBQ, self).save(*args, **kwargs)
<<<<<<< HEAD
        self._create_vaild_candidates()
=======
        # self._create_candidate() # data 업데이트 이후 수정 필요
        # self.create_default_anchor() # 마찬가지
>>>>>>> Add user management and API

    def get_id_list(self):
        id_list = []
        for candidate in self.candidates.all():
            id_list.append(candidate.OCRSearchRequest_id)
        return id_list

    def _candidate_list(self):
<<<<<<< HEAD
        candidates_qs = OCRSearchRequest.objects.filter(
                        ocr_question_logs__qbase_question_id=self.QBaseQuestion_id)[:50]
        return candidates_qs
=======
        candidates_list = OCRSearchRequest.objects.filter(
                        ocr_question_logs__qbase_question_id=self.QBaseQuestion_id).order_by('-pk')[:CANDIDATES_COUNT]
        return candidates_list
>>>>>>> Add user management and API

    def _create_candidate(self):
        for candidate in self._candidate_list():
            QBQ_source = QBQ.objects.get(id=self.pk)
<<<<<<< HEAD
            CandidateInfo.objects.create(QBQ_source=QBQ_source,
                                      OCRSearchRequest_id=candidate.id,
                                      image_key=candidate.image_key)

    def _create_vaild_candidates(self):
        if self.candidates.all().exists():
            pass
        else:
            self._create_candidate()
=======
            CandidateInfo.objects.get_or_create(QBQ_source=QBQ_source,
                                      OCRSearchRequest_id=candidate.id,
                                      image_key=candidate.image_key)

    def _call_api(self):
        data = {'image_url': self.image_url,}
        try:
            result = json.loads(requests.post('http://125.129.239.235:14025/api/similar/', data=data).text)
        except:
            result = None
        return result['boxes']# 여기다가 self.api_satatus라는 필드 만들어서 한번 호출하면 True로 바꾸고 True 이면 call 안하기

    def create_default_anchor(self):
        failed_ids=[]
        try:
            anchor_boxes = self._call_api()
            valid_anchor_boxes = list(filter(lambda x:x['prob']>0.9, anchor_boxes))
            for box in valid_anchor_boxes:
                Anchor.objects.get_or_create(QBQ_source=self,
                                                  left=box['left'],
                                                  top=box['top'],
                                                  right=box['right'],
                                                  bottom=box['bottm'])
        except:
            failed_ids.append(self.pk)
>>>>>>> Add user management and API


class Anchor(models.Model):
    QBQ_source = models.ForeignKey(QBQ,  null=True, blank=True, related_name='anchor', on_delete=models.CASCADE) #여기에 QBQ: 원본 정보 저장하는 필드
    anchor_group = models.ForeignKey(AnchorGroup, null=True, blank=True, related_name='anchors', on_delete=models.SET_NULL)
    left = models.DecimalField(max_digits=PRECISION + 1, decimal_places=PRECISION)
    top = models.DecimalField(max_digits=PRECISION + 1, decimal_places=PRECISION)
    right = models.DecimalField(max_digits=PRECISION + 1, decimal_places=PRECISION)
    bottom = models.DecimalField(max_digits=PRECISION + 1, decimal_places=PRECISION)
    anchor_image = models.ImageField(upload_to='anchor')
<<<<<<< HEAD
    work_user = models.ForeignKey(User, related_name='worked_anchor', on_delete=models.CASCADE)
=======
    # work_user = models.ForeignKey(User, null=True, blank=True, related_name='worked_anchor', on_delete=models.CASCADE)
    valid = models.NullBooleanField()
>>>>>>> Add user management and API

    @property
    def prev(self):
        return Anchor.objects.filter(pk__lt=self.pk).order_by('pk').last()

    @property
    def next(self):
        return Anchor.objects.filter(pk__gt=self.pk).order_by('pk').first()

    @property
<<<<<<< HEAD
=======
    def anchor_image_url(self):
        return self.anchor_image.url

    @property
>>>>>>> Add user management and API
    def valid_frame_first(self):
        frames = self.frame_from_anchor.all()
        frame = frames.filter(valid=False).order_by('pk')
        if frame.exists():
            frame = frame.first()
            return frame
        else:
            frame = frames.order_by('pk').last()
            return frame

    @property
    def valid_count(self):
        frames = self.frame_from_anchor
        return frames.filter(valid=True).count()

    @property
    def count_box(self):
        frames = self.frame_from_anchor
        counts = frames.filter(box_from_frame__isnull = False)
        return len(counts)

    @property
    def count_anchors(self):
        anchors = self.QBQ_source.anchor.all()
        count = len(anchors)
        return count

    def validate_coordinates(self):
        if self.left >= self.right:
            raise Exception('left >= right')
        elif self.top >= self.bottom:
            raise Exception('top >= bottom')
        self.left = 0 if self.left < 0 else self.left
        self.top = 0 if self.top < 0 else self.top
        self.right = 1 if self.right > 1 else self.right
        self.bottom = 1 if self.bottom > 1 else self.bottom

    def save(self, *args, **kwargs):
        self.validate_coordinates()
        super(Anchor, self).save(*args, **kwargs)
        self._save_anchor_image()
        self._make_frames()

<<<<<<< HEAD
    def update(self, left, top, right, bottom, **kwargs):
        if not equals(float(self.left), left) or \
                not equals(float(self.top), top) or \
                not equals(float(self.right), right) or \
                not equals(float(self.bottom), bottom):
            self.left = left
            self.top = top
            self.right = right
            self.bottom = bottom
=======
    def update(self, left, top, right, bottom, valid,**kwargs):
        try:
            if not equals(float(self.left), left) or \
                    not equals(float(self.top), top) or \
                    not equals(float(self.right), right) or \
                    not equals(float(self.bottom), bottom):
                self.left = left
                self.top = top
                self.right = right
                self.bottom = bottom
                self.save()
        except:
            pass
        try:
            self.valid = valid
            self.save()
        except:
            pass

    def update_valid(self, valid, **kwargs):
            self.valid = valid
>>>>>>> Add user management and API
            self.save()

    def _save_anchor_image(self):
        from PIL import Image
        resp = requests.get(self.QBQ_source.image_url)
        image = Image.open(BytesIO(resp.content))
        width, height = image.size
        left = width * self.left
        top = height * self.top
        right = width * self.right
        bottom = height * self.bottom
        crop_data = image.crop((int(left), int(top), int(right), int(bottom)))
        # http://stackoverflow.com/questions/3723220/how-do-you-convert-a-pil-image-to-a-django-file
        crop_io = BytesIO()
        crop_data.save(crop_io, format=self.QBQ_source.get_image_extension())
        crop_file = InMemoryUploadedFile(crop_io, None, get_box_filename(), 'image/jpeg', len(crop_io.getvalue()), None)
        self.anchor_image.save(get_box_filename(), crop_file, save=False)
        # To avoid recursive save, call super.save
        super(Anchor, self).save()

    def _make_frames(self):
        candidates= self.QBQ_source.candidates.all()
        for candidate in candidates:
            Frame.objects.get_or_create(anchor_source=self, candidate_info=candidate)

    def __str__(self):
        if self.id:
            return 'B%d' % self.id
        return ''


class CandidateInfo(models.Model):
    QBQ_source = models.ForeignKey(QBQ, related_name='candidates', on_delete=models.CASCADE)
    OCRSearchRequest_id = models.CharField(max_length=100) #OCRSearchRequest id만 저장
    image_key = models.UUIDField() #OCRSearchRequest uuid 저장 -> image url
    rotation_angle = models.IntegerField(blank=True, null=True)
    rotated_image = models.ImageField(upload_to='rotated_image')#S3 image가 저장될 필드

    def get_image_extension(self):
        return 'jpeg'

    @property
    def image_url(self):
        return 'https://qanda-storage.s3.amazonaws.com/{}.jpg'.format(self.image_key)

    @property
    def QBQ_image_url(self):
        return self.QBQ_source.image_url

    @property
<<<<<<< HEAD
=======
    def rotation_image_url(self):
        return self.rotated_image.url

    @property
>>>>>>> Add user management and API
    def prev(self):
        return CandidateInfo.objects.filter(pk__lt=self.pk).order_by('pk').last()

    @property
    def next(self):
        return CandidateInfo.objects.filter(pk__gt=self.pk).order_by('pk').first()

    def save(self, *args, **kwargs):
        super(CandidateInfo, self).save(*args, **kwargs)
        self._save_rotation_image()

    def _save_rotation_image(self):
        from Sean_boxing.utils import resize_img, rotate_img
        from PIL import Image
        resp = requests.get(self.image_url)
        image = Image.open(BytesIO(resp.content))
        image = resize_img(image)
        image, rotate_angle = rotate_img(image, self.OCRSearchRequest_id)
        # http://stackoverflow.com/questions/3723220/how-do-you-convert-a-pil-image-to-a-django-file
        crop_io = BytesIO()
        source = OCRSearchRequest.objects.get(id = self.OCRSearchRequest_id)
        image.save(crop_io, format='jpeg')
        crop_file = InMemoryUploadedFile(crop_io, None, get_box_filename(), 'image/jpeg', len(crop_io.getvalue()), None)
        self.rotated_image.save(get_box_filename(), crop_file, save=False)
        # To avoid recursive save, call super.save
        self.rotation_angle = rotate_angle
        super(CandidateInfo, self).save()


class Frame(models.Model):
    anchor_source = models.ForeignKey(Anchor, related_name='frame_from_anchor', on_delete=models.CASCADE)
    candidate_info = models.ForeignKey(CandidateInfo, related_name='frame_from_candidate', on_delete=models.CASCADE)
    valid = models.NullBooleanField(default=False)
<<<<<<< HEAD

    @property
    def prev(self):
        return Frame.objects.filter(pk__lt=self.pk).order_by('pk').last()
=======
    valid_updated_at = models.DateTimeField(blank=True, null=True)

    @property
    def prev(self):
        frame = Frame.objects.get(pk=self.pk)
        anchor = frame.anchor_source
        prev_frame = anchor.frame_from_anchor.filter(pk__lt=self.pk).order_by('pk').last()
        return prev_frame
>>>>>>> Add user management and API

    @property
    def next(self):
        frame = Frame.objects.get(pk=self.pk)
<<<<<<< HEAD
        frame.valid=True
        frame.save()
        return Frame.objects.filter(pk__gt=self.pk).order_by('pk').first()
=======
        anchor = frame.anchor_source
        next_frame = anchor.frame_from_anchor.filter(pk__gt=self.pk).order_by('pk').first()
        frame.valid=True
        frame.valid_updated_at = datetime.now()
        frame.save()
        return next_frame
>>>>>>> Add user management and API

    @property
    def valid_next(self):
        return Frame.objects.filter(valid=False).filter(pk__gt=self.pk).order_by('pk').first()


class Box(models.Model):
    left = models.DecimalField(max_digits=PRECISION+1, decimal_places=PRECISION)
    top = models.DecimalField(max_digits=PRECISION+1, decimal_places=PRECISION)
    right = models.DecimalField(max_digits=PRECISION+1, decimal_places=PRECISION)
    bottom = models.DecimalField(max_digits=PRECISION+1, decimal_places=PRECISION)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    work_user = models.ForeignKey(User, related_name='worked_box', on_delete=models.CASCADE)
    frame_source = models.OneToOneField(Frame, related_name='box_from_frame', on_delete=models.CASCADE)

    def validate_coordinates(self):
        if self.left >= self.right:
            raise Exception('left >= right')
        elif self.top >= self.bottom:
            raise Exception('top >= bottom')
        self.left = 0 if self.left < 0 else self.left
        self.top = 0 if self.top < 0 else self.top
        self.right = 1 if self.right > 1 else self.right
        self.bottom = 1 if self.bottom > 1 else self.bottom

    def save(self, *args, **kwargs):
        self.validate_coordinates()
        super(Box, self).save(*args, **kwargs)
<<<<<<< HEAD
=======
        self._update_anchor_valid()
>>>>>>> Add user management and API

    def update(self, left, top, right, bottom, **kwargs):
        if not equals(float(self.left), left) or \
                not equals(float(self.top), top) or \
                not equals(float(self.right), right) or \
                not equals(float(self.bottom), bottom):
            self.left = left
            self.top = top
            self.right = right
            self.bottom = bottom
            self.save()

    def __str__(self):
        if self.id:
            return 'B%d' % self.id
        return ''

<<<<<<< HEAD
=======
    def _update_anchor_valid(self):
        box = Box.objects.get(id=self.pk)
        frame = box.frame_source
        anchor = frame.anchor_source
        anchor.valid=True
        anchor.save()
>>>>>>> Add user management and API

class BoxTag(models.Model):
    box = models.ForeignKey(Box, related_name='tags', on_delete=models.CASCADE)
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
<<<<<<< HEAD
=======


class Project(models.Model):
    assigned_user = models.ForeignKey(User,related_name='project', on_delete=models.CASCADE)
    assigned_anchor = models.OneToOneField(Anchor, related_name='project', on_delete=models.CASCADE)
    valid = models.NullBooleanField()

    @property
    def valid_prev(self):
        valid_prev = Project.objects.filter(valid=None).filter(pk__lt=self.pk).order_by('pk').last()
        return valid_prev

    @property
    def valid_next(self):
        valid_next = Project.objects.filter(valid=None).filter(pk__gt=self.pk).order_by('pk').first()
        return valid_next

>>>>>>> Add user management and API
