from dateutil.relativedelta import relativedelta
from datetime import date
from django.test import TestCase

from users.models import User, UserSubscription


class UsersModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='user@mail.com', username='user', password='12345')

    def test_user_str_method(self):
        self.assertEqual(str(self.user), 'user')

    def test_user_manager_create_superuser(self):
        superuser = User.objects.create_superuser(email='superuser@mail.com', username='superuser', password='12345')
        self.assertTrue(superuser.is_staff)

    def test_user_manager_create_user_with_no_email(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(email='', username='superuser', password='12345')

        self.assertTrue('Users must have an email address' in str(context.exception))

    def test_user_manager_create_user_with_no_username(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(email='superuser@mail.com', username='', password='12345')

        self.assertTrue('Users must have a username' in str(context.exception))

    def test_user_check_subscription(self):
        self.assertFalse(self.user.is_subscribed())
        paid_cost = UserSubscription.get_cost(months_count=2)
        self.assertEqual(paid_cost, UserSubscription.SUBSCRIPTION_COST * 2)
        self.user.extend_subscription(months_count=2, paid_cost=paid_cost)
        self.assertTrue(self.user.is_subscribed())

    def test_user_extend_subscription(self):
        paid_cost = UserSubscription.get_cost(months_count=2)
        self.assertEqual(paid_cost, UserSubscription.SUBSCRIPTION_COST*2)
        self.user.extend_subscription(months_count=2, paid_cost=paid_cost)
        self.assertTrue(self.user.is_subscribed())

    def test_user_get_end_date_of_subscription(self):
        self.assertIsNone(self.user.get_end_date_of_subscription())
        paid_cost = UserSubscription.get_cost(months_count=2)
        self.assertEqual(paid_cost, UserSubscription.SUBSCRIPTION_COST * 2)
        self.user.extend_subscription(months_count=2, paid_cost=paid_cost)
        self.assertTrue(self.user.is_subscribed())
        end_date = date.today() + relativedelta(months=+2)
        self.assertEqual(self.user.get_end_date_of_subscription(), end_date)

    def test_user_subscription_check_cost(self):
        one_month_cost = UserSubscription.SUBSCRIPTION_COST
        self.assertEqual(UserSubscription.get_cost(months_count=1), one_month_cost)
        self.assertEqual(UserSubscription.get_cost(months_count=3),
                         round(3 * one_month_cost * UserSubscription.DEPRECIATION_FOR_THREE_MONTHS, 2))
        self.assertEqual(UserSubscription.get_cost(months_count=7),
                         round(7 * one_month_cost * UserSubscription.DEPRECIATION_FOR_SIX_MONTHS, 2))
        self.assertEqual(UserSubscription.get_cost(months_count=14),
                         round(14 * one_month_cost * UserSubscription.DEPRECIATION_FOR_TWELVE_MONTHS, 2))
