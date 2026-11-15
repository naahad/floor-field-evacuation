import numpy as np
import matplotlib.pyplot as plt

def make_room(L=61):
    """(L+2)×(L+2) 배열. 바깥 테두리 1칸은 벽, 안쪽 L×L은 방.
    반환: walkable (bool 배열), door (i, j) 튜플"""
    walkable = np.zeros((L+2, L+2), dtype=bool)

    walkable[1:-1, 1:-1] = True     # room
    door = (0, L//2 + 1)
    walkable[door] = True           # exit
    return walkable, door

def static_field(walkable, door):
    """walkable 칸마다 S 값. 벽 칸은 0으로 둔다.
    반환: S (float 배열, walkable과 같은 크기)"""
    ii, jj = np.indices(walkable.shape)
    i_d, j_d = door

    dist = np.sqrt((ii-i_d)**2 + (jj-j_d)**2)

    mask = walkable
    dmax = dist[mask].max()
    S = np.where(mask, dmax - dist, 0)
    return S

def place_people(walkable, door, rho=0.3, rng=None):
    """방 칸(출구 제외) 중 비율 rho만큼 무작위로 골라 사람을 놓는다.
    반환: pos (N×2 int 배열, 한 줄 = 한 사람의 (i, j))"""
    roi = walkable.copy(); roi[door] = False

    cells = np.argwhere(roi)

    if rng is None:
        rng = np.random.default_rng()
    pos = rng.choice(len(cells), size=round(rho * len(cells)), replace=False)
    return cells[pos]

MOVES = np.array([[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1]])  # 제자리, 상, 하, 좌, 우

def move_probs(p, S, walkable, occ, k_S):
    """사람 한 명(p = (i, j))의 5방향 이동 확률.
    occ: 사람이 있는 칸 True인 bool 배열
    반환: 길이 5 float 배열, 합 1, 순서는 MOVES와 같음"""
    nb = p + MOVES

    ni, nj = nb.T
    S_nb = S[ni, nj]
    walk_nb = walkable[ni, nj]
    occ_nb = occ[ni, nj]

    free_nb = ~occ_nb; free_nb[0] = True

    w = np.exp(k_S * (S_nb - S_nb.max())) * walk_nb * free_nb
    probs = w / w.sum()
    return probs

def choose_targets(pos, S, walkable, occ, k_S, rng):
    """사람마다 move_probs 확률로 5방향 중 하나를 뽑는다.
    반환: targets (N×2 int 배열, pos와 같은 순서, 한 줄 = 그 사람이 가려는 칸)"""
    targets = np.zeros_like(pos)

    for n in range(len(pos)):
        probs = move_probs(pos[n], S, walkable, occ, k_S)
        k = rng.choice(5, p=probs)
        targets[n] = pos[n] + MOVES[k]
    return targets

def resolve_conflicts(pos, targets, rng):
    """같은 칸을 고른 사람이 여럿이면 무작위로 한 명만 이동, 나머지는 제자리 (μ=0).
    반환: new_pos (N×2 int 배열, pos와 같은 순서)"""
    new_pos = targets.copy()
    claims = dict()
    for n in range(len(pos)):
        claims.setdefault(tuple(targets[n]), []).append(n)
    for _, people in claims.items():
        if len(people) >= 2:
            winner = rng.choice(people)
            for m in people:
                if m != winner:
                    new_pos[m] = pos[m]
    return new_pos

def step(pos, S, walkable, door, k_S, rng):
    """한 스텝: 점유 → 목표 선택 → 충돌 해결 → 문 칸 도착자 제거.
    반환: 남은 사람의 pos (M×2, M ≤ N)"""
    occ = np.zeros_like(walkable)
    occ[pos[:,0], pos[:,1]] = True

    targets = choose_targets(pos, S, walkable, occ, k_S, rng)
    new_pos = resolve_conflicts(pos, targets, rng)
    at_door = (new_pos == door).all(axis=1)
    return new_pos[~at_door]

if __name__ == "__main__":
    k_S = 0.4
    walkable, door = make_room()
    # print(walkable.shape, walkable.sum(), door)

    S = static_field(walkable, door)
    # print(S[door], S[63, 1], S[63, 63], S[0, 0])
    # plt.imshow(S); plt.colorbar(); plt.show()

    rng = np.random.default_rng(0)
    pos = place_people(walkable, door, rng=rng)
    # print(len(pos), len(np.unique(pos, axis=0)), walkable[pos[:, 0], pos[:, 1]].all(), (pos == door).all(axis=1).any())

    for t in range(300):
        pos = step(pos, S, walkable, door, k_S, rng)
        if t % 50 == 0:
            print(t, len(pos))