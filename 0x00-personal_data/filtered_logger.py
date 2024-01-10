#!/usr/bin/env python3
"""
filtered logger
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    obfuscating info in log message
    """
    for field in fields:
        pattern = re.compile(
            rf'(\b{field}=)[^{separator}]*({separator})'
        )
        message = pattern.sub(rf'\1{redaction}\2', message)

    return message
