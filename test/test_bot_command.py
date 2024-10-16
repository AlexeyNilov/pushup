import pytest
from unittest.mock import MagicMock
from bot.command import set_timer


@pytest.mark.asyncio
async def test_set_timer(update, context):
    # Act
    await set_timer(update, context)

    # Assert
    context.job_queue.run_once.assert_called_once()
    job_args = context.job_queue.run_once.call_args[0]
    job_kwargs = context.job_queue.run_once.call_args[1]

    assert job_args[1] == 60.0  # Check if the timer is set for 60 seconds
    assert job_kwargs["data"] == 60.0

    update.effective_message.reply_text.assert_called_once_with(
        "Timer successfully set!"
    )


@pytest.mark.asyncio
async def test_set_timer_removes_existing_job(update, context):
    # Arrange
    existing_job = MagicMock()
    context.job_queue.get_jobs_by_name.return_value = [existing_job]

    # Act
    await set_timer(update, context)

    # Assert
    existing_job.schedule_removal.assert_called_once()

    context.job_queue.run_once.assert_called_once()
    update.effective_message.reply_text.assert_called_once_with(
        "Timer successfully set!"
    )
