# Proyecto Gráfico: Visualización de NFA y DFA

## Descripción
Este proyecto tiene como objetivo visualizar Autómatas Finitos No Deterministas (NFA) y Autómatas Finitos Deterministas (DFA) basados en una expresión regular dada. El proyecto sigue la arquitectura Modelo-Vista-Controlador (MVC) y utiliza el algoritmo de Thompson para construir el NFA. Además, se emplean las bibliotecas `customtkinter`, `graphviz` y `sqlite3`.

## Basado en el Repositorio Original

Este proyecto se basa en el repositorio MaIsabelSolano/UVG_DLP_Regex-NFA-DFA. Utilicé su código como punto de partida para crear un visualizador de expresiones regulares (regex) a autómatas finitos deterministas (DFA) o no deterministas (NFA) utilizando Python.

Agradezco al los autores por proporcionar una base sólida para mi proyecto y por compartir su trabajo con la comunidad.

## Características
- Ingresar una expresión regular.
- Generar el NFA y el DFA según la preferencia.
- Mostrar los gráficos del NFA y el DFA.
- Almacenar información de los autómatas (expresión regular, NFA y DFA) en una base de datos SQLite.

## Estructura del Proyecto
- `main.py`: Punto de entrada principal de la aplicación.
- `models`: Contiene la clase abstracta `Automata` (base para NFA y DFA).
- `nfa.py`: Implementa el NFA utilizando el algoritmo de Thompson.
- `dfa.py`: Construye el DFA a partir del NFA.
- `views`: Maneja la interfaz gráfica de usuario (GUI) utilizando `customtkinter`.
- `automata_interface.py`: Gestiona la base de datos SQLite para almacenar información de los autómatas.

## Instalación
1. Necesario Python 3.x.
2. Instala los paquetes requeridos:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta `main.py` para iniciar la aplicación.

¡Diviértete explorando los autómatas y su representación gráfica! 🤖🔍
