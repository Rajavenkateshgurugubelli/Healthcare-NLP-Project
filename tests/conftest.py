import sys
from unittest.mock import MagicMock

# Mock 'pwd' module on Windows to prevent import errors in langchain_community
if sys.platform == "win32":
    pwd_mock = MagicMock()
    pwd_mock.getpwuid.return_value = MagicMock(pw_name="dummy_user")
    sys.modules["pwd"] = pwd_mock
