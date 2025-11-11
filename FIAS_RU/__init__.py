"""
FIAS_RU - Простой и надёжный SDK для работы с ФИАС API

🚀 Быстрый старт:
    pip install FIAS-RU

📖 Использование:
    from FIAS_RU import SPAS

    # Вариант 1: Токен из переменной окружения (рекомендуется)
    export FIAS_TOKEN="your_token"
    spas = SPAS()

    # Вариант 2: Явно указать токен
    spas = SPAS(token="your_token")

    # Умный поиск (автоопределение типа запроса)
    address = spas.search("Москва, Тверская 1")  # по строке
    address = spas.search(123456)                 # по ID
    address = spas.search("77:01:0001001:1")     # по кадастру

    # Быстрый доступ к свойствам
    print(address.full_name)    # "г Москва, ул Тверская, д 1"
    print(address.postal_code)  # "125009"
    print(address.oktmo)        # "45000000"

    # Автокомплит для форм ввода
    hints = spas.autocomplete("Москва, Тв")
    for hint in hints[:5]:
        print(hint.full_name)

    # Получить все регионы РФ
    regions = spas.get_regions()
    for region in regions[:5]:
        print(f"{region.region_code}: {region.full_name}")

📧 Получить токен:
    Напишите на api.fias@tax.gov.ru с данными организации.
    Подробнее: см. TOKEN_GUIDE.md

🔗 Полезные ссылки:
    - Документация: https://github.com/eclips-team/FIAS_RU
    - PyPI: https://pypi.org/project/FIAS-RU/
    - Официальный ФИАС: https://fias.nalog.ru/
"""

__version__ = "0.1.0"
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
    "__author__",
    "__email__",

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