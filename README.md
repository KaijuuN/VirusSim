## Virus SIM ##

Virus SIM ist eine grafische Simulation der Ausbreitung eines Virus in einer Population, die mithilfe von Pygame visualisiert wird. Die Simulation modelliert den Verlauf einer Epidemie, bei der Individuen in verschiedenen Gesundheitszuständen wie anfällig, infiziert, krank, genesen oder tot sein können. Sie können die Simulation starten, pausieren, Personen infizieren und Informationen über bestimmte Individuen durch Anklicken abrufen.

## Features

    Start/Pause der Simulation: Starten und pausieren Sie die Simulation mit einem Button.
    Zufällige Bewegung der Individuen: Jedes Individuum bewegt sich zufällig auf dem Bildschirm.
    Infektionsmechanismus: Infizierte Personen können andere Personen innerhalb eines bestimmten Radius anstecken.
    Krankheitsverlauf:
        Personen wechseln von anfällig zu infiziert (orange).
        Nach einer Inkubationszeit werden sie krank (rot).
        Kranke Personen verlieren Gesundheit und sterben möglicherweise (grau) oder genesen (grün).
    Individuen anklicken: Durch Anklicken eines Individuums werden seine Informationen angezeigt.
    Zufällige Resistenz: Einige Personen sind resistent gegen die Infektion.
    Rasterdarstellung: Optional kann ein Raster zur besseren Visualisierung aktiviert werden.

## Installation

    Python 3.x installieren.
    Installiere die Abhängigkeiten:

    bash

    pip install pygame numpy

## Ausführung

Starte die Simulation, indem du das Python-Skript ausführst:

bash

python virus_sim.py

## Steuerung

    Reset: Startet die Simulation neu und generiert eine neue Population.
    Infect: Infiziert eine zufällige anfällige Person in der Population.
    Start/Pause: Startet oder pausiert die Simulation.
    I/O Grid: Schaltet das Raster zur besseren Visualisierung der Zellen ein und aus.
    Individuum auswählen: Klicken Sie auf ein Individuum, um seine Gesundheitsinformationen zu sehen.

## Funktionsweise der Simulation
Gesundheitszustände

    Susceptible (Anfällig): Blaue Personen können infiziert werden.
    Infected (Infiziert): Orange markiert die Inkubationszeit; Personen können andere anstecken.
    Sick (Krank): Rote Personen sind krank und verlieren Gesundheit.
    Recovered (Genesen): Grüne Personen haben die Krankheit überstanden und sind immun.
    Dead (Tot): Graue Personen sind an der Krankheit gestorben.

## Infektionsprozess

    Anfällige Personen können innerhalb eines bestimmten Radius von infizierten Personen angesteckt werden.
    Sobald eine Person infiziert ist, wechselt sie nach einer bestimmten Inkubationszeit zu krank.
    Kranke Personen verlieren über die Zeit Gesundheit und können entweder sterben oder genesen.

## Projektstruktur

bash

virus_sim/
│
├── main.py         # Hauptskript mit der Simulationslogik
└── README.md            # Diese README-Datei

## Anpassungsmöglichkeiten

    Population: Ändern Sie die Anzahl der Individuen in der Simulation, indem Sie den Wert von population_size anpassen.
    Geschwindigkeit: Sie können die Geschwindigkeit der Simulation durch das Ändern der time_step-Werte beeinflussen.
    Infektionsradius und -wahrscheinlichkeit: Passen Sie den Infektionsradius und die Wahrscheinlichkeit der Ansteckung in den Parametern infection_radius und infection_chance an.

## Voraussetzungen

    Python 3.x
    Pygame
    Numpy

Lizenz

Dieses Projekt steht unter der MIT-Lizenz.