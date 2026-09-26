# pricetag 랜딩 페이지

빌드 과정이 없는 순수 HTML/CSS/JS 사이트예요. 폴더를 그대로 웹 호스팅에 올리면 됩니다.

```
index.html          한국어 페이지 (/)
en/index.html       영문 페이지 (/en/)
privacy.html        개인정보 처리방침 한국어 (/privacy.html)
en/privacy.html     개인정보 처리방침 영문 (/en/privacy.html)
subscribed.html     메일 확인 후 등록 완료 페이지 (Mailchimp에서 이 주소로 보냄)
assets/site.css     디자인 (pricetag 디자인 시스템 기준)
assets/site.js      다크 모드, 상품 데모, Mailchimp 가입
assets/fonts/       Pretendard (OFL 라이선스 포함)
assets/img/         로고, 상품 이미지
```

## 공개 전에 확인할 것

1. **상품 이미지**: Unsplash 무료 사진(운동화 Mojtaba Fahiminia, 헤드폰 Cosmin Ursea, 영양제 Supliful, 세럼 Muhammad Sulyman)을 같은 비율로 자른 것이에요. Unsplash 라이선스는 사진 사용만 허락하고 사진 속 상표까지 허락하지는 않아요. 헤드폰에 작은 제조사 로고가 있으니 신경 쓰이면 같은 파일 이름으로 덮어쓰세요.
2. **크롬 웹스토어 링크**: `build.py`의 `STORE_URL`에 들어 있어요. 바꾸면 `python3 build.py`를 다시 실행해요.
3. **개인정보 처리방침**: `privacy.html`, `en/privacy.html`로 만들어 두었고 두 언어 푸터와 가입 폼 아래 동의 안내에 링크돼 있어요. 크롬 웹스토어 개발자 대시보드의 "개인정보 보호 관행"에 `privacy.html` 주소를 넣으세요. 확장 프로그램이나 수집 항목이 바뀌면 `src/privacy/`도 함께 고쳐요.

## 올리는 방법 (둘 중 하나)

- **Netlify Drop**: app.netlify.com/drop 에 이 폴더를 끌어다 놓으면 바로 주소가 생겨요. 가장 쉬워요.
- **GitHub Pages**: 새 저장소에 이 폴더 내용을 올리고 Settings → Pages에서 main 브랜치를 선택해요. 확장 프로그램 저장소는 비공개이니 사이트용 저장소를 따로 만드세요.

## 문구를 고칠 때

`src/content.json`(랜딩 페이지)이나 `src/privacy/ko.html`·`en.html`(처리방침 본문)에서 한국어·영문 문구를 고친 뒤 `python3 build.py`를 실행하면 네 페이지가 다시 만들어져요. HTML 파일을 직접 고치면 다음 빌드 때 덮어써지니 주의하세요.

## Mailchimp 가입 연결

`assets/site.js` 맨 위 `MAILCHIMP_URL`과 두 HTML의 `<form action="...">`에 가입 주소가 들어 있어요. 버튼을 누르면 페이지를 벗어나지 않고 그 자리에서 결과 메시지가 나옵니다. 자바스크립트가 꺼진 브라우저에서는 Mailchimp 페이지가 새 탭으로 열려 가입돼요.

가입할 때 `LANG` 값(`ko` 또는 `en`)이 함께 전송돼요. Mailchimp에 LANG 필드를 만들어 두면 언어별로 나눠서 메일을 보낼 수 있어요.
