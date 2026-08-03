import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# 物理常数
c0 = 3e8  # 真空中的光速 (m/s)
mu0 = 4e-7 * np.pi  # 真空磁导率 (H/m)
epsilon0 = 1 / (mu0 * c0 ** 2)  # 真空介电常数 (F/m)

# 仿真参数
nx, ny = 200, 200  # 网格大小
dx = 1e-3  # 空间步长 (m)
dy = dx
dt = dx / (2 * c0)  # 时间步长 (s)

# 时间步数
n_steps = 500

# PML参数
pml_size = 20
sigma_max = 1e2  # 增大sigma_max以提高PML吸收效果

# 初始化电场和磁场以及辅助变量
Ez = np.zeros((nx, ny))
Hx = np.zeros((nx, ny))
Hy = np.zeros((nx, ny))

# 辅助变量用于PML
Dz = np.zeros((nx, ny))
Bx = np.zeros((nx, ny))
By = np.zeros((nx, ny))

# 材料参数
epsilon = epsilon0 * np.ones((nx, ny))
mu = mu0 * np.ones((nx, ny))
sigma_e = np.zeros((nx, ny))  # 电导率
sigma_m = np.zeros((nx, ny))  # 磁导率（此处设为0）

# 设置金属小球
radius = 20  # 小球半径 (网格单位)
center_x, center_y = nx // 2, ny // 2
for i in range(nx):
    for j in range(ny):
        if (i - center_x) ** 2 + (j - center_y) ** 2 <= radius ** 2:
            sigma_e[i, j] = 1e7  # 高电导率模拟金属

# 设置PML区域的电导率和磁导率
sigma_e_x = np.zeros((nx, ny))
sigma_e_y = np.zeros((nx, ny))
sigma_m_x = np.zeros((nx, ny))
sigma_m_y = np.zeros((nx, ny))

for i in range(pml_size):
    sigma = sigma_max * ((pml_size - i) / pml_size) ** 3
    sigma_e_x[i, :] = sigma
    sigma_e_x[-i - 1, :] = sigma
    sigma_e_y[:, i] = sigma
    sigma_e_y[:, -i - 1] = sigma
    sigma_m_x[i, :] = sigma
    sigma_m_x[-i - 1, :] = sigma
    sigma_m_y[:, i] = sigma
    sigma_m_y[:, -i - 1] = sigma

# 预计算更新系数
ca = (1 - dt * sigma_e / (2 * epsilon)) / (1 + dt * sigma_e / (2 * epsilon))
cb = dt / (epsilon * dx) / (1 + dt * sigma_e / (2 * epsilon))

da = (1 - dt * sigma_m / (2 * mu)) / (1 + dt * sigma_m / (2 * mu))
db = dt / (mu * dx) / (1 + dt * sigma_m / (2 * mu))

# 定义Total-Field/Scattered-Field (TF/SF)界面
tfsf_x_start = pml_size + 1
tfsf_x_end = nx - pml_size - 1
tfsf_y_start = pml_size + 1
tfsf_y_end = ny - pml_size - 1

# 入射波参数
frequency = 1e9  # 频率1 GHz
omega = 2 * np.pi * frequency  # 角频率
k = omega / c0  # 波数

# 主循环
fig, ax = plt.subplots(figsize=(6, 6))
im = ax.imshow(Ez.T, cmap='RdBu', vmin=-0.01, vmax=0.01, origin='lower')
plt.colorbar(im)
ax.set_title('Electric Field Ez')


def update(n):
    global Ez, Hx, Hy, Dz, Bx, By

    # 更新磁场Hx, Hy
    # Hy更新
    Hy[:, :-1] = Hy[:, :-1] + (db[:, :-1] / dy) * (Ez[:, 1:] - Ez[:, :-1])
    # Hx更新
    Hx[:-1, :] = Hx[:-1, :] - (db[:-1, :] / dx) * (Ez[1:, :] - Ez[:-1, :])

    # 在TF/SF界面上加入入射场（磁场）
    Hy[tfsf_x_start:tfsf_x_end, tfsf_y_start - 1] -= (db[tfsf_x_start:tfsf_x_end, tfsf_y_start - 1] / dy) * \
                                                     np.sin(omega * dt * n)

    # 更新电场Ez
    Ez[1:, 1:] = ca[1:, 1:] * Ez[1:, 1:] + \
                 (cb[1:, 1:] * ((Hy[1:, 1:] - Hy[1:, :-1]) / dx - (Hx[1:, 1:] - Hx[:-1, 1:]) / dy))

    # 在TF/SF界面上加入入射场（电场）
    Ez[tfsf_x_start:tfsf_x_end, tfsf_y_start] += np.sin(omega * dt * (n + 0.5))

    # 更新图像
    im.set_array(Ez.T)
    ax.set_xlabel(f'Time step: {n}')
    return [im]


ani = animation.FuncAnimation(fig, update, frames=n_steps, interval=50, blit=True)
plt.show()
