import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import HTMLSerializer, ReplaceTextSerializer


@swagger_auto_schema(method="post", request_body=HTMLSerializer)
@api_view(["POST"])
def extract_text(request):
    serializer = HTMLSerializer(data=request.data)
    if serializer.is_valid():
        html = serializer.validated_data["html"]
        # Удаление тегов script и style вместе с их содержимым
        html = re.sub(r"<script.*?</script>", "", html, flags=re.DOTALL)
        html = re.sub(r"<style.*?</style>", "", html, flags=re.DOTALL)
        # Удаление всех тегов, оставляя только текстовое содержимое
        text_content = re.sub(r"<[^>]+>", "", html)
        # Удаление последовательных пробелов и переносов строк
        text_content = re.sub(r"\s+", " ", text_content).strip()
        return Response({"text_content": text_content})
    return Response(serializer.errors, status=400)


@swagger_auto_schema(method="post", request_body=ReplaceTextSerializer)
@api_view(["POST"])
def replace_text(request):
    serializer = ReplaceTextSerializer(data=request.data)
    if serializer.is_valid():
        html = serializer.validated_data["html"].replace("\n", "").replace("\r", "")
        old_text = serializer.validated_data["old_text"]
        new_text = serializer.validated_data["new_text"]

        # Функция для замены текста внутри тегов
        def replace_text_inside_tags(match):
            tag = match.group(1)
            text = match.group(2)
            replaced_text = re.sub(re.escape(old_text), new_text, text)
            return f'<{tag}>{replaced_text}</{tag.split(" ")[0]}>'

        # Замена текста только внутри тегов
        updated_html = re.sub(
            r"<([^>]+)>(.*?)</\1>", replace_text_inside_tags, html, flags=re.DOTALL
        )

        return Response(updated_html)
    return Response(serializer.errors, status=400)


@swagger_auto_schema(method="post", request_body=HTMLSerializer)
@api_view(["POST"])
def count_tags(request):
    serializer = HTMLSerializer(data=request.data)
    if serializer.is_valid():
        html = serializer.validated_data["html"]
        tags = re.findall(r"<[^/].*?>", html)
        tag_count = len(tags)
        unique_tags = set(tag[1:-1].split(" ")[0] for tag in tags)
        return Response(
            {"tag_count": tag_count, "unique_tags": sorted(list(unique_tags))}
        )
    return Response(serializer.errors, status=400)


@swagger_auto_schema(method="post", request_body=HTMLSerializer)
@api_view(["POST"])
def validate_html(request):
    serializer = HTMLSerializer(data=request.data)
    if serializer.is_valid():
        html = serializer.validated_data["html"]
        stack = []
        for tag in re.findall(r"<.*?>", html):
            if tag.startswith("</"):
                if not stack or stack.pop() != tag[2:-1]:
                    return Response({"is_valid": False})
            else:
                stack.append(tag[1:-1])
        is_valid = len(stack) == 0
        return Response({"is_valid": is_valid})
    return Response({"is_valid": False})
