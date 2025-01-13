import feedparser
from datetime import datetime
import os
from pathlib import Path
from email.utils import parsedate_to_datetime

# 상수 정의
BLOG_URL = "https://secrett2633.github.io/feed.xml"
MAX_POSTS = 5
README_PATH = "README.md"
BLOG_SECTION_TITLE = "### Latest Blog Posts"

def get_posts():
    """RSS 피드에서 블로그 포스트를 가져옵니다."""
    feed = feedparser.parse(BLOG_URL)
    return feed.entries[:MAX_POSTS]

def format_date(date_str):
    """RSS 피드의 날짜를 원하는 형식으로 변환합니다."""
    # email.utils의 parsedate_to_datetime을 사용하여 RFC 2822 형식의 날짜를 파싱
    date = parsedate_to_datetime(date_str)
    return date.strftime("%Y.%m.%d")

def build_post_line(post):
    """각 포스트를 마크다운 형식의 문자열로 변환합니다."""
    title = post.title
    date = format_date(post.published)
    link = post.link
    return f"- [{title} ({date})]({link})"

def update_readme():
    """README.md 파일을 최신 블로그 포스트로 업데이트합니다."""
    try:
        # README 파일 읽기
        if os.path.exists(README_PATH):
            with open(README_PATH, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = ""

        # 블로그 포스트 섹션 이전 내용 가져오기
        before_posts = content.split(BLOG_SECTION_TITLE)[0].strip()

        # 최신 포스트 가져오기
        posts = get_posts()
        post_lines = [build_post_line(post) for post in posts]
        posts_content = "\n".join(post_lines)

        # 새로운 README 내용 생성
        new_content = f"{before_posts}\n\n{BLOG_SECTION_TITLE}\n{posts_content}"

        # 파일 저장
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)

        print("README.md has been updated successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e

if __name__ == "__main__":
    update_readme()