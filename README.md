# floor-field-evacuation

Floor Field 셀 오토마톤 모델로 방 대피를 시뮬레이션하고, 출구 앞에 둔 대피 보조 로봇의 위치가 대피 시간에 주는 영향을 실험하는 프로젝트.

## 진행 상황

- [x] 0단계: 원 논문 읽기 → 설계 노트 → 레포 (2026-11)
- [ ] 1단계: Python 셀 오토마톤 구현 (정적·동적 플로어 필드, 패닉도, 경쟁·양보, 관성) → 대피 애니메이션
- [ ] 2단계: 로봇(장애물) 위치·패닉도별 대피 시간 비교 실험 → 그래프·해석
- [ ] 3단계: 군중 밀도 기반 로봇 위치 선택 규칙 + ROS 2 노드 → 데모

## 문서

- [설계 노트](docs/design-note.md): 격자·규칙·파라미터·재현 검증 기준
- [원메모 (2024-03-20)](docs/original-memo-2024-03-20.txt): 이 프로젝트의 출발점이 된 『정체학』 독서 메모

## 참고 논문

1. C. Burstedde, K. Klauck, A. Schadschneider, J. Zittartz (2001). *Simulation of pedestrian dynamics using a 2-dimensional cellular automaton*. Physica A 295. [arXiv:cond-mat/0102397](https://arxiv.org/abs/cond-mat/0102397)
2. A. Kirchner, A. Schadschneider (2002). *Simulation of evacuation processes using a bionics-inspired cellular automaton model for pedestrian dynamics*. Physica A 312. [arXiv:cond-mat/0203461](https://arxiv.org/abs/cond-mat/0203461)
3. A. Kirchner, K. Nishinari, A. Schadschneider (2003). *Friction effects and clogging in a cellular automaton model for pedestrian dynamics*. Phys. Rev. E 67. [arXiv:cond-mat/0209383](https://arxiv.org/abs/cond-mat/0209383)
