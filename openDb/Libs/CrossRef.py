import requests


def get_title_from_doi(doi: str) -> str:
    """
    使用 CrossRef API，根据论文的 DOI 获取其标题。

    Args:
        doi: 论文的 DOI 字符串，例如 "10.1109/TC.2019.2923220"。

    Returns:
        如果成功，返回论文的标题字符串。
        如果失败（例如 DOI 不存在或网络错误），返回一条错误信息。
    """
    # 1. 构建 API 请求 URL
    # CrossRef API 的基本结构是 "https://api.crossref.org/works/{DOI}"
    base_url = "https://api.crossref.org/works/"
    url = f"{base_url}{doi}"

    # 2. 设置请求头 (Header)
    # 遵循 CrossRef 的 "polite" 礼貌原则，在 User-Agent 中提供联系方式是个好习惯
    headers = {"User-Agent": "MySimpleDOIResolver/1.0 (mailto:your-email@example.com)"}

    try:
        # 3. 发送 GET 请求
        response = requests.get(url, headers=headers, timeout=10)

        # 4. 检查请求是否成功
        # .raise_for_status() 会在遇到 4xx 或 5xx 错误时自动抛出异常
        response.raise_for_status()

        # 5. 解析 JSON 数据
        data = response.json()

        # 6. 从返回的数据中提取标题
        # CrossRef 的标题通常在 data['message']['title'][0]
        # 使用 .get() 方法可以安全地访问，避免因缺少键而导致的程序崩溃
        title = data.get("message", {}).get("title", ["Title not found"])[0]

        return title

    except requests.exceptions.HTTPError as e:
        # 处理 HTTP 错误，最常见的是 404 Not Found (DOI 不存在)
        if e.response.status_code == 404:
            return f"Error: DOI '{doi}' not found on CrossRef."
        else:
            return (
                f"Error: HTTP request failed with status code {e.response.status_code}."
            )

    except requests.exceptions.RequestException as e:
        # 处理网络连接等其他请求错误
        return f"Error: A network error occurred: {e}"
    except (KeyError, IndexError):
        # 处理 JSON 结构不符合预期的情况
        return "Error: Could not parse the title from the API response."


# --- 主程序：演示如何使用这个函数 ---
if __name__ == "__main__":
    # 示例 1: 一个有效的 DOI
    valid_doi = "10.1109/ICIPCA65645.2025.11138557"
    print(f"查询 DOI: {valid_doi}")
    title1 = get_title_from_doi(valid_doi)
    print(f"论文标题: {title1}\n")
