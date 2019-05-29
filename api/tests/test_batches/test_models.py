from decimal import Decimal
from random import choice

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from api.models import Batch
from api.tests.testingutils.factory import (create_batch, create_order,
                                            create_user)


class BatchTestCase(TestCase):
    def setUp(self):
        self.user = create_user(
            username='mauro',
            email='mauro@python.com',
            password='123456',
        )

        names = ['São Clênio', 'São Firmino', 'São Esmeraldino']

        self.order_1 = create_order(
            reference='BR123',
            purchase_channel='Dong123',
            client_name=choice(names),
            address='Av. Amintas Barros Nº 3700 - Torre Business, Sala 702 - Lagoa Nova CEP: 59075-250',
            delivery_service='SEDEX',
            total_value=Decimal(123.30),
            line_items='[{sku: case-my-best-friend, model: iPhone X, case type: Rose Leather}, {sku: powebank-sunshine, capacity: 10000mah}, {sku: earphone-standard, color: white}]',
            user=self.user
        )

        self.order_2 = create_order(
            reference='BR123',
            purchase_channel='Dong123',
            client_name=choice(names),
            address='Av. Amintas Barros Nº 3700 - Torre Business, Sala 702 - Lagoa Nova CEP: 59075-250',
            delivery_service='SEDEX',
            total_value=Decimal(123.30),
            line_items='[{sku: case-my-best-friend, model: iPhone X, case type: Rose Leather}, {sku: powebank-sunshine, capacity: 10000mah}, {sku: earphone-standard, color: white}]',
            user=self.user
        )

        self.orders = [self.order_1, self.order_2]

    def test_create_batch(self):
        batch = create_batch(
            reference='BR123',
            purchase_channel='Dong123',
            user=self.user,
        )

        batch.orders.set(self.orders)
        batch.save()

        self.assertEqual(batch.user, self.user)
        self.assertEqual(batch.reference, 'BR123')
        self.assertEqual(batch.purchase_channel, 'Dong123')
        self.assertEqual(len(batch.orders.all()), 2)

    def test_update_batch(self):
        batch = create_batch(
            reference='BR123',
            purchase_channel='Dong123',
            user=self.user,
        )

        batch.orders.set(self.orders)
        batch.save()

        new_order = create_order(
            reference='BR123',
            purchase_channel='Dong123',
            client_name='Marinaldo',
            address='Av. Amintas Barros Nº 3700 - Torre Business, Sala 702 - Lagoa Nova CEP: 59075-250',
            delivery_service='SEDEX',
            total_value=Decimal(123.30),
            line_items='[{sku: case-my-best-friend, model: iPhone X, case type: Rose Leather}, {sku: powebank-sunshine, capacity: 10000mah}, {sku: earphone-standard, color: white}]',
            user=self.user
        )

        batch.reference = 'BR321'
        batch.purchase_channel = 'Dong321'
        batch.orders.add(new_order)
        batch.save()

        self.assertEqual(batch.user, self.user)

        self.assertNotEqual(batch.reference, 'BR123')
        self.assertEqual(batch.reference, 'BR321')
        self.assertNotEqual(batch.purchase_channel, 'Dong123')
        self.assertEqual(batch.purchase_channel, 'Dong321')
        self.assertNotEqual(len(batch.orders.all()), 2)
        self.assertEqual(len(batch.orders.all()), 3)

    def test_delete_batch(self):
        batch = create_batch(
            reference='BR123',
            purchase_channel='Dong123',
            user=self.user,
        )

        batch.orders.set(self.orders)
        batch.save()

        batch.delete()

        with self.assertRaises(ObjectDoesNotExist):
            batch = Batch.objects.get(
                reference='BR123',
                purchase_channel='Dong123',
            )

