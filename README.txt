# Joystick Mapper

[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-MVP-yellow.svg)]()
[![Platform](https://img.shields.io/badge/platforms-Windows%20%7C%20macOS-lightgrey.svg)]()

Joystick Mapper es una aplicación multiplataforma desarrollada en Python que permite transformar las entradas de cualquier gamepad en acciones de teclado y mouse. Diseñado para gamers y usuarios que buscan mayor accesibilidad, este proyecto facilita el uso de controles en aplicaciones y juegos que carecen de soporte nativo para periféricos.

## 🚀 Características principales

*   **Gestión inteligente de dispositivos:** Detección automática de controles y reconexión en caliente sin reiniciar la app.
*   **Mapeo flexible:** Asignación de botones, D-Pad y gatillos a teclas o acciones del mouse.
*   **Control preciso:** Configuración avanzada de `Deadzone`, `Polling rate` y sensibilidad del mouse.
*   **Perfiles personalizados:** Sistema de perfiles independiente para cada juego, con carga automática del último estado.
*   **Interfaz visual:** Visualización en tiempo real del estado de los botones y ejes del control conectado.

---

## 📸 Capturas de pantalla

| Vista general | Mapeo de entradas |
| :---: | :---: |
| ![Perfiles](screenshots/profiles.png) | ![Mapeo](screenshots/mapping.png) |

---

## 📂 Estructura de Perfiles

Joystick Mapper utiliza archivos `.json` para gestionar configuraciones independientes, permitiendo una portabilidad sencilla:

```text
profiles/
├── Default.json
├── League of Legends.json
├── Minecraft.json
└── RetroArch.json