#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PY_FILE="$SCRIPT_DIR/TSGT2G.pyw"
ENV_FILE="$SCRIPT_DIR/environment.yml"

CONDA_ENV="tsg2tg"

echo
echo "+-----------------+"
echo "| TSG2TG Launcher |"
echo "+-----------------+"
echo

function pause() {
    local MESSAGE="${1:-"Press any key to continue . . ."}"
    read -n 1 -s -r -p "$MESSAGE"
    echo
}

function prompt_exit() {
    pause "Press any key to exit . . ."
    exit
}

ANACONDA_PATH="$HOME/anaconda3"
MINICONDA_PATH="$HOME/miniconda3"
function conda_not_found() {
    echo "Could not find a conda installation!"
    echo
    echo "ERROR: No conda installation found! Unable to launch!"
    echo "Download Miniconda from here: https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    echo
    prompt_exit
}

if ! command -v conda > /dev/null 2>&1; then
    if [[ -f "$ANACONDA_PATH/bin/conda" ]]; then
        CONDA_PATH="$ANACONDA_PATH"
        echo "Conda installation found!"
    else
        if [[ -f "$MINICONDA_PATH/bin/conda" ]]; then
            CONDA_PATH="$MINICONDA_PATH"
            echo "Conda installation found!"
        else
            conda_not_found
        fi
    fi
else
    CONDA_PATH="$(dirname $(dirname $(which conda)))"
    echo "Conda installation found!"
fi

CONDA_BIN="$CONDA_PATH/bin/conda"
CONDA_PYTHON="$CONDA_PATH/envs/$CONDA_ENV/bin/python"

echo
if ! [[ -f "$CONDA_PYTHON" ]]; then
    echo "Could not find the conda environment \"$CONDA_ENV\", installing it..."
    echo
    
    "$CONDA_BIN" env create -f "$ENV_FILE"
    echo
    
    echo "Conda enviroment is ready!"
else
    echo "Found conda environment!"
fi



echo
echo "Launching TSG2TG..."
nohup "$CONDA_PYTHON" "$PY_FILE" >/dev/null 2>&1 &
sleep 1
