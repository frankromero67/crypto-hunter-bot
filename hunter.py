import os
import requests

# Имя репозитория, который мы хотим мониторить (Выбираю сам)
REPO_OWNER = "ethereum"
REPO_NAME = "go-ethereum"
FILE_PATH = "README.md" # Файл, который мы хотим проверить

# Получаем токен из переменной окружения
GITHUB_TOKEN = os.environ.get("PAT_CRYPTO_MONITOR")
if not GITHUB_TOKEN:
    print("Error: PAT_CRYPTO_MONITOR secret not found.")
    exit(1)

API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3.raw"
}

def monitor_documentation():
    print(f"Monitoring documentation for {REPO_OWNER}/{REPO_NAME}...")
    try:
        # 1. Запрос содержимого файла
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        content = response.text
        
        # 2. Поиск потенциальной ошибки (ОЧЕНЬ простое правило)
        # Ищем, например, часто встречающуюся опечатку 'publically' (вместо 'publicly')
        typo_to_find = "publically"
        
        if typo_to_find in content:
            print(f"\n✅ НАЙДЕНА ЦЕЛЬ! Опечатка '{typo_to_find}' найдена в {FILE_PATH}.")
            print("Action required: Создайте Pull Request с исправлением!")
            # В реальном скрипте здесь можно отправить уведомление на почту или в Slack
            
            # Создаем файл-индикатор для лога Action
            with open("target_found.log", "w") as f:
                f.write(f"Found target in {REPO_OWNER}/{REPO_NAME}")
                
            return True
        else:
            print(f"❌ Clean. No typo '{typo_to_find}' found today.")
            return False

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e} - Check repository name and token permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    monitor_documentation()
