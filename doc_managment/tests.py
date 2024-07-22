from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import RefBook, RefBookVersion, RefBookElement
from datetime import datetime


class RefBookAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.refbook1 = RefBook.objects.create(code='001', name='Справочник 1')
        self.refbook2 = RefBook.objects.create(code='002', name='Справочник 2')

        self.version1 = RefBookVersion.objects.create(refbook=self.refbook1, version='1.0', start_date=datetime.now())
        self.version2 = RefBookVersion.objects.create(refbook=self.refbook1, version='2.0', start_date='2023-06-01')

        self.element1 = RefBookElement.objects.create(refbook_version=self.version1, code='001', value='Элемент 1')
        self.element2 = RefBookElement.objects.create(refbook_version=self.version2, code='002', value='Элемент 2')

    def test_get_refbooks(self):
        url = reverse('refbook-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['refbooks']), 2)

        response = self.client.get(url, {'date': datetime.now().strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['refbooks']), 1)

    def test_get_refbook_elements(self):
        url = reverse('refbook-elements', kwargs={'id': self.refbook1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['elements']), 1)

        response = self.client.get(url, {'version': '1.0'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['elements']), 1)

    def test_check_refbook_element(self):
        url = reverse('refbook-check-element', kwargs={'id': self.refbook1.id})
        response = self.client.get(url, {'code': '001', 'value': 'Элемент 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['exists'])

        response = self.client.get(url, {'code': '002', 'value': 'Элемент 2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['exists'])

    def test_get_refbook_elements_with_optional_parameters(self):
        url = reverse('refbook-elements', kwargs={'id': self.refbook1.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['elements']), 1)
        self.assertEqual(response.data['elements'][0]['code'], '001')

        response = self.client.get(url, {'version': '2.0'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['elements']), 1)
        self.assertEqual(response.data['elements'][0]['code'], '002')

    def test_check_refbook_element_with_optional_parameters(self):
        url = reverse('refbook-check-element', kwargs={'id': self.refbook1.id})

        response = self.client.get(url, {'code': '001', 'value': 'Элемент 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['exists'])

        response = self.client.get(url, {'code': '002', 'value': 'Элемент 2', 'version': '2.0'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['exists'])

        response = self.client.get(url, {'code': '002', 'value': 'Элемент 2', 'version': '1.0'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['exists'])
