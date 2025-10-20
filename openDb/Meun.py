from Libs.OpenAlex import OpenAlexReturn
from Libs.SemanticScholar import SemanticScholarReturn

from Libs.getDOI import get_title_from_doi_resolver


def Get():
    print("欢迎使用论文信息查询工具！")
    KEYWORDS = " xxxxxx00 "
    AFFILIATION = (
        "National University of Defense Technology"  # 用于在原始单位字符串中搜索
    )
    if OpenAlexReturn(KEYWORDS, AFFILIATION) != 0:
        SemanticScholarReturn(KEYWORDS, AFFILIATION)


def ReadDOI():
    doi = input("请输入论文的 DOI（例如 10.1109/5.771073）：").strip()
    title = get_title_from_doi_resolver(
        doi
    )  # if DOI means https://doi.org/{DOI} is accessible
    print(f"通过 DOI 获取的论文标题: {title}")


if __name__ == "__main__":
    Get()
    # ReadDOI()
