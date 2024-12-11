# Instrucciones de Ejecución

Para ejecutar la aplicación, sigue estos pasos:

1. **Clonar el Repositorio**:
    Clona el repositorio en tu máquina local usando el siguiente comando:
    ```sh
    git clone https://github.com/jmxzapata/pok_schnorr.git
    ```

2. **Navegar al Directorio del Proyecto**:
    Cambia tu directorio actual al directorio del proyecto:
    ```sh
    cd pok_schnorr
    ```

3. **Configurar Variables de Entorno**:
    Crea una carpeta `.env` en la raíz del directorio del proyecto. Luego activa el entorno para instalar las dependencias.

    ```sh
    python -m venv .env
    .env\Scripts\activate (CMD)
    ```

4. **Instalar Dependencias**:
    Instala las dependencias necesarias usando el gestor de paquetes `pip`, ejecuta:
    ```sh
    pip install -r requirements.txt
    ```

5. **Ejecutar la Aplicación**:

    ```sh
    python .\server\app.py
    ```
    Esto iniciará el servidor de la aplicación. Escucha las solicitudes entrantes en el puerto especificado (0.0.0.0:5001).

6. **Ejecutar el Cliente**:
    Abre una nueva terminal en el directorio del proyecto y ejecuta el siguiente comando para iniciar el cliente:
    ```sh
    python .\client\client.py
    ```

7. **Seguir los Pasos**:
    El cliente te pedirá que ingreses el número de opción para registrarte, autenticarte o salir de la aplicación.
