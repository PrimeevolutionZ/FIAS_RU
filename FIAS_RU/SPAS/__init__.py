"""
FIAS_RU/FIAS_RU/SPAS/__init__.py

Модуль для конвертации и интеграции адресов (SPAS API)
Экспортирует клиент SPAS и связанные модели
"""

from .client import SPAS
from .models import (
    AddressType,
    AddressItem,
    SearchHint,
    AddressDetails,
    AddressObject,
    StructuredAddress,
)

__all__ = [
    "SPAS",
    "AddressType",
    "AddressItem",
    "SearchHint",
    "AddressDetails",
    "AddressObject",
    "StructuredAddress",
]