#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

NPP_DIR="$( dirname "$SCRIPT_DIR" )"

CONF_FILE="$NPP_DIR/dosbox.conf"
MOUNT_DIR="$NPP_DIR"

BCPP31_DIR="$MOUNT_DIR/bc.31"

echo
echo "+------------------+"
echo "| Noctis++ Builder |"
echo "+------------------+"
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

if command -v dosbox-x > /dev/null 2>&1; then
    echo "DOSBox-X installation found!"
else
    echo "DOSBox-X is not installed!"
    echo
    echo "ERROR: No DOSBox-X installation found! Unable to launch!"
    echo "Install it with: sudo snap install dosbox-x"
    echo
    prompt_exit
fi

echo

if [[ -f "$CONF_FILE" ]]; then
    echo "Using conf file: \"$CONF_FILE\""
else
    echo "Could not find conf file: \"$CONF_FILE\""
    echo
    echo "ERROR: Configuration file not found! Unable to launch!"
    echo "Download here: https://github.com/nimaid/Noctis-Plus-Plus/raw/refs/heads/main/dosbox.conf"
    echo
    prompt_exit
fi

if ! [[ -f "$MOUNT_DIR/source/compile.bat" ]]; then
    echo
    echo "ERROR: Noctis++ not found! Unable to launch!"
    echo "Download Noctis++ from here: https://github.com/nimaid/Noctis-Plus-Plus/releases/latest"
    echo
    prompt_exit
fi

if ! [[ -f "$BCPP31_DIR/BIN/MAKE.EXE" ]]; then
    echo
    echo "ERROR: Borland C++ 3.1 not found! Unable to launch!"
    echo "Download Borland C++ 3.1 here: https://archive.org/download/bcpp31/BCPP31.ZIP"
    echo "Extract the contents to: $BCPP31_DIR"
    echo
    prompt_exit
fi



echo
echo "Launching Noctis IV..."
dosbox-x -c "mount n \"$MOUNT_DIR\"" -c "n:" -c "cd source" -c "compile.bat" -conf "$CONF_FILE" -exit &
