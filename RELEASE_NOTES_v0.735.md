# v0.735 — 미검증 테스트 버전

> **전체 플레이 검증이 끝나지 않은 테스트 버전입니다.** 모든 대사·영상·원음과 자막 타이밍을 끝까지 확인하지 않았습니다.

## 수정 내용

- **음성·모션 즉시 넘기기:** Ⅱ로 글자를 완성한 뒤 Ⅰ을 누르면 현재 음성과 캐릭터 모션을 끊고 다음 대사로 넘어갑니다. 다음 음성과 모션은 해당 대사의 시작부터 재생합니다. v0.73의 음성 종료 대기를 수정했습니다.
- **영상 자막 위치:** 새 문장으로 바뀔 때 자막이 잠깐 화면 상단에 튀던 현상을 수정했습니다.
- **대사 표기:** `제~대로`를 `제대로`로 수정했습니다.
- 한국어 대사 1,371개, 영상 8개 장면 자막 168개, 한글 시작 화면, 기본 창에서 패치 버튼이 보이는 GUI 패처를 포함합니다. 원래 영어인 UI 문구는 유지합니다.

## 확인한 범위

미션 1 브리핑에서 Ⅱ → Ⅰ을 반복하고, 음성이 끝나기 전 다음 대사와 모션으로 넘어가는 것을 확인했습니다. 최종 디스크 코드로도 재확인했습니다. 자막 위치 오류는 동일 구간의 수정 전후 영상 프레임과 좌표 기록을 비교했습니다. 디스크 재읽기 검사와 일본판 원본에 대한 패치 적용 검사를 통과했습니다.

**모든 장면의 빠른 넘기기와 전체 플레이 검증은 아직 완료되지 않았습니다.** 번역과 자막에도 추가 수정이 필요할 수 있습니다.

## 화면

![한국어 시작 화면](https://raw.githubusercontent.com/OldManCraveGuitars-bit/PC-FX-Team-Innocent-Kr/v0.735/images/title-in-game.png)

| Ⅱ로 글자를 완성 | 음성 도중 Ⅰ을 눌러 다음 대사로 전환 |
| --- | --- |
| ![현재 대사 완성](https://raw.githubusercontent.com/OldManCraveGuitars-bit/PC-FX-Team-Innocent-Kr/v0.735/images/dialogue-complete-v0.735.png) | ![다음 대사와 모션 시작](https://raw.githubusercontent.com/OldManCraveGuitars-bit/PC-FX-Team-Innocent-Kr/v0.735/images/dialogue-next-v0.735.png) |

![여성 캐릭터의 한글 게임 대사](https://raw.githubusercontent.com/OldManCraveGuitars-bit/PC-FX-Team-Innocent-Kr/v0.735/images/dialogue-mission1-female-1.png)

## 적용 방법

**Team-Innocent-KR-Patcher.exe**를 실행하고 일본판 원본 CUE를 선택한 뒤 **한국어 패치 적용**을 누르세요. Python 설치가 필요 없습니다. ZIP에는 EXE, 안내, tipatch와 xdelta가 들어 있습니다. 게임 디스크 파일은 포함하지 않습니다.

v0.73 패치본 위에 덧씌우지 말고 **일본판 원본에서 다시 적용**하세요. 업데이트 후 새 디스크를 처음부터 부팅하세요. 이전 버전의 에뮬레이터 강제 저장 상태에는 예전 실행 코드가 남아 있을 수 있으므로, 새 부팅 후 게임 내 저장 파일을 불러오세요.

지원 원본 Track 02 SHA-256: `56931167724db296481606b6ba4d873097754faf4a59bd352a030dd8301028aa`

## 감사

[Team Innocent 영어 패치 팀](https://github.com/DerekPascarella/TeamInnocent-EnglishPatchPCFX)의 자료와 텍스트 변경 범위가 이 한국어 작업에 큰 도움이 됐습니다. 영어 패치에 참여한 모든 분께 감사드립니다.
