# Security Policy

## 🔒 Политика безопасности FIAS_RU SDK

Мы серьёзно относимся к безопасности и приватности данных наших пользователей. Этот документ описывает нашу политику безопасности и процесс сообщения об уязвимостях.

## 🛡️ Встроенные меры безопасности

### 1. Валидация входных данных

SDK автоматически валидирует все входные данные перед отправкой в API:

```python
# ✅ Безопасно: валидация перед отправкой
spas.find_address("Москва")  

# ❌ Блокируется: пустой запрос
spas.find_address("")  # → FIASValidationError

# ❌ Блокируется: некорректный ID
spas.get_by_id(-1)  # → FIASValidationError
```

**Защищает от:**
- Injection-атак через параметры
- Некорректных данных, вызывающих сбои API
- Переполнения буфера

### 2. Защита токенов авторизации

**КРИТИЧЕСКИ ВАЖНО:** SDK требует токен авторизации для работы с ФИАС API.

#### ✅ Безопасное хранение токенов

```python
import os
from dotenv import load_dotenv

# Загрузить токен из переменных окружения
load_dotenv()
token = os.getenv("FIAS_TOKEN")

spas = SPAS("https://fias-public-service.nalog.ru", token=token)
```

**Файл `.env` (ОБЯЗАТЕЛЬНО добавьте в .gitignore!):**
```env
FIAS_TOKEN=ваш_секретный_токен_здесь
```

**Файл `.gitignore`:**
```gitignore
.env
*.env
.env.*
```

#### ❌ НИКОГДА не делайте так:

```python
# НЕ ХРАНИТЕ ТОКЕН В КОДЕ!
spas = SPAS("https://...", token="my_secret_token_12345")

# НЕ КОММИТЬТЕ ТОКЕНЫ В GIT!
# НЕ ПУБЛИКУЙТЕ ТОКЕНЫ В ПУБЛИЧНЫХ РЕПОЗИТОРИЯХ!
# НЕ ЛОГИРУЙТЕ ТОКЕНЫ!
```

#### 🔍 Проверка утечки токенов

Если ваш токен попал в публичный репозиторий:

1. **НЕМЕДЛЕННО** отзовите скомпрометированный токен на портале ФНС
2. Сгенерируйте новый токен
3. Очистите историю Git (используйте `git-filter-repo` или BFG Repo-Cleaner)
4. Уведомите команду безопасности: develop@eclips-team.ru

### 3. Rate Limiting

Встроенный rate limiter предотвращает:
- DoS атаки на API
- Блокировку вашего IP за превышение лимитов
- Непреднамеренную перегрузку системы

```python
# Rate limiting включён по умолчанию
spas = SPAS(
    "https://fias-public-service.nalog.ru",
    token=os.getenv("FIAS_TOKEN"),
    rate_limit_requests=100,    # Макс. 100 запросов
    rate_limit_window=60.0      # За 60 секунд
)
```

### 4. Connection Pooling с ограничениями

Предотвращает утечку ресурсов и исчерпание соединений:

```python
spas = SPAS(
    "https://fias-public-service.nalog.ru",
    token=os.getenv("FIAS_TOKEN"),
    max_connections=100,              # Макс. соединений
    max_keepalive_connections=20      # Макс. keep-alive
)
```

### 5. Timeout защита

Все запросы имеют таймауты для предотвращения зависания:

```python
spas = SPAS(
    "https://fias-public-service.nalog.ru",
    token=os.getenv("FIAS_TOKEN"),
    timeout=30.0  # 30 секунд максимум
)
```

### 6. HTTPS Only

SDK работает **только** с HTTPS endpoints:

```python
# ✅ Разрешено
SPAS("https://fias-public-service.nalog.ru", token=token)

# ❌ Заблокировано
SPAS("http://fias-public-service.nalog.ru", token=token)  # → FIASValidationError
```

### 7. Безопасное логирование

Чувствительные данные **никогда** не логируются:
- ✅ Токены авторизации автоматически скрываются в логах
- ✅ Ошибки обрезаются до 200 символов
- ✅ Логируются только статус-коды и типы ошибок
- ✅ Headers с Authorization не попадают в логи

```python
import logging

logging.basicConfig(level=logging.DEBUG)

spas = SPAS(
    "https://fias-public-service.nalog.ru",
    token="secret_token_12345"
)

# В логах токен будет скрыт:
# INFO: Request to /api/spas/v2.0/SearchAddressItem
# DEBUG: Authorization: Bearer ***HIDDEN***
```

### 8. Graceful Degradation

При ошибках SDK не раскрывает внутренние детали:

```python
try:
    spas.find_address("test")
except FIASAPIError as e:
    # ✅ Безопасное сообщение
    print(e)  # "Ошибка сервера (500)"
    
    # ❌ Внутренние детали не раскрываются
    # НЕ логируется: stack traces, SQL запросы, токены
```

## 🚨 Сообщение об уязвимостях

### Как сообщить о проблеме безопасности

Если вы обнаружили уязвимость в FIAS_RU SDK, **НЕ создавайте публичный issue**. Вместо этого:

1. **Отправьте email на**: develop@eclips-team.ru
2. **Укажите**:
   - Описание уязвимости
   - Шаги для воспроизведения
   - Потенциальное влияние
   - Версию SDK
   - Ваши контактные данные (опционально)

### Что делать НЕ нужно

❌ **НЕ** публикуйте детали уязвимости в открытых issue  
❌ **НЕ** пытайтесь эксплуатировать уязвимость на production системах  
❌ **НЕ** делитесь информацией с третьими лицами до исправления  
❌ **НЕ** публикуйте PoC код до выхода патча  

### Процесс обработки

1. **Подтверждение (24 часа)**: Мы подтвердим получение в течение 1 рабочего дня
2. **Оценка (3-5 дней)**: Оценим серьёзность и начнём работу над патчем
3. **Патч (7-14 дней)**: Разработаем и протестируем исправление
4. **Релиз**: Выпустим обновление с исправлением
5. **Публикация**: Опубликуем информацию об уязвимости (через 30 дней после патча)

### Вознаграждение

Мы ценим помощь исследователей безопасности:
- 🏆 Упоминание в CONTRIBUTORS.md (если вы согласны)
- 🎁 Символическое вознаграждение за критические уязвимости
- 📧 Наша благодарность и признательность

## 🔐 Рекомендации по безопасному использованию

### 1. Не храните токены в коде

❌ **Плохо:**
```python
# НЕ ДЕЛАЙТЕ ТАК!
spas = SPAS("https://fias-public-service.nalog.ru", token="my_secret_key_12345")
```

✅ **Хорошо:**
```python
import os
token = os.getenv("FIAS_TOKEN")

if not token:
    raise ValueError("FIAS_TOKEN environment variable is not set")

spas = SPAS("https://fias-public-service.nalog.ru", token=token)
```

### 2. Используйте .env файлы для разработки

```bash
# .env файл (добавьте в .gitignore!)
FIAS_TOKEN=ваш_токен_для_разработки
FIAS_API_URL=https://fias-public-service.nalog.ru
```

```python
from dotenv import load_dotenv
import os

load_dotenv()

spas = SPAS(
    os.getenv("FIAS_API_URL"),
    token=os.getenv("FIAS_TOKEN")
)
```

### 3. Используйте Secret Management для production

```python
# AWS Secrets Manager
import boto3
import json

def get_fias_token():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId='fias_api_token')
    return json.loads(response['SecretString'])['token']

spas = SPAS(
    "https://fias-public-service.nalog.ru",
    token=get_fias_token()
)
```

### 4. Регулярно ротируйте токены

```python
# Установите напоминание для ротации токенов каждые 90 дней
# Используйте автоматическую ротацию если поддерживается API
```

### 5. Ограничивайте права доступа токенов

- ✅ Создавайте отдельные токены для dev/staging/production
- ✅ Используйте токены с минимально необходимыми правами
- ✅ Отзывайте неиспользуемые токены
- ✅ Мониторьте использование токенов

### 6. Валидируйте пользовательский ввод

```python
# ✅ Хорошо: валидация перед использованием
user_input = request.form.get("address", "").strip()

if not user_input:
    return "Адрес не может быть пустым", 400

if len(user_input) < 3:
    return "Адрес слишком короткий", 400

if len(user_input) > 500:
    return "Адрес слишком длинный", 400

try:
    address = spas.find_address(user_input)
except FIASValidationError as e:
    return f"Некорректный адрес: {e}", 400
```

### 7. Используйте HTTPS в production

```python
# ✅ Production
spas = SPAS(
    "https://fias-public-service.nalog.ru",
    token=os.getenv("FIAS_TOKEN")
)

# ⚠️ Development only (если есть локальный тестовый сервер)
# spas = SPAS("http://localhost:8000", token="dev_token")
```

### 8. Обрабатывайте ошибки безопасно

```python
try:
    address = spas.find_address(user_query)
except FIASValidationError as e:
    # ✅ Безопасное сообщение пользователю
    logger.info(f"Validation error for query: {user_query}")
    return "Некорректный запрос"
    
except FIASAPIError as e:
    # ✅ Логируем, но не показываем детали
    logger.error(f"API error: {type(e).__name__}")
    return "Временная ошибка сервиса"
    
except Exception as e:
    # ✅ Общая обработка
    logger.exception("Unexpected error in address search")
    return "Внутренняя ошибка сервера"
```

### 9. Регулярно обновляйте SDK

```bash
# Проверяйте обновления регулярно
pip install --upgrade FIAS_RU

# Или используйте автоматические обновления в CI/CD
pip install --upgrade --pre FIAS_RU  # для pre-release версий
```

### 10. Мониторьте использование

```python
import logging

# Включите логирование для мониторинга
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Отслеживайте подозрительную активность:
# - Аномально высокая частота запросов
# - Необычные паттерны ошибок
# - Попытки injection
# - Множественные 403 ошибки (неверный токен)
```

## 🔍 Известные ограничения

### Что SDK НЕ защищает

1. **Network layer attacks**: Man-in-the-middle, DNS spoofing (зависит от вашей инфраструктуры)
2. **Server-side vulnerabilities**: Уязвимости в самом FIAS API (не под нашим контролем)
3. **Client-side storage**: Небезопасное хранение результатов на клиенте
4. **Business logic**: Некорректная логика использования SDK в вашем приложении
5. **Token leaks**: Утечки токенов в логах вашего приложения (ответственность клиента)

### Ваша ответственность

- ✅ Безопасное хранение токенов авторизации
- ✅ Регулярная ротация токенов
- ✅ Валидация данных от пользователей перед передачей в SDK
- ✅ Защита от CSRF/XSS в веб-приложениях
- ✅ Регулярные обновления зависимостей
- ✅ Мониторинг и логирование
- ✅ Защита .env файлов и secrets
- ✅ Контроль доступа к токенам в команде

## 🚨 Чек-лист безопасности

Перед деплоем в production проверьте:

- [ ] Токен хранится в переменных окружения или secret manager
- [ ] .env файлы добавлены в .gitignore
- [ ] История Git не содержит токенов
- [ ] Используется HTTPS для API
- [ ] Настроен rate limiting
- [ ] Логирование не содержит чувствительных данных
- [ ] Есть обработка всех типов ошибок
- [ ] Валидируется пользовательский ввод
- [ ] SDK обновлён до последней версии
- [ ] Настроен мониторинг использования API
- [ ] Токены имеют минимально необходимые права
- [ ] Есть процесс ротации токенов

## 📚 Дополнительные ресурсы

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [HTTPX Security](https://www.python-httpx.org/)
- [Pydantic Security](https://docs.pydantic.dev/latest/)
- [Secret Management Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

## 📞 Контакты

- **Security email**: develop@eclips-team.ru
- **General support**: develop@eclips-team.ru
- **GitHub Issues**: [github.com/your-org/FIAS_RU/issues](https://github.com/your-org/FIAS_RU/issues) (для несекьюрных вопросов)

## 📜 История изменений безопасности

### Version 0.2.0 (2024-11)
- ✅ Добавлена обязательная авторизация через токен
- ✅ Реализована защита токенов в логах
- ✅ Добавлена валидация всех входных данных
- ✅ Реализован rate limiting
- ✅ Добавлен connection pooling с ограничениями
- ✅ HTTPS-only enforcement
- ✅ Безопасное логирование с скрытием чувствительных данных

### Version 0.1.0 (2024-10)
- ℹ️ Начальный релиз (базовая функциональность)
- ⚠️ Токены не были обязательными

---

**Последнее обновление**: 10.11.2024  
**Версия документа**: 2.0

Спасибо за помощь в поддержании безопасности FIAS_RU! 🙏