# Repository Structure

## bot/
Contains the main bot logic:
- `cody.py`: The main bot implementation with various commands and handlers
- `command.py`: Command handlers for the bot
- `conversation.py`: Conversation handlers for the bot
- `message.py`: Message handlers for the bot
- `utils.py`: Utility functions for the bot

### conf/
Configuration files:
- `settings.py.sample`: Sample configuration file (actual `settings.py` is gitignored)

### data/
Data-related functionality:
- `fastlite_db.py`: Database setup and table definitions using FastLite
- `logger.py`: Logging configuration
- `backup_db.py`: Database backup functionality
- `generate_schema.py`: Script to generate database schemas
- `yamler.py`: YAML file handling
- `migrate_db.py`: Database migration script
- `view_db.py`: Script to view database contents
- `schema.sql`: SQL schema for the database

### db/
Database and data files:
- Various YAML files (`workout.yaml`, `intermediate.yaml`, `beginner.yaml`, `idea.yaml`, `warmup.yaml`, `cooldown.yaml`): Contain structured data for different aspects of the application

### doc/
Documentation files:
- `repo.md`: Repository structure
- `ec2.md`: Instructions for running the bot on AWS EC2
- `user_story.md`: User stories and feature ideas
- `training.md`: Information about the training program
- `roadmap.md`: Roadmap and todo list

### infra/
Infrastructure and deployment-related files:
- `start_bot.sh`: Script to start the bot
- `github_syncer.sh`: Script to sync code from GitHub
- `backup_to_s3.sh`: Script to backup the database to S3
- Various systemd service and timer files for automating processes

### model/
Data models:
- `create_dataclasses.py`: Script to create dataclasses from database schema

### sample/
Sample scripts:
- `simply.py`: A simple bot implementation for testing
- `filter_user.py`: User authentication and authorization example

### service/
Business logic and services:
- `repo.py`: Repository pattern implementation for data access
- `workout.py`: Workout-related functionality
- `idea.py`: Idea generation functionality
- `fitness_test.py`: Fitness test standards and calculations
- `warmup.py`: Warm-up exercise functionality
- `cooldown.py`: Cool-down exercise functionality (implementation not provided in snippets)

### test/
Unit tests:
- `test_cody_bot.py`: Tests for the main bot functionality
- `test_auth_bot.py`: Tests for authentication functionality
- `test_repo.py`: Tests for the repository functions
- `test_workout.py`: Tests for workout-related functions
- `test_idea.py`: Tests for idea generation
- `test_cooldown.py`: Tests for cool-down functionality
