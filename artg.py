import cv2
import glob
import numpy as np

# Função utilizada para carregar e passar cada imagem da pasta por vez
path = glob.glob("imgs\*.png")
for image in path:

    # Lê a imagem e cria uma cópia cortada (Apenas a região da simulação do Gazebo)  
    img = cv2.imread(image)
    copia_img = img.copy()
    copia_cortada = copia_img[137:708, 342:1345]
    

    # Aplica filtros para identificar o contorno dos ARTAGs na imagem
    B1 = cv2.cvtColor(copia_cortada, cv2.COLOR_BGR2HSV)
    BL1 = np.array([0,0,70])
    BH1 = np.array([0,0,255])
    mascara = cv2.inRange(B1, BL1, BH1)

    _, thresh = cv2.threshold(mascara, 0,255, cv2.THRESH_BINARY)

    edges = cv2.Canny(thresh, 20, 250)

    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    # Loop para identificar os contornos
    for c in contours:
     perimeter = cv2.arcLength(c,True)

     if perimeter > 100 and perimeter < 1300:  # Condição criada para otimizar a identificação do ARTAG
         #cv2.drawContours(copia_cortada, [c], 0, (0,0,255), 3) #Caso queira desenhar os contornos

         # Corta o ARTAG
         x,y,w,h = cv2.boundingRect(c)
         crop1 = copia_cortada[y:y+h, x:x+w]
         copia_crop = crop1.copy()

         # Função criada para pegar os pixels cinzas do ARTAG e converter para Branco, a fim de facilitar a leitura
         copia_crop[np.where((copia_crop==[41,41,41]).all(axis=2))] = [255,255,255] 

         cv2.imshow('Imagem', copia_crop)
         cv2.waitKey()
         cv2.destroyAllWindows()
   