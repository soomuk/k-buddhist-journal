# K-Buddhist Journal — 한국 불교학 학술지 편집검토 스킬

한국 불교학 학술지 29종의 투고규정·원고작성요령을 내장한 Claude 스킬입니다. 학술지 이름과 원고만 주면 그 학술지 규정에 따라 형식·각주·참고문헌·대장경 표기·오탈자·사실관계를 전수 점검합니다. 결과는 편집자가 바로 반영할 수 있는 편집점검보고서(.docx)로 나옵니다.

**제작** 수묵학술문화연구소 (Soomuk) · **라이선스** [MIT](LICENSE)

---

## 설치

### Claude Code

Claude Code를 실행한 뒤 아래 두 줄을 차례로 입력합니다.

```
/plugin marketplace add soomuk/k-buddhist-journal
/plugin install k-buddhist-journal@soomuk
```

설치 후 Claude Code를 다시 시작하거나 `/reload-plugins`를 입력하면 바로 쓸 수 있습니다.

터미널에서 바로 설치하려면 다음처럼 입력합니다.

```bash
claude plugin marketplace add soomuk/k-buddhist-journal
claude plugin install k-buddhist-journal@soomuk
```

### Claude 웹·데스크톱 앱 (claude.ai)

1. [Releases](https://github.com/soomuk/k-buddhist-journal/releases)에서 `journal-review.zip`을 내려받습니다.
2. Claude 설정의 스킬(Skills) 메뉴에서 이 zip 파일을 업로드합니다.
3. 대화에서 아래 사용 예처럼 요청합니다.

---

## 사용 예

원고 파일을 첨부하거나 경로를 알려 주고 이렇게 요청하면 됩니다.

- `『선학』 투고규정으로 이 논문 편집 검토해줘`
- `불교학연구에 낼 원고야. 형식 오류랑 오탈자 잡아줘`
- `이 폴더 논문 5편 전부 한국불교학 규정으로 편집점검보고서 만들어줘`

직접 불러올 수도 있습니다: `/k-buddhist-journal:journal-review 선학 논문.pdf`

검토는 다음 순서로 진행됩니다.

1. 학술지 규정 분석: 명시 규정 / 예시 관행 / 규정 부재 항목
2. 저널 전용 편집 기준표 작성
3. 논문별 전수 검토: 형식, 문장, 각주, 참고문헌, 불교학 문헌·대장경 표기, 사실관계
4. 수정사항 표 작성: 등급(필수수정·강력권고·권고·확인필요), 위치, 수정안, 규정 근거
5. 편집점검보고서 `.docx` 저장

- **원고 형식**: PDF, DOCX, HWPX, ZIP을 받습니다. 구형 HWP는 PDF나 HWPX로 저장해서 주세요.
- **목록에 없는 학술지**: 투고규정 PDF를 함께 주면 같은 절차로 검토합니다.

---

## 수록 학술지 (29종)

강좌미술사 · 대각사상 · 동아시아불교문화 · 동악미술사학 · 명상심리상담 · 무형문화연구 · 보조사상 · 불교문예연구 · 불교미술사학 · 불교연구 · 불교와 사회 · 불교철학 · 불교학리뷰 · 불교학밀교학연구 · 불교학보 · 불교학연구 · 선문화연구 · 선학 · 세화불학 · 원불교사상과 종교문화 · 인도철학 · 전자불전 · 정토학연구 · 종학연구 · 한국교수불자연합 · 한국불교사연구 · 한국불교학 · 한마음연구 · IJBTC

---

## 저장소 구조

```
.claude-plugin/marketplace.json        ← 플러그인 마켓 등록 정보
plugins/k-buddhist-journal/
├─ .claude-plugin/plugin.json          ← 플러그인 정보(버전)
└─ skills/journal-review/
   ├─ SKILL.md                         ← 검토 절차
   ├─ references/
   │  ├─ journal-index.md              ← 학술지 목록
   │  ├─ review-rules.md               ← 정밀 검토 세부 규칙
   │  ├─ journals/*.md                 ← 학술지별 규정 원문 텍스트(쪽별)
   │  └─ pdfs/*.pdf                    ← 학술지별 규정 원본 PDF
   └─ scripts/report_to_docx.py        ← 보고서 Word 변환
```

## 규정이 바뀌었을 때

1. `references/pdfs/`의 해당 PDF를 새 파일로 교체합니다.
2. `references/journals/`의 해당 `.md` 파일도 함께 고칩니다.
3. `plugin.json`의 `version`을 올립니다(예: 1.0.0 → 1.0.1).
4. GitHub에 올립니다.

사용자는 `/plugin marketplace update soomuk`으로 새 버전을 받습니다.

---

## 주의사항

- AI 검토 결과는 참고자료입니다. 최종 판단은 연구자·편집자가 직접 해야 합니다.
- 인명·생몰연대·문헌명·대장경 번호·최신 투고규정은 반드시 사람이 재확인하십시오.
- 수록된 규정은 수집 시점 기준입니다. 학회 홈페이지에서 최신 규정을 확인하고, 바뀌었다면 최신 PDF를 함께 주십시오.
- 학술지 규정 문서(`references/pdfs/`, `references/journals/`)의 저작권은 각 학회에 있으며 MIT 라이선스 대상이 아닙니다.
