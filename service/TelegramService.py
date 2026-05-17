import os
import requests

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from core.config import get_config

class TelegramService:
    mensajes = list()


    def __init__(self, use_config=True):
        """Initialize TelegramService with credentials from environment variables.

        Args:
            use_config: If True, load from environment variables. If False, use provided values.
        """
        if use_config:
            config = get_config()
            self.appID = config.telegram.telegram_app_id
            self.appAPIHash = config.telegram.telegram_app_api_hash
            self.tokenBot = config.telegram.telegram_token_bot
            self.tokenBot1 = config.telegram.telegram_token_bot_alt
            self.numeroTelefono = config.telegram.telegram_phone_number
            self.idChat = config.telegram.telegram_chat_id
            self.idGrupo = config.telegram.telegram_group_id
        else:
            # Fallback for backward compatibility - should not be used
            self.appID = os.getenv('TELEGRAM_APP_ID', '')
            self.appAPIHash = os.getenv('TELEGRAM_APP_API_HASH', '')
            self.tokenBot = os.getenv('TELEGRAM_TOKEN_BOT', '')
            self.tokenBot1 = os.getenv('TELEGRAM_TOKEN_BOT_ALT', '')
            self.numeroTelefono = os.getenv('TELEGRAM_PHONE_NUMBER', '')
            self.idChat = int(os.getenv('TELEGRAM_CHAT_ID', '0'))
            self.idGrupo = int(os.getenv('TELEGRAM_GROUP_ID', '0'))


    def send_message(self, message):
        print("Conectando con Telegram...")
        # Creamos sesión de Telegram
        clienteTelegram = TelegramClient('sesión', self.appID, self.appAPIHash)

        print("Iniciando sesión en Telegram...")
        # Iniciamos una sesión de Telegram
        clienteTelegram.connect()

        # Si se ejecuta por primera vez, Telegram generará un código de inicio de sesión
        # en el chat de Telegram "Telegram", si es así, la aplicación
        # pedirá este código de inicio de sesión
        print("Comprobando autorización...")
        if not clienteTelegram.is_user_authorized():
            clienteTelegram.send_code_request(self.numeroTelefono)
            # Pedimos el código de inicio de sesión que haya enviado Telegram al usuario
            try:
                clienteTelegram.sign_in(self.numeroTelefono, input('Introduzca el Código de inicio de sesión: '))
            except SessionPasswordNeededError:
                clienteTelegram.sign_in(self.numeroTelefono, input('Introduzca la contraseña: '))

        # *** Enviar mensaje usando el ID de chat de Telegram ***
        try:
            print("Creando un receptor de Telegram a partir del ID de chat de Tetlegram...")
            receptorChat = clienteTelegram.get_input_entity(self.idChat)

            async def main():
                # Enviamos el mensaje al chat de Telegram
                # Se enviará al chat de Telegram del Bot con ID indicado en el receptor
                print("Enviando mensaje a chat de Bot del receptor de Telegram (ID Chat)...")
                await clienteTelegram.send_message(receptorChat, message)
                # Solo a modo informativo, obtenemos el nombre del Bot de Telegram al que enviamos el mensaje
                print("Enviado mensaje a chat de Bot [{}] de Telegram".format(self.idChat))

            # Para que se ejecute la tarea anterior del método asíncrono
            clienteTelegram.loop.run_until_complete(main())

        except Exception as e:
            print("Se ha producido un error en el envío por ID de Chat: {}".format(e));

        # # *** Enviar mensaje usando nombre de usuario de Telegram ***
        # try:
        #     print("Creando un receptor de Telegram a partir del nombre de usuario de Tetlegram...")
        #     receptorNombre = clienteTelegram.get_input_entity(nombreUsuarioTelegram)
        #
        #     async def main():
        #         # Enviamos el mensaje al chat de Telegram
        #         # Se enviará al chat de Telegram del Bot con el usuario indicado en el receptor
        #         print("Enviando mensaje a chat de Bot del receptor de Telegram (usuario)...")
        #         await clienteTelegram.send_message(receptorNombre, mensaje2)
        #         print("Enviado mensaje a chat de Bot del receptor [{}] de Telegram".format(nombreUsuarioTelegram))
        #
        #     clienteTelegram.loop.run_until_complete(
        #         main())  # Para que se ejecute la tarea anterior del método asíncrono
        #
        # except Exception as e:
        #     print("Se ha producido un error en el envío por nombre de usuario: {}".format(e));

        # Desconectamos la sesión de Telegram abierta
        print("Desconectando sesión de Telegram...")
        clienteTelegram.disconnect()
        print("Desconectado y fin del programa")

    def enviarMensaje(self,mensaje):
        requests.post('https://api.telegram.org/bot' + self.tokenBot + '/sendMessage',
                      data={'chat_id': self.idGrupo, 'text': mensaje, 'parse_mode': 'HTML'})

    def enviarMensaje(self, mensaje, token, grupo):
        requests.post('https://api.telegram.org/bot' + token+ '/sendMessage',
                      data={'chat_id': grupo, 'text': mensaje, 'parse_mode': 'HTML'})

    def enviarDocumento(self,ruta, grupo=-613511116, caption = ""):
        requests.post('https://api.telegram.org/bot' + self.tokenBot + '/sendDocument',
                      files={'document': (ruta,open(ruta, 'rb'))},
                      data={'chat_id': grupo, 'caption': caption})

    def enviarDocumento2(self,ruta):
        requests.post('https://api.telegram.org/bot' + self.tokenBot + '/sendDocument',
                      files={'document': open(ruta, 'rb')},
                      data={'chat_id': self.idGrupo, 'caption': 'imagen caption'})

    def enviarDocumento3(self,ruta):

        requests.post('https://api.telegram.org/bot' + self.tokenBot + '/sendDocument',
                      files={'document': open(ruta, 'rb')},
                      data={'chat_id': self.idGrupo, 'caption': 'imagen caption'})

    def prepararLlamada(self,mensaje):
        self.mensajes.append(mensaje)
        # requests.get(f'https://api.callmebot.com/start.php?user=@Reynaldoag&lang=es-ES-Wavenet-C&text={mensaje}' )

    def hacerLlamadaFinal(self):
        mensaje = "Hay una tendencia en: "
        hasMensaje = False
        for mensa in self.mensajes:
            mensaje = mensaje+" "+mensa
            hasMensaje = True
        if hasMensaje:
            self.hacerLlamada(mensaje)

    def hacerLlamada(self,mensaje):
        requests.get(f'https://api.callmebot.com/start.php?user=@Reynaldoag&lang=es-ES-Neural2-A&text={mensaje}' )

def main():
    telegram = TelegramService()
    # telegram.send_message("test Mensaje")
    # telegram.enviarMensaje("hola 2 ",telegram.tokenBot,-648460624)
    telegram.enviarDocumento("./img/image.jpg")


if __name__ == "__main__":
    main()