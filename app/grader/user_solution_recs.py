from typing import List
import os
from dotenv import load_dotenv
import requests
import json


url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

class GetRecGiga:
    def __init__(self, 
                 errors: List[str], 
                 user_solution: str,
                ):
        """
        :param errors: Ошибки исполнения кода во время открытых и скрытых тестов.
        :param user_solution: Пользовательское решение в виде строки с разделителями \n.

        :return: Рекомендацию в виде str.
        """
        load_dotenv()
        self.errors = errors
        self.user_solution = user_solution
        self.credentials = os.getenv("GIGACHAT_CREDENTIALS")

    def get_recomendation(self):
        payload = json.dumps({
  "model": "GigaChat",
  "messages": [
    {
      "role": "system",
      "content": "Ты профессиональный переводчик на английский язык. Переведи точно сообщение пользователя."
    },
    {
      "role": "user",
      "content": "GigaChat — это сервис, который умеет взаимодействовать с пользователем в формате диалога, писать код, создавать тексты и картинки по запросу пользователя."
    }
  ],
  "stream": False,
  "update_interval": 0
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer <TOKEN>'
}

response = requests.request("POST", url, headers=headers, data=payload)







