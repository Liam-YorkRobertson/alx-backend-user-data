#!/usr/bin/env python3
"""
filtered logger
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    obfuscating info in log message
    """
    pattern = re.compile(
        rf'(\b{"|".join(fields)}=)[^{separator}]*?(?={separator})'
    )
    obf_message = pattern.sub(rf'\1{redaction}', message)
    return obf_message
