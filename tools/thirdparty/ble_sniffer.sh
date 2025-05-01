# Copyright 2025 Daniel Paredes (daleonpz)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
APP_DIR="${SCRIPT_DIR}/ble_sniffer"

mkdir -p "${APP_DIR}"

###### MODIFY THIS VARIABLE TO CHANGE THE INSTALLATION DIRECTORY ###########
SNIFF_JLINK_INSTALL_DIR="${APP_DIR}/jlink_sniffer"
SNIFFER_FW_DIR="${APP_DIR}/sniffer_fw"

# This version of JLink is required for the nRF Sniffer to work properly
SNIFF_JLINK_VER="818"
SNIFF_JLINK_DIR="JLink_Linux_V${SNIFF_JLINK_VER}_x86_64"
SNIFF_JLINK_FILE="${SNIFF_JLINK_DIR}.tgz"
SNIFF_JLINK_URL="https://www.segger.com/downloads/jlink/${SNIFF_JLINK_FILE}"

SNIFF_UTIL_URL="https://files.nordicsemi.com/artifactory/swtools/external/nrfutil/executables/x86_64-unknown-linux-gnu/nrfutil"
SNIFF_UTIL_FILE="nrfutil"

COMMAND=$1
ARGS=("${@:2}")

help_menu(){
    echo "Usage: $0 <command> [args]"
    echo "Commands:"
    echo "  install   Install the BLE Sniffer"
    echo "  uninstall Uninstall the BLE Sniffer"
    echo "  run       Run the BLE Sniffer with specified arguments"
    echo "  help      Show this help message"
}

run_ble_sniffer_tool(){
    if [ -z "$1" ]; then
        echo "No arguments provided. Please provide the arguments for the sniffer tool."
        exit 1
    fi

    if [ ! -d "${SNIFFER_FW_DIR}" ]; then
        echo "Sniffer tool not found. Please install it first."
        exit 1
    fi

    if [ ! -d "${SNIFF_JLINK_INSTALL_DIR}" ]; then
        echo "JLink installation directory not found. Please install it first."
        exit 1
    fi

    LD_LIBRARY_PATH="${SNIFF_JLINK_INSTALL_DIR}/${SNIFF_JLINK_DIR}" "${SCRIPT_DIR}/${SNIFF_UTIL_FILE}" "${ARGS[@]}"
}

install_ble_sniffer(){
    if [ ! -f "${SCRIPT_DIR}/${SNIFF_JLINK_FILE}" ]; then
        echo "Downloading JLink installer..."
        curl -L -o "${SCRIPT_DIR}/${SNIFF_JLINK_FILE}" "${SNIFF_JLINK_URL}" --data accept_license_agreement=accepted
        mkdir -p "${SNIFF_JLINK_INSTALL_DIR}"
        tar -xzf "${SCRIPT_DIR}/${SNIFF_JLINK_FILE}" -C "${SNIFF_JLINK_INSTALL_DIR}"
    else
        echo "JLink ${SNIFF_JLINK_VER} installer already exists."
    fi

    if [ ! -f "${SCRIPT_DIR}/${SNIFF_UTIL_FILE}" ]; then
        echo "Downloading sniffer tool..."
        curl -L -o "${SCRIPT_DIR}/${SNIFF_UTIL_FILE}" "${SNIFF_UTIL_URL}"
        chmod +x "${SCRIPT_DIR}/${SNIFF_UTIL_FILE}"
    else
        echo "sniffer tool already exists."
    fi

    SNIFF_UTIL_EXEC="${SCRIPT_DIR}/${SNIFF_UTIL_FILE}"

    ${SNIFF_UTIL_EXEC} install ble-sniffer
    if [ $? -ne 0 ]; then
        echo "Error installing BLE Sniffer. Please check the logs."
        exit 1
    fi

    ${SNIFF_UTIL_EXEC} install device
    if [ $? -ne 0 ]; then
        echo "Error installing device. Please check the logs."
        exit 1
    fi

    NRF_RULES_URL="https://raw.githubusercontent.com/NordicSemiconductor/nrf-udev/refs/heads/main/nrf-udev_1.0.1-all/lib/udev/rules.d/71-nrf.rules"
    NRF_RULES_BLACKLIST_URL="https://raw.githubusercontent.com/NordicSemiconductor/nrf-udev/refs/heads/main/nrf-udev_1.0.1-all/lib/udev/rules.d/99-mm-nrf-blacklist.rules"

    if [ ! -f /lib/udev/rules.d/71-nrf.rules ]; then
        echo "Downloading nRF rules..."
        wget "${NRF_RULES_URL}" -O ${SCRIPT_DIR}/71-nrf.rules
        echo "**NOTE**: From outside nix-shell copy nRF rules to /lib/udev/rules.d/ to avoid permission issues."
        echo "         run 'sudo cp ${SCRIPT_DIR}/71-nrf.rules /lib/udev/rules.d/'"
        echo " Restart your computer to apply the changes."
    else
        echo "nRF rules already exist."
    fi

    if [ ! -f /lib/udev/rules.d/99-mm-nrf-blacklist.rules ]; then
        echo "Downloading nRF blacklist rules..."
        wget "${NRF_RULES_BLACKLIST_URL}" -O ${SCRIPT_DIR}/99-mm-nrf-blacklist.rules
        echo "**NOTE**: From outside nix-shell copy nRF blacklist rules to /lib/udev/rules.d/ to avoid permission issues."
        echo "         run 'sudo cp ${SCRIPT_DIR}/99-mm-nrf-blacklist.rules /lib/udev/rules.d/'"
        echo " Restart your computer to apply the changes."
    else
        echo "nRF blacklist rules already exist."
    fi

    SNIFFER_FW_FILE="nrf_sniffer_for_bluetooth_le_4.1.1.zip"
    SNIFFER_FW_URL="https://nsscprodmedia.blob.core.windows.net/prod/software-and-other-downloads/desktop-software/nrf-sniffer/sw/${SNIFFER_FW_FILE}"

    if [ ! -d "${SNIFFER_FW_DIR}" ]; then
        echo "Downloading nRF Sniffer firmware..."
        mkdir -p "${SNIFFER_FW_DIR}"
        curl -L -o "${SNIFFER_FW_DIR}/${SNIFFER_FW_FILE}" "${SNIFFER_FW_URL}"
        unzip "${SNIFFER_FW_DIR}/${SNIFFER_FW_FILE}" -d "${SNIFFER_FW_DIR}"
        echo "You can find the firmware in ${SNIFFER_FW_DIR}/"
    else
        echo "nRF Sniffer firmware already exists."
    fi
}

if [ "$COMMAND" == "install" ]; then
    echo "Installing BLE Sniffer..."
    install_ble_sniffer
elif [ "$COMMAND" == "uninstall" ]; then
    echo "Uninstalling BLE Sniffer..."
    rm -rf "${APP_DIR}"
    rm -f "${SCRIPT_DIR}/${SNIFF_JLINK_FILE}"
    rm -f "${SCRIPT_DIR}/${SNIFF_UTIL_FILE}"
    exit 0
elif [ "$COMMAND" == "run" ]; then
    echo "Running BLE Sniffer..."
    run_ble_sniffer_tool "${ARGS[@]}"
elif [ "$COMMAND" == "help" ]; then
    echo "Showing help menu..."
    help_menu
    exit 0
else
    help_menu
    exit 1
fi


