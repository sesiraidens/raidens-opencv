"""
Deteccao de linha com OpenCV.

Detecta e segue linhas usando processamento de imagem.
"""
import cv2
import numpy as np


class DetectorLinha:
    """
    Detector de linha usando Hough Transform.
    
    Detecta linhas retas e calcula angulo e posicao.
    """
    
    def __init__(self):
        self.limiar_canny = 50
        self.limiar_hough = 50
        self.comprimento_minimo = 50
        
    def preprocessar(self, frame):
        """
        Preprocessa frame para deteccao de linha.
        
        Steps:
            1. Escala de cinza
            2. Blur gaussiano
            3. Canny edge detection
        """
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(cinza, (5, 5), 0)
        bordas = cv2.Canny(blur, self.limiar_canny, self.limiar_canny * 2)
        return bordas
        
    def detectar_linhas(self, frame):
        """
        Detecta linhas usando Transformada de Hough.
        
        Returns:
            list: Lista de linhas detectadas [(x1,y1,x2,y2), ...]
        """
        bordas = self.preprocessar(frame)
        
        linhas = cv2.HoughLinesP(
            bordas,
            rho=1,
            theta=np.pi / 180,
            threshold=self.limiar_hough,
            minLineLength=self.comprimento_minimo,
            maxLineGap=10
        )
        
        if linhas is None:
            return []
            
        resultado = []
        for linha in linhas:
            x1, y1, x2, y2 = linha[0]
            resultado.append((x1, y1, x2, y2))
            
        return resultado
        
    def calcular_angulo(self, linha):
        """
        Calcula angulo da linha em graus.
        
        Args:
            linha: Tupla (x1, y1, x2, y2)
            
        Returns:
            float: Angulo em graus (-90 a 90)
        """
        x1, y1, x2, y2 = linha
        
        if x2 - x1 == 0:
            return 90.0
            
        angulo = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        return angulo
        
    def calcular_comprimento(self, linha):
        """Calcula comprimento da linha."""
        x1, y1, x2, y2 = linha
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
    def calcular_ponto_medio(self, linha):
        """Retorna ponto medio da linha."""
        x1, y1, x2, y2 = linha
        return ((x1 + x2) // 2, (y1 + y2) // 2)
        
    def filtrar_por_angulo(self, linhas, angulo_min=-45, angulo_max=45):
        """Filtra linhas por faixa de angulo."""
        filtradas = []
        for linha in linhas:
            angulo = self.calcular_angulo(linha)
            if angulo_min <= angulo <= angulo_max:
                filtradas.append(linha)
        return filtradas
        
    def filtrar_por_comprimento(self, linhas, minimo=50):
        """Filtra linhas por comprimento minimo."""
        return [l for l in linhas if self.calcular_comprimento(l) >= minimo]
        
    def desenhar_linhas(self, frame, linhas, cor=(0, 255, 0), espessura=2):
        """Desenha linhas detectadas no frame."""
        resultado = frame.copy()
        for linha in linhas:
            x1, y1, x2, y2 = linha
            cv2.line(resultado, (x1, y1), (x2, y2), cor, espessura)
        return resultado
        
    def obter_linha_principal(self, linhas):
        """
        Retorna a linha mais longa.
        
        Returns:
            tuple: Linha principal ou None
        """
        if not linhas:
            return None
            
        return max(linhas, key=self.calcular_comprimento)
        
    def calcular_direcao(self, linhas, centro_x):
        """
        Calcula direcao para seguir a linha.
        
        Args:
            linhas: Lista de linhas
            centro_x: Posicao X do centro da imagem
            
        Returns:
            float: Valor negativo = esquerda, positivo = direita
        """
        linha_principal = self.obter_linha_principal(linhas)
        
        if linha_principal is None:
            return 0
            
        ponto_medio = self.calcular_ponto_medio(linha_principal)
        
        desvio = ponto_medio[0] - centro_x
        
        return desvio


class DetectorLinhaPreta(DetectorLinha):
    """
    Detector especifico para linha preta em fundo branco.
    """
    
    def preprocessar(self, frame):
        """Preprocessa para detectar linha preta."""
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        _, binarizada = cv2.threshold(cinza, 60, 255, cv2.THRESH_BINARY_INV)
        
        bordas = cv2.Canny(binarizada, 50, 150)
        
        return bordas


class DetectorIntersecao:
    """
    Detector de intersecoes de linha.
    
    Detecta cruzamentos e T-intersecoes.
    """
    
    def __init__(self):
        selfDetectorLinha = DetectorLinha()
        
    def detectar(self, frame):
        """
        Detecta intersecoes no frame.
        
        Returns:
            list: Lista de pontos de intersecao [(x, y), ...]
        """
        bordas = self._DetectorLinha__DetectorLinha__preprocessar(frame) if hasattr(self, '_DetectorLinha__DetectorLinha__preprocessar') else self._preprocessar(frame)
        
        pontos = cv2.goodFeaturesToTrack(bordas, maxCorners=10, qualityLevel=0.3, minDistance=7)
        
        if pontos is None:
            return []
            
        return [(int(p[0][0]), int(p[0][1])) for p in pontos]
        
    def _preprocessar(self, frame):
        """Preprocessa para deteccao de intersecao."""
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(cinza, (5, 5), 0)
        return cv2.Canny(blur, 50, 150)
