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


class ExtractTextTestCase(TestCase):
    def test_extract_text(self):
        url = reverse("extract_text")
        html_input = """
            <html>
                <head>
                    <title>Test Page</title>
                </head>
                <body>
                    <h1>Welcome</h1>
                    <p>This is a <strong>test</strong> page.</p>
                    <script>console.log('Hello');</script>
                    <style>body { background-color: white; }</style>
                </body>
            </html>
        """
        response = self.client.post(
            url, data={"html": html_input}, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {"text_content": "Test Page Welcome This is a test page."}
        self.assertEqual(response.json(), expected_data)


class ReplaceTextTestCase(TestCase):
    def test_replace_text_inside_tags(self):
        url = reverse("replace_text")
        html_input = (
            "<html><body><h1>Welcome</h1><p>This is a test page.</p></body></html>"
        )
        replace_data = {"html": html_input, "old_text": "test", "new_text": "sample"}
        response = self.client.post(
            url, data=replace_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_html = (
            "<html><body><h1>Welcome</h1><p>This is a sample page.</p></body></html>"
        )

        self.assertEqual(
            response.content.decode("utf-8").strip()[1:-1], expected_html.strip()
        )
