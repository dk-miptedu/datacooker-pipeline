import requests
import json

url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

token = {"access_token":"eyJjdHkiOiJqd3QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.ZDuP8nsrNCRShRGZmZEiQk4LiI2__e9LVgCVFt-ZY5rbytKMwTG6I6Z3mmyNfSk6RN4k-8yo4dHiQTVnx3JbXPRNEtZdrAWzY93JyyNE_K-6pQ12uBIIzw46Z84xFN0HDK7ghinb52UDgZXKbQ0qq6h0WTktQxPsyOm59GMwZgyoTvp8odH7CoaJg-k_Yd3JRCPPSQilfbaTkvBj4oEnJzgLiNhlLDsFVk2TokKrypqSe4uwHSqPtBCoozvUKsbM6fcjAYtkCdpF137esAUZ5gQOYeb9b4EK0uFt2SJIlz6ZWTIWu1M_RPDO_nQyua6KiWudlrxJtLiGdlP23hKKlQ.IYITjHIxRFCnPf_fsb8cIw.4h5TuAJTTYpvSpufzMa8gzeIr-3ZjhgMpouRhlGF-NPgkwgsTmL1qQZXovkWrFk4FDsFV7B0TYlcF-KiYky7suaVNseYrTwg2v-hltjTKgo4KfxLWeGQ0YskE5-ebNjdYc86lxQV1a9p6-zG8XXEW9QFhbWuKmCLRlY1u_EBtuSyw7sIursIBxACjfOp2F8MUFOM-AyGENXtUXV7WMT2-GxAXOD_gklyDC-UrSLMbL6732XojXZJy6lj-2ohGNALDa0wUxmfCqOeFUEkn_CK1aKalfgNInu8PBE4GUNdF0SXCemXNXE0nWN6CEEYz6qnEw0YgACGljaeh-jAexmkz2GHZkWwTCh-WfuaMnmXo9Prvpew0FIWpP7RzhaM0TELQSOujj5oNkYPpTM8RlnXaOHUo5lZJlKNrS-CG-c-xvDtErLQvxT0d_GPO9Q8-zgCU1QgNCpTdhxlNt3UrfhHBnxEjqAaArvsvs5xFmSLiMxJhc4toDYDGB87nVl2FvdW9fKLYbYwL68Y9xKrrttFa6kVAKp-UFpOWWf3Ipm6rGDEEGHOzMKDmFRNDy_oxS6TDadBE9n9bDJS77qXVe6G98Dge5m3J0KPC18vqTgNsEM_VVFYdjYG31mj_009djGIw8p8Btz0MNDkhZL7eX64R7ozME9RodHpM-npyYXq8X74VskLtdBr224Lk0clMf0gXXevDwWpSxIgII6FuViIbnTtD3onoO3Z20lHezRCYtY.N3L_2jD040A_QVoiOfheRllUSWTwJfOU_HBe5MGpwSM","expires_at":1732819049372}
answer = '''
{"personData":{"firstName":"Иван","lastName":"Иванов","middleName":"Иванович","gender":"M","birthDate":"19.12.2005","citizenship":"RUSSIA","educationStatus":"3","bachelorInfo":{"universityName":"Псковский Государственный университет","universityAddress":"Псковская область, г. Псков ул.Советская 21","educationSpecialty":"Информатика и вычислительная техника","educationStartDate":"01.09.2023","educationEndDate":"01.09.2027"},"schoolInfo":{"schoolName":"ГБОУ СОШ №1","schoolAddress":"Псковская область, г. Псков ул.Советская 21","schoolStartDate":"01.09.2012","schoolEndDate":"01.09.2023","diplomaID":"9283233923","finalExamSubjects":["Русский","Математика","Информатика"],"participationOlympiad":true,"prizePlaceOlympiad":0,"subjects":[{"subjectName":"Информатика","grade":"5"},{"subjectName":"Литература","grade":"4"},{"subjectName":"История","grade":"4"},{"subjectName":"Английский","grade":"2"},{"subjectName":"Математика","grade":"5"}]}}}
'''
payload = json.dumps({
  "model": "GigaChat",
  "messages": [
    {
      "role": "system",
      "content": f'получил ответ от ресурса образование об аттестате, помоги рассчитать средний балл: {answer}'
    },
#    {
#      "role": "user",
#      "content": "GigaChat — это сервис, который умеет взаимодействовать с пользователем в формате диалога, писать код, создавать тексты и картинки по запросу пользователя."
#    }
  ],
  "stream": False,
  "update_interval": 0
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': f'Bearer {token["access_token"]}'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.text)