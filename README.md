# Connect to Raspberry PI and run
1. ssh aiproject2@aiproject2 | password = aiproject2
2. cd ai-project2
3. python3 main.py

# Raspberry PI modules:
1. pip install picamera (Pre-installed on Raspberry PI)
2. pip install RPi.GPIO (Pre-installed on Raspberry PI)

# Text detection modules:
1. Install Tesseract-OCR:
   Windows: https://digi.bib.uni-mannheim.de/tesseract/
   Linux: sudo apt install tesseract-ocr
		    sudo apt install libtesseract-dev
2. pip install pytesseract
3. pip install Pillow==9.2.0
4. pip install imutils
5. pip install scikit-image

# Text-to-speech modules:
1. sudo apt install espeak
2. pip install pyttsx3
3. pip install pygame
# Work:
1. Đan + Lương + Hải: Text detection
2. Nhật : Raspberry PI