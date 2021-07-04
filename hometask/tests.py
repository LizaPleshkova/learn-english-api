from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate

from hometask.serializers import HometaskSerializer
from hometask.models import Hometask, CompletedHometask

from hometask.services import HometaskService, UserProgressService
from hometask.views import HometaskView, HometaskUserList, HometaskList, \
    EvaluatedHometask, CompletedHometaskUser, SubmitHometask

User = get_user_model()


class HometaskViewTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='first', password='147123')
        self.user2 = User.objects.create(username='second', password='123147')

        self.user1_token = Token.objects.create(user=self.user1)
        self.user2_token = Token.objects.create(user=self.user2)

        self.hometask1 = Hometask.objects.create(
            task='ДЗ-1',
            description='Это дз-1 для first',
            user=self.user1
        )

        self.hometask2 = Hometask.objects.create(
            task='ДЗ-2',
            description='Это дз-2 для first',
            user=self.user1
        )
        self.hometask3 = Hometask.objects.create(
            task='ДЗ-1',
            description='Это дз-1 для second',
            user=self.user2
        )

        # file_mock = mock.MagicMock(spec=File, name='hometask.txt')
        # self.my_file = open("./file_txt.txt", "w+")
        # self.my_file.write('Hello \n World dfgfgd dfg ')
        # self.my_file.close()
        # self.file_size = os.path.getsize("./file_txt.txt")  # get size file
        # print('file_size', self.file_size)
        #
        # # def __init__(self, file, field_name, name, content_type, size, charset, content_type_extra=None):
        #
        # with open('./file_txt.txt', 'r') as file:
        #     my_files = InMemoryUploadedFile(file, 'file_txt', 'file_txt',
        #                                          'text/plain', self.file_size, 'utf8')

        self.completed_hometask1 = CompletedHometask.objects.create(
            hometask=self.hometask1,
            file_txt=SimpleUploadedFile(name='hometask.txt', content=b'', content_type='text/plain'),
            mark=12,
            completed=True
        )
        self.completed_hometask2 = CompletedHometask.objects.create(
            hometask=self.hometask2,
            file_txt=SimpleUploadedFile(name='hometask.txt', content=b'11', content_type='text/plain'),
            completed=True
        )

        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_hometask_list_invalid_auth(self):
        request = self.factory.get('all-hometask-list')
        response = HometaskList.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_hometask_list_valid_auth(self):
        request = self.factory.get('all-hometask-list')
        force_authenticate(request, user=self.user1, token=self.user1_token)
        response = HometaskList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_hometask_user_list_invalid_auth(self):
        request = self.factory.get('hometask-user-list')
        response = HometaskList.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_hometask_user_list_valid_auth(self):
        request = self.factory.get('hometask-user-list')
        force_authenticate(request, user=self.user1, token=self.user1_token)
        response = HometaskUserList.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

    def test_hometask_user_detail_invalid_auth(self):
        request = self.factory.get('hometask-user-list')
        response = HometaskList.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_hometask_user_detail_valid(self):
        request = self.factory.get(reverse('hometask-user-detail', kwargs={"hometask_id": self.hometask3.id}))
        force_authenticate(request, user=self.user1, token=self.user1_token)
        response = HometaskView.as_view({'get': 'retrieve'})(request, hometask_id=self.hometask1.id)
        self.assertEqual(response.status_code, 200)

    def test_hometask_user_detail_invalid(self):
        request = self.factory.get(reverse('hometask-user-detail', kwargs={"hometask_id": self.hometask3.id}))
        force_authenticate(request, user=self.user1, token=self.user1_token)
        response = HometaskView.as_view({'get': 'retrieve'})(request, hometask_id=self.hometask3.id)
        self.assertEqual(response.status_code, 404)

    def test_submit_hometask_invalid(self):
        data = {
            "file_txt": ""
        }
        view = SubmitHometask.as_view()
        request = self.factory.post('hometask-submit', data, format='json')
        force_authenticate(request, user=self.user2, token=self.user2_token)
        response = view(request, hometask_id=self.hometask3.id)

        response.render()
        self.assertEqual(response.status_code, 412)

    def test_evaluated_hometask_user(self):
        request = self.factory.get('evaluated-hometask')
        force_authenticate(request, user=self.user1, token=self.user1_token)
        response = EvaluatedHometask.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

    def test_completed_hometask_user(self):
        request = self.factory.get('completed-hometask')

        force_authenticate(request, user=self.user1, token=self.user1_token)
        response = CompletedHometaskUser.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, 200)


class HometaskServiceTest(APITestCase, HometaskService, UserProgressService):

    def setUp(self):
        self.user1 = User.objects.create(username='first', password='147123')
        self.user2 = User.objects.create(username='second', password='123147')

        self.user1_token = Token.objects.create(user=self.user1)
        self.user2_token = Token.objects.create(user=self.user2)

        self.hometask1 = Hometask.objects.create(
            task='ДЗ-1',
            description='Это дз-1 для first',
            user=self.user1
        )

        self.hometask2 = Hometask.objects.create(
            task='ДЗ-2',
            description='Это дз-2 для first',
            user=self.user1
        )
        self.hometask3 = Hometask.objects.create(
            task='ДЗ-1',
            description='Это дз-1 для second',
            user=self.user2
        )

        # self.file_mock = mock.MagicMock(spec=File, name='hometask.txt')
        self.completed_hometask1 = CompletedHometask.objects.create(
            hometask=self.hometask1,
            file_txt=SimpleUploadedFile(name='hometask.txt', content=b'', content_type='text/plain'),
            mark=12,
            completed=True
        )
        self.completed_hometask2 = CompletedHometask.objects.create(
            hometask=self.hometask2,
            file_txt=SimpleUploadedFile(name='hometask.txt', content=b'', content_type='text/plain'),
            completed=True,
            mark=5
        )

        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_get_serializer_data(self):
        result = self.get_serializer_data(self.user1, self.hometask1.id)
        ht = Hometask.objects.get(user=self.user1, id=self.hometask1.id)
        serializer = HometaskSerializer(ht)
        self.assertEqual(result, serializer.data)

    #
    def test_average_score_hometask(self):
        self.assertEqual(self.completed_hometask1.completed, True)
        self.assertEqual(self.completed_hometask2.completed, True)

        result = UserProgressService._average_score_hometask(self.user1)

        mark = (self.completed_hometask1.mark + self.completed_hometask2.mark) / 2
        self.assertEqual(result, mark)
