import pytest
from unittest.mock import MagicMock
from bot import command


@pytest.mark.asyncio
async def test_stats_command(msg, update, context):
    await command.stats_for_today(update, context)
    msg.reply_text.assert_called_once_with("Today sum: 0, max: 0")


@pytest.mark.asyncio
async def test_stats_command_fail(msg, illegal_update, context):
    await command.stats_for_today(illegal_update, context)
    msg.reply_text.assert_called_once_with(
        "Sorry, you are not authorized to use this bot, /join first"
    )


@pytest.mark.asyncio
async def test_set_timer(update, context):
    # Act
    await command.set_timer(update, context)

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
    await command.set_timer(update, context)

    # Assert
    existing_job.schedule_removal.assert_called_once()

    context.job_queue.run_once.assert_called_once()
    update.effective_message.reply_text.assert_called_once_with(
        "Timer successfully set!"
    )


@pytest.mark.asyncio
async def test_record(msg, update, context):
    await command.stats_all_time(update, context)
    msg.reply_text.assert_called_once_with("Record set: 0, sum per day: 0")


@pytest.mark.asyncio
async def test_get_practice(msg, update, context):
    await command.get_practice(update, context)
    msg.reply_html.assert_called()


@pytest.mark.asyncio
async def test_complete_workout(msg, update, context):
    await command.complete_workout(update, context)
    msg.reply_text.assert_called_once_with("Workout completed!")


@pytest.mark.asyncio
async def test_stop_training_program(msg, update, context):
    await command.stop_training_program(update, context)
    msg.reply_text.assert_called_once_with("Training program deactivated")


@pytest.mark.asyncio
async def test_rating_command(msg, update, context, profile):
    await command.rating_command(update, context)
    msg.reply_text.assert_called_once()
