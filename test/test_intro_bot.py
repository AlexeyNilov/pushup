# import pytest
# from unittest.mock import AsyncMock, patch
# from telegram import Chat, ChatMember, User, Update, ChatMemberUpdated
# from telegram.ext import ContextTypes, Application
# from bot.intro import greet_user  # Import your greet_user function


# @pytest.mark.asyncio
# async def test_greet_user_private_chat():
#     """Test that the bot sends a greeting when a user starts a private chat."""

#     # Create mock user, chat, and chat member objects
#     user = User(id=12345, is_bot=False, first_name="John")
#     chat = Chat(id=67890, type=Chat.PRIVATE, title="Test Chat")

#     # Simulate the old and new chat member state
#     old_chat_member = ChatMember(user=user, status=ChatMember.LEFT)
#     new_chat_member = ChatMember(user=user, status=ChatMember.MEMBER)

#     # Create an Update object simulating a 'my_chat_member' update
#     update = Update(
#         update_id=1,
#         my_chat_member=ChatMemberUpdated(
#             chat=chat,
#             from_user=user,
#             old_chat_member=old_chat_member,
#             new_chat_member=new_chat_member,
#             date=None,
#         ),
#     )

#     # Initialize the Application instance
#     application = Application.builder().token("TEST_TOKEN").build()

#     # Create the context using the initialized application
#     context = ContextTypes.DEFAULT_TYPE(application)

#     # Use patch to mock the send_message method on the bot
#     with patch.object(application.bot, "send_message", AsyncMock()) as mock_send_message:
#         # Call the greet_user function with the mocked objects
#         await greet_user(update, context)

#         # Verify the send_message method was called with the correct parameters
#         mock_send_message.assert_called_once_with(
#             chat_id=67890,
#             text="Hello, John! 👋\nWelcome to the bot.",
#         )
