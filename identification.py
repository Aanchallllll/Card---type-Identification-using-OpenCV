import cv2
import numpy as np
from matplotlib import pyplot as plt

def process_image(path):
    gray = cv2.imread(path, 0)
    _, threshed = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    inverted = cv2.bitwise_not(threshed)

    num_labels, labels = cv2.connectedComponents(inverted)

    areas = []
    for label in range(1, num_labels):
        component = (labels == label).astype(np.uint8) * 255
        area = cv2.countNonZero(component)
        areas.append(area)

    sorted_areas = np.sort(areas)

    val1 = sorted_areas[-4]
    val2 = sorted_areas[-3]

    index1 = 0
    index2 = 0

    for i, area in enumerate(areas):
        if area == val1 or area == val2:
            if index1 == 0:
                index1 = i
            elif index2 == 0:
                index2 = i
                break

    number_mapping = {7: '2', 9: '3', 11: '4', 13: '5', 15: '6'}
    suit_mapping = {2: 'Ace', 3: 'Heart', 4: 'Club', 5: 'Spade', 6: 'Diamond'}

    try:
        card = number_mapping[index2] + ' of ' +suit_mapping[index1]
    except KeyError:
        raise Exception("Invalid card detected.")

    return card

def main(path):
    rotations = [0, 90, 180, 270]
    for rotation in rotations:
        try:
            card = process_image(path)
            print(f"Output {path} = {card}")
            break
        except Exception as e:
            gray = cv2.imread(path, 0)
            rotated = cv2.rotate(gray, cv2.ROTATE_90_CLOCKWISE)
            path = "rotated_temp.png"
            cv2.imwrite(path, rotated)
    else:
        print("All rotation attempts failed.")

main("tc2-3.png")
