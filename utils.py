import cv2
import numpy as np

def preenche(img):
	imgfloodfill = img.copy()
	h, w = img.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)
	cv2.floodFill(imgfloodfill, mask, (0,0), 255);
	imgInvertida = cv2.bitwise_not(imgfloodfill)
	imgFinal = img | imgInvertida
	return imgFinal

def redimensiona(img, escala=40):
    escala = escala
    largura = int(img.shape[1] * escala/100)
    altura = int(img.shape[0] * escala/100)
    dim = (largura, altura)
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return img

def segmenta(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    limInf = np.array([60, 60, 55])
    limSup = np.array([130, 255, 255])

    imgSegmentada =	cv2.inRange(imgHSV, limInf, limSup)

    return imgSegmentada

def trataRuido(img):
    elementoEstruturante = cv2.getStructuringElement(cv2.MORPH_CROSS, (2, 2))
    img =	cv2.erode(img, elementoEstruturante, iterations = 1)
    img =	cv2.dilate(img, elementoEstruturante, iterations = 1)
    return img

def expandeSabre(img, iterations=8):
    elementoEstruturante = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    img =	cv2.dilate(img, elementoEstruturante, iterations = iterations)
    img =	cv2.erode(img, elementoEstruturante, iterations = 5)
    return img

def erodeSabre(img):
    elementoEstruturante = cv2.getStructuringElement(cv2.MORPH_CROSS, (2, 2))
    img =	cv2.erode(img, elementoEstruturante, iterations = 1)
    return img

def write(filename, frames, fps, show=False):
        fps = max(1, fps)
        out = None

        try:
            for image in frames:
                frame = cv2.imread(image)
                if show:
                    cv2.imshow('video', frame)

                if not out:
                    height, width, channels = frame.shape
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(filename, fourcc, 20, (width, height))

                out.write(frame)

        finally:
            out and out.release()
            cv2.destroyAllWindows() 