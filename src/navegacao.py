"""
Planejamento de caminho com OpenCV.

Algoritmos de navegacao basados em visao computacional.
"""
import cv2
import numpy as np


class NavegadorVisual:
    """
    Navegador visual para robos autonomous.
    
    Usa processamento de imagem para decisoes de navegacao.
    """
    
    def __init__(self, largura=640, altura=480):
        self.largura = largura
        self.altura = altura
        self.centro_x = largura // 2
        self.centro_y = altura // 2
        
    def seguir_linha(self, frame):
        """
        Calcula comando de navegacao para seguir linha.
        
        Args:
            frame: Frame BGR da camera
            
        Returns:
            dict: Comando com direcao e confianca
        """
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        _, binarizada = cv2.threshold(cinza, 60, 255, cv2.THRESH_BINARY_INV)
        
        contours, _ = cv2.findContours(binarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return {"direcao": 0, "confianca": 0, "linha_detectada": False}
            
        maior_contorno = max(contours, key=cv2.contourArea)
        
        M = cv2.moments(maior_contorno)
        
        if M["m00"] == 0:
            return {"direcao": 0, "confianca": 0, "linha_detectada": False}
            
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        desvio = cx - self.centro_x
        
        confianca = min(1.0, cv2.contourArea(maior_contorno) / 10000)
        
        return {
            "direcao": desvio,
            "confianca": confianca,
            "linha_detectada": True,
            "centro_x": cx,
            "centro_y": cy
        }
        
    def evitar_obstaculo(self, frame, distancia_minima=100):
        """
        Detecta obstaculos e sugere desvio.
        
        Args:
            frame: Frame BGR
            distancia_minima: Distancia minima considerada segura
            
        Returns:
            dict: Comando de desvio
        """
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        bordas = cv2.Canny(cinza, 50, 150)
        
        contornos, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        obstaculos = []
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if area > 1000:
                M = cv2.moments(contorno)
                if M["m00"] > 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    obstaculos.append({"centro": (cx, cy), "area": area})
                    
        if not obstaculos:
            return {"obstaculo": False, "direcao": 0}
            
        obstaculo_mais_proximo = min(obstaculos, key=lambda o: abs(o["centro"][0] - self.centro_x))
        
        desvio = obstaculo_mais_proximo["centro"][0] - self.centro_x
        
        if desvio > 0:
            direcao_sugerida = -1  # Ir para esquerda
        else:
            direcao_sugerida = 1  # Ir para direita
            
        return {
            "obstaculo": True,
            "direcao": direcao_sugerida,
            "distancia_obstaculo": obstaculo_mais_proximo["centro"]
        }
        
    def seguir_cor(self, frame, hsv_min, hsv_max):
        """
        Segue objeto de cor especifica.
        
        Args:
            frame: Frame BGR
            hsv_min: Limite inferior HSV
            hsv_max: Limite superior HSV
            
        Returns:
            dict: Comando de navegacao
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower = np.array(hsv_min, np.uint8)
        upper = np.array(hsv_max, np.uint8)
        
        mascara = cv2.inRange(hsv, lower, upper)
        
        kernel = np.ones((5, 5), np.uint8)
        mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
        mascara = cv2.morphologyEx(mascara, cv2.MORPH_DILATE, kernel)
        
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contornos:
            return {"objeto_detectado": False, "direcao": 0}
            
        maior_contorno = max(contornos, key=cv2.contourArea)
        
        M = cv2.moments(maior_contorno)
        
        if M["m00"] == 0:
            return {"objeto_detectado": False, "direcao": 0}
            
        cx = int(M["m10"] / M["m00"])
        
        desvio = cx - self.centro_x
        
        ((x, y), raio) = cv2.minEnclosingCircle(maior_contorno)
        
        return {
            "objeto_detectado": True,
            "direcao": desvio,
            "centro": (cx, int(M["m01"] / M["m00"])),
            "raio": raio,
            "area": cv2.contourArea(maior_contorno)
        }
        
    def mapear_area(self, frame):
        """
        Mapeia areas do frame em regioes.
        
        Divides imagem em 3x3 e analisa cada regiao.
        
        Returns:
            dict: Analise de cada regiao
        """
        h = frame.shape[0] // 3
        w = frame.shape[1] // 3
        
        regioes = {}
        
        nomes = [
            "cima_esquerda", "cima_centro", "cima_direita",
            "meio_esquerda", "meio_centro", "meio_direita",
            "baixo_esquerda", "baixo_centro", "baixo_direita"
        ]
        
        idx = 0
        for i in range(3):
            for j in range(3):
                y1 = i * h
                y2 = (i + 1) * h
                x1 = j * w
                x2 = (j + 1) * w
                
                regiao = frame[y1:y2, x1:x2]
                
                cinza = cv2.cvtColor(regiao, cv2.COLOR_BGR2GRAY)
                media = np.mean(cinza)
                desvio = np.std(cinza)
                
                regioes[nomes[idx]] = {
                    "luminosidade": float(media),
                    "contraste": float(desvio),
                    "preta": media < 60,
                    "branca": media > 200
                }
                idx += 1
                
        return regioes
