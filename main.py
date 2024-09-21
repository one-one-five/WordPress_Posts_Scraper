import json
import requests
from fake_useragent import UserAgent

# Создаем объект UserAgent для генерации случайных User-Agent заголовков
# Create UserAgent object to generate random User-Agent headers
ua = UserAgent(verify_ssl=False)

# Основной URL для запроса к API WordPress (необходимо вставить реальный URL)
# Main URL for requesting WordPress API (replace with actual URL)
URL = 'https://........../wp-json/wp/v2/posts?per_page=100&page=1'

# Имя файла, в который будут сохранены данные в формате JSON
# File name to store the scraped data in JSON format
FILE_NAME = '...........json'


def main():
    # Определяем заголовки для запроса, включая случайный User-Agent
    # Define request headers, including a random User-Agent
    headers = {
        'accept': '*/*',
        'user-agent': ua.random
    }

    # Делаем запрос, чтобы узнать общее количество страниц с постами
    # Make a request to get the total number of pages with posts
    count_post = int(requests.get(url=URL).headers['X-WP-TotalPages'])

    # Открываем файл для записи данных в формате JSON
    # Open a file to save the data in JSON format
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        file.write("[")  # Начало списка JSON / Start of the JSON list
        # Цикл по страницам API, начиная с первой страницы до последней
        # Loop through API pages from the first to the last
        for page in range(1, count_post):
            # Создаем динамическую ссылку для каждой страницы
            # Create a dynamic link for each page
            LINK = f'https://........../wp-json/wp/v2/posts?per_page=100&page={page}'
            # Делаем запрос к API для получения данных с каждой страницы
            # Make a request to the API to get data from each page
            response = requests.get(url=LINK, headers=headers)
            print(f'[*] Being processed: {LINK}')
            data = response.json()  # Преобразуем ответ в формат JSON / Convert the response to JSON format

            # Проходим по каждому посту на странице
            # Iterate through each post on the page
            content = {}
            for i in data:
                # Извлекаем необходимые данные для каждого поста
                # Extract required data for each post
                content['id'] = i.get('id')  # ID поста / Post ID
                content['title'] = i.get('title')['rendered']  # Заголовок поста / Post title
                content['date'] = i.get('date')  # Дата публикации / Date of publication
                content['link'] = i.get('link')  # Ссылка на пост / Link to the post
                content['content'] = i.get('content')['rendered']  # Содержимое поста / Post content

                # Записываем данные в JSON файл
                # Write the data to the JSON file
                json.dump(content, file, indent=4, ensure_ascii=False)
                file.write(',\n')  # Добавляем разделитель для следующего объекта / Add separator for the next object

        file.write(']')  # Закрываем список JSON / End the JSON list


if __name__ == '__main__':
    main()  # Запускаем основную функцию / Run the main function
