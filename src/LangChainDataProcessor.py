import json
import re
from typing import List, Dict, Any
from langchain_gigachat.chat_models import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage
#from gigachat import GigaChat

class LangChainDataProcessor:
    """
    Класс для обработки нескольких файлов JSON и формирования выходного JSON
    на основе JSON-схемы с использованием LangChain и LLM (OpenAI).
    """

    def __init__(self, credentials: str, temperature: float = 0.8):
        """
        Инициализация процессора с использованием LLM от GigaChat LangChain.
        :param credentials: Ключ API.
        :param temperature: Параметр генерации для управления креативностью модели.
        """
        self.credentials = credentials
        self.temperature = temperature
        self.llm = self.initialize_model()

    def initialize_model(self):
        """Инициализирует объект GigaChat для работы с LLM."""
        
        return GigaChat(
            credentials=self.credentials,
            verify_ssl_certs=False,
            temperature=self.temperature
        )   

    def extract_description(self, data, schema):
        """Рекурсивно извлекает значения из данных на основе схемы."""
        description = {}
        for key, value in schema.get('properties', {}).items():
            if key in data:
                # Если свойство является объектом, рекурсивно обрабатываем его
                if value.get('type') == 'object':
                    nested_description = self.extract_description(data[key], value)
                    description[value.get('description', key)] = nested_description
                else:
                    # Добавляем значение из данных с использованием описания из схемы
                    description[value.get('description', key)] = data[key]
        return description

    def generate_descriptions(self, input_files: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Генерирует список описаний атрибутов из JSON Schema и их значениями из файла данных."""
        all_descriptions = []
        
        for file_pair in input_files:
            data_file = file_pair['data']
            schema_file = file_pair['schema']

            # Чтение данных из файла JSON
            with open(data_file, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            # Чтение схемы из файла JSON Schema
            with open(schema_file, 'r', encoding='utf-8') as schema_file:
                schema = json.load(schema_file)

            # Генерация описания с учетом вложенности
            description = self.extract_description(data, schema)
            all_descriptions.append(description)
        
        output_json_file = "temprorary.json"
        with open(output_json_file, 'w', encoding='utf-8') as output_file:
            json.dump(all_descriptions, output_file, ensure_ascii=False, indent=4)            

        return all_descriptions

    def load_json(self, file_path: str) -> Dict[str, Any]:
        """Загрузить JSON файл."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def process_files(self, input_files: List[Dict[str, str]], schema_file: str)-> Dict[str, Any]:
        """Обработать несколько файлов JSON и сформировать выходной JSON на основе схемы."""
        
        # Считываем все входные файлы
        input_data = self.generate_descriptions(input_files)

        # Считываем файл схемы
        schema = self.load_json(schema_file)

        #print(f'\n\nschema: \n{schema}')

        # Генерируем выходной JSON
        #print(f'Генерируем выходной JSON')
        output_json = self.generate_output_json(input_data, schema)

        #print('=' * 100)
        #print(output_json)
        #print('=' * 100)

        return output_json

    def generate_output_json(self, input_data: List[Dict[str, Any]], schema: Dict[str, Any]) -> Dict[str, Any]:
        """Сгенерировать выходной JSON на основе данных и схемы с использованием LangChain."""
        
        prompt = self.create_prompt(input_data, schema)
        # Переинициализация модели перед каждым запросом
        self.llm = self.initialize_model()       

        # Отправляем запрос в LLM с подготовленным запросом
        messages=[
            SystemMessage(content=prompt),
            #HumanMessage(content="Исключи повторяющиеся данные, сделай маппинг и верни JSON")
        ]
        response = self.llm.invoke(messages)
        #response = self.llm.chat(messages=[prompt])

        json_string = response.content.strip()
        json_match = re.search(r'```json\s*(.*?)\s*```', json_string, re.DOTALL)
        if json_match:
              json_string = json_match.group(1)

        #print(f'\n\n{json_string}\n\n')
        #print(f'\n\n{response.choices[0].message.content}\n\n')


        try:
            # Преобразуем ответ в словарь
            
            output_data = json.loads(json_string)
            #output_data = json.loads(response.choices[0].message.content)

        except json.JSONDecodeError as e:
            raise ValueError(f"Не удалось преобразовать ответ LLM в JSON: {e}")

        return output_data

    def create_prompt(self, input_data: List[Dict[str, Any]], schema: Dict[str, Any]) -> str:
        """Создать промпт для LLM."""
        
        input_data_str = json.dumps(input_data, separators=(', ', ": "), ensure_ascii=False)
        schema_str = json.dumps(schema, separators=(',', ":"), ensure_ascii=False)

        prompt_template = f"""
        Помоги, как кредитный менеджер, с учетом входных JSON-данных:
        {input_data_str}
        
        рассчитать значения для атрибутов указанных в JSON-схеме:
        {schema_str}
        
        и сформировать JSON для оценки заемщика. Убедись, что значения полей корректны и соответствуют требованиям схемы.
        Верни данные в формате JSON без комментариев и лишнего текста.
        """
        print(f"\n\nprompt_template:\n{prompt_template}\n")
        return prompt_template

    def save_output(self, output_path: str, data: Dict[str, Any]) -> None:
        """Сохранить итоговый JSON файл."""
        
        print(data)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

