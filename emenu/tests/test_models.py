from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from datetime import time

from ..models import Dish, DishCard


def create_dishes():
    dish1 = Dish.objects.create(
        name='Schabowy', description='Kotlet schabowy z surówką z kapusty kiszonej.', price=25.0,
        prep_time=time(minute=20))
    dish2 = Dish.objects.create(
        name='Omlet', description='Cienki placek z jajek.', price=15.0, prep_time=time(minute=15), vegetarian=True)

    return dish1, dish2


class DishTest(TestCase):
    """ Test module for Dish model """

    PREP_TIME_REGEX = r'^((?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$)'
    PREP_TIME_MIN = time(0, 0, 0, 1)
    PREP_TIME_MAX = time(23, 59, 59, 999999)

    def setUp(self):
        create_dishes()

        self.valid_payload = {

        }

    def test_dish_name_max_size(self):
        dish_schabowy = Dish.objects.get(name='Schabowy')
        dish_omlet = Dish.objects.get(name='Omlet')
        name_schab = dish_schabowy.name
        name_omlet = dish_omlet.name
        self.assertLessEqual(len(name_schab), 255)
        self.assertLessEqual(len(name_omlet), 255)

    def test_dish_name_is_required(self):
        with self.assertRaises(ValidationError):
            Dish.objects.create(
                description='Kotlet schabowy z surówką z kapusty kiszonej.', price=25.0, prep_time=time(minute=20))

    def test_dish_name_is_string(self):
        dish_schabowy = Dish.objects.get(name='Schabowy')
        dish_omlet = Dish.objects.get(name='Omlet')
        name_schab = dish_schabowy.name
        name_omlet = dish_omlet.name
        self.assertIsInstance(name_schab, str)
        self.assertIsInstance(name_omlet, str)

    def test_dish_description_is_required(self):
        with self.assertRaises(ValidationError):
            Dish.objects.create(name='Omlet', price=15.0, prep_time=time(minute=15), vegetarian=True)

    def test_dish_description_is_string(self):
        dish_schabowy = Dish.objects.get(name='Schabowy')
        dish_omlet = Dish.objects.get(name='Omlet')
        desc_schab = dish_schabowy.description
        desc_omlet = dish_omlet.description
        self.assertIsInstance(desc_schab, str)
        self.assertIsInstance(desc_omlet, str)

    def test_dish_price_is_required(self):
        with self.assertRaises(ValidationError):
            Dish.objects.create(
                name='Schabowy', description='Kotlet schabowy z surówką z kapusty kiszonej.', prep_time=time(minute=20))

    def test_dish_price_is_decimal(self):
        dish_schabowy = Dish.objects.get(name='Schabowy')
        dish_omlet = Dish.objects.get(name='Omlet')
        self.assertIsInstance(dish_schabowy.price, Decimal)
        self.assertIsInstance(dish_omlet.price, Decimal)

    def test_dish_price_max_value(self):
        dish_schabowy = Dish.objects.get(name='Schabowy')
        dish_omlet = Dish.objects.get(name='Omlet')
        self.assertLessEqual(dish_schabowy.price, Decimal(9999.99))
        self.assertLessEqual(dish_omlet.price, Decimal(9999.99))

    def test_dish_prep_time_regex(self):
        dish_schabowy = Dish.objects.get(name='Schabowy')
        dish_bigos = Dish.objects.get(name='Omlet')
        prep_time_schab = dish_schabowy.prep_time
        prep_time_bigos = dish_bigos.prep_time
        self.assertRegex(str(prep_time_schab), self.PREP_TIME_REGEX)
        self.assertRegex(str(prep_time_bigos), self.PREP_TIME_REGEX)

    def test_dish_prep_time_is_time(self):
        dish_schabowy = Dish.objects.get(name='Schabowy')
        dish_bigos = Dish.objects.get(name='Omlet')
        prep_time_schab = dish_schabowy.prep_time
        prep_time_bigos = dish_bigos.prep_time
        self.assertIsInstance(prep_time_schab, time)
        self.assertIsInstance(prep_time_bigos, time)

    def test_dish_prep_time_min(self):
        dish_schabowy = Dish.objects.get(name='Schabowy')
        dish_bigos = Dish.objects.get(name='Omlet')
        prep_time_schab = dish_schabowy.prep_time
        prep_time_bigos = dish_bigos.prep_time
        self.assertGreaterEqual(prep_time_schab, self.PREP_TIME_MIN)
        self.assertGreaterEqual(prep_time_bigos, self.PREP_TIME_MIN)

    def test_dish_prep_time_max(self):
        dish_schabowy = Dish.objects.get(name='Schabowy')
        dish_bigos = Dish.objects.get(name='Omlet')
        prep_time_schab = dish_schabowy.prep_time
        prep_time_bigos = dish_bigos.prep_time
        self.assertLessEqual(prep_time_schab, self.PREP_TIME_MAX)
        self.assertLessEqual(prep_time_bigos, self.PREP_TIME_MAX)

    def test_dish_vegetarian_is_false_default(self):
        Dish.objects.create(
            name="Schabowy_2", description='Kotlet schabowy z surówką z kapusty kiszonej.', price=25.0,
            prep_time=time(minute=20))
        dish_schabowy = Dish.objects.get(name='Schabowy_2')
        self.assertEqual(dish_schabowy.vegetarian, False)

    def test_dish_vegetarian_is_bool(self):
        dish_schabowy = Dish.objects.get(name='Schabowy')
        dish_bigos = Dish.objects.get(name='Omlet')
        vege_schab = dish_schabowy.vegetarian
        vege_bigos = dish_bigos.vegetarian
        self.assertIsInstance(vege_schab, bool)
        self.assertIsInstance(vege_bigos, bool)


class DishCardTest(TestCase):
    """ Test module for Dish model """

    def setUp(self):
        dish1, dish2 = create_dishes()

        dish_card = DishCard.objects.create(name='Karta dań', description='Karta polskich dań.')
        dish_card.dishes.add(dish1, dish2)

    def test_dish_card_name_is_required(self):
        with self.assertRaises(ValidationError):
            DishCard.objects.create(description='Karta dań różnych')

    def test_dish_card_description_is_required(self):
        with self.assertRaises(ValidationError):
            DishCard.objects.create(name='Karta dań')
