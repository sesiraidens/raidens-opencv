<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" width="80">

# raidens-opencv

Biblioteca de visao computacional para robotica com OpenCV.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-d9333b?style=flat)
![Status](https://img.shields.io/badge/Status-Active-2ea043?style=flat)

</div>

---

## Sobre

O **raidens-opencv** fornece ferramentas de visao computacional para robos: deteccao de cores, deteccao de linha e navegacao visual.

---

## Estrutura

`
raidens-opencv/
├── src/
│   ├── deteccao.py       # Deteccao de cores HSV
│   ├── linha.py          # Deteccao de linha com Hough
│   ├── navegacao.py      # Navegacao visual
│   └── __init__.py
├── examples/
│   ├── detector_cores.py
│   ├── seguidor_visual.py
│   └── mapear_area.py
└── README.md
`

---

## Modulos

### deteccao.py - Deteccao de Cores

Detecta objetos por cor usando mascaras HSV.

`python
from src.deteccao import DetectorCor, CORES

detector = DetectorCor()
detector.abrir_camera(0)

frame = detector.ler_frame()
objetos = detector.encontrar_objetos(frame, CORES["vermelho"]["hsv_min"], CORES["vermelho"]["hsv_max"])

for obj in objetos:
    centro = detector.obter_centro(obj)
    raio = detector.obter_raio(obj)
    print(f"Objeto em {centro}, raio {raio}")
`

**Cores pre-definidas:**
- ermelho - Deteccao de area vermelha
- erde - Deteccao de area verde
- zul - Deteccao de area azul
- marelo - Deteccao de area amarela
- preto - Deteccao de linha preta
- ranco - Deteccao de area branca

### linha.py - Deteccao de Linha

Detecta linhas usando Transformada de Hough.

`python
from src.linha import DetectorLinha

detector = DetectorLinha()
frame = camera.read()

linhas = detector.detectar_linhas(frame)

for linha in linhas:
    angulo = detector.calcular_angulo(linha)
    comp = detector.calcular_comprimento(linha)
    print(f"Linha: {comp:.0f}px, {angulo:.1f} graus")

direcao = detector.calcular_direcao(linhas, centro_x=320)
`

### navegacao.py - Navegacao Visual

Algoritmos de navegacao autonoma.

`python
from src.navegacao import NavegadorVisual

nav = NavegadorVisual(largura=640, altura=480)

# Seguir linha preta
comando = nav.seguir_linha(frame)
if comando["linha_detectada"]:
    print(f"Desvio: {comando['direcao']}")
    
# Evitar obstaculo
comando = nav.evitar_obstaculo(frame)
if comando["obstaculo"]:
    print(f"Desviar para: {comando['direcao']}")
    
# Seguir cor
comando = nav.seguir_cor(frame, hsv_min=[36, 100, 100], hsv_max=[86, 255, 255])
`

---

## Funcoes Principais

### Converter para HSV

`python
import cv2
import numpy as np

frame_bgr = camera.read()
frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

lower = np.array([36, 100, 100])
upper = np.array([86, 255, 255])
mascara = cv2.inRange(frame_hsv, lower, upper)
`

### Encontrar Contornos

`python
contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for contorno in contornos:
    area = cv2.contourArea(contorno)
    if area > 500:
        M = cv2.moments(contorno)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
`

### Transformada de Hough

`python
bordas = cv2.Canny(cinza, 50, 150)
linhas = cv2.HoughLinesP(bordas, 1, np.pi/180, 50, minLineLength=50, maxLineGap=10)
`

---

## Exemplos

### Detector de Cores

`ash
python examples/detector_cores.py
`

Abre camera e detecta objetos verdes em tempo real.

### Seguidor Visual

`ash
python examples/seguidor_visual.py
`

Usa camera para seguir linha preta.

### Mapear Area

`ash
python examples/mapear_area.py
`

Divide imagem em 3x3 e analisa cada regiao.

---

## Dependencias

`ash
pip install opencv-python numpy
`

---

## Equipe

**RAIDENS - SESI Aluminio 192**

Desenvolvido para uso interno da equipe. Licenciado sob MIT.