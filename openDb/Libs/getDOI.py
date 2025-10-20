import requests


def get_title_from_doi_resolver(doi: str) -> str:
    """
    使用通用的 doi.org 解析器和内容协商，根据 DOI 获取论文标题。
    这个方法适用于任何 DOI 注册机构（如 CrossRef, DataCite 等）。

    Args:
        doi: 论文的 DOI 字符串，例如 "10.1109/5.771073"。

    Returns:
        如果成功，返回论文的标题字符串。
        如果失败（例如 DOI 不存在或网络错误），返回一条错误信息。
    """
    # 1. 构建 doi.org 的 URL
    url = f"https://doi.org/{doi}"

    # 2. 设置请求头，这是最关键的一步！
    # 'Accept' header 告诉服务器我们想要什么格式的数据。
    # 'application/citeproc+json' 是一种标准的引文数据 JSON 格式。
    headers = {"Accept": "application/citeproc+json"}

    try:
        print(f"正在向 doi.org 请求 DOI: {doi} 的元数据...")
        # 3. 发送 GET 请求
        response = requests.get(url, headers=headers, timeout=10)

        # 4. 检查请求是否成功 (例如，处理 404 Not Found 错误)
        response.raise_for_status()

        # 5. 解析返回的 JSON 数据
        data = response.json()

        # 6. 安全地从 JSON 中提取标题
        # 在 citeproc+json 格式中，标题通常直接在 'title' 键下
        title = data.get("title", "Title not found in the response.")

        return title

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"Error: DOI '{doi}' not found."
        elif e.response.status_code == 406:
            return f"Error: The DOI resolver does not have metadata for '{doi}' in the requested format."
        else:
            return (
                f"Error: HTTP request failed with status code {e.response.status_code}."
            )

    except requests.exceptions.RequestException as e:
        return f"Error: A network or connection error occurred: {e}"
    except (KeyError, IndexError, ValueError):  # ValueError for bad JSON
        return "Error: Could not parse the title from the API response."


# --- 演示如何使用这个函数 ---
if __name__ == "__main__":
    # 示例 1: 一个来自 CrossRef 的经典论文 DOI
    doi1 = "10.1109/5.771073"  # "The structure of the page table..."
    title1 = get_title_from_doi_resolver(doi1)
    print(f"标题: {title1}\n" + "-" * 30)
