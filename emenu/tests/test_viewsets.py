import random
from collections import Counter
from datetime import time
from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from emenu.models import Dish, DishCard

DISH_VALID_DICTS = (
    dict(name='Schabowy', description='Kotlet schabowy z surówką z kapusty kiszonej.', price=Decimal('25.0'),
         prep_time=time(minute=20)),
    dict(name='Omlet', description='Cienki placek z jajek.', price=Decimal('15.0'), prep_time=time(minute=15),
         vegetarian=True),
    dict(name='Schabowy45', description='123Kotlet schabowy z surówką z kapusty kiszonej.321',
         price=Decimal('199.0'), prep_time=time(1, 20, 30)),
    dict(name='Omlet123', description='321Cienki placek z jajek.123', price=Decimal('601.54'), prep_time=time(8, 3),
         vegetarian=True),
    dict(name='#$%^&*()*&^%$', description='(*&^%Opisopispnfjdslfjs%^&*)', price=Decimal('9999.99'),
         prep_time=time(23, 59, 59, 999999), vegetarian=True),
    dict(name='TGHNO(*&Uik776ythj', description='ALE SMACZNE!!!!!!!!1111', price=Decimal('0.01'),
         prep_time=time(0, 0, 0, 1))
)

DISH_CARD_VALID_DICTS = (
    dict(name='Menu 1', description='Standardowe menu restauracji.'),
    dict(name='Menu 2', description='Alternatywne menu restauracji.'),
    dict(name='MENUE', description='Menue dziwnej restauracji.'),
    dict(name='%^&*(IJYTT%^TGHJk76tyhjkliewt90g4wergfk', description='sdvghtfjyfktrdy75r7ttttk6u45*&^&UIRTGH^y.'),
    dict(name='YUJMIgjbbjdfg.eroiyg5', description='Standardowe menu restauracji.'),
    dict(name='1', description='Standardowe menu fast fooda.'),
)


class BaseTest(APITestCase):
    def setUp(self):
        self.rand_idx = list(range(6))
        random.shuffle(self.rand_idx)
        self.dish1 = Dish.objects.create(**DISH_VALID_DICTS[self.rand_idx[0]])
        self.dish2 = Dish.objects.create(**DISH_VALID_DICTS[self.rand_idx[1]])

    def _test_query(self, resource, http_method, pk, status_code, data=None):
        response = getattr(self.client, http_method)(f'/{resource}/{pk}/', data)
        self.assertEqual(response.status_code, status_code)
        return response

    def _test_get(self, resource, pk, status_code):
        response = self._test_query(resource, "get", pk, status_code)
        c = Counter(response.data.keys())
        self.assertEqual(c['id'], not c['detail'])


class DishRouteTest(BaseTest):
    def test_dish_list(self):
        response = self.client.get('/dishes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dish.objects.count(), 2)

    def test_dish_get_valid(self):
        dish1_pk = Dish.objects.get(name=self.dish1.name).pk
        self._test_get("dishes", dish1_pk, status.HTTP_200_OK)

        dish2_pk = Dish.objects.get(name=self.dish2.name).pk
        self._test_get("dishes", dish2_pk, status.HTTP_200_OK)

    def test_dish_get_invalid(self):
        dish1_pk = Dish.objects.get(name=self.dish1.name).pk
        self._test_get("dishes", dish1_pk + 50, status.HTTP_404_NOT_FOUND)
        self._test_get("dishes", "dish2_pk", status.HTTP_404_NOT_FOUND)

    def test_dish_patch_valid(self):
        dish1_pk = Dish.objects.get(name=self.dish1.name).pk
        dish2_pk = Dish.objects.get(name=self.dish2.name).pk
        self._test_query("dishes", "patch", dish1_pk, status.HTTP_200_OK, {"description": "Zmieniony opis."})
        self._test_query("dishes", "patch", dish2_pk, status.HTTP_200_OK, {"name": "Ziemniak"})

    def test_dish_patch_invalid(self):
        dish1_pk = Dish.objects.get(name=self.dish1.name).pk
        dish2_pk = Dish.objects.get(name=self.dish2.name).pk
        self._test_query("dishes", "patch", dish1_pk, status.HTTP_400_BAD_REQUEST,
                         {"description": "", "price": "dbg234"})
        self._test_query("dishes", "patch", dish2_pk, status.HTTP_400_BAD_REQUEST,
                         {"name": "", "prep_time": "", "vegeterian": None})

    def test_dish_put_valid(self):
        dish1_pk = Dish.objects.get(name=self.dish1.name).pk
        dish2_pk = Dish.objects.get(name=self.dish2.name).pk
        self._test_query("dishes", "put", dish1_pk, status.HTTP_200_OK, DISH_VALID_DICTS[self.rand_idx[2]])
        self._test_query("dishes", "put", dish2_pk, status.HTTP_200_OK, DISH_VALID_DICTS[self.rand_idx[3]])

    def test_dish_put_invalid(self):
        dish1_pk = Dish.objects.get(name=self.dish1.name).pk
        dish2_pk = Dish.objects.get(name=self.dish2.name).pk
        self._test_query("dishes", "put", dish1_pk, status.HTTP_400_BAD_REQUEST,
                         dict(name='Owsianka', description='Danie z owsu.', price=Decimal('10.0')))
        self._test_query("dishes", "put", dish2_pk, status.HTTP_400_BAD_REQUEST,
                         dict(name='Antrykot', price=Decimal('30.0'), prep_time=time(minute=40)))

    def test_dish_delete_valid(self):
        dish1_pk = Dish.objects.get(name=self.dish1.name).pk
        dish2_pk = Dish.objects.get(name=self.dish2.name).pk
        self._test_query("dishes", "delete", dish1_pk, status.HTTP_204_NO_CONTENT)
        self._test_query("dishes", "delete", dish2_pk, status.HTTP_204_NO_CONTENT)

    def test_dish_delete_invalid(self):
        dish1_pk = Dish.objects.get(name=self.dish1.name).pk
        dish2_pk = Dish.objects.get(name=self.dish2.name).pk
        self._test_query("dishes", "delete", dish1_pk + 50, status.HTTP_404_NOT_FOUND)
        self._test_query("dishes", "delete", dish2_pk + 60, status.HTTP_404_NOT_FOUND)

    def test_dish_post_valid(self):
        response_1 = self.client.post(f'/dishes/', DISH_VALID_DICTS[self.rand_idx[2]])
        response_2 = self.client.post(f'/dishes/', DISH_VALID_DICTS[self.rand_idx[3]])
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)

    def test_dish_post_invalid(self):
        response_1 = self.client.post(
            f'/dishes/',
            dict(name='', description='(*&^%Opisopispnfjdslfjs%^&*)', price=Decimal('9999.99'),
                 prep_time=time(23, 59, 59, 999999), vegetarian=True))
        response_2 = self.client.post(
            f'/dishes/',
            dict(name='#$%^&*()*&^%$', description='', price=Decimal('9999.99'),
                 prep_time=time(23, 59, 59, 999999), vegetarian=True)
        )
        response_3 = self.client.post(
            f'/dishes/', dict(name='#$%^&*()*&^%$', description='', prep_time=time(23, 59, 59, 999999), vegetarian=True)
        )
        response_4 = self.client.post(
            f'/dishes/',
            dict(name='TGHNO(*&Uik776ythj', description='ALE SMACZNE!!!!!!!!1111', price=Decimal('0.01'))
        )
        response_5 = self.client.post(
            f'/dishes/',
            dict(name='TGHNO(*&Uik776ythj', description='ALE SMACZNE!!!!!!!!1111', price=Decimal('0.01'),
                 prep_time=time(23, 59, 59, 999999), vegetarian=None)
        )
        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_4.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_5.status_code, status.HTTP_400_BAD_REQUEST)


class DishCardRouteTest(BaseTest):
    def setUp(self):
        super(DishCardRouteTest, self).setUp()
        self.dish_card1 = DishCard.objects.create(**DISH_CARD_VALID_DICTS[self.rand_idx[0]])
        self.dish_card1.dishes.add(self.dish1, self.dish2)

        self.dish_card2 = DishCard.objects.create(**DISH_CARD_VALID_DICTS[self.rand_idx[1]])
        self.dish_card2.dishes.create(**DISH_VALID_DICTS[self.rand_idx[2]])
        self.dish_card2.dishes.create(**DISH_VALID_DICTS[self.rand_idx[3]])

    def test_dish_card_list(self):
        response = self.client.get('/dish_cards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DishCard.objects.count(), 2)

    def test_dish_card_get_valid(self):
        self._test_get('dish_cards', self.dish_card1.pk, status.HTTP_200_OK)
        self._test_get('dish_cards', self.dish_card2.pk, status.HTTP_200_OK)

    def test_dish_card_get_invalid(self):
        self._test_get('dish_cards', self.dish_card1.pk + 50, status.HTTP_404_NOT_FOUND)
        self._test_get('dish_cards', 'dish_cards', status.HTTP_404_NOT_FOUND)

    def test_dish_card_patch_valid(self):
        self._test_query("dish_cards", "patch", self.dish_card1.pk, status.HTTP_200_OK,
                         {"description": "Zmieniony opis.", "name": "1234567"})
        self._test_query("dish_cards", "patch", self.dish_card2.pk, status.HTTP_200_OK, {"name": "Ziemniak"})

    def test_dish_card_patch_invalid(self):
        self._test_query("dish_cards", "patch", self.dish_card1.pk, status.HTTP_400_BAD_REQUEST,
                         {"description": "", "name": ""})
        self._test_query("dish_cards", "patch", self.dish_card2.pk, status.HTTP_400_BAD_REQUEST,
                         {"description": "", "dishes": [DISH_VALID_DICTS[self.rand_idx[4]]]})
        self._test_query("dish_cards", "patch", self.dish_card1.pk, status.HTTP_400_BAD_REQUEST, {"dishes": [12354]})
        self._test_query("dish_cards", "patch", self.dish_card1.pk, status.HTTP_400_BAD_REQUEST, {"name": ""})

    def test_dish_card_put_valid(self):
        self._test_query("dish_cards", "put", self.dish_card1.pk, status.HTTP_200_OK,
                         {**DISH_CARD_VALID_DICTS[self.rand_idx[2]], "dishes": [DISH_VALID_DICTS[self.rand_idx[4]]]})
        self._test_query("dish_cards", "put", self.dish_card1.pk, status.HTTP_200_OK,
                         {**DISH_CARD_VALID_DICTS[self.rand_idx[3]], "dishes": [DISH_VALID_DICTS[self.rand_idx[5]]]})

    def test_dish_card_put_invalid(self):
        self._test_query("dish_cards", "put", self.dish_card1.pk, status.HTTP_400_BAD_REQUEST,
                         {**DISH_CARD_VALID_DICTS[self.rand_idx[2]], "dishes": [124]})
        self._test_query("dish_cards", "put", self.dish_card1.pk, status.HTTP_400_BAD_REQUEST,
                         {"name": "", "description": "ery456yhrt", "dishes": []})
        self._test_query("dish_cards", "put", self.dish_card1.pk, status.HTTP_400_BAD_REQUEST,
                         {"name": "dhdrtj", "description": "", "dishes": [DISH_VALID_DICTS[3]]})

    def test_dish_card_delete_valid(self):
        self._test_query("dish_cards", "delete", self.dish_card1.pk, status.HTTP_204_NO_CONTENT)

    def test_dish_card_delete_invalid(self):
        self._test_query("dish_cards", "delete", self.dish_card2.pk + 50, status.HTTP_404_NOT_FOUND)

    def test_dish_card_post_valid(self):
        response_1 = self.client.post(f'/dish_cards/', DISH_CARD_VALID_DICTS[self.rand_idx[2]])
        response_2 = self.client.post(f'/dish_cards/', DISH_CARD_VALID_DICTS[self.rand_idx[3]])
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)

    def test_dish_card_post_invalid(self):
        response_1 = self.client.post(f'/dish_cards/', dict(name='', description='Standardowe menu restauracji.'))
        response_2 = self.client.post(f'/dish_cards/', dict(name='Menu 1'))
        response_3 = self.client.post(
            f'/dish_cards/', dict(name='Menu 1', description='Standardowe menu restauracji.', dishes=[342543]))
        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_3.status_code, status.HTTP_400_BAD_REQUEST)
