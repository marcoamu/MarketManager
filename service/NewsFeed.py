import feedparser
from service.TelegramService import TelegramService
import json
from datetime import datetime

class NewsFeed:

    def __init__(self):

        self.telegram = TelegramService()

        # if "WINDOWS" in self.env:
        # self.PROCESSED_NEWS_FILE= "processed_news.json"
        # else:
        self.PROCESSED_NEWS_FILE = "/home/MarketManager/service/processed_news.json"


        self.fuentes_rss = {
            "Xataka": "https://www.xataka.com/feed",
            "Hipertextual": "https://hipertextual.com/feed",
            "Genbeta": "https://www.genbeta.com/feed",
            "El Androide Libre": "https://elandroidelibre.elespanol.com/feed",
            "Omicrono": "https://omicrono.elespanol.com/feed",
            "CNN": "https://cnnespanol.cnn.com/feed/"
        }

    def load_processed_news(self):
        """Carga noticias procesadas desde un archivo local."""
        try:
            with open(self.PROCESSED_NEWS_FILE, "r") as file:
                return set(json.load(file))
        except FileNotFoundError:
            return set()

    def save_processed_news(self,processed_news):
        """Guarda noticias procesadas en un archivo local."""
        with open(self.PROCESSED_NEWS_FILE, "w") as file:
            json.dump(list(processed_news), file)

    def obtener_noticias_rss(self, url, limite=10):
        """
        Obtiene noticias de un feed RSS.
        :param url: URL del feed RSS.
        :param limite: Número máximo de noticias a recuperar.
        :return: Lista de noticias.
        """
        feed = feedparser.parse(url)
        processed_news = self.load_processed_news()
        noticias = []
        for entrada in feed.entries[:limite]:
            news_id = entrada.link  # Usar el enlace como identificador único
            if news_id not in processed_news:
                noticias.append({
                    "title": entrada.title,
                    "summary": entrada.summary,
                    "link": entrada.link,
                    "published": entrada.published if "published" in entrada else "No disponible"
                })
                processed_news.add(news_id)
        # Guardar las noticias procesadas
        self.save_processed_news(processed_news)
        return noticias

    def buscarNoticias(self):
        message = ""
        hasmsm = False
        for fuente, url in self.fuentes_rss.items():
            # message = ""
            hasmsm = False

            # print(f"Noticias de {fuente}:\n")
            noticias = self.obtener_noticias_rss(url)
            message = f"Noticias de <b>{fuente}</b>:\n"
            # message += f"   Publicado: <b>{noticia['published']}</b>\n"
            for i, noticia in enumerate(noticias, 1):
                hasmsm = True
                if i ==1:
                    message +=  f"   Publicado: {noticia['published']}\n"
                message +=  f"{i}. {noticia['title']}\n"
                # print(f"{i}. {noticia['title']}")
                # message +=  f"   Publicado: {noticia['published']}\n"
                # print(f"   Publicado: {noticia['published']}")
                # print(f"   Link: {noticia['link']}\n")
                message +=  f"   Link: {noticia['link']}\n"
            # print("-" * 50)
            if hasmsm:
                print(message)
                self.telegram.enviarMensaje(message, self.telegram.tokenBot, -4605296715)
            if not noticias:
                print(f"\nNo hay noticias nuevas ({datetime.now()}).")
def main():
    newsFeed = NewsFeed()
    newsFeed.buscarNoticias()

if __name__ == "__main__":
    main()