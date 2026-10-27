<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" alt="Logo RAIDENS" width="140">

# raidens-opencv

**Visão computacional para robótica: detecção de cores, linhas e navegação por câmera**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![Licença MIT](https://img.shields.io/badge/Licen%C3%A7a-MIT-D9333B?style=flat-square)

[Sobre](#sobre) · [Instalação](#instalação) · [Módulos](#módulos) · [Uso](#uso) · [Receitas](#receitas-com-opencv)

</div>

---

## Sobre

O **raidens-opencv** dá olhos aos robôs da RAIDENS. Ele parte de um frame da câmera e chega a uma decisão: *a linha está à esquerda*, *há um obstáculo à frente*, *o objeto verde está no centro*. Os módulos ficam em camadas, do pré-processamento da imagem até a navegação, para que cada etapa possa ser testada e ajustada separadamente.

Para encontrar os valores HSV ou LAB certos para a sua iluminação, use o [`raidens-lab`](https://github.com/sesiraidens/raidens-lab) e traga os ranges para cá.

## Instalação

```bash
git clone https://github.com/sesiraidens/raidens-opencv.git
cd raidens-opencv
pip install opencv-python numpy
```

## Módulos

| Módulo | Responsabilidade | Principais elementos |
|---|---|---|
| `filters.py` | Pré-processamento | `gaussian_blur`, `median_blur`, `bilateral_filter`, `clahe` |
| `color_detection.py` | Segmentação em HSV ou LAB | `detect_color`, `get_color_area`, `filter_by_area` |
| `deteccao.py` | Objetos por cor | `DetectorCor`, dicionário `CORES`, `detectar_cor` |
| `linha.py` | Linhas pela Transformada de Hough | `DetectorLinha`, `DetectorLinhaPreta`, `DetectorIntersecao` |
| `navegacao.py` | Decisão de movimento | `NavegadorVisual` |

Cores pré-definidas em `CORES`: `vermelho`, `verde`, `azul`, `amarelo`, `preto` e `branco`.

## Uso

### Detectar objetos por cor

```python
from src.deteccao import DetectorCor, CORES

detector = DetectorCor()
detector.abrir_camera(0)
frame = detector.ler_frame()

vermelho = CORES["vermelho"]
for obj in detector.encontrar_objetos(frame, vermelho["hsv_min"], vermelho["hsv_max"]):
    print(detector.obter_centro(obj), detector.obter_raio(obj))
```

### Detectar linhas

```python
from src.linha import DetectorLinha

detector = DetectorLinha()
linhas = detector.detectar_linhas(frame)

for linha in linhas:
    print(f"{detector.calcular_comprimento(linha):.0f}px · {detector.calcular_angulo(linha):.1f}°")

direcao = detector.calcular_direcao(linhas, centro_x=320)
```

### Navegar

```python
from src.navegacao import NavegadorVisual

nav = NavegadorVisual(largura=640, altura=480)

cmd = nav.seguir_linha(frame)
if cmd["linha_detectada"]:
    print("Desvio:", cmd["direcao"])

cmd = nav.evitar_obstaculo(frame)
if cmd["obstaculo"]:
    print("Desviar para:", cmd["direcao"])

cmd = nav.seguir_cor(frame, hsv_min=[36, 100, 100], hsv_max=[86, 255, 255])
regioes = nav.mapear_area(frame)   # análise da imagem em grade 3x3
```

## Receitas com OpenCV

<details>
<summary><b>Máscara de cor em HSV</b></summary>

```python
import cv2
import numpy as np

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mascara = cv2.inRange(hsv, np.array([36, 100, 100]), np.array([86, 255, 255]))
```
</details>

<details>
<summary><b>Centro de um contorno</b></summary>

```python
contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for c in contornos:
    if cv2.contourArea(c) > 500:
        M = cv2.moments(c)
        cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
```
</details>

<details>
<summary><b>Transformada de Hough</b></summary>

```python
cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
bordas = cv2.Canny(cinza, 50, 150)
linhas = cv2.HoughLinesP(bordas, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=10)
```
</details>

## Estrutura

```text
raidens-opencv/
└── src/   # Filtros, segmentação, detecção e navegação
```

## Ecossistema RAIDENS

Este repositório faz parte de um conjunto de bibliotecas da equipe. Elas usam os mesmos nomes de classes e convenções, então o que você aprende em uma serve nas outras.

| Repositório | Para quê |
|---|---|
| [`raidens-python`](https://github.com/sesiraidens/raidens-python) | Biblioteca principal em Python: sensores, motores e robôs prontos (seguidor, parede, resgate) |
| [`raidens-arduino`](https://github.com/sesiraidens/raidens-arduino) | As mesmas abstrações em C++ para rodar direto no Arduino |
| [`raidens-sensores`](https://github.com/sesiraidens/raidens-sensores) | Catálogo completo de sensores com calibração e filtragem |
| [`raidens-motores`](https://github.com/sesiraidens/raidens-motores) | Motores DC, servo, passo, driver L298N e rodas mecanum |
| [`raidens-pid`](https://github.com/sesiraidens/raidens-pid) | Controladores PID, PID avançado, cascata e sintonia Ziegler-Nichols |
| [`raidens-lab`](https://github.com/sesiraidens/raidens-lab) | Calibração interativa de cores em HSV e LAB |
| [`raidens-obr`](https://github.com/sesiraidens/raidens-obr) | Robô completo para a OBR, integrando sensores, motores e missões |
| [`raidens-electronics`](https://github.com/sesiraidens/raidens-electronics) | Cálculos e modelos de componentes eletrônicos |
| [`raidens-3d`](https://github.com/sesiraidens/raidens-3d) | Peças 3D paramétricas geradas em OpenSCAD |
| [`raidens-ros`](https://github.com/sesiraidens/raidens-ros) | Estrutura de nodes e tópicos ROS 2 |
| [`raidens-snippets`](https://github.com/sesiraidens/raidens-snippets) | Trechos de código prontos para copiar e colar |

---

<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" alt="Logo RAIDENS" width="56">

**Equipe RAIDENS** · SESI 192 Alumínio/SP

[![Email](https://img.shields.io/badge/Email-sesiraidens%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:sesiraidens@gmail.com)
[![Linktree](https://img.shields.io/badge/Linktree-sesiraidens-39E06B?style=flat-square&logo=linktree&logoColor=white)](https://linktr.ee/sesiraidens)
[![GitHub](https://img.shields.io/badge/GitHub-sesiraidens-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/sesiraidens)

<sub>Desenvolvido pela equipe RAIDENS para fins educacionais. Licenciado sob MIT.</sub>

</div>
