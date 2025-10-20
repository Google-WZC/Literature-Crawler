import requests
import os


def SemanticScholarReturn(KEYWORDS, AFFILIATION):
    # --- 搜索参数 ---
    FULL_QUERY = f'({KEYWORDS}) AND affiliation:("{AFFILIATION}")'

    # --- 构建API请求 ---
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": FULL_QUERY,
        "limit": 25,
        "fields": "title,externalIds",
    }

    # API申请页面：https://www.semanticscholar.org/product/api#api-key-form
    api_key_path = os.path.join(os.path.dirname(__file__), "SemanticScholarAPIKey")
    if os.path.exists(api_key_path):
        with open(api_key_path, "r") as f:
            YOUR_API_KEY = f.read().strip()
    else:
        YOUR_API_KEY = ""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    # 如果 API Key 存在，就添加到请求头中
    if YOUR_API_KEY:
        headers["x-api-key"] = YOUR_API_KEY
    else:
        print(
            "【警告】未使用 Semantic Scholar API Key，可能会遇到 429 请求速率限制错误。"
        )

    try:
        print("正在请求 Semantic Scholar API...")
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # 这行会在遇到 429 等错误时抛出异常

        data = response.json()

        total_results = data.get("total", 0)
        results_list = data.get("data", [])

        if total_results == 0:
            print(
                "未找到相关论文，你可手动从[https://scholar.google.com/][https://ieeexplore.ieee.org/Xplore/home.jsp]查找论文"
            )
            return 1
        print(f"从 Semantic Scholar 找到 {total_results} 篇相关论文，显示前几篇：")
        print("-" * 30)

        for work in results_list:
            title = work.get("title", "N/A")

            doi = work.get("externalIds", {}).get("DOI")

            doi_url = f"https://doi.org/{doi}" if doi else "No DOI available"

            bibtex = "BibTeX not available (no DOI)"
            if doi:
                bibtex_url = f"https://api.citeas.org/product/{doi}"
                try:
                    # 增加超时以防止请求卡住
                    bib_res = requests.get(bibtex_url, headers=headers, timeout=5)
                    if bib_res.status_code == 200:
                        bibtex = (
                            bib_res.json()
                            .get("citations", [{}])[0]
                            .get("citation", "Could not fetch BibTeX")
                        )
                except Exception as bib_e:
                    print(f"Fetching BibTeX for {doi} failed: {bib_e}")

            print(f"标题: {title}")
            print(f"网址 (DOI): {doi_url}")
            print(f"BibTeX 引用:\n{bibtex}\n")
            print("-" * 30)
        return 0

    except requests.exceptions.HTTPError as e:
        print(f"请求失败，HTTP错误: {e}")
        print(f"返回的状态码: {e.response.status_code}")
        print(f"返回的内容: {e.response.text}")
        if e.response.status_code == 429:
            print(
                "\n【解决方案】你遇到了 '请求过多' (429) 错误。请等待5分钟后再试，或者申请一个免费的 API Key 并填入脚本中以获得更高的请求限制。"
            )
    except requests.exceptions.RequestException as e:
        print(f"请求失败，网络或连接错误: {e}")


if __name__ == "__main__":
    # --- 搜索参数 ---
    KEYWORDS = ' "Physically Unclonable Function" OR "PUF" '
    AFFILIATION = (
        "National University of Defense Technology"  # 用于在原始单位字符串中搜索
    )

    SemanticScholarReturn(KEYWORDS, AFFILIATION)
