import json
import re
from openai import OpenAI
import uuid

# Инициализация OpenAI
client = OpenAI(api_key="XXX")

# Загрузка данных
with open("regex.json", "r") as regex_file:
    regex_data = json.load(regex_file)

with open("logic.json", "r") as logic_file:
    logic_data = json.load(logic_file)

with open("stan.json", "r") as stan_file:
    stan_data = json.load(stan_file)

# Функция для проверки значения через OpenAI
def validate_with_openai(value, criteria):
    """
    Проверяет значение `value` с помощью OpenAI на соответствие критериям.
    """
    prompt = f"""
    You are a validation assistant. Your task is to verify if a given value satisfies a list of criteria.
    - The value is: "{value}".
    - The criteria are:
      {criteria}

    Answer with "Yes" if the value satisfies all the criteria, or "No" if it does not.
    Provide no additional text, only "Yes" or "No".
    """
    try:
        response = client.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5  # Сокращаем длину ответа, чтобы избежать лишнего текста
        )
        result = response.choices[0].message.content.strip()
        return result.lower() == "yes"
    except Exception as e:
        print(f"Error with OpenAI: {e}")
        return False


# Проверка значений из `stan.json`
results = []

for item in stan_data:
    label = item.get("label")
    value = item.get("value")
    status = 1  # По умолчанию успешный статус

    # print(f"\nProcessing label: {label}, value: {value}")  # Отладочный вывод

    # Проверяем наличие совпадений по label в regex.json и logic.json
    regex_pattern = regex_data["regex"] if regex_data.get("label") == label else None
    criteria = (
        "\n".join([v for k, v in logic_data.items() if k.startswith("criteria_")])
        if logic_data.get("label") == label
        else None
    )

    if not regex_pattern and not criteria:
        # Если совпадений по label нет
        # print(f"No match found for label: {label}")  # Отладочный вывод
        results.append({"label": label, "value": value, "status": -1})
        continue

    # Проверка регулярного выражения
    if regex_pattern:
        if not re.fullmatch(regex_pattern, value):  # Используем fullmatch
            # print(f"Value '{value}' does not match regex '{regex_pattern}'")  # Отладочный вывод
            results.append({"label": label, "value": value, "status": -1})  # Не соответствует regex
            continue

    # Проверка значения через criteria
    if criteria:
        if not validate_with_openai(value, criteria):
            # print(f"Value '{value}' does not satisfy criteria")  # Отладочный вывод
            status = 0  # Не соответствует criteria

    # Добавляем результат
    results.append({"label": label, "value": value, "status": status})

# Сохранение результатов
with open("validation_results.json", "w") as result_file:
    json.dump(results, result_file, indent=4)

# Добавление уникального ID
with open("validation_results.json", "r+") as result_file:  # Открываем файл для чтения и записи
    validation_results = json.load(result_file)
    
    # Добавляем ID
    for item in validation_results:
        item["id"] = str(uuid.uuid4())  # Генерация уникального ID
    
    # Перематываем указатель в начало файла, чтобы перезаписать данные
    result_file.seek(0)
    json.dump(validation_results, result_file, indent=4)
    result_file.truncate()  # Удаляем оставшийся текст (если новый JSON короче)

print("Validation complete. IDs added to validation_results.json.")
