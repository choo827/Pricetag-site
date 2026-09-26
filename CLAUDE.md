# pricetag 랜딩 페이지 — Claude Code 작업 지침

이 저장소는 크롬 확장 프로그램 pricetag의 소개 웹사이트다. 확장 프로그램 코드는 별도의 비공개 저장소에 있다.

## 구조

```
build.py              src/content.json → index.html, en/index.html / src/privacy/*.html → privacy.html, en/privacy.html 생성
src/content.json      한국어(ko)·영문(en) 문구와 데모 데이터 전부
src/privacy/          개인정보 처리방침 본문 조각(ko.html, en.html). 머리말·푸터는 build.py가 붙인다
index.html            한국어 페이지 (생성 결과물)
en/index.html         영문 페이지 (생성 결과물)
privacy.html          개인정보 처리방침 한국어 (생성 결과물)
en/privacy.html       개인정보 처리방침 영문 (생성 결과물)
.nojekyll             GitHub Pages가 Jekyll 처리를 건너뛰게 한다
assets/site.css       스타일 (디자인 토큰을 CSS 변수로 사용)
assets/site.js        다크 모드, 언어 기억, 상품 데모 회전, Mailchimp 가입
assets/fonts/         Pretendard 300·400·500·700 + OFL 라이선스
assets/img/           로고 SVG, 상품 사진(Unsplash)
design/tokens.json    pricetag 디자인 시스템 원본 값
```

## 작업 규칙

1. **생성된 HTML을 직접 고치지 않는다.** 문구는 `src/content.json`, 처리방침 본문은 `src/privacy/`, 마크업은 `build.py`의 템플릿을 고친 뒤 `python3 build.py`를 실행한다. 한국어와 영문을 항상 함께 고친다.
2. **빌드 도구·npm 의존성·외부 CDN을 추가하지 않는다.** 순수 HTML/CSS/JS를 유지한다. 폰트와 이미지는 저장소에 포함한다.
3. **디자인 값은 `design/tokens.json`과 `assets/site.css`의 CSS 변수만 쓴다.** 새 색이나 크기를 추측해서 만들지 않는다. 핵심 규칙: 가격 표시는 말풍선이며 모서리 하나만 각지게(0) 두고 그 모서리가 가격 출처를 가리킨다. 브랜드 파랑 `#2E39A9`는 변환된 가격, 주요 버튼, 로고에만 쓴다.
4. **제품에 대한 주장은 실제 확장 프로그램 동작과 일치해야 한다.** 161개 통화(귀금속·XDR 제외), Frankfurter 기준 환율(보통 하루 1회 갱신, 추정치), 선택한 가격 텍스트만 읽음, 환율 요청에는 두 통화 코드만 전송, 계정 없음, 추적 없음. 확장 프로그램은 모든 웹사이트에서 동작하므로 "권한이 적다"는 식으로 과장하지 않는다. Pro(가격 히스토리, 위시리스트)는 아직 출시 전이며 "출시 예정"으로만 표기한다. 가격 하락 알림은 계획에서 빠졌으니 언급하지 않는다.
5. 반응형(860px, 440px 기준), 라이트·다크 모드, 키보드 조작, `prefers-reduced-motion`을 깨뜨리지 않는다. 변경 후 두 언어·두 모드·데스크톱·모바일 폭에서 확인한다.
6. 작업 단위마다 작게 커밋한다.

## Mailchimp

`assets/site.js`의 `MAILCHIMP_URL`과 `build.py` 템플릿의 `<form action>`에 같은 가입 주소가 들어 있다. 제출은 JSONP(`/post-json?...&c=콜백`)로 페이지 안에서 처리하고, 자바스크립트가 없으면 Mailchimp로 일반 전송된다. 함께 보내는 값은 `EMAIL`, 숨김 필드 `LANG`(ko/en), 스팸 방지 칸 `b_7a4b34e1ab518009c85cb469d_03c1a33707`(비워 둬야 함)이다. Mailchimp 쪽에는 LANG 필드(숨김)와 이중 확인이 설정돼 있다. 이 값들의 이름을 바꾸지 않는다.

## 남은 일

- 크롬 웹스토어 링크: `build.py`의 `STORE_URL`이 `#`이다. 주소를 받으면 채운다.
- 도메인이 정해지면 `canonical`, `og:url`, `og:image`, 절대 경로 `hreflang`을 추가한다.
- 배포: GitHub Pages(main 브랜치 루트). 처리방침은 호스팅을 GitHub Pages로 적고 있으니 호스팅을 바꾸면 `src/privacy/`도 고친다.
- 개인정보 처리방침이나 수집 항목이 바뀌면 두 언어 본문과 시행일을 함께 고친다.
