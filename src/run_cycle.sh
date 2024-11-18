#!/bin/bash

# Projektpfad und virtuelle Umgebung
PROJECT_DIR=$(dirname "$0")
VENV_DIR="$PROJECT_DIR/venv"

# Virtuelle Umgebung erstellen, falls nicht vorhanden
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
else
  echo "Virtual environment detected."
fi

# Virtuelle Umgebung aktivieren
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Abhängigkeiten installieren
if [ -f "$PROJECT_DIR/../requirements.txt" ]; then
  echo "Updating requirements...."
  pip install --upgrade pip
  pip install -r "$PROJECT_DIR/../requirements.txt"
else
  echo "Warning: requirements.txt not found."
fi

# Anwendung starten und Argumente weitergeben
echo "Running main.py ..."
python "$PROJECT_DIR/main.py" "120" "--fps=45" "--env" #"$@"

# Virtuelle Umgebung deaktivieren
deactivate
