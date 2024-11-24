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
    You are a validation assistant. A value needs to be checked against specific criteria.
    The value is: {value}
    The criteria are:
    {criteria}

    Does the value satisfy all criteria? Return "Yes" if it satisfies all, otherwise return "No".
    """
    try:
        response = client.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
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
    status = 1  # По умолчанию ставим 1, если все проверки пройдены

    # Найти regex для текущего label
    regex_pattern = regex_data["regex"] if regex_data.get("label") == label else None
    
    # Найти criteria для текущего label
    criteria = (
        "\n".join([v for k, v in logic_data.items() if k.startswith("criteria_")])
        if logic_data.get("label") == label
        else None
    )

    # Если совпадение label не найдено в regex.json или logic.json
    if not regex_pattern and not criteria:
        results.append({"label": label, "value": value, "status": -1})  # Не найдено соответствие
        continue

    # Проверка значения через regex
    if regex_pattern and not re.match(regex_pattern, value):
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
