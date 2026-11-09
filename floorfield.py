import numpy as np
import matplotlib.pyplot as plt

def make_room(L=63):
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

if __name__ == "__main__":
    walkable, door = make_room()
    print(walkable.shape, walkable.sum(), door)
    S = static_field(walkable, door)
    print(S[door], S[63, 1], S[63, 63], S[0, 0])
    plt.imshow(S); plt.colorbar(); plt.show()