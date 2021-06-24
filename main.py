import cv2
from utils import preenche, redimensiona, segmenta, expandeSabre, trataRuido, erodeSabre

img = cv2.imread("jedi.jpeg")

imgOriginal = img.copy()
img = redimensiona(img, 80)

# Segmenta vassoura
imgSegmentada =	segmenta(img)

# Remove ruidos
imgSemRuidos = trataRuido(imgSegmentada)

# Preenche buracos caso necessário
imgPreenchida = preenche(imgSemRuidos)

# Expande o sabre de luz
imgAumentada = expandeSabre(imgPreenchida, 7)

# Cria uma referência para cada canal de cor
canal0 = img[:,:,0]
canal1 = img[:,:,1]
canal2 = img[:,:,2]

imgfinal = img

# Remove o cabo da vassoura
imgfinal[:,:,0] = cv2.add(canal0, imgAumentada)
imgfinal[:,:,1] = cv2.add(canal1, imgAumentada)
imgfinal[:,:,2] = cv2.add(canal2, imgAumentada)

# Cria o efeito de luz colorida no sabre
imgBorrada = cv2.GaussianBlur(imgAumentada, (33,  33), 0)
imgBorradaExpandida = expandeSabre(imgBorrada, 8)

imgfinal[:,:,0] = cv2.add(canal0, imgBorradaExpandida)
# imgfinal[:,:,1] = cv2.add(canal1, imgBorradaExpandida)
imgfinal[:,:,2] = cv2.add(canal2, imgBorradaExpandida)

# Printa imagens
cv2.imshow("Original", imgOriginal)	
cv2.imshow("Segmentada", imgSegmentada)
cv2.imshow("Expandida", imgAumentada)
cv2.imshow("Final", img)

cv2.waitKey(0)
cv2.destroyAllWindows()