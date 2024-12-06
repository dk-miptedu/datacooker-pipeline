from gigachat import GigaChat
import json

def send_prompt_to_llm(student_fedresource: dict, parent1_fedresource: dict, parent2_fedresource: dict):

    credentials = 'MzgyZTdkNGItZTc5MS00NmU3LTg4NjctNDA0MjVlOGNjYjY5OjU1YWIyOWVmLTc4NWEtNGYyOC1iZDg2LTk3YzBkMzYxMmQzNg=='

    # Формируем промпт для LLM
    prompt = f"""
    Вы получили три JSON-файла:
    1. Данные о студенте: {json.dumps(student_fedresource, ensure_ascii=False)}
    2. Данные о первом родителе: {json.dumps(parent1_fedresource, ensure_ascii=False)}
    3. Данные о втором родителе: {json.dumps(parent2_fedresource, ensure_ascii=False)}

    Задача:
    1. Определите количество административных нарушений студента.
    2. Проверьте наличие процедуры банкротства у родителей.
    3. Сформируйте JSON-ответ по следующей структуре:

    {{
        "studentData": {{
            "administrativeOffense": <количество административных нарушений>
        }},
        "parentsData": {{
            "parentsBankruptcy": <true/false>
        }}
    }}

    
        """
    with GigaChat(credentials=credentials, verify_ssl_certs=False) as giga:
        response = giga.chat(prompt)
        # print(response.choices[0].message.content)

    return response.choices[0].message.content

def compare_results(local_result: dict, llm_result: str):
    llm_result_json = json.loads(llm_result)

    # Сравниваем результаты
    if local_result == llm_result_json:
        print("Результаты совпадают.")
    else:
        print("Результаты отличаются.")
        print("Локальный результат:", json.dumps(local_result, indent=4, ensure_ascii=False))
        print("Ответ LLM:", json.dumps(llm_result_json, indent=4, ensure_ascii=False))

def main():
    # Пример чтения файлов и выполнения функции
    with open("student_fedresource.json", 'r', encoding='utf-8') as f:
        student_fedresource = json.load(f)

    with open("parent1_fedresource.json", 'r', encoding='utf-8') as f:
        parent1_fedresource = json.load(f)

    with open("parent2_fedresource.json", 'r', encoding='utf-8') as f:
        parent2_fedresource = json.load(f)

    # Выполнение локальной функции для получения результата
    local_result = {
        "studentData": {
            "administrativeOffense": len([
                offense for offense in student_fedresource["result"].get("offesnseHistory", [])
                if offense["type"] == "административное"
            ])
        },
        "parentsData": {
            "parentsBankruptcy": any(
                parent.get("result", {}).get("bankruptcy", {}).get("currentBankruptcyProcedure", False)
                for parent in [parent1_fedresource, parent2_fedresource]
            )
        }
    }

    llm_result = send_prompt_to_llm(student_fedresource, parent1_fedresource, parent2_fedresource)
    return  llm_result,

    # compare_results(local_result, llm_result)

print(main())
if __name__ == "__main__":
    main()