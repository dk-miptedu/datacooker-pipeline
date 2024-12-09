from src.LangChainDataProcessor import LangChainDataProcessor

if __name__ == "__main__":
    temprorary_file_data = "input_information_data.json"
    
    processor = LangChainDataProcessor(credentials="OGU0ZjY4ZmQtMmFmZS00YmNkLTllODUtN2Q3ZGI3ZTRlNGYzOjEzNjFiZmViLTY4MTktNGE4ZS1iNDllLWFjZDA0MGU1ZDNlMg==")



    input_files = [
        {"data": "assets/анкета_на_получение_кредита.json", "schema": "assets/анкета_на_получение_кредита_схема.json"},
        {"data": "assets/объединенное_кредитное_бюро.json", "schema": "assets/объединенное_кредитное_бюро_схема.json"},
        {"data": "assets/ресурс_комитета_по_образованию.json", "schema": "assets/ресурс_комитета_по_образованию_схема.json"},
        {"data": "assets/федресурс_схема.json", "schema":"assets/федресурс_схема.json"}    
    ]

    schema_path = "assets/модель_схема.json"

    try:
        # Обрабатываем файлы и формируем JSON на основе схемы
        output_json = processor.process_files(input_files, schema_path)

        # Сохраняем выходной файл
        
        processor.save_output("модель_AI.json", output_json)

        print(f"Итоговый файл 'модель_AI.json' успешно создан.")
    
    except Exception as e:
        print(f"Ошибка: {e}")