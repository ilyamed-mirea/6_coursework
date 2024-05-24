from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class CountTagsTestCase(TestCase):
    def test_count_tags(self):
        url = reverse("count_tags")  # Замените 'count_tags' на имя вашего URL-шаблона

        # Тестовые данные
        html_input = """
            <html>
                <head>
                    <title>Test Page</title>
                </head>
                <body>
                    <h1>Welcome</h1>
                    <p class='main'>This is a test page.</p>
                    <div>
                        <p>Another paragraph</p>
                    </div>
                </body>
            </html>
        """

        # Отправка POST-запроса на API endpoint
        response = self.client.post(
            url, data={"html": html_input}, content_type="application/json"
        )

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка возвращаемых данных
        expected_data = {
            "tag_count": 8,
            "unique_tags": ["body", "div", "h1", "head", "html", "p", "title"],
        }
        self.assertEqual(response.json(), expected_data)
