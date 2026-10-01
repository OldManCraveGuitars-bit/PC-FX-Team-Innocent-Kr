# v0.72 — 미검증 테스트 버전

> **전체 플레이 검증이 끝나지 않았습니다.** 모든 문구와 영상의 자연 호출, 일본어 원음과 자막 타이밍을 끝까지 확인하지 않았습니다. 누락·오역·표시 오류를 발견하면 스크린샷과 함께 Issues에 알려 주세요.

## 이번 수정

- 미션 1 초반 브리핑에서 모니터 아래 배경이 잘못 그려지던 문제를 고쳤습니다. 자막 화면 설정이 게임 화면으로 넘어갈 때 원판 값으로 복원됩니다.
- 패치 프로그램의 기본 창에서 **한국어 패치 적용** 버튼과 진행 기록이 바로 보이도록 크기와 배치를 고쳤습니다.
- 첫 오프닝 후반의 일본어 화면 문장과 빠졌던 음성 대사 자막 초안을 추가했습니다.
- 두 번째 오프닝 노래에 한국어 자막 초안을 추가했습니다. **노래 가사와 타이밍은 원음 재검수가 필요합니다.**
- 별도 화면 레이어 자막은 확인된 영상 장면 8개, 총 168개입니다. 게임 대사 1,371개와 원래 영어인 UI 유지 방침은 같습니다.

## 확인한 범위

일본판 원본과 v0.72를 같은 조작 순서로 미션 1 브리핑까지 실행했습니다. 잘못 그려지던 배경의 크기와 위치가 원판과 일치하고, 화면 설정값도 원판과 같았습니다. 디스크 저장 데이터 재읽기 검사를 통과했고, tipatch와 xdelta를 원본 Track 02에 각각 적용한 결과가 v0.72 목표 해시와 일치했습니다. EXE에 들어간 패치 데이터 검사와 기본 창의 버튼 표시 검사도 통과했습니다. **게임 전체 플레이와 모든 자막의 원음 대조는 아직 남아 있습니다.**

## 화면

![한글 시작 화면](https://raw.githubusercontent.com/OldManCraveGuitars-bit/PC-FX-Team-Innocent-Kr/v0.72/images/title-in-game.png)

![v0.72에서 수정된 브리핑 배경](https://raw.githubusercontent.com/OldManCraveGuitars-bit/PC-FX-Team-Innocent-Kr/v0.72/images/briefing-background-v0.72.png)

![여성 캐릭터의 한글 게임 대사](https://raw.githubusercontent.com/OldManCraveGuitars-bit/PC-FX-Team-Innocent-Kr/v0.72/images/dialogue-mission1-female-1.png)

## 적용

ZIP을 풀고 **Team-Innocent-KR-Patcher.exe**를 실행하거나 EXE를 단독으로 내려받으세요. 일본판 14트랙 CUE를 선택한 뒤 **한국어 패치 적용**을 누릅니다. 원본 파일은 수정하지 않으며, 결과는 새 폴더에 만듭니다. 원본 Track 02 SHA-256은 `56931167724db296481606b6ba4d873097754faf4a59bd352a030dd8301028aa`여야 합니다. Python을 사용하는 경우 ZIP의 `apply_patch.cmd`를 실행할 수 있습니다.

## 감사

[Team Innocent 영어 패치 팀](https://github.com/DerekPascarella/TeamInnocent-EnglishPatchPCFX)의 자료와 텍스트 변경 범위가 이 한국어 작업에 큰 도움이 됐습니다. 영어 패치에 참여한 모든 분께 감사드립니다.
