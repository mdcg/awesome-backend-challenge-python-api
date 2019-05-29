from decimal import Decimal

from django.test import TestCase

from api.models import Order
from api.tests.testingutils.factory import create_user, create_order
from django.core.exceptions import ObjectDoesNotExist


class OrderTestCase(TestCase):
    def setUp(self):
        self.user = create_user(
            username='mauro',
            email='mauro@python.com',
            password='123456',
        )

    def test_create_order(self):
        create_order(
            reference='BR102030',
            purchase_channel='Site BR',
            client_name='São Clênio',
            address='Av. Amintas Barros Nº 3700 - Torre Business, Sala 702 - Lagoa Nova CEP: 59075-250',
            delivery_service='SEDEX',
            total_value=Decimal(123.30),
            line_items='[{sku: case-my-best-friend, model: iPhone X, case type: Rose Leather}, {sku: powebank-sunshine, capacity: 10000mah}, {sku: earphone-standard, color: white}]',
            user=self.user
        )

        order = Order.objects.get(
            reference='BR102030',
            client_name='São Clênio',
        )

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.delivery_service, 'SEDEX')
        self.assertAlmostEqual(order.total_value, Decimal(123.30))

    def test_update_order(self):
        create_order(
            reference='BR102030',
            purchase_channel='Site BR',
            client_name='São Clênio',
            address='Av. Amintas Barros Nº 3700 - Torre Business, Sala 702 - Lagoa Nova CEP: 59075-250',
            delivery_service='SEDEX',
            total_value=Decimal(123.30),
            line_items='[{sku: case-my-best-friend, model: iPhone X, case type: Rose Leather}, {sku: powebank-sunshine, capacity: 10000mah}, {sku: earphone-standard, color: white}]',
            user=self.user
        )

        order = Order.objects.get(
            reference='BR102030',
            client_name='São Clênio',
        )

        order.reference = 'BR102031'
        order.purchase_channel = 'Site NA'
        order.client_name = 'São Joaquim'
        order.save()

        self.assertNotEqual(order.reference, 'BR102030')
        self.assertEqual(order.reference, 'BR102031')
        self.assertNotEqual(order.purchase_channel, 'Site BR')
        self.assertEqual(order.purchase_channel, 'Site NA')
        self.assertNotEqual(order.client_name, 'São Clênio')
        self.assertEqual(order.client_name, 'São Joaquim')

    def test_delete_order(self):
        create_order(
            reference='BR102030',
            purchase_channel='Site BR',
            client_name='São Clênio',
            address='Av. Amintas Barros Nº 3700 - Torre Business, Sala 702 - Lagoa Nova CEP: 59075-250',
            delivery_service='SEDEX',
            total_value=Decimal(123.30),
            line_items='[{sku: case-my-best-friend, model: iPhone X, case type: Rose Leather}, {sku: powebank-sunshine, capacity: 10000mah}, {sku: earphone-standard, color: white}]',
            user=self.user
        )

        order = Order.objects.get(
            reference='BR102030',
            client_name='São Clênio',
        )

        order.delete()

        with self.assertRaises(ObjectDoesNotExist):
            order = Order.objects.get(
                reference='BR102030',
                client_name='São Clênio',
            )
