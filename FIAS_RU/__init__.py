"""
FIAS_RU - Простой и надёжный SDK для работы с ФИАС API

Использование:
    from FIAS_RU import SPAS

    # Самый простой способ
    spas = SPAS("https://api.fias.ru")
    address = spas.find_address("Москва, Тверская 1")
    print(address.full_name)

    # Автокомплит
    hints = spas.autocomplete("Москва, Тв")
    for hint in hints:
        print(hint.full_name)
"""

__version__ = "0.2.0"
__author__ = "Eclips team"
__email__ = "develop@eclips-team.ru"

# Импорты базовых классов
from .SPAS import (
    AddressType,
    AddressItem,
    SearchHint,
    AddressDetails,
    AddressObject,
    StructuredAddress,
    SPAS,
)

# Импорты исключений
from .SPAS.exceptions import (
    FIASError,
    FIASValidationError,
    FIASAPIError,
    FIASNetworkError,
    FIASTimeoutError,
    FIASNotFoundError,
)

__all__ = [
    # Версия
    "__version__",

    # Модели
    "AddressType",
    "AddressItem",
    "SearchHint",
    "AddressDetails",
    "AddressObject",
    "StructuredAddress",

    # Клиент
    "SPAS",

    # Исключения
    "FIASError",
    "FIASValidationError",
    "FIASAPIError",
    "FIASNetworkError",
    "FIASTimeoutError",
    "FIASNotFoundError",
]