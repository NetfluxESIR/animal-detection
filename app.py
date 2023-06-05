import cv2
import numpy as np

from pathlib import Path

import typer

animal_list = [
    "lion", "gazelle", "zebra", "elephant", "rhinoceros",
    "hippopotamus", "giraffe", "cow", "pig", "horse",
    "sheep", "chicken", "duck", "goose", "turkey",
    "dog", "cat", "rabbit", "hamster", "guinea pig",
    "canary", "parrot", "goldfish", "turtle", "snake",
    "lizard", "bird", "butterfly", "bee", "spider", "worm"
]

app = typer.Typer()


@app.command()
def run(
        input_file: Path = typer.Option(
            ...,
            "-i",
            "--input",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            allow_dash=False,
            help="Input file path",
        )
):
    neural_network = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    with open("yolov3_classes.txt", "r") as f:
        classes = [line.strip() for line in f]

    animals = {}

    cap = cv2.VideoCapture(str(input_file.absolute()))
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        frame_count += 1
        if not ret:
            break
        if frame_count % 10 != 0:
            continue
        blob = cv2.dnn.blobFromImage(
            frame,
            1 / 255,
            (416, 416),
            (0, 0, 0),
            swapRB=True,
            crop=False
        )

        neural_network.setInput(blob)
        outs = neural_network.forward(neural_network.getUnconnectedOutLayersNames())

        animals_detected = set()
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                if classes[class_id] in animal_list:
                    animals_detected.add(classes[class_id])

        for animal in animals_detected:
            if animal not in animals:
                animals[animal] = []
            animals[animal].append(frame_count)

    cap.release()
    print("Animals detected:" + str(len(animals)))
    print("Animal: [frame where detected] (we analyze 1 frame every 10 frames)")
    for animal in animals:
        print(animal + ": frames " + str(animals[animal]))


if __name__ == "__main__":
    app()
