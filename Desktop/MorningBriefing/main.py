import os
import json
import requests
from datetime import datetime
from playwright.sync_api import sync_playwright

# 환경 변수 (GitHub Secrets 등으로 관리)
KAKAO_REST_API_KEY = os.environ.get("KAKAO_REST_API_KEY")
KAKAO_REFRESH_TOKEN = os.environ.get("KAKAO_REFRESH_TOKEN")

def refresh_access_token():
    """
    6시간마다 만료되는 액세스 토큰을 리프레시 토큰으로 자동 갱신
    """
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": KAKAO_REST_API_KEY,
        "refresh_token": KAKAO_REFRESH_TOKEN
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("access_token")
    else:
        raise Exception(f"토큰 갱신 실패: {response.text}")

def generate_mindmap_html():
    """
    5가지 나뭇가지와 색상 코드가 적용된 마인드맵 HTML 생성
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: 'Apple SD Gothic Neo', sans-serif; background: #f8fafc; margin: 0; padding: 30px; }
            .container { width: 1200px; background: white; padding: 40px; border-radius: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
            .header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #e2e8f0; padding-bottom: 20px; }
            .title { font-size: 24px; font-weight: 800; color: #0f172a; margin: 0; }
            .center-node { background: #0f172a; color: white; padding: 16px; border-radius: 10px; text-align: center; margin-bottom: 25px; font-size: 18px; font-weight: bold; }
            .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
            .branch { border-left: 5px solid; padding-left: 14px; background: #f8fafc; padding: 12px; border-radius: 0 8px 8px 0; }
            .branch h3 { margin: 0 0 6px 0; font-size: 16px; }
            .branch ul { margin: 0; padding-left: 16px; color: #334155; font-size: 13px; line-height: 1.4; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div style="color: #64748b; font-size: 13px; margin-bottom: 5px;">GLOBAL MARKET MORNING BRIEFING</div>
                <h1 class="title">세계 경제 & 증시 핵심 인사이트 마인드맵</h1>
            </div>
            <div class="center-node">🎯 중심 이슈: 연준 금리 인하 기대감 후퇴 및 미 국채 금리 급등</div>
            <div class="grid">
                <div class="branch" style="border-color: #3b82f6;">
                    <h3 style="color: #3b82f6;">1. 미국 증시 영향</h3>
                    <ul><li>나스닥 기술주 중심 차익실현 매물 출회</li><li>대형 빅테크 밸류에이션 부담 가중</li></ul>
                </div>
                <div class="branch" style="border-color: #10b981;">
                    <h3 style="color: #10b981;">2. 환율 및 외환시장</h3>
                    <ul><li>원달러 환율 1,380원선 상향 돌파</li><li>엔화 약세 심화에 따른 아시아 통화 동반 약세</li></ul>
                </div>
                <div class="branch" style="border-color: #f59e0b;">
                    <h3 style="color: #f59e0b;">3. 원자재 및 에너지</h3>
                    <ul><li>중동 지정학적 리스크 완화로 유가 안정세</li><li>금·구리 등 안전자산 및 산업재 혼조세</li></ul>
                </div>
                <div class="branch" style="border-color: #8b5cf6;">
                    <h3 style="color: #8b5cf6;">4. 반도체 및 공급망</h3>
                    <ul><li>AI 반도체 수요 견조하나 단기 단가 조정</li><li>글로벌 반도체 설비투자(CAPEX) 경쟁 지속</li></ul>
                </div>
                <div class="branch" style="border-color: #ec4899; grid-column: span 2;">
                    <h3 style="color: #ec4899;">5. 국내 증시 (KOSPI / KOSDAQ)</h3>
                    <ul><li>외국인 순매도세 전환 및 코스피 2,650선 테스트, 수급 이탈 주의</li></ul>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    filename = "briefing.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    return os.path.abspath(filename)

def convert_html_to_image(html_path):
    """
    Playwright를 이용해 HTML 파일을 고해상도 PNG 이미지로 변환
    """
    image_path = "briefing.png"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(f"file://{html_path}")
        page.screenshot(path=image_path, full_page=True)
        browser.close()
    return os.path.abspath(image_path)

def send_kakao_memo(access_token):
    """
    카카오톡 '나에게 보내기' API 전송
    """
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # [주의] 본인의 GitHub 아이디와 저장소명으로 수정하세요!
    public_image_url = "git remote set-url origin https://github.com/tkdtjrk-sangbong/Morning-briefing.git" 

    template_object = {
        "object_type": "feed",
        "content": {
            "title": f"[{datetime.now().strftime('%m/%d')} 모닝 브리핑] 세계 경제 & 증시 마인드맵",
            "description": "오늘 아침 증시에 가장 큰 영향을 미칠 핵심 뉴스와 5가지 연관 브랜치 분석 리포트입니다.",
            "image_url": public_image_url,
            "image_width": 1200,
            "image_height": 800,
            "link": {
                "web_url": "https://developers.kakao.com",
                "mobile_web_url": "https://developers.kakao.com"
            }
        }
    }
    
    response = requests.post(url, headers=headers, data={"template_object": json.dumps(template_object)})
    if response.status_code == 200:
        print("카카오톡 전송 성공!")
    else:
        print(f"전송 실패: {response.text}")

if __name__ == "__main__":
    print("1. 토큰 갱신 중...")
    token = refresh_access_token()
    
    print("2. HTML 마인드맵 생성 중...")
    html_file = generate_mindmap_html()
    
    print("3. 이미지 변환 중...")
    img_file = convert_html_to_image(html_file)
    print(f"이미지 생성 완료: {img_file}")
    
    send_kakao_memo(token)