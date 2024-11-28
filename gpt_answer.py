import json
from jsonschema import validate, ValidationError
import os

# --- ШАГ 1: Чтение и валидация данных анкеты ---
def read_and_validate_json(file_path, schema_path):
    """Читает JSON файл и проверяет его на соответствие схеме."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        with open(schema_path, 'r', encoding='utf-8') as schema_file:
            schema = json.load(schema_file)

        validate(instance=data, schema=schema)
        print(f"Файл {file_path} успешно прошел валидацию.")
        return data
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except ValidationError as e:
        print(f"Ошибка валидации JSON файла {file_path}: {e.message}")
    except Exception as e:
        print(f"Ошибка при обработке {file_path}: {e}")

    return None

# --- ШАГ 2: Чтение внешних данных ---
def read_external_json(file_path):
    """Читает внешний JSON файл, который может иметь изменяющуюся структуру."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"Файл {file_path} успешно прочитан.")
            return data
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")

    return None

# --- ШАГ 3: Приведение данных к модели ---
def normalize_data(data, model_schema):
    """Приводит данные к структуре, указанной в модели."""
    normalized_data = {}
    for key in model_schema.get('properties', {}):
        if key in data:
            normalized_data[key] = data[key]
        else:
            normalized_data[key] = None  # Заполняем пустыми значениями, если данных нет

    return normalized_data

# --- ШАГ 4: Сбор данных из всех источников ---
def merge_data(anketa_data, external_data_list, model_schema):
    """Объединяет данные анкеты и внешних источников."""
    final_data = {}

    # Добавление данных анкеты
    final_data['anketa'] = normalize_data(anketa_data, model_schema)

    # Добавление данных из внешних источников
    for i, external_data in enumerate(external_data_list):
        source_name = f"external_source_{i + 1}"
        final_data[source_name] = normalize_data(external_data, model_schema)

    return final_data

# --- ШАГ 5: Запись итогового JSON файла ---
def write_json(output_path, data):
    """Записывает итоговые данные в JSON файл."""
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Итоговый JSON файл записан в {output_path}.")
    except Exception as e:print(f"Ошибка при записи JSON файла: {e}")

# --- ШАГ 6: Основная функция ---
def main():
    anketa_path = "/mnt/data/анкета_на_получение_кредита_схема"
    external_paths = [
        "/mnt/data/объединенное_кредитное_бюро_схема",
        # Дополнительные внешние файлы можно добавлять сюда
    ]
    model_schema_path = "/mnt/data/модель_схема"
    output_path = "/mnt/data/итоговая_модель.json"

    # Чтение и валидация анкеты
    anketa_data = read_and_validate_json(anketa_path, anketa_path)

    if anketa_data is None:
        print("Ошибка при обработке анкеты. Завершение работы.")
        return

    # Чтение внешних данных
    external_data_list = [read_external_json(path) for path in external_paths]
    external_data_list = [data for data in external_data_list if data is not None]

    if not external_data_list:
        print("Ошибка при обработке внешних данных. Завершение работы.")
        return

    # Чтение схемы модели
    with open(model_schema_path, 'r', encoding='utf-8') as file:
        model_schema = json.load(file)

    # Объединение данных
    final_data = merge_data(anketa_data, external_data_list, model_schema)

    # Запись итогового JSON файла
    write_json(output_path, final_data)

if __name__ == "__main__":
    main()