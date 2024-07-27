# import os
# import shutil
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import Select
# from bs4 import BeautifulSoup
# import stat

# download_dir = "/workspaces/extracao-b3-ingestao-s3"  
# arquivos_csv_dir = "/workspaces/extracao-b3-ingestao-s3/arquivos_csv" 



# def mover_arquivo(origem, destino):
#        try:
#            shutil.move(origem, destino)
#            print(f"Arquivo movido para: {destino}")
#        except Exception as e:
#            print(f"Erro ao mover arquivo: {e}")




# def extrair_dados(): 

#     # Configurar opções do Chrome
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--headless")  # Executar em modo headless, se necessário
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--window-size=1920x1080")
#     chrome_options.add_argument("--start-maximized")
#     chrome_options.add_argument("--disable-extensions")
#     chrome_options.add_argument("--disable-infobars")

#     # Especificar a versão do Chrome manualmente
#     chrome_version = "126.0.6478.127"  # Substitua pela versão correta do seu Chrome

#     # Inicializar o WebDriver
#     try:
#         driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
#     except Exception as e:
#         print(f"Erro ao inicializar o WebDriver: {e}")
#         return None

     
   

#     # Verificar se o diretório de download existe
#     if not os.path.exists(download_dir):
#        os.makedirs(download_dir)

#     prefs = {
#        "download.default_directory": download_dir,
#        "download.prompt_for_download": False,
#        "download.directory_upgrade": True,
#        "safebrowsing.enabled": True
#    }
#     chrome_options.add_experimental_option("prefs", prefs)
#     # definir_permissoes(download_dir)
    
    

#     try:
#         url = "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br"  # Substitua pela URL correta
#         print(f"Acessando a URL: {url}")
#         driver.get(url)

# #         # Esperar até que o link de download esteja disponível e clicar nele
# #         download_link = WebDriverWait(driver, 20).until(
# #     EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Download')]"))
# # )
# #         print("Link de download encontrado, baixando...")
# #         download_link.click()

#     # Encontre o elemento <select> pelo seu ID
#         select_element = driver.find_element(By.ID, "segment")

#         select = Select(select_element)
#         select.select_by_visible_text("Setor de Atuação")

#         # Rolar até o final da página
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#         # Aguardar o elemento estar presente e visível
#         wait = WebDriverWait(driver, 20)  # Aumentar o tempo de espera
#         dropdown = wait.until(
#             EC.visibility_of_element_located((By.XPATH, "//select[@id='selectPage']")))  # Clicar no dropdown para abri-lo

#         # Clica no dropdown
#         dropdown.click()

#         # Aguardar a opção '120' estar visível
#         option_120 = wait.until(EC.visibility_of_element_located((By.XPATH, "//select[@id='selectPage']/option[text()='120']")))

#         # Selecionar a opção '120'
#         option_120.click()

#         time.sleep(3)

#         # Encontrar a tabela
#         table = driver.find_element(By.CSS_SELECTOR, "table.table-responsive-sm.table-responsive-md")

#         # Obter o HTML da tabela
#         html_table = table.get_attribute('innerHTML')

#         # Analisar o HTML com BeautifulSoup
#         soup = BeautifulSoup(html_table, 'html.parser')

#         # Extrair os nomes das colunas
#         column_names = [th.text.strip() for th in soup.find_all('th')]

#         # Extrair os dados da tabela
#         rows = soup.find_all('tr')
#         data = []
#         for row in rows:
#             cells = row.find_all('td')
#             row_data = [cell.text.strip() for cell in cells]
#             data.append(row_data)
#             # Esperar um tempo para garantir que o download seja concluído
#             time.sleep(10)  # Ajuste o tempo conforme necessário

#         # Listar arquivos no diretório de download para encontrar o mais recente
#         files = os.listdir(download_dir)
#         paths = [os.path.join(download_dir, basename) for basename in files if basename.endswith('.csv')]

#         if not paths:
#                     print("Nenhum arquivo CSV encontrado no diretório de download.")
#                     return None

#         newest_file = max(paths, key=os.path.getctime)

#         print(f"Arquivo baixado: {newest_file}")

#         # mover_arquivo(newest_file, os.path.join(arquivos_csv_dir, os.path.basename(newest_file)))
#         return newest_file

#     except Exception as e:
#         print(f"Erro durante a extração: {e}")
#         return None
    
#     finally:
#         driver.quit()

# if __name__ == "__main__":
    
#     # excluir_arquivos()
#     extrair_dados()

import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

download_dir = "/workspaces/extracao-b3-ingestao-s3"
arquivos_csv_dir = "/workspaces/extracao-b3-ingestao-s3/arquivos_csv"

def mover_arquivo(origem, destino):
    try:
        shutil.move(origem, destino)
        print(f"Arquivo movido para: {destino}")
    except Exception as e:
        print(f"Erro ao mover arquivo: {e}")

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

    # Configurar preferências de download
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Inicializar o WebDriver
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    except Exception as e:
        print(f"Erro ao inicializar o WebDriver: {e}")
        return None

    # Verificar se o diretório de download existe
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    try:
        url = "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br"  # Substitua pela URL correta
        print(f"Acessando a URL: {url}")
        driver.get(url)

        # Encontre o elemento <select> pelo seu ID
        select_element = driver.find_element(By.ID, "segment")
        select = Select(select_element)
        select.select_by_visible_text("Setor de Atuação")

        # Rolar até o final da página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Aguardar o elemento estar presente e visível
        wait = WebDriverWait(driver, 20)  # Aumentar o tempo de espera
        dropdown = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//select[@id='selectPage']"))
        )

        # Clica no dropdown
        dropdown.click()

        # Aguardar a opção '120' estar visível
        option_120 = wait.until(EC.visibility_of_element_located((By.XPATH, "//select[@id='selectPage']/option[text()='120']")))

        # Selecionar a opção '120'
        option_120.click()

        time.sleep(3)

        # # Encontrar a tabela
        # table = driver.find_element(By.CSS_SELECTOR, "table.table-responsive-sm.table-responsive-md")

        # # Obter o HTML da tabela
        # html_table = table.get_attribute('innerHTML')

        # # Analisar o HTML com BeautifulSoup
        # soup = BeautifulSoup(html_table, 'html.parser')

        # # Extrair os nomes das colunas
        # column_names = [th.text.strip() for th in soup.find_all('th')]

        # # Extrair os dados da tabela
        # rows = soup.find_all('tr')
        # data = []
        # for row in rows:
        #     cells = row.find_all('td')
        #     row_data = [cell.text.strip() for cell in cells]
        #     data.append(row_data)

        # Esperar até que o link de download esteja disponível e clicar nele
        download_link = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Download')]"))
)
        print("Link de download encontrado, baixando...")
        download_link.click()


        # Esperar um tempo para garantir que o download seja concluído
        time.sleep(3)  # Ajuste o tempo conforme necessário

        # Listar arquivos no diretório de download para encontrar o mais recente
        files = os.listdir(download_dir)
        paths = [os.path.join(download_dir, basename) for basename in files if basename.endswith('.csv')]

        if not paths:
            print("Nenhum arquivo CSV encontrado no diretório de download.")
            return None

        newest_file = max(paths, key=os.path.getctime)
        print(f"Arquivo baixado: {newest_file}")

        # Mover o arquivo para o diretório de destino
        mover_arquivo(newest_file, os.path.join(arquivos_csv_dir, os.path.basename(newest_file)))
        return newest_file

    except Exception as e:
        print(f"Erro durante a extração: {e}")
        return None

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_dados()