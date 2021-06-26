import cv2
from utils import preenche, redimensiona, segmenta, expandeSabre, trataRuido, write

# img = cv2.imread("jedidog.jpeg")
# imgOriginal = img.copy()

def lightSaberProcesser(img):
  # img = redimensiona(img, 100)

  # Segmenta vassoura
  imgSegmentada =	segmenta(img)

  # Remove ruidos
  imgSemRuidos = trataRuido(imgSegmentada)

  # Preenche buracos caso necessário
  imgPreenchida = preenche(imgSemRuidos)

  # Expande o sabre de luz
  imgAumentada = expandeSabre(imgPreenchida, 10)

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
  for i in range(5): 
    imgBorrada = cv2.GaussianBlur(imgAumentada, (37,  37), 0)
    imgBorradaExpandida = expandeSabre(imgBorrada, 8)
    imgfinal[:,:,0] = cv2.add(canal0, cv2.subtract(imgBorradaExpandida, 40))  # B = 255 - 40 = 215
    imgfinal[:,:,1] = cv2.add(canal1, cv2.subtract(imgBorradaExpandida, 150)) # G = 255 - 150 = 105
    imgfinal[:,:,2] = cv2.add(canal2, cv2.subtract(imgBorradaExpandida, 80))  # R = 255 - 80 = 175
  return img

captura = cv2.VideoCapture('ultimo.mp4')

frame_width = int(captura.get(3))
frame_height = int(captura.get(4))

out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

while(1):
  ret, frame = captura.read()

  if not ret:
    print("Can't receive frame (stream end?). Exiting ...")
    break
  frame = lightSaberProcesser(frame)

  # write on file
  out.write(frame)

  cv2.imshow('frame', frame)
  k = cv2.waitKey(30) & 0xff
  if k == 27:
    break

captura.release()
out.release()

cv2.destroyAllWindows()
cv2.waitKey(0)