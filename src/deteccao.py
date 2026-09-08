"""
Deteccao de cores com OpenCV.

Detecta objetos por cor usando espaco de cor HSV.
"""
import cv2
import numpy as np


class DetectorCor:
    """
    Detector de cores usando mascaras HSV.
    
    Permite detectar objetos por faixa de cor.
    """
    
    def __init__(self):
        self.cap = None
        self.mascara_kernel = np.ones((5, 5), np.uint8)
        
    def abrir_camera(self, indice=0):
        """Abre a camera."""
        self.cap = cv2.VideoCapture(indice)
        return self.cap.isOpened()
        
    def fechar(self):
        """Fecha a camera e janelas."""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        
    def ler_frame(self):
        """Le um frame da camera."""
        if self.cap is None:
            return None
        ret, frame = self.cap.read()
        return frame if ret else None
        
    def converter_hsv(self, frame):
        """Converte frame BGR para HSV."""
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
    def criar_mascara(self, hsv, hsv_min, hsv_max):
        """
        Cria mascara para faixa de cor.
        
        Args:
            hsv: Frame em HSV
            hsv_min: Limite inferior [H, S, V]
            hsv_max: Limite superior [H, S, V]
            
        Returns:
            numpy.ndarray: Mascara binaria
        """
        lower = np.array(hsv_min, np.uint8)
        upper = np.array(hsv_max, np.uint8)
        return cv2.inRange(hsv, lower, upper)
        
    def limpar_mascara(self, mascara, operacoes=2):
        """Aplica operacoes morfologicas na mascara."""
        mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, self.mascara_kernel)
        mascara = cv2.morphologyEx(mascara, cv2.MORPH_DILATE, self.mascara_kernel)
        return mascara
        
    def encontrar_contornos(self, mascara):
        """Encontra contornos na mascara."""
        contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contornos
        
    def desenhar_contornos(self, frame, contornos, cor=(0, 255, 0), espessura=2):
        """Desenha contornos no frame."""
        cv2.drawContours(frame, contornos, -1, cor, espessura)
        return frame
        
    def encontrar_objetos(self, frame, hsv_min, hsv_max, area_min=500):
        """
        Encontra objetos de uma cor no frame.
        
        Args:
            frame: Frame BGR
            hsv_min: Limite inferior HSV
            hsv_max: Limite superior HSV
            area_min: Area minima para considerar objeto
            
        Returns:
            list: Lista de contornos validos
        """
        hsv = self.converter_hsv(frame)
        mascara = self.criar_mascara(hsv, hsv_min, hsv_max)
        mascara = self.limpar_mascara(mascara)
        contornos = self.encontrar_contornos(mascara)
        
        objetos = []
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if area >= area_min:
                objetos.append(contorno)
                
        return objetos
        
    def obter_centro(self, contorno):
        """Retorna centro de massa do contorno."""
        M = cv2.moments(contorno)
        if M["m00"] == 0:
            return (0, 0)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return (cx, cy)
        
    def obter_raio(self, contorno):
        """Retorna raio do circulo envolvente."""
        ((x, y), raio) = cv2.minEnclosingCircle(contorno)
        return raio


# Cores pre-definidas para OBR
CORES = {
    "vermelho": {
        "hsv_min": [0, 120, 70],
        "hsv_max": [10, 255, 255],
        "hsv_min2": [170, 120, 70],
        "hsv_max2": [180, 255, 255],
        "cor_bgr": (0, 0, 255)
    },
    "verde": {
        "hsv_min": [36, 100, 100],
        "hsv_max": [86, 255, 255],
        "cor_bgr": (0, 255, 0)
    },
    "azul": {
        "hsv_min": [100, 100, 100],
        "hsv_max": [130, 255, 255],
        "cor_bgr": (255, 0, 0)
    },
    "amarelo": {
        "hsv_min": [20, 100, 100],
        "hsv_max": [40, 255, 255],
        "cor_bgr": (0, 255, 255)
    },
    "preto": {
        "hsv_min": [0, 0, 0],
        "hsv_max": [180, 255, 50],
        "cor_bgr": (0, 0, 0)
    },
    "branco": {
        "hsv_min": [0, 0, 200],
        "hsv_max": [180, 30, 255],
        "cor_bgr": (255, 255, 255)
    }
}


def detectar_cor(frame, nome_cor):
    """
    Detecta objetos de uma cor pre-definida.
    
    Args:
        frame: Frame BGR
        nome_cor: Nome da cor (vermelho, verde, azul, amarelo, preto, branco)
        
    Returns:
        list: Objetos detectados
    """
    detector = DetectorCor()
    config = CORES.get(nome_cor.lower())
    
    if config is None:
        raise ValueError(f"Cor nao encontrada: {nome_cor}")
        
    hsv_min = config["hsv_min"]
    hsv_max = config["hsv_max"]
    
    objetos = detector.encontrar_objetos(frame, hsv_min, hsv_max)
    
    if "hsv_min2" in config:
        objetos2 = detector.encontrar_objetos(frame, config["hsv_min2"], config["hsv_max2"])
        objetos.extend(objetos2)
        
    return objetos
