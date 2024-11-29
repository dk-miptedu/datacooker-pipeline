import requests
import yaml
import os


def load_config(file_path= 'assets/config/__gigachat_api_key.yaml'):
    if not os.path.isfile(file_path):
        # Убираем "__" из имени файла
        file_path = file_path.replace('__', '', 1)

    if not os.path.exists(file_path):
        print(os.getcwd())
        print(f'Файл не найден: {file_path}')
        exit(1)

    with open(file_path, 'rt') as config_file:
        config = yaml.safe_load(config_file)
    return config


#file_path = '.config/__fin_bot_config.yaml'
config = load_config()
print(config)


url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
auth_key = str(config['Authorization Key'])
payload={
  'scope': 'GIGACHAT_API_PERS'
}
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': 'f54dd776-93c7-4741-a007-f92fc7f09bb7',
  'Authorization': f'Basic {auth_key}'
}

print(f'{headers}')
response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.text)