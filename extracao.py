import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def extrair_dados():
    # Configurar opções do Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")  # Executar em modo headless, se necessário
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    
# Especificar a versão do Chrome manualmente
    chrome_version = "126.0.6478.127"  # Substitua pela versão correta do seu Chrome
    
    # Inicializar o WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    download_dir = "/workspaces/extracao-b3-ingestao-s3" 
    try:
        driver.get("https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br")  # Substitua pela URL correta

        # Esperar até que o link de download esteja disponível e clicar nele
        download_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "btn btn-b3 dwn")]'))
        )
        download_link.click()

        # Esperar um tempo para garantir que o download seja concluído
        time.sleep(10)  # Ajuste o tempo conforme necessário

        # Listar arquivos no diretório de download para encontrar o mais recente
        files = os.listdir(download_dir)
        paths = [os.path.join(download_dir, basename) for basename in files if basename.endswith('.csv')]
        newest_file = max(paths, key=os.path.getctime)

        print(f"Arquivo baixado: {newest_file}")
        return newest_file

    except Exception as e:
        print(f"Erro durante a extração: {e}")
        raise

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_dados()