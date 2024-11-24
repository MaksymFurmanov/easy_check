import json
import re
from openai import OpenAI

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

    # Найти regex для текущего label
    regex_pattern = regex_data["regex"] if regex_data.get("label") == label else None
    
    # Найти criteria для текущего label
    criteria = (
        "\n".join([v for k, v in logic_data.items() if k.startswith("criteria_")])
        if logic_data.get("label") == label
        else None
    )

    # Проверка регулярного выражения
    if regex_pattern:
        if not re.fullmatch(regex_pattern, value):  # Используем fullmatch
            results.append({"label": label, "value": value, "status": -1})  # Не соответствует regex
            continue

    # Проверка значения через criteria
    if criteria:
        if not validate_with_openai(value, criteria):
            status = 0  # Не соответствует criteria

    # Добавляем результат
    results.append({"label": label, "value": value, "status": status})

# Сохранение результатов
with open("validation_results.json", "w") as result_file:
    json.dump(results, result_file, indent=4)

print("Validation complete. Results saved in validation_results.json.")
