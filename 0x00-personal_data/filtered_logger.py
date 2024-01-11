#!/usr/bin/env python3
"""
replacing occurrences of field values
"""
import re
from typing import List, Tuple
import logging
import os
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        initialization of function
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        formats the log record
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    returns regex obfuscated log message
    """
    for field in fields:
        message = re.sub(rf'({field}=)[^{separator}]*{separator}',
                         rf'\1{redaction}{separator}', message)
    return message


PII_FIELDS = ['name', 'email', 'phone', 'ssn', 'password']


def get_logger() -> logging.Logger:
    """
    create and configure logger
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MYSQLConnection:
    """
    connects to database and retrieves data
    """
    connection = mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME", ""),
    )
    return connection


def main():
    """
    main function
    """
    db = get_db()
    if db:
        with db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users;")
            print(cursor.fetchone()[0])
        db.close()


if __name__ == "__main__":
    main()
