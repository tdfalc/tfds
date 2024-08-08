import logging
from pathlib import Path
import pytest
from tfds.log import create_logger


def test_create_logger_no_filename():
    # Create logger without filename
    logger = create_logger("test_logger")

    # Check logger name
    assert logger.name == "test_logger"

    # Check logger level
    assert logger.level == logging.INFO

    # Check handlers
    handlers = logger.handlers
    assert len(handlers) == 1  # Should only have the console handler

    # Check formatter
    console_handler = handlers[0]
    assert isinstance(console_handler, logging.StreamHandler)
    assert (
        console_handler.formatter._fmt
        == "[%(asctime)s] %(name)s (%(levelname)s): %(message)s"
    )


def test_create_logger_with_filename(tmp_path):
    # Create a temporary file path
    temp_file = tmp_path / "test.log"

    # Create logger with filename
    logger = create_logger("test_logger_with_file", filename=temp_file)

    # Check logger name
    assert logger.name == "test_logger_with_file"

    # Check logger level
    assert logger.level == logging.INFO

    # Check handlers
    handlers = logger.handlers
    assert len(handlers) == 2  # Should have both console and file handlers

    # Check console handler
    console_handler = handlers[0]
    assert isinstance(console_handler, logging.StreamHandler)
    assert (
        console_handler.formatter._fmt
        == "[%(asctime)s] %(name)s (%(levelname)s): %(message)s"
    )

    # Check file handler
    file_handler = handlers[1]
    assert isinstance(file_handler, logging.FileHandler)
    assert file_handler.baseFilename == str(temp_file)
    assert (
        file_handler.formatter._fmt
        == "[%(asctime)s] %(name)s (%(levelname)s): %(message)s"
    )
