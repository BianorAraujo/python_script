from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from playsound import playsound
from dotenv import load_dotenv
import os

import time

# Carregar variáveis do arquivo .env
load_dotenv()

# Obter as variáveis
email = os.getenv("LOGIN_EMAIL")
senha = os.getenv("LOGIN_SENHA")
url_inicial = os.getenv("URL")

if not email or not senha or not url_inicial:
    raise ValueError("As variáveis de ambiente URL, LOGIN_EMAIL ou LOGIN_SENHA não estão definidas.")

# Configurações globais
def configurar_driver():
    # Configuração do ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36")
    chrome_options.add_argument("--profile-directory=Default")

    #chrome_options.add_argument("--headless")  # Remove essa linha se quiser ver o navegador
    service = Service("/Users/bianor/Downloads/chromedriver-mac-arm64/chromedriver")  # Substitua pelo caminho do seu ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# Função para acessar o site
def acessar_site(driver, url):
    try:
        driver.get(url)

        # Executar script para simular requisição
        driver.execute_script("""
            fetch('/algum-endpoint', {
                method: 'POST',
                headers: {
                    'Origin': 'https://prenotami.esteri.it',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ key: 'value' })
            }).then(response => console.log(response));
        """)

        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("Página carregada.")
    except Exception as e:
        print(f"Error acessar_site: {e}")


# Função para preencher o formulário de login
def login(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-email"))).send_keys(email)
        time.sleep(3)
        driver.find_element(By.ID, "login-password").send_keys(senha, Keys.RETURN)
        
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-password"))).send_keys(senha)
        #time.sleep(3)

        print("Login realizado com sucesso.")

        elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "profileImg"))
        )
        
        if elemento:
            print("A página inicial foi carregada com sucesso.")
        else:
            print(f"Erro ao carregar a página inicial")

        # WebDriverWait(driver, 10).until(
        #     lambda d: d.execute_script("return document.readyState") == "complete"
        # )
    except Exception as e:
        print(f"Erro ao carregar a página inicial: {e}")


# Função para clicar no menu Book
def clicar_no_book(driver):
    try:
        advanced_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "advanced")))
        advanced_link.click()
        print("Clicou no menu Book com sucesso.")
        time.sleep(3)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("A Página de serviços foi carregada com sucesso.")
    except Exception as e:
        print(f"Erro clicar no menu Book: {e}")


# Função para clicar no botão de agendamento do passaporte
def clicar_botao_passaporte(driver):
    try:
        passport_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/Services/Booking/1162']"))
        )
        passport_link.click()
        print("Clicou no botão de agendamento de passaporte com sucesso.")
    except Exception as e:
        print(f"Erro clicar no botao passaporte: {e}")


# Função para verificar se apareceu a mensagem sem agendamento
def verificar_mensagem(driver):
    try:
        # Esperar pelo modal visível
        modal = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".jconfirm.jconfirm-light.jconfirm-open"))
        )

        if modal:
            print("Modal visível!")

            # Verificar o botão "OK" dentro do modal
            botao_ok = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='jconfirm-buttons']/button[@type='button']"))
            )

            # Garantir que o botão está na tela
            driver.execute_script("arguments[0].scrollIntoView(true);", botao_ok)

            botao_ok.click()
            print("Botão 'OK' clicado com sucesso!")
            time.sleep(180)
            verificar_agendamento(driver)
        else:
            print("A mensagem não apareceu!")
            alerta()

    except Exception as e:
        print(f"Erro para fechar a mensagem: {e}")


# Função verificar agendamento
def verificar_agendamento(driver):
    clicar_botao_passaporte(driver)
    time.sleep(3)
    verificar_mensagem(driver)


# Função para tocar alerta
def alerta():
    playsound("alert.mp3")


# Função para deslogar
def logout(driver):
    try:
        logoutForm = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "logoutForm")))

        # Encontrar o botão dentro da div e clicar nele
        button = logoutForm.find_element(By.TAG_NAME, "button")
        button.click()
        print("Deslogado com sucesso.")
    except Exception as e:
        print(f"Error: Botão logout não encontrado. {e}")


#função principal
def main():    
    driver = configurar_driver()

    try:
        acessar_site(driver, url_inicial)
        time.sleep(3)
        login(driver)
        time.sleep(3)
        clicar_no_book(driver)
        time.sleep(3)
        verificar_agendamento(driver)

    # Continue com o restante do fluxo...
    except Exception as e:
        print(f"Error: {e}")
    finally:
        logout(driver)
        time.sleep(5)
        driver.quit()



# Executar o programa
if __name__ == "__main__":
    main()

