import os
import json
import logging
import requests
from mia.backend.etl.classes.classes import ETLTask

from bs4 import BeautifulSoup
from lxml import etree

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BoeETLTask(ETLTask):
    def __init__(self, config: dict):
        super().__init__(config)
        self.config = config
        self.date = config.get("date")
        self.day = self.date.split("/")[2]
        self.month = self.date.split("/")[1]
        self.year = self.date.split("/")[0]

    def scrape_web(self):
        if (
            not self.date
            or not isinstance(self.date, str)
            or not self.date.startswith("/")
            or not self.date.endswith("/")
        ):
            raise ValueError(
                "The 'day' config must be a string in the format '/YYYY/MM/DD/'"
            )

        url = f"https://www.boe.es/boe/dias{self.date}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response_text = response.text

        soup = BeautifulSoup(response_text, "lxml")
        
        # Extract title and BOE number
        titulo_sumario = soup.find('div', id='indiceSumario').find('div', class_='tituloSumario')
        title = titulo_sumario.find('h2').text.strip()
        boe_num = titulo_sumario.find('abbr', title='Número').next_sibling.strip()
        link_sumario = soup.find('div', class_='linkSumario')
        boe_pdf_link = link_sumario.find('a', title=lambda x: x and 'PDF' in x)['href']
        fecha_de_publicacion = title.split(":")[1].split(",")[0].strip()

        data = {
            "boe_num": boe_num,
            "title": title,
            "fecha_de_publicacion": fecha_de_publicacion,
            "boe_pdf_link": boe_pdf_link,
            "disposiciones": []
        }
        # Extract dispos
        dispos = soup.find_all(class_='dispo')
        for dispo in dispos:
            title = dispo.find('p').text.strip()
            pdf_link = dispo.find('li', class_='puntoPDF').find('a')['href']
            data["disposiciones"].append({
                "title": title,
                "pdf_route": pdf_link,
            })
        return data
        

    def run(self):
        logger.info("Running Boe ETL task")
        result = self.scrape_web()
        logger.info(result)
        # save_path = os.path.join(
        #     self.config.get("output_path"),
        #     "boe",
        #     "raw",
        #     self.year,
        #     self.month,
        #     self.day,
        #     "test.txt",
        # )
        # logger.info(f"Saving result to {save_path}")
        # os.makedirs(os.path.dirname(save_path), exist_ok=True)
        # with open(save_path, "w") as f:
        #     f.write(result.prettify())


if __name__ == "__main__":
    config = {
        "date": "/2024/12/28/",
        "output_path": "/Users/alvaromoure/desarrollo/mia/data",
    }

    task = BoeETLTask(config)
    task.run()
