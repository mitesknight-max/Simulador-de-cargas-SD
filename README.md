# Voltio - Simulador Electrostático Interactivo

Este proyecto es un **Simulador Electrostático Interactivo en 2D y 1D** desarrollado en Python. Permite modelar sistemas de cargas puntuales, calcular las distancias euclidianas entre ellas, obtener la fuerza eléctrica neta mediante el Principio de Superposición (con descomposición en componentes rectangulares) y evaluar el campo eléctrico total en puntos específicos definidos por el usuario.

El software sigue un flujo lógico estricto y secuencial, libre de datos preestablecidos, asegurando que toda la simulación nazca de las configuraciones reales tecleadas por el usuario, implementando un control de rango dinámico para evitar la alteración o desborde del sistema.

---

## Características Principales

* **Modelado Dimensional:** Selección inicial entre entornos lineales 1D (sobre el eje X) o bidimensionales 2D (Plano Cartesiano).
* **Captura de Datos Dinámica:** Formulario secuencial paso a paso para el registro de magnitudes, coordenadas de las cargas y un mínimo de 3 puntos de interés para el campo eléctrico.
* **Motor Gráfico Interactivo:** Renderizado en tiempo real usando Matplotlib que permite el arrastre dinámico (*Drag and Drop*) de las cargas con el mouse, recalculando la física del sistema al vuelo.
* **Análisis Vectorial Avanzado:** Representación gráfica y analítica de la Fuerza Neta (vector morado), sus componentes rectangulares F_x y F_y (vectores naranja y azul claro), y los vectores de Campo Eléctrico en el espacio (vectores verdes).
* **Panel de Resultados Tabulado:** Reporte matemático extendido y formateado a la derecha del plano para facilitar la extracción de datos y la elaboración de reportes físicos.
* **Validaciones Físicas y de Software:** Protección contra ingresos de datos no numéricos, colisión extrema de cargas espaciales, duplicación de coordenadas e indeterminaciones matemáticas por división entre cero.

---

## Librerías Utilizadas

El núcleo del software se apoya exclusivamente en las siguientes librerías de la suite de Python:

1.  **`numpy` (v1.26+)**: Utilizada para el manejo de vectores algebraicos, cálculo de normas euclidianas (distancias entre puntos) y operaciones trigonométricas polares (`arctan2`).
2.  **`matplotlib` (v3.8+)**: Encargada de renderizar el plano cartesiano, las mallas milimétricas, los gráficos de dispersión de las cargas puntuales y el trazado de campos vectoriales mediante el uso de `quiver`.
3.  **`tkinter` (Nativa)**: Librería encargada de construir toda la Interfaz Gráfica de Usuario (GUI), los contenedores avanzados (`LabelFrame`), los menús dinámicos (`Combobox`) y los cuadros de diálogo para alertas de seguridad (`messagebox`).

---

##  Instrucciones de Instalación

Si deseas ejecutar o auditar el **código fuente** directamente, requieres tener instalado Python 3.10 o superior (se recomienda el uso del gestor moderno `uv` para automatizar el entorno).

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/Voltio-Simulador.git](https://github.com/TU_USUARIO/Voltio-Simulador.git)
    cd Voltio-Simulador
    ```

2.  **Instalar las dependencias requeridas:**
    * *Si utilizas el gestor estándar de Python (pip):*
        ```bash
        pip install numpy matplotlib
        ```
    * *Si utilizas el entorno protegido moderno de `uv`:*
        ```bash
        uv pip install numpy matplotlib --system
        ```

---

## Instrucciones de Ejecución

Tienes dos métodos independientes para desplegar el simulador en cualquier computadora:

### Método A: Desde el Código Fuente (Desarrollo)
Una vez instaladas las dependencias, ejecuta la aplicación desde tu terminal ejecutando el script principal:
```bash
python simulador_interactivo_v0.3.py
```

Método B: Desde el Archivo Ejecutable (Producción)
Para entornos donde no se cuente con un intérprete de Python instalado de fábrica, la aplicación incluye una versión compilada e independiente:

Navega a la carpeta dist/ dentro del proyecto.

Ejecuta con un doble clic el archivo independiente: simulador_interactivo_v0.3.exe.
(Nota: El arranque inicial puede demorar unos segundos mientras el sistema descomprime en memoria el motor matemático de Matplotlib).
