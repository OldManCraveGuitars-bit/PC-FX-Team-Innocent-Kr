# v0.73 — 미검증 테스트 버전

> **전체 플레이 검증이 끝나지 않았습니다.** 게임의 모든 대사와 영상, 일본어 원음과 자막 타이밍을 끝까지 확인하지 않았습니다. 누락·오역·표시 오류를 발견하면 스크린샷과 함께 알려 주세요.

## 이번 수정

- 글자가 나오는 동안 **Ⅱ를 한 번 누르면** 현재 대사가 원래 줄바꿈대로 끝까지 표시됩니다. 손을 떼도 완성 상태가 유지됩니다.
- 이후 **Ⅰ을 누르면** 다음 대사로 넘어가며 그 장면의 모션과 글자가 처음부터 시작합니다. 다음 대사에서도 같은 조작을 반복할 수 있습니다.
- 현재 대사의 음성은 Ⅱ 입력 뒤에도 계속됩니다. 현재 캐릭터 모션을 마지막 자세로 강제 고정하는 기능은 포함하지 않았습니다.
- v0.72의 한국어 대사 1,371개, 영상 8개 장면 자막 168개, 한글 시작 화면, 브리핑 배경 수정과 GUI 패처를 포함합니다. 원래 영어인 UI 문구는 유지했습니다.

## 확인한 범위

디스크 데이터를 다시 읽어 글씨와 자막 데이터가 일치하는지 확인했습니다. 미션 1 도입 브리핑에서 Ⅱ를 짧게 누르고 Ⅰ로 다음 대사에 넘어가는 과정을 두 차례 반복해 화면과 음성을 확인했습니다. 새 기능의 모든 대사 장면 적용, 게임 전체 플레이, 영상 자막 원음 대조는 아직 검증하지 않았습니다. **테스트용으로 사용해 주세요.**

## 화면

![한국어 시작 화면](https://raw.githubusercontent.com/OldManCraveGuitars-bit/PC-FX-Team-Innocent-Kr/v0.73/images/title-in-game.png)

| 대사 표시 중 | Ⅱ를 눌러 대사 완성 |
| --- | --- |
| ![대사 표시 중](https://raw.githubusercontent.com/OldManCraveGuitars-bit/PC-FX-Team-Innocent-Kr/v0.73/images/dialogue-fast-before-v0.73.png) | ![Ⅱ를 눌러 대사 완성](https://raw.githubusercontent.com/OldManCraveGuitars-bit/PC-FX-Team-Innocent-Kr/v0.73/images/dialogue-fast-after-v0.73.png) |

![여성 캐릭터의 한글 게임 대사](https://raw.githubusercontent.com/OldManCraveGuitars-bit/PC-FX-Team-Innocent-Kr/v0.73/images/dialogue-mission1-female-1.png)

## 적용

ZIP을 풀어 **Team-Innocent-KR-Patcher.exe**를 실행하거나 EXE를 단독으로 내려받으세요. 보유한 일본판 14트랙 CUE를 선택해 **한국어 패치 적용**을 누르면 새 폴더에 결과가 만들어집니다. 원본 파일은 수정하지 않습니다. 지원 원본의 Track 02 SHA-256은 `56931167724db296481606b6ba4d873097754faf4a59bd352a030dd8301028aa`입니다.

## 감사

[Team Innocent 영어 패치 팀](https://github.com/DerekPascarella/TeamInnocent-EnglishPatchPCFX)의 자료와 텍스트 변경 범위가 이 한국어 작업에 큰 도움이 됐습니다. 영어 패치에 참여한 모든 분께 감사드립니다.
