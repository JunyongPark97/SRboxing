import json
import pandas as pd
from scipy import ndimage
from PIL import Image
import requests
from io import BytesIO
from tqdm import tqdm
from collections import Counter
<<<<<<< HEAD


from qanda.ocr.models import *
from qbase.models import *

from Sean_boxing.models import Anchor, QBQ, CandidateInfo

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
=======
from qanda.ocr.models import *
from qbase.models import *
from Sean_boxing.models import *
from Sean_boxing.models import Anchor, QBQ

book_lst = \
    [
        'SSEN중등수학3하',
>>>>>>> Add user management and API
    ]


def resize_img(img):
    width = img.size[0]
    height = img.size[1]

    if width >= height:
        baseheight = 200
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseheight), Image.ANTIALIAS)

    else:
        basewidth = 200
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)

    return img


def check_include_img(qbase_id):
    text = ""

    for ia in QBaseQuestion.objects.get(id=qbase_id).images.first().annotations.all():

        if ia.processor_name == 'google_fullTextAnnotation':
            text += ia.data['text']

        if ia.processor_name == 'google_textAnnotations':
            text += ia.data[0]['description']

    if '그림' in text:
        return True

    else:
        return False


def request_drip(image_url):
    request_options = [
        {
            'backend': 'google_vision',
            'version': 1,
            'use_cache': True,
        }
    ]

    data = {
        'image_url': image_url,
        'requests': request_options,
    }

    try:
        result = json.loads(requests.post(  # Request / Post method
            'http://drip-server-production.ap-northeast-2.elasticbeanstalk.com/api/image:processParallel',
            json=data).text)

    except:
        result = None

    return result[0]


def detect_rotation(ocr_search_request_id):
    def _detect_rotation_candidate(annotation):

        top_left, top_right, bottom_right, bottom_left = annotation['boundingPoly']['vertices']

        try:
            horizontal_direction = bottom_right.get('x') - top_left.get('x')
            vertical_direction = bottom_right.get('y') - top_left.get('y')

            # diagonal vector direction
            if horizontal_direction > 0 and vertical_direction > 0:
                return 0

            elif horizontal_direction < 0 and vertical_direction > 0:
                return 90

            elif horizontal_direction < 0 and vertical_direction < 0:
                return 180

            elif horizontal_direction > 0 and vertical_direction < 0:
                return 270

            else:
                return 0

        except:
            return 0

    sr = OCRSearchRequest.objects.get(id=ocr_search_request_id)
    annotations = \
    request_drip(OCRSearchRequest.objects.get(id=ocr_search_request_id).image_key.url)['data']['responses'][0]['textAnnotations']
    rotation_candidates = [_detect_rotation_candidate(annot) for annot in annotations[:15]]
    rotation_angle = Counter(rotation_candidates).most_common()[0][0]

    return rotation_angle


def rotate_img(img, sr_id):
    width = img.size[0]
    height = img.size[1]
    rotation_angle = 0

    if height > width:
        rotation_angle = detect_rotation(sr_id)
        img = ndimage.rotate(img, rotation_angle)
        img = Image.fromarray(img)

    return img, rotation_angle


def download_image_sim_data():
    ERROR_COUNT = 0

    qs = QBaseQuestion.objects \
        .filter(captured_question__isnull=True) \
        .filter(barista_question__isnull=False) \
        .filter(barista_question__container__container_type=2) \
        .filter(barista_question__container__subject_id__lt=6) \
        .values('id', 'barista_question__uuid', 'barista_question__container__id',
<<<<<<< HEAD
                'barista_question__container__title')[1001:7000]
=======
                'barista_question__container__title')
>>>>>>> Add user management and API

    df = pd.DataFrame(list(qs))
    df = df.query('barista_question__container__title.isin({})'.format(book_lst))# ?
    df = df.sort_values('barista_question__container__title')
    dd = df.to_json(orient='records', default_handler=str)
<<<<<<< HEAD
    da = json.loads(dd)# 여기까지는 book_lst 안에 있는 문제들(from book_lst)


    anchor_ids=[]
=======
    da = json.loads(dd)

    ii=0
>>>>>>> Add user management and API
    for i in da:
        if check_include_img(i['id']):
            uuid = i['barista_question__uuid']
            url = QBaseQuestion.objects.filter(barista_question__uuid=uuid)[
                0].images.all().first().image_url
            book_title = i['barista_question__container__title']
            book_id = i['barista_question__container__id']
<<<<<<< HEAD
=======
            ii+=1
            print('===',ii)
>>>>>>> Add user management and API
            QBQ.objects.create(QBaseQuestion_id=i['id'],
                                      image_url=url,
                                      book_title=book_title,
                                      book_id=book_id)


<<<<<<< HEAD
            anchor_ids.append(i['id'])


            for anchor_id in anchor_ids:
                candidates_qs = OCRSearchRequest.objects.filter(ocr_question_logs__qbase_question_id=anchor_id)[:5]

                for candidate in candidates_qs:
                    print(candidate)
                    anchor_obj = Anchor.objects.get(QBaseQuestion_id=anchor_id)#pk?? 만약에 anchor가 2개 이상이면? 여러개의 사진이 있을때
                    # """
                    # Qbase-id는 겹치니까 pk로 저장해야 한다...
                    # """
                    CandidateInfo.objects.create(origin_anchor=anchor_obj,
                                              OCRSearchRequest_id=candidate.id,
                                              image_key=candidate.image_key)
                    # candi = Candidates.objects.last()
                    # candi.save()


    for _, each_row in tqdm(df.iterrows(), total=len(df), ncols=40):
        if check_include_img(each_row.id):# 이걸 통해서 '그림'이라는 말이 들어간 문제들 거르기
            #그 다음 qsa에서 걸러진 anchor문제들에 대해 candidates 생성 :50개씩
            qsa = OCRSearchRequest.objects.filter(ocr_question_logs__qbase_question_id__in=[each_row.id])[:10]
            for q in qsa:

                response = requests.get(q.image_key.url)
                img = Image.open(BytesIO(response.content))
                img = resize_img(img)
                img, rotation_angle = rotate_img(img, q.id)


            # ERROR_COUNT += 1
            # print("ERROR OCCURS : # of Error {}".format(ERROR_COUNT))
            # continue


if __name__ == '__main__':
    download_image_sim_data()
=======

def request_box(image_url):
#default box를 칠 수 있는 API 입니다.
   data = {
       'image_url': image_url,
   }

   try:
       result = json.loads(
           requests.post( 'http://125.129.239.235:14025/api/similar/', data=data).text)

   except:
       result = None

   return result['boxes']

request_box('http://qanda-storage.s3.amazonaws.com/9af819bf-7d79-4519-9f78-a3f77c12d6fa.jpg')

# if __name__ == '__main__':
#     download_image_sim_data()
>>>>>>> Add user management and API
