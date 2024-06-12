import uuid

from django.test import TestCase

from .validators import is_valid_uuid4


# Create your tests here.
class TestValidateUuid(TestCase):

    def test_validate_uuid(self):
        self.assertTrue(is_valid_uuid4(str(uuid.uuid4())))

        self.assertFalse(is_valid_uuid4(str(uuid.uuid1())))
        self.assertFalse(
            is_valid_uuid4(str(uuid.uuid3(uuid.UUID(int=123), "123456789")))
        )
        self.assertFalse(
            is_valid_uuid4(str(uuid.uuid5(uuid.UUID(int=123), "123456789")))
        )
        self.assertFalse(is_valid_uuid4("12123"))
        self.assertFalse(is_valid_uuid4("dhaefjhsajfjkdsf"))
        self.assertFalse(is_valid_uuid4("2131321q3"))
        self.assertFalse(is_valid_uuid4(str(uuid.uuid4())[1:]))
