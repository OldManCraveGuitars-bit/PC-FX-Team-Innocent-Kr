# v0.8 — 스테이지 1 검수 완료 · 대사 검수 및 화면 정렬

> **스테이지 1 검수 완료.** 사용자 플레이 테스트와 제보 사항 반영 기준입니다. 스테이지 2·3, 모든 분기 및 실기 동작은 아직 전체 검증 전인 테스트 버전입니다.

## v0.8 — 스테이지 1 검수 완료

**스테이지 1 검수 완료.** 사용자 플레이 테스트와 제보 사항 반영을 기준으로 합니다. 스테이지 2·3의 전체 플레이와 모든 분기 검수는 계속 진행합니다.

### 이번 변경 사항

- 미션 1 클리어 후 누락됐던 나레이션 **3종**을 한글화했습니다. 이 부분은 영상이 아닌 게임의 스크롤 문구이며, 현재 나레이션 문구 23개를 반영했습니다.
- 전체 대사 1,371개와 초기 문구 207개를 검수해 **267개 항목의 띄어쓰기·표현·문장 길이**를 수정했습니다. 원문의 명시적 줄바꿈과 제어 코드를 유지했습니다.
- 타이머 확인 문구에 남아 있던 일본어 분 단위 `分`을 **분**으로 수정했습니다.
- 결과 화면의 **SCENARIO POINT, 점수 숫자, MISSION CLEAR, PERFECT CLEAR, TRY AGAIN, SAME MISSION, CONGRATULATIONS!**를 가운데 정렬했습니다.
- 미션 1·2·3 선택 화면의 제목도 글자 길이에 맞춰 가운데 정렬했습니다.
- 기존 대사 빠른 넘기기, 영상 건너뛰기, MO 재생 및 타이틀 복귀 수정도 포함합니다.

### 화면 확인

아래는 에뮬레이터에서 정렬을 확인한 재현 화면입니다.

| 미션 제목 가운데 정렬 | 결과 문구·점수 가운데 정렬 |
| --- | --- |
| ![미션 2 한글 제목 가운데 정렬](https://raw.githubusercontent.com/OldManCraveGuitars-bit/PC-FX-Team-Innocent-Kr/v0.8/images/mission2-title-v0.8.png) | ![미션 1 결과 문구와 점수 가운데 정렬](https://raw.githubusercontent.com/OldManCraveGuitars-bit/PC-FX-Team-Innocent-Kr/v0.8/images/mission1-result-v0.8.png) |

<p align="center">
  <img src="https://raw.githubusercontent.com/OldManCraveGuitars-bit/PC-FX-Team-Innocent-Kr/v0.8/images/perfect-clear-v0.8.png" alt="CONGRATULATIONS와 PERFECT CLEAR 가운데 정렬" width="600">
</p>

일반 Mednafen에서 세 미션의 제목과 일반 클리어·재도전·퍼펙트 클리어 결과 화면을 확인했습니다. 별도 귀환 재현에서는 한글 나레이션이 끝난 뒤 대사창 없이 결과 화면으로 넘어가는 것도 확인했습니다. 전체 완료 조건별 분기와 PC-FX 실기 동작까지 검증한 것은 아닙니다.

## 조작 방법

- 글자가 나오는 동안 **Ⅱ**: 현재 대사를 끝까지 표시합니다. 음성은 계속 재생됩니다.
- 대사가 모두 표시된 뒤 **Ⅰ**: 현재 음성과 모션을 중단하고 다음 대사로 넘어갑니다.
- **MO 01 인물 자료**: PLAY에서 **Ⅱ로 글자 완성 → Ⅰ로 다음 자료**를 반복할 수 있습니다.
- 오프닝·인게임 영상에서 **Ⅰ을 약 1.2초간 유지**: 영상·음성·자막을 종료하고 다음 장면으로 넘어갑니다. 짧은 입력은 누적하지 않습니다.

## 다운로드와 적용

- **Team-Innocent-KR-Patcher.exe**: 패치 데이터가 포함된 Windows UI 패처입니다. Python 설치가 필요 없습니다.
- **Team-Innocent-KR-v0.8-test.zip**: EXE, 패치 파일, 설명서, 스크린샷, 라이선스를 포함합니다.
- **.tipatch / .xdelta**: 개별 패치 파일입니다.
- **SHA256SUMS-v0.8.txt**: 배포 파일의 무결성 확인용 해시입니다.

**일본판 원본 CUE/BIN에 새로 적용해 주세요.** 이전 패치본에 덧씌우지 마세요. 원본 게임 CUE/BIN은 배포물에 포함하지 않습니다.

**업데이트 후에는 새 디스크를 처음부터 부팅해 주세요.** 이전 버전의 에뮬레이터 강제 저장 상태에는 예전 코드가 남아 있을 수 있습니다. 게임 안에서 만든 저장 파일은 새로 부팅한 뒤 불러오세요.

## 감사

[Team Innocent 영어 패치 팀](https://github.com/DerekPascarella/TeamInnocent-EnglishPatchPCFX)의 공개 자료와 작업이 한국어 패치 제작에 **큰 도움**이 됐습니다. 영어 패치에 참여한 모든 분께 감사드립니다.
