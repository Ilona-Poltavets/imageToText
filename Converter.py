from PIL import Image
import pytesseract
import cv2
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = './Tesseract-OCR/tesseract.exe'


def findWordOnImage(path, txt, lang):
    image = cv2.imread(path)

    image_copy = image.copy()
    target_word = txt
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, lang=lang)
    word_occur = [i for i, word in enumerate(data["text"]) if word.lower() == target_word]

    for occ in word_occur:
        w = data["width"][occ]
        h = data["height"][occ]
        l = data["left"][occ]
        t = data["top"][occ]

        p1 = (l, t)
        p2 = (l + w, t)
        p3 = (l + w, t + h)
        p4 = (l, t + h)

        image_copy = cv2.line(image_copy, p1, p2, color=(255, 0, 0), thickness=2)
        image_copy = cv2.line(image_copy, p2, p3, color=(255, 0, 0), thickness=2)
        image_copy = cv2.line(image_copy, p3, p4, color=(255, 0, 0), thickness=2)
        image_copy = cv2.line(image_copy, p4, p1, color=(255, 0, 0), thickness=2)

        plt.imsave("found_words.png", image_copy)
        cv2.imshow("Image", image_copy)
        # plt.show()


def convetImageToTxt(path, lang):
    image = Image.open(path)
    string = pytesseract.image_to_string(image, lang=lang)
    return string
