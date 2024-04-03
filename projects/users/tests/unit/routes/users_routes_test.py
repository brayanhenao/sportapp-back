import json
import unittest

from unittest.mock import patch, MagicMock

from faker import Faker

from app.models.schemas.schema import UserAdditionalInformation, UserCreate
from app.routes import users_routes
from app.utils.user_cache import UserCache
from app.models.users import UserIdentificationType, Gender

fake = Faker()


class TestUsersRoutes(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        UserCache.users = []
        UserCache.users_with_errors_by_email_map = {}
        UserCache.users_success_by_email_map = {}

    async def test_register_user(self):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        password = f"{fake.password()}A123!"

        user_data = {"first_name": first_name, "last_name": last_name, "email": email, "password": password}

        user_create = UserCreate(**user_data)

        UserCache.users_success_by_email_map = {email: user_data}
        response = await users_routes.register_user(user_create)
        async_gen = response.body_iterator

        async for data in async_gen:
            self.assertEqual(data.strip(), "User created")
            break

        self.assertEqual(len(UserCache.users), 1)
        self.assertEqual(UserCache.users[0].first_name, first_name)
        self.assertEqual(UserCache.users[0].last_name, last_name)
        self.assertEqual(UserCache.users[0].email, email)
        self.assertEqual(UserCache.users[0].password, password)
        self.assertEqual(len(UserCache.users_success_by_email_map), 0)

    async def test_register_user_email_repeated(self):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        password = f"{fake.password()}A123!"

        user_data = {"first_name": first_name, "last_name": last_name, "email": email, "password": password}

        user_create = UserCreate(**user_data)

        UserCache.users_with_errors_by_email_map = {email: user_data}
        response = await users_routes.register_user(user_create)
        async_gen = response.body_iterator

        async for data in async_gen:
            self.assertEqual(data.strip(), "User already exists")
            break

        self.assertEqual(len(UserCache.users), 1)
        self.assertEqual(UserCache.users[0].first_name, first_name)
        self.assertEqual(UserCache.users[0].last_name, last_name)
        self.assertEqual(UserCache.users[0].email, email)
        self.assertEqual(UserCache.users[0].password, password)
        self.assertEqual(len(UserCache.users_with_errors_by_email_map), 0)

    async def test_register_user_processing(self):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        password = f"{fake.password()}A123!"

        user_data = {"first_name": first_name, "last_name": last_name, "email": email, "password": password}

        user_create = UserCreate(**user_data)

        response = await users_routes.register_user(user_create)
        async_gen = response.body_iterator
        max_loops = 3

        async for data in async_gen:
            self.assertEqual(data.strip(), "Processing...")
            max_loops -= 1
            if max_loops == 0:
                break
        self.assertEqual(UserCache.users[0].first_name, first_name)
        self.assertEqual(UserCache.users[0].last_name, last_name)
        self.assertEqual(UserCache.users[0].email, email)
        self.assertEqual(UserCache.users[0].password, password)
        self.assertEqual(len(UserCache.users_success_by_email_map), 0)
        self.assertEqual(len(UserCache.users_with_errors_by_email_map), 0)

    @patch("app.services.users.UsersService.complete_user_registration")
    async def test_complete_user_registration(self, complete_user_registration):
        user_id = fake.uuid4()
        identification_type = fake.enum(UserIdentificationType).value
        identification_number = fake.numerify(text="############")
        gender = fake.enum(Gender).value
        country_of_birth = fake.country()
        city_of_birth = fake.city()
        country_of_residence = fake.country()
        city_of_residence = fake.city()
        residence_age = fake.random_int(min=1, max=100)
        birth_date = fake.date_of_birth(minimum_age=18).strftime("%Y-%m-%d")

        user_data = {
            "identification_type": identification_type,
            "identification_number": identification_number,
            "gender": gender,
            "country_of_birth": country_of_birth,
            "city_of_birth": city_of_birth,
            "country_of_residence": country_of_residence,
            "city_of_residence": city_of_residence,
            "residence_age": residence_age,
            "birth_date": birth_date,
        }

        user_additional_information = UserAdditionalInformation(**user_data)

        db = MagicMock()
        complete_user_registration.return_value = user_data
        response = await users_routes.complete_user_registration(user_id, user_additional_information, db)
        response_body = json.loads(response.body)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_body, user_data)