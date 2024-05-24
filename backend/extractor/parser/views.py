import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import HTMLSerializer


@swagger_auto_schema(method="post", request_body=HTMLSerializer)
@api_view(["POST"])
def extract_text(request):
    serializer = HTMLSerializer(data=request.data)
    if serializer.is_valid():
        html = serializer.validated_data["html"]
        text_fragments = re.findall(r"<.*?>(.*?)</.*?>", html)
        return Response(text_fragments)
    return Response(serializer.errors, status=400)


@swagger_auto_schema(method="post", request_body=HTMLSerializer)
@api_view(["POST"])
def replace_text(request):
    serializer = HTMLSerializer(data=request.data)
    if serializer.is_valid():
        html = serializer.validated_data["html"]
        modified_html = re.sub(r"<.*?>(.*?)</.*?>", "REPLACED", html)
        return Response(modified_html)
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
