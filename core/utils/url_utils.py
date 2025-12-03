from urllib.parse import urlparse, parse_qs

STATIC_EXT = {
    # 前端资源
    ".js", ".mjs", ".ts", ".jsx", ".tsx",
    ".css", ".scss", ".sass", ".less",
    # 图片资源
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg",
    ".webp", ".ico", ".tiff", ".tif", ".avif",
    # 字体资源
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    # 视频/音频
    ".mp4", ".webm", ".mov", ".avi", ".mp3", ".wav", ".ogg",
    # 数据类文件（一般视为静态）
    ".json", ".xml", ".rss", ".atom",
    # 静态下载内容
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2",
    ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx",
    # source map
    ".map",
    # 其他常见资源
    ".apk", ".ipa",
    ".csv", ".txt", ".yaml", ".yml",
}


def detect_path_type(path: str) -> str:
    """
    Detect path type.
    """
    if not path or path == "/":
        return "PAGE"
    lower = path.lower()
    for ext in STATIC_EXT:
        if lower.endswith(ext):
            return "STATIC"
    return "NORMAL"


def parse_request(request: str):
    """
    Parse nginx $request into method, path, raw query, protocol.
    Example: "GET /api/list?id=3&v=1 HTTP/1.1"
    """

    if not request:
        return {
            "method": "",
            "path": "",
            "query": "",
            "protocol": "",
            "path_type": ""
        }

    try:
        method, url, protocol = request.split(" ", 2)
    except ValueError:
        return {
            "method": "",
            "path": "",
            "query": "",
            "protocol": "",
            "path_type": ""
        }

    parsed = urlparse(url)

    return {
        "method": method,
        "path": parsed.path,
        "query": parsed.query,
        "protocol": protocol,
        "path_type": detect_path_type(parsed.path)
    }
