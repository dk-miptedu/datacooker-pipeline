import requests
import json

auth_token = "eyJjdHkiOiJqd3QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.RSg_BS_1Qn8xDkKjodQrqEMVH2l6nHKCr_R2vIBWJYmfY5o1aRL5bhLhme0s47mOZPkU5yKTVAAps7u4AEFGTBCN--gqGVkAlTLUkK-68mB8mXJJQsfMmteqAft0HEQlxERmg3ZoraWNmWyY83_MgwZu_SVMKZvUZCUMb22vmcQY1B6v2PuAkRAnVYd9N1mzH-3sUFC0OKN4BLVHBVw0xr3tZEAwLtK26fVOM3fTofKPHunLMk_5SCT2DCYjMcSDHxM-zPOE5UqaW30GFaMGRU1031CuL25-0OHgDNCZckKQAzgmMOdHLWhA1SB_DNNW3Sk3AIX_7pa1aQxwIuutWg.foGlv1FxBy8DfbxoJ3VZug.GaHqmwBTDPhtOeHanDptL0PxEVdXFgf73iU24SSsMIhh0oSHSs9GFnPmep9fxFnMQU71fcRKDCsfbmXQYnScNipY7jYpK0uMM4XtEHlCfvVleJ_CUp8dSPcLEtYpZgAcg4aGVSFThFAx2ZJ69d_2UmCOJZhpPfRGrI1zA9FkNS7TpWznxqS0SErxEfNrPzNxltlZ6P9AykSoTbtv4peWGc_1oA96mH0RH99PyYeN5ecFebV8WuP54GelEsRpjFXt2RQP99WWRNFKKzoOB0h3GKbRN7Zc9GjTqoiDhu9tHWCwm8h2hTst9eBiPuCuNpg92bSGLYWxPr44A7MNlUG-QmFEe1F3WOOsEdo1ySc7fKG7Cz_0RfOTm9s83XZ21tLG2rmcWeZYm35KarUXAdMkwF1--6pqSGgq1p-ESGggVD48CfOh68Aqoig-zfxLbZgJ1ttZlXwZ6_E-l99-kFWMtVYscU8sbDESlUbFu1aCzNOdELp_q9XgUaIEjMwRsMrJYp7hWbibKKTm_5bDIP0c8nmuYOv0DNLaefMD6vhtKQ-G5kr0xVjUG542t4FtHKd6rPsv4HBWsUvl5XakVGH06ETOjOBpvKsRskK5GFi-md47z4Urt2XxPkcOdRM86zm2KYSenhnnI9yjtH_3iPaGfrcrsaiL_LofzQLVnKoMVZTbjj54IA-Bh0Yv33E3IysdNxT6kRdh3cDsiBdaZrwyjfgrYJ3r5gVy8J-xsIJV_qE.BHosnRkdoxFRyX28OYZvz7K-T_UqTEYx_6y-BAq3aPI"

def get_chat_completion(auth_token, user_message, conversation_history=None):
    """
    Отправляет POST-запрос к API чата для получения ответа от модели GigaChat в рамках диалога.

    Параметры:
    - auth_token (str): Токен для авторизации в API.
    - user_message (str): Сообщение от пользователя, для которого нужно получить ответ.
    - conversation_history (list): История диалога в виде списка сообщений (опционально).

    Возвращает:
    - response (requests.Response): Ответ от API.
    - conversation_history (list): Обновленная история диалога.
    """
    # URL API, к которому мы обращаемся
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    # Если история диалога не предоставлена, добавляем в неё системный промт
    if conversation_history is None or conversation_history == []:
        conversation_history = [
            {
                "role": "system",
                "content": "ты менеджер по продажам, твоя задача сообщать цены из прайс-листа и погоду"
                }
            ]

    # Добавляем сообщение пользователя в историю диалога
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    # json схемы доступных функций
    giga_functions = [
    {
        "name": "weather_forecast",
        "description": "Возвращает температуру в Москве",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Местоположение, например, название города"
                    }
            },
            "required": ["location"]
            },
        "return_parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Местоположение, например, название города"
                    },
                "temperature": {
                    "type": "integer",
                    "description": "Температура для заданного местоположения"
                    },
                "forecast": {
                    "type": "array",
                    "items": {
                        "type": "string"
                        },
                    "description": "Описание погодных условий"
                    },
                "error": {
                    "type": "string",
                    "description": "Возвращается при возникновении ошибки. Содержит описание ошибки"
                    }
                }
            }
        },
        {
            "name": "get_full_pricelist",
            "description": "Возвращает цены на всю имеющуюуся продукцию",
            "parameters": {
                "type": "object",
                "properties": {
                    "products": {
                        "type": "string",
                        "description": f"список наиболее подходящих продуктов из списка {price_list['вид продукции'].to_list()}"
                        }
                    },
                "required": ["products"]
                },
            "return_parameters": {
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "Наименование продукции"
                        },
                    "price": {
                        "type": "integer",
                        "description": "Цена продукции в рублях РФ"
                        },
                    "error": {
                        "type": "string",
                        "description": "Возвращается при возникновении ошибки. Содержит описание ошибки"
                        }
                    }
                }
            },
             {
                 "name": "get_prices",
                 "description": "Возвращает цену на запрашиваемый продукт",
                 "parameters": {
                     "type": "object",
                     "properties": {
                         "products": {
                             "type": "string",
                             "description": f"список наиболее подходящих продуктов из списка {price_list['вид продукции'].to_list()}"
                             }
                         },
                     "required": [
                         "products"
                         ]
                     },
                 "few_shot_examples": [
                     {
                         "request": "сколько стоит лопатка?",
                         "params": {
                             "products": ["Свиная лопатка"]
         Функция при запросе выдаёт все доступные цены из прайслиста, здесь так же используется фиктивный параметр 'products'. Создадим json схему функций для модели:                     }
                         }
                     ],
                 "return_parameters": {
                     "type": "object",
                     "properties": {
                         "products": {
                             "type": "string",
                             "description": "Наименование продукции"
                             },
                         "price": {
                             "type": "integer",
                             "description": "Цена для данного вида продукции"
                             },
                         "error": {
                             "type": "string",
                             "description": "Возвращается при возникновении ошибки. Содержит описание ошибки"
                             }
                         }
                     }
                 }
    ]
    # Подготовка данных запроса в формате JSON
    payload = json.dumps({
        "model": "GigaChat-Pro-preview",
        "messages": conversation_history,
        "function_call": "auto",
        "functions": giga_functions,
        "temperature": 0.5,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 32000,
        "repetition_penalty": 1,
        "update_interval": 0
    })
    # Заголовки запроса
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }
    # словарь с функциями для обработки запроса
    available_functions = {
        "weather_forecast": weather_forecast,
        "get_full_pricelist": get_full_pricelist,
        "get_prices": get_prices
        }
    # Выполнение POST-запроса и возвращение ответа
    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        response_data = response.json()
        # проверяем ответ модели на наличие обращений к функциям
        try:
          # json с информацией о необходимой функции
          func_calls = response_data['choices'][0]['message']['function_call']
          # имя вызываемой функции
          func_name = func_calls['name']
          # аргументы вызываемой функции
          func_args = func_calls['arguments']
          # достаём нужную функцию из словаря 
          function_to_call = available_functions[func_name]
          
          # добавляем в историю сообщений ответ модели с вызовом функции, БЕЗ ЭТОГО МОДЕЛЬ НЕ ОТВЕТИТ
          conversation_history.append(response_data['choices'][0]['message'])
          # добавляем в историю сообщений результаты функции
          conversation_history.append(
              {
                  "role": "function",
                  "content": function_to_call(**func_args),
                  "name": func_name
                  }
              )
          # обновляем данные
          payload = json.dumps({
              "model": "GigaChat-Pro-preview",
              "messages": conversation_history,
              "function_call": "auto",
              "functions": giga_functions,
              "temperature": 0.5,
              "top_p": 0.1,
              "n": 1,
              "stream": False,
              "max_tokens": 32000,
              "repetition_penalty": 0.5,
              "update_interval": 0
              })
          # повторяем зарос  
          response = requests.post(url, headers=headers, data=payload, verify=False)
          response_data = response.json()
          # for func in func_calls:
        except:
          pass

        # Добавляем ответ модели в историю диалога
        conversation_history.append({
            "role": "assistant",
            "content": response_data['choices'][0]['message']['content']
        })

        return response, conversation_history
    except requests.RequestException as e:
        # Обработка исключения в случае ошибки запроса
        print(f"Произошла ошибка: {str(e)}")
        return None, conversation_history
    
conversation_history = []
esponse, conversation_history = get_chat_completion(auth_token, "дай цены по всей продукции", conversation_history)
print(response, conversation_history)