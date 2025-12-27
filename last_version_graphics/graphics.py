import matplotlib.pyplot as plt
import math
import csv

#CONSTS
x = [0]
y = [0]
m = [367000]
vx = [0]
vy = [0]
v = [0]
l = [0]
ro = [1.2754]
dl = 0.6357
dm = 3000
dt = 0.01
t = [0]
u = 2020
G = 6.67 * 10 ** -11
M = 5.3 * 10 ** 22
R = 600000
k = 2.5
h = [0]
teta = [0]

firstquater = True
secondquater = False
thirdquater = False
fourthquater = False

def findCurrentTeta(tetaPrev, tetaCurr):
    global firstquater, secondquater, thirdquater, fourthquater, x, y, R
    if firstquater and tetaPrev > 0 and tetaCurr < 0:
        secondquater = True
        firstquater = False
        return math.pi + math.atan(x[-1] / (y[-1] + R))

    elif secondquater and tetaPrev < 0 and tetaCurr > 0:
        secondquater = False
        thirdquater = True
        return math.pi + math.atan(x[-1] / (y[-1] + R))

    elif thirdquater and tetaPrev > 0 and tetaCurr < 0:
        thirdquater = False
        fourthquater = True
        return math.atan(x[-1] / (y[-1] + R))

    elif fourthquater and tetaPrev < 0 and tetaCurr > 0:
        fourthquater = False
        firstquater = True
        return math.atan(x[-1] / (y[-1] + R))

    elif firstquater:
        return math.atan(x[-1] / (y[-1] + R))

    elif secondquater:
        return math.pi + math.atan(x[-1] / (y[-1] + R))

    elif thirdquater:
        return math.pi + math.atan(x[-1] / (y[-1] + R))

    elif fourthquater:
        return math.atan(x[-1] / (y[-1] + R))

    return "error"

while t[-1] < 80:
    dvy = u * dm * math.cos(math.radians(l[-1])) * dt / m[-1] - k * ro[-1] * vy[-1] ** 2 * math.cos((math.pi / 2) if vy[-1] == 0 else math.atan(vx[-1] / vy[-1])) * dt / m[-1] - G * M * math.cos(teta[-1]) * dt / (x[-1] ** 2 + (y[-1] + R) ** 2)
    dvx = u * dm * math.sin(math.radians(l[-1])) * dt / m[-1] - k * ro[-1] * vx[-1] ** 2 * math.sin((math.pi / 2) if vy[-1] == 0 else math.atan(vx[-1] / vy[-1])) * dt / m[-1] - G * M * math.sin(teta[-1]) * dt / (x[-1] ** 2 + (y[-1] + R) ** 2)
    ro.append(ro[0] * math.exp(-h[-1]/8000))
    h.append(math.sqrt((x[-1] ** 2 + (y[-1] + R) ** 2)) - R)
    x.append(x[-1] + vx[-1] * dt)
    y.append(y[-1] + vy[-1] * dt)
    teta.append(findCurrentTeta(math.atan(x[-2] / (y[-2] + R)), math.atan(x[-1] / (y[-1] + R))))
    v.append(math.sqrt(vx[-1] ** 2 + vy[-1] ** 2))
    vx.append(vx[-1] + dvx)
    vy.append(vy[-1] + dvy)
    l.append(l[-1] + dl * dt)
    m.append(m[-1] - dm * dt)
    t.append(t[-1] + dt)

while h[-1] > h[-2]:
    dvy = -k * ro[-1] * vy[-1] ** 2 * math.cos((math.pi / 2) if vy[-1] == 0 else math.atan(vx[-1] / vy[-1])) * dt / m[-1] - G * M * math.cos(teta[-1]) * dt / (x[-1] ** 2 + (y[-1] + R) ** 2)
    dvx = -k * ro[-1] * vx[-1] ** 2 * math.sin((math.pi / 2) if vy[-1] == 0 else math.atan(vx[-1] / vy[-1])) * dt / m[-1] - G * M * math.sin(teta[-1]) * dt / (x[-1] ** 2 + (y[-1] + R) ** 2)
    ro.append(ro[0] * math.exp(-h[-1] / 8000))
    h.append(math.sqrt((x[-1] ** 2 + (y[-1] + R) ** 2)) - R)
    x.append(x[-1] + vx[-1] * dt)
    y.append(y[-1] + vy[-1] * dt)
    teta.append(findCurrentTeta(math.atan(x[-2] / (y[-2] + R)), math.atan(x[-1] / (y[-1] + R))))
    v.append(math.sqrt(vx[-1] ** 2 + vy[-1] ** 2))
    vx.append(vx[-1] + dvx)
    vy.append(vy[-1] + dvy)
    m.append(m[-1])
    t.append(t[-1] + dt)

dm = 1050
u = 2857
v_cosm = math.sqrt(G * M * (h[-2] + R) / (x[-1] ** 2 + (y[-1] + R) ** 2))

h.append(math.sqrt((x[-1] ** 2 + (y[-1] + R) ** 2)) - R)
v.append(v[-1])
m.append(m[-1] - 40000)
t.append(t[-1] + dt)

while v[-1] < v_cosm:
    dvy = u * dm * -math.sin(teta[-1]) * dt / m[-1] - G * M * math.cos(teta[-1]) * dt / (x[-1] ** 2 + (y[-1] + R) ** 2)
    dvx = u * dm * math.cos(teta[-1]) * dt / m[-1] - G * M * math.sin(teta[-1]) * dt / (x[-1] ** 2 + (y[-1] + R) ** 2)
    h.append(math.sqrt((x[-1] ** 2 + (y[-1] + R) ** 2)) - R)
    x.append(x[-1] + vx[-1] * dt)
    y.append(y[-1] + vy[-1] * dt)
    teta.append(findCurrentTeta(math.atan(x[-2] / (y[-2] + R)), math.atan(x[-1] / (y[-1] + R))))
    v.append(math.sqrt(vx[-1] ** 2 + vy[-1] ** 2))
    vx.append(vx[-1] + dvx)
    vy.append(vy[-1] + dvy)
    m.append(m[-1] - dm * dt)
    t.append(t[-1] + dt)

while t[-1] < 2500:
    dvy = -G * M * math.cos(teta[-1]) * dt / (x[-1] ** 2 + (y[-1] + R) ** 2)
    dvx = -G * M * math.sin(teta[-1]) * dt / (x[-1] ** 2 + (y[-1] + R) ** 2)
    h.append(math.sqrt((x[-1] ** 2 + (y[-1] + R) ** 2)) - R)
    x.append(x[-1] + vx[-1] * dt)
    y.append(y[-1] + vy[-1] * dt)
    teta.append(findCurrentTeta(math.atan(x[-2] / (y[-2] + R)), math.atan(x[-1] / (y[-1] + R))))
    v.append(math.sqrt(vx[-1] ** 2 + vy[-1] ** 2))
    vx.append(vx[-1] + dvx)
    vy.append(vy[-1] + dvy)
    m.append(m[-1])
    t.append(t[-1] + dt)

with open("data.csv", "r") as f:
    velocities = []
    times = []
    for line in f.readlines():
        line = line.split(',')
        times.append(float(line[0]))
        velocities.append(float(line[1]))

# Создаём график
plt.figure(figsize=(10, 6))

# Гладкая кривая
plt.plot(times, velocities, 'tab:orange', linewidth=2, label='Данные из игры')
plt.plot(t, v, 'b-', linewidth=2, label='Физмодель')

# Настройка графика
plt.xlabel('Время t, с', fontsize=12)
plt.ylabel('Скорость v, м/с', fontsize=12)
plt.title('Изменение скорости ракеты на начальном участке полёта', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.xlim(0, 600)
plt.ylim(0, 3000)

# Сохраняем график в файл
plt.tight_layout()
plt.savefig('speed.png', dpi=300, bbox_inches='tight')
plt.close()  # Закрываем фигуру

with open("data.csv", "r") as f:
    heights = []
    times = []
    for line in f.readlines():
        line = line.split(',')
        times.append(float(line[0]))
        heights.append(float(line[3]))

plt.figure(figsize=(10, 6))

plt.plot(times, heights, 'tab:orange', linewidth=2, label='Данные из игры')
plt.plot(t, h, 'b-', linewidth=2, label='Физмодель')

# Настройка графика
plt.xlabel('Время t, с', fontsize=12)
plt.ylabel('Высота h, м', fontsize=12)
plt.title('Изменение высоты ракеты на начальном участке полёта', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.xlim(0, 600)
plt.ylim(0, 270000)

# Сохраняем график в файл
plt.tight_layout()
plt.savefig('height.png', dpi=300, bbox_inches='tight')
plt.close()  # Закрываем фигуру

with open("data.csv", "r") as f:
    weights = []
    times = []
    for line in f.readlines():
        line = line.split(',')
        times.append(float(line[0]))
        weights.append(float(line[5]))

plt.figure(figsize=(10, 6))

plt.plot(times, weights, 'tab:orange', linewidth=2, label='Данные из игры')
plt.plot(t, m, 'b-', linewidth=2, label='Физмодель')

# Настройка графика
plt.xlabel('Время t, с', fontsize=12)
plt.ylabel('Масса m, кг', fontsize=12)
plt.title('Изменение массы ракеты на начальном участке полёта', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.xlim(0, 600)
plt.ylim(0, 300000)

# Сохраняем график в файл
plt.tight_layout()
plt.savefig('weight_plot.png', dpi=300, bbox_inches='tight')
plt.close()  # Закрываем фигуру

fig, ax = plt.subplots(figsize=(10, 10))

circle = plt.Circle((0, -R), 600000, color='blue', alpha=0.5, fill=True)

ax.plot(x, y, 'b-', linewidth=2, label='Физмодель')

ax.add_patch(circle)

ax.set_xlim(-1000000, 1000000)
ax.set_ylim(-1500000, 500000)
ax.set_aspect('equal')
ax.grid(True)
ax.legend()

ax.set_xlabel('X координата (м)', fontsize=12)
ax.set_ylabel('Y координата (м)', fontsize=12)
ax.set_title('Траектория')
ax.grid(True, linestyle='--', alpha=0.6)

# Сохраняем график в файл
plt.tight_layout()
plt.savefig('traectory.png', dpi=300, bbox_inches='tight')
plt.close()
# Закрываем фигуру












        
