import cv2
import numpy as np

from pathlib import Path

import typer

# Liste des animaux à détecter
animal_list = [
    "lion", "gazelle", "zebra", "elephant", "rhinoceros", 
    "hippopotamus", "giraffe",
    "cow", "pig", "horse", "sheep", "chicken", "duck", "goose", "turkey", 
    "dog", "cat",
    "rabbit", "hamster", "guinea pig", "canary", "parrot", "goldfish", 
    "turtle", "snake", "lizard",
    "bird", "butterfly", "bee", "spider", "worm"
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
    ),
    output_file: Path = typer.Option(
        ...,
        "-o",
        "--output",
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=False,
        resolve_path=True,
        allow_dash=False,
        help="Output file path",
    ),
):
    # Chargement du modèle YOLOv3 et des classes
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    with open("yolov3_classes.txt", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # Lecture de la vidéo
    cap = cv2.VideoCapture(input_file)


    # Boucle sur chaque image de la vidéo
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Préparation de l'image pour la détection d'objet
        blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

        # Passer l'image dans le réseau de neurones YOLOv3 pour détecter les objets
        net.setInput(blob)
        outs = net.forward(net.getUnconnectedOutLayersNames())

        # Analyse des détections d'animaux
        animals_detected = set()
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                if classes[class_id] in animal_list:
                    animals_detected.add(classes[class_id])


        # Affichage des résultats de détection sur la console
        for animal in animals_detected:
            print(f"{animal}", sep="", end="\n")

    # Fermeture du fichier de sortie et libération des ressources
    cap.release()





if __name__ == "__main__":
    app()



