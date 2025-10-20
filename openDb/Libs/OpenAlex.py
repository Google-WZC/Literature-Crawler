import requests


def OpenAlexReturn(KEYWORDS, AFFILIATION):
    # --- 构建API请求 ---
    base_url = "https://api.openalex.org/works"

    # 请求参数
    params = {
        "filter": f"raw_affiliation_strings.search:{AFFILIATION},default.search:{KEYWORDS}",
        # "per-page": 100, # 最大化输出
        "mailto": "15227663216@163.com",  # 你的邮箱
    }

    # 添加 User-Agent 请求头，这是非常好的习惯
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()

        if data["meta"]["count"] == 0:
            print("未找到相关论文，更改到SemanticScholar数据库....")
            return 1
        print(f"从 OpenAlex 找到 {data['meta']['count']} 篇相关论文，显示前几篇：")
        print("-" * 30)

        id = 0
        for work in data["results"]:
            title = work.get("title", "N/A")
            doi_url = work.get("doi", "No DOI available")

            bibtex = "BibTeX not available (no DOI)"
            if work.get("doi"):
                doi_id = work["doi"].replace("https://doi.org/", "")
                bibtex_url = f"https://api.citeas.org/product/{doi_id}"
                try:
                    bib_res = requests.get(bibtex_url, headers=headers)
                    if bib_res.status_code == 200:
                        bibtex = (
                            bib_res.json()
                            .get("citations", [{}])[0]
                            .get("citation", "Could not fetch BibTeX")
                        )
                except Exception as bib_e:
                    print(f"Fetching BibTeX for {doi_id} failed: {bib_e}")
            id += 1
            print(f"第{id}篇 标题: {title}")
            print(f"网址 (DOI): {doi_url}")
            print(f"BibTeX 引用:\n{bibtex}\n")
            print("-" * 30)
        return 0

    except requests.exceptions.HTTPError as e:
        print(f"请求失败，HTTP错误: {e}")
        print(f"返回的状态码: {e.response.status_code}")
        print(f"返回的内容: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"请求失败，网络或连接错误: {e}")


if __name__ == "__main__":
    # --- 搜索参数 ---
    KEYWORDS = ' "Physically Unclonable Function" OR "PUF" '
    AFFILIATION = (
        "National University of Defense Technology"  # 用于在原始单位字符串中搜索
    )

    OpenAlexReturn(KEYWORDS, AFFILIATION)
