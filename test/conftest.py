import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, Chat, Message, User
from telegram.ext import ContextTypes
import os

os.environ["PUSHUP_DB_PATH"] = "db/test_empty.sqlite"

from data.fastlite_db import recreate_db
from service.repo import update_profile


@pytest.fixture
def authorized_user() -> User:
    return User(id=123456789, is_bot=False, first_name="TestUser")


@pytest.fixture
def msg() -> MagicMock:
    message = MagicMock(spec=Message)
    message.reply_text = AsyncMock()
    return message


@pytest.fixture
def update(authorized_user, msg) -> MagicMock:
    recreate_db()
    update_profile({"user_id": 123456789})
    upd = MagicMock(spec=Update)
    upd.message = msg
    upd.effective_message = AsyncMock(spec=Message)
    upd.effective_user = authorized_user
    upd.effective_chat.type = Chat.PRIVATE
    upd.effective_chat.id = 123456
    return upd


@pytest.fixture
def context():
    ctx = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    ctx.job_queue = MagicMock()
    ctx.job_queue.run_once = MagicMock()
    ctx.job_queue.get_jobs_by_name = MagicMock(return_value=[])
    return ctx


@pytest.fixture
def illegal_user():
    return User(id=111111111, is_bot=False, first_name="TestUser")


@pytest.fixture
def illegal_update(illegal_user, msg):
    upd = MagicMock(spec=Update)
    upd.effective_user = illegal_user
    upd.message = msg
    upd.effective_chat.type = Chat.PRIVATE
    return upd
