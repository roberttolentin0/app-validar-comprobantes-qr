import logging
import os
import traceback

class Logger():

    def __set_logger(self):
        log_directory = 'src/utils/log'
        log_filename = 'app.log'

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG) # solo en debug

        log_path = os.path.join(log_directory, log_filename)
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        if (logger.hasHandlers()):
            logger.handlers.clear()
        logger.addHandler(file_handler)

        # Solo en modo Desarrollo
        # Para mostrar en consola
        console_handler = logging.StreamHandler()  # Controlador de consola
        console_handler.setLevel(logging.DEBUG)   # Establecer nivel de registro para consola
        console_handler.setFormatter(formatter)  # Aplicar el mismo formato a la consola
        logger.addHandler(console_handler)  # Agregar el controlador de consola

        return logger

    @classmethod
    def add_to_log(cls, level, message):
        try:
            logger = cls.__set_logger(cls)

            if (level == "critical"):
                logger.critical(message)
            elif (level == "debug"):
                logger.debug(message)
            elif (level == "error"):
                logger.error(message)
            elif (level == "info"):
                logger.info(message)
            elif (level == "warn"):
                logger.warn(message)
        except Exception as ex:
            print(traceback.format_exc()) # Muestra todo el flujo de archivos antes de llegar a la exception
            print(ex)
