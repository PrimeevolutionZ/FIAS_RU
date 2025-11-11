# Security Policy

## 🔒 Политика безопасности FIAS_RU SDK

Мы серьёзно относимся к безопасности и приватности данных наших пользователей. Этот документ описывает нашу политику безопасности и процесс сообщения об уязвимостях.

---

## 🔑 Как получить токен для ФИАС API

### Официальный публичный API (для разработчиков)

Для работы с публичным API `fias-public-service.nalog.ru` необходим **master-token**.

#### Шаг 1: Подготовьте заявку

Создайте документ с информацией о вашей организации:

**Для юридических лиц:**
```
Наименование организации: ООО "Название"
ИНН: 1234567890
КПП: 123456789
ОГРН: 1234567890123
Адрес: г. Москва, ...
Контактное лицо: Иванов Иван Иванович
Email: contact@company.ru
Телефон: +7 (999) 123-45-67
Цель использования API: [опишите задачу]
Примерная нагрузка: до 10000 запросов/день
```

**Для физических лиц / ИП:**
```
ФИО: Иванов Иван Иванович
ИНН: 123456789012 (если есть)
Email: contact@example.com
Телефон: +7 (999) 123-45-67
Цель использования API: [опишите задачу]
Примерная нагрузка: до 10000 запросов/день
```

#### Шаг 2: Отправьте заявку

Отправьте заполненную заявку на email:

📧 **api.fias@tax.gov.ru**

Тема письма: "Запрос токена для доступа к API ФИАС"

#### Шаг 3: Дождитесь ответа

Обычно токен приходит в течение **3-7 рабочих дней**. Проверяйте папку "Спам".

В ответе вы получите:
- ✅ `master-token` - ваш токен авторизации
- ℹ️ Инструкции по использованию
- ⚠️ Лимиты запросов (обычно до 10,000 запросов/день)

#### Шаг 4: Начните использовать

```python
from FIAS_RU import SPAS

# Укажите токен из письма
spas = SPAS(token="ваш_токен_из_письма")

# Готово! Можно работать
address = spas.search("Москва, Тверская 1")
print(address.full_name)
```

---

### Альтернативные варианты (если нужен быстрый старт)

Если вам нужно начать работу срочно, пока токен не получен:

#### 1. **Dadata API** (платный, но работает сразу)

```python
# Регистрация: https://dadata.ru/
# Получите API ключ сразу после регистрации

import requests

api_key = "your_dadata_token"
url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/fias"

response = requests.post(
    url,
    headers={
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    },
    json={"query": "Москва, Тверская"}
)

print(response.json())
```

**Тарифы Dadata:**
- 🆓 Бесплатно: до 10,000 запросов/месяц
- 💰 Платные тарифы: от 990₽/мес за 100,000 запросов

#### 2. **Локальная база ФИАС** (бесплатно, но требует настройки)

Скачайте полную базу ФИАС:
- 🔗 https://fias.nalog.ru/
- 📦 Размер: ~10-15 ГБ (ZIP)
- 🗄️ Формат: XML, DBF, SQL

```bash
# Скачать базу
wget http://fias.nalog.ru/Public/Downloads/latest/fias_xml.rar

# Распаковать
unrar x fias_xml.rar

# Импортировать в PostgreSQL/MySQL
# (требуется написание скриптов импорта)
```

---

## 🛡️ Встроенные меры безопасности

### 1. Валидация входных данных

SDK автоматически валидирует все входные данные перед отправкой в API:

```python
# ✅ Безопасно: валидация перед отправкой
spas.search("Москва")  

# ❌ Блокируется: пустой запрос
spas.search("")  # → FIASValidationError

# ❌ Блокируется: некорректный ID
spas.search(-1)  # → FIASValidationError
```

**Защищает от:**
- Injection-атак через параметры
- Некорректных данных, вызывающих сбои API
- Переполнения буфера

### 2. Защита токенов авторизации

**КРИТИЧЕСКИ ВАЖНО:** SDK требует токен авторизации для работы с ФИАС API.

#### ✅ Безопасное хранение токенов

**Вариант 1: Переменные окружения (рекомендуется)**

```bash
# Linux/Mac
export FIAS_TOKEN="your_secret_token_here"

# Windows PowerShell
$env:FIAS_TOKEN="your_secret_token_here"

# Windows CMD
set FIAS_TOKEN=your_secret_token_here
```

```python
from FIAS_RU import SPAS

# Токен автоматически читается из переменной окружения
spas = SPAS()

# Или явно
import os
spas = SPAS(token=os.getenv("FIAS_TOKEN"))
```

**Вариант 2: .env файл (для разработки)**

Создайте файл `.env`:

```env
FIAS_TOKEN=your_secret_token_here
FIAS_BASE_URL=https://fias-public-service.nalog.ru
```

**ОБЯЗАТЕЛЬНО добавьте в `.gitignore`:**

```gitignore
# Секретные файлы
.env
.env.*
*.env
.env.local
.env.production

# Конфиги с токенами
config.local.py
secrets.py
credentials.json
```

Используйте `python-dotenv`:

```python
from dotenv import load_dotenv
from FIAS_RU import SPAS

load_dotenv()  # Загружает .env файл

spas = SPAS()  # Токен автоматически подтянется
```

**Вариант 3: Secret Management (для production)**

```python
# AWS Secrets Manager
import boto3
import json

def get_fias_token():
    client = boto3.client('secretsmanager', region_name='eu-west-1')
    response = client.get_secret_value(SecretId='prod/fias/token')
    return json.loads(response['SecretString'])['token']

spas = SPAS(token=get_fias_token())
```

```python
# Azure Key Vault
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
vault_url = "https://your-vault.vault.azure.net"
client = SecretClient(vault_url=vault_url, credential=credential)

token = client.get_secret("fias-token").value
spas = SPAS(token=token)
```

```python
# HashiCorp Vault
import hvac

client = hvac.Client(url='http://127.0.0.1:8200')
client.token = 'your-vault-token'

secret = client.secrets.kv.v2.read_secret_version(path='fias')
token = secret['data']['data']['token']

spas = SPAS(token=token)
```

#### ❌ НИКОГДА не делайте так:

```python
# ❌ НЕ ХРАНИТЕ ТОКЕН В КОДЕ!
spas = SPAS(token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")

# ❌ НЕ КОММИТЬТЕ ТОКЕНЫ В GIT!
# ❌ НЕ ПУБЛИКУЙТЕ ТОКЕНЫ В ПУБЛИЧНЫХ РЕПОЗИТОРИЯХ!
# ❌ НЕ ЛОГИРУЙТЕ ТОКЕНЫ!
# ❌ НЕ ОТПРАВЛЯЙТЕ ТОКЕНЫ В SLACK/TELEGRAM/EMAIL БЕЗ ШИФРОВАНИЯ!
```

#### 🔍 Что делать если токен утёк

Если ваш токен попал в публичный репозиторий или стал известен третьим лицам:

1. **НЕМЕДЛЕННО** напишите на `api.fias@tax.gov.ru` с просьбой отозвать токен
2. Запросите новый токен (повторите процедуру получения)
3. Очистите историю Git:

```bash
# Используйте git-filter-repo
pip install git-filter-repo

# Удалить файл из истории
git filter-repo --path .env --invert-paths

# Или используйте BFG Repo-Cleaner
java -jar bfg.jar --delete-files .env
```

4. Проверьте все форки и копии репозитория
5. Смените токены во всех окружениях (dev, staging, prod)
### 3. Rate Limiting

Встроенный rate limiter предотвращает:
- DoS атаки на API
- Блокировку вашего токена за превышение лимитов
- Непреднамеренную перегрузку системы

```python
# Rate limiting включён по умолчанию
spas = SPAS(
    token=os.getenv("FIAS_TOKEN"),
    rate_limit_requests=100,    # Макс. 100 запросов
    rate_limit_window=60.0      # За 60 секунд
)
```

**Лимиты ФИАС API (от ФНС):**
- 🔢 Обычно: до **10,000 запросов/день**
- ⏱️ Рекомендуется: не более **100 запросов/минуту**
- 🚫 При превышении: временная блокировка на 1-24 часа

### 4. Connection Pooling с ограничениями

Предотвращает утечку ресурсов и исчерпание соединений:

```python
spas = SPAS(
    token=os.getenv("FIAS_TOKEN"),
    max_connections=100,              # Макс. соединений
    max_keepalive_connections=20      # Макс. keep-alive
)
```

### 5. Timeout защита

Все запросы имеют таймауты для предотвращения зависания:

```python
spas = SPAS(
    token=os.getenv("FIAS_TOKEN"),
    timeout=30.0  # 30 секунд максимум
)
```

### 6. HTTPS Only

SDK работает **только** с HTTPS endpoints:

```python
# ✅ Разрешено
SPAS(token=token)  # По умолчанию HTTPS

# ❌ Заблокировано
SPAS(base_url="http://fias-public-service.nalog.ru", token=token)  
# → FIASValidationError: "URL должен использовать HTTPS"
```

### 7. Безопасное логирование

Чувствительные данные **никогда** не логируются:

```python
import logging

logging.basicConfig(level=logging.DEBUG)

spas = SPAS(token="secret_token_12345")

# ✅ В логах токен будет скрыт:
# INFO: Request to /api/spas/v2.0/SearchAddressItem
# DEBUG: Headers: {'master-token': '***'}
```

SDK автоматически скрывает:
- ✅ Токены в headers
- ✅ Токены в URL parameters
- ✅ Ошибки обрезаются до 200 символов
- ✅ Stack traces не содержат токенов

### 8. Graceful Degradation

При ошибках SDK не раскрывает внутренние детали:

```python
try:
    spas.search("test")
except FIASAPIError as e:
    # ✅ Безопасное сообщение
    print(e)  # "❌ Доступ запрещён. Проверьте токен."
    
    # ❌ Внутренние детали НЕ раскрываются
    # Не логируется: SQL запросы, внутренние пути, токены
```

---

## 🚨 Сообщение об уязвимостях

### Как сообщить о проблеме безопасности

Если вы обнаружили уязвимость в FIAS_RU SDK, **НЕ создавайте публичный issue**. Вместо этого:

1. **Отправьте email на**: `develop@eclips-team.ru`
2. **Укажите**:
   - Описание уязвимости
   - Шаги для воспроизведения
   - Потенциальное влияние

### Что делать НЕ нужно

❌ **НЕ** публикуйте детали уязвимости в открытых issue  
❌ **НЕ** пытайтесь эксплуатировать уязвимость на production системах  
❌ **НЕ** делитесь информацией с третьими лицами до исправления  
❌ **НЕ** публикуйте PoC код до выхода патча  

### Процесс обработки

1. **Подтверждение (48 часов)**: Мы подтвердим получение в течение 2 рабочих дней (за частую 1< дня)
2. **Оценка (3-5 дней)**: Оценим серьёзность и начнём работу над патчем
3. **Патч (2-3 дней)**: Разработаем и протестируем исправление
4. **Релиз**: Выпустим обновление с исправлением
5. **Публикация**: Опубликуем информацию об уязвимости (через 30 дней после патча)
---

## 🔐 Рекомендации по безопасному использованию

### 1. Регулярно ротируйте токены

```python
# ⏰ Рекомендуемая частота: каждые 90 дней
# 
# 1. Запросите новый токен на api.fias@tax.gov.ru
# 2. Обновите в Secret Manager / .env
# 3. Отзовите старый токен
# 4. Проверьте работу всех сервисов
```

### 2. Используйте отдельные токены для окружений

```python
# Development
FIAS_TOKEN_DEV=dev_token_...

# Staging
FIAS_TOKEN_STAGING=staging_token_...

# Production
FIAS_TOKEN_PROD=prod_token_...
```

### 3. Мониторьте использование токена

```python
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TokenUsageMonitor:
    def __init__(self):
        self.requests_count = 0
        self.last_reset = datetime.now()
    
    def log_request(self):
        self.requests_count += 1
        logger.info(f"FIAS requests today: {self.requests_count}")
        
        # Alert если близко к лимиту
        if self.requests_count > 9000:
            logger.warning("⚠️ Approaching daily limit!")

monitor = TokenUsageMonitor()

spas = SPAS(token=os.getenv("FIAS_TOKEN"))
result = spas.search("Москва")
monitor.log_request()
```

### 4. Валидируйте пользовательский ввод

```python
from FIAS_RU import SPAS, FIASValidationError

def safe_address_search(user_input: str):
    # Очистка
    user_input = user_input.strip()
    
    # Валидация длины
    if len(user_input) < 3:
        raise ValueError("Адрес слишком короткий")
    
    if len(user_input) > 500:
        raise ValueError("Адрес слишком длинный")
    
    # Запрещённые символы
    forbidden = ['<', '>', '{', '}', '|', '\\', '^', '`']
    if any(char in user_input for char in forbidden):
        raise ValueError("Адрес содержит запрещённые символы")
    
    # Поиск
    try:
        spas = SPAS(token=os.getenv("FIAS_TOKEN"))
        return spas.search(user_input)
    except FIASValidationError as e:
        logger.warning(f"Invalid input: {user_input}")
        raise ValueError(f"Некорректный адрес: {e}")
```

### 5. Обрабатывайте ошибки безопасно

```python
from FIAS_RU import SPAS, FIASError, FIASValidationError, FIASAPIError

def search_address_safe(query: str):
    try:
        spas = SPAS(token=os.getenv("FIAS_TOKEN"))
        return spas.search(query)
        
    except FIASValidationError as e:
        # ✅ Логируем, показываем общее сообщение
        logger.info(f"Validation error for query: {query}")
        return {"error": "Некорректный запрос"}
        
    except FIASAPIError as e:
        # ✅ Не раскрываем детали API
        logger.error(f"API error: {type(e).__name__}")
        return {"error": "Временная ошибка сервиса"}
        
    except FIASError as e:
        # ✅ Общая обработка
        logger.error(f"FIAS error: {e}")
        return {"error": "Ошибка поиска адреса"}
        
    except Exception as e:
        # ✅ Критические ошибки
        logger.exception("Unexpected error")
        return {"error": "Внутренняя ошибка сервера"}
```

---

## 🚨 Чек-лист безопасности

Перед деплоем в production проверьте:

### Токены
- [ ] Токен хранится в переменных окружения или secret manager
- [ ] `.env` файлы добавлены в `.gitignore`
- [ ] История Git не содержит токенов (проверьте `git log -p | grep "FIAS_TOKEN"`)
- [ ] Токены разные для dev/staging/prod
- [ ] Настроен процесс ротации токенов (каждые 90 дней)

### Конфигурация
- [ ] Используется HTTPS для API
- [ ] Настроен rate limiting (не более 100 req/min)
- [ ] Установлены таймауты (30-60 секунд)
- [ ] Connection pooling настроен корректно

### Код
- [ ] Валидируется пользовательский ввод
- [ ] Есть обработка всех типов ошибок
- [ ] Логирование не содержит чувствительных данных
- [ ] SDK обновлён до последней версии

### Мониторинг
- [ ] Настроен мониторинг использования API
- [ ] Настроены алерты на превышение лимитов
- [ ] Логируются все ошибки авторизации
---

## 📞 Контакты

- **Security email**: develop@eclips-team.ru
- **Token requests**: api.fias@tax.gov.ru
- **General support**: develop@eclips-team.ru
---

## 📚 Дополнительные ресурсы

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [HTTPX Security](https://www.python-httpx.org/)
- [Pydantic Security](https://docs.pydantic.dev/latest/)
- [Secret Management Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---
 
**Версия документа**: 0.1.0