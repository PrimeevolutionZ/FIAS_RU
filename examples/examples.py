"""
Примеры использования FIAS_RU SDK

Запуск:
    python examples.py
"""

import os
from FIAS_RU import SPAS, AddressType, FIASError


def example_1_basic_search():
    """Пример 1: Базовый поиск адреса"""
    print("\n" + "="*60)
    print("ПРИМЕР 1: Базовый поиск адреса")
    print("="*60)

    spas = SPAS()

    # Простой поиск
    address = spas.search("Москва, Тверская 1")

    if address:
        print(f"✅ Найден адрес:")
        print(f"   Полное название: {address.full_name}")
        print(f"   Короткое название: {address.short_name}")
        print(f"   Уровень: {address.level_name}")
        print(f"   ID: {address.id}")
        print(f"   GUID: {address.guid}")


def example_2_smart_search():
    """Пример 2: Умный поиск (автоопределение типа)"""
    print("\n" + "="*60)
    print("ПРИМЕР 2: Умный поиск")
    print("="*60)

    spas = SPAS()

    queries = [
        "Москва, Красная площадь 1",           # По строке
        "77000000-0000-0000-0000-000000000000", # По GUID (пример)
        "77:01:0001001:1",                      # По кадастру (пример)
        123456                                   # По ID (пример)
    ]

    for query in queries:
        print(f"\n🔍 Поиск: {query}")
        try:
            address = spas.search(query)
            if address:
                print(f"   ✅ {address.full_name}")
            else:
                print(f"   ❌ Не найдено")
        except FIASError as e:
            print(f"   ⚠️ Ошибка: {e}")


def example_3_autocomplete():
    """Пример 3: Автокомплит для формы ввода"""
    print("\n" + "="*60)
    print("ПРИМЕР 3: Автокомплит")
    print("="*60)

    spas = SPAS()

    # Пользователь начинает вводить адрес
    partial_queries = ["Мо", "Моск", "Москва, Тв"]

    for partial in partial_queries:
        print(f"\n💡 Ввод пользователя: '{partial}'")
        hints = spas.autocomplete(partial, limit=5)

        print(f"   Подсказки ({len(hints)}):")
        for i, hint in enumerate(hints, 1):
            print(f"   {i}. {hint.full_name}")


def example_4_address_details():
    """Пример 4: Получение деталей адреса"""
    print("\n" + "="*60)
    print("ПРИМЕР 4: Детали адреса")
    print("="*60)

    spas = SPAS()

    address = spas.search("Москва, Тверская 1")

    if address:
        print(f"📍 Адрес: {address.full_name}\n")

        # Быстрый доступ к деталям
        print("Основная информация:")
        print(f"  • Почтовый индекс: {address.postal_code or '—'}")
        print(f"  • ОКТМО: {address.oktmo or '—'}")
        print(f"  • ОКАТО: {address.okato or '—'}")
        print(f"  • КЛАДР: {address.kladr_code or '—'}")
        print(f"  • Кадастр: {address.cadastral_number or '—'}")

        print("\nНалоговые органы:")
        print(f"  • ИФНС (ЮЛ): {address.ifns_ul or '—'}")
        print(f"  • ИФНС (ФЛ): {address.ifns_fl or '—'}")

        # Получить все детали
        details = spas.get_details(address)
        if details:
            print("\n📋 Полные детали:")
            for key, value in details.to_dict().items():
                print(f"  • {key}: {value}")


def example_5_regions():
    """Пример 5: Список регионов"""
    print("\n" + "="*60)
    print("ПРИМЕР 5: Регионы РФ")
    print("="*60)

    spas = SPAS()

    regions = spas.get_regions()

    print(f"📊 Всего регионов: {len(regions)}\n")
    print("Первые 10 регионов:")
    for region in regions[:10]:
        print(f"  {region.region_code:02d}. {region.full_name}")


def example_6_export():
    """Пример 6: Экспорт данных"""
    print("\n" + "="*60)
    print("ПРИМЕР 6: Экспорт данных")
    print("="*60)

    spas = SPAS()

    address = spas.search("Москва, Тверская 1")

    if address:
        # В словарь
        print("\n📄 Экспорт в dict:")
        data = address.to_dict(include_details=False)
        print(f"  Поля: {list(data.keys())}")

        # В JSON
        print("\n📄 Экспорт в JSON:")
        json_str = address.to_json(indent=2)
        print(json_str[:200] + "...")  # Первые 200 символов


def example_7_batch_search():
    """Пример 7: Пакетный поиск"""
    print("\n" + "="*60)
    print("ПРИМЕР 7: Пакетный поиск адресов")
    print("="*60)

    spas = SPAS()

    addresses_to_search = [
        "Москва, Тверская 1",
        "Санкт-Петербург, Невский проспект 1",
        "Казань, Кремлевская 1",
        "Екатеринбург, проспект Ленина 1",
        "Новосибирск, Красный проспект 1"
    ]

    print(f"🔍 Ищем {len(addresses_to_search)} адресов:\n")

    results = []
    for query in addresses_to_search:
        try:
            address = spas.search(query)
            results.append((query, address))

            if address:
                print(f"✅ {query}")
                print(f"   → {address.full_name}")
                print(f"   → ОКТМО: {address.oktmo or '—'}")
            else:
                print(f"❌ {query} - не найден")
        except FIASError as e:
            print(f"⚠️ {query} - ошибка: {e}")

        print()


def example_8_error_handling():
    """Пример 8: Обработка ошибок"""
    print("\n" + "="*60)
    print("ПРИМЕР 8: Обработка ошибок")
    print("="*60)

    spas = SPAS()

    # Примеры некорректных запросов
    test_cases = [
        ("", "Пустая строка"),
        ("М", "Слишком короткий запрос"),
        ("Несуществующий адрес 12345 xyz", "Несуществующий адрес")
    ]

    for query, description in test_cases:
        print(f"\n🧪 Тест: {description}")
        print(f"   Запрос: '{query}'")

        try:
            address = spas.search(query)
            if address:
                print(f"   ✅ Найдено: {address.full_name}")
            else:
                print(f"   ❌ Не найдено")
        except FIASError as e:
            print(f"   ⚠️ Ожидаемая ошибка: {e}")


def example_9_context_manager():
    """Пример 9: Context manager"""
    print("\n" + "="*60)
    print("ПРИМЕР 9: Context manager (автозакрытие)")
    print("="*60)

    print("\n🔧 Используем context manager...")

    with SPAS() as spas:
        address = spas.search("Москва, Тверская 1")
        if address:
            print(f"✅ Найдено: {address.full_name}")

    print("✅ Соединения автоматически закрыты")


def example_10_custom_config():
    """Пример 10: Кастомная конфигурация"""
    print("\n" + "="*60)
    print("ПРИМЕР 10: Кастомная конфигурация")
    print("="*60)

    # Пример с явной конфигурацией
    spas = SPAS(
        timeout=60.0,           # Увеличенный таймаут
        max_retries=5,          # Больше попыток
        max_connections=50,     # Меньше соединений
        rate_limit_requests=50, # Строже rate limit
        rate_limit_window=60.0
    )

    print("⚙️ Конфигурация:")
    print(f"   • Timeout: {spas.timeout}s")
    print(f"   • Max retries: {spas.max_retries}")
    print(f"   • Rate limit: {spas.rate_limiter.max_requests} req/{spas.rate_limiter.time_window}s")

    address = spas.search("Москва, Тверская 1")
    if address:
        print(f"\n✅ Поиск работает: {address.full_name}")


def main():
    """Запуск всех примеров"""

    # Проверка токена
    token = os.getenv("FIAS_TOKEN")
    if not token:
        print("❌ ОШИБКА: Токен не найден!")
        print("\nУстановите токен одним из способов:")
        print("1. export FIAS_TOKEN='your_token'")
        print("2. Создайте .env файл с FIAS_TOKEN=your_token")
        return

    print("="*60)
    print(" ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ FIAS_RU SDK")
    print("="*60)
    print(f"✅ Токен найден: {token[:10]}...")

    try:
        # Запускаем примеры
        example_1_basic_search()
        example_2_smart_search()
        example_3_autocomplete()
        example_4_address_details()
        example_5_regions()
        example_6_export()
        example_7_batch_search()
        example_8_error_handling()
        example_9_context_manager()
        example_10_custom_config()

        print("\n" + "="*60)
        print("✅ ВСЕ ПРИМЕРЫ ВЫПОЛНЕНЫ")
        print("="*60)

    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()