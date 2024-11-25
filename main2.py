import requests
import time
from playsound import playsound
from dotenv import load_dotenv
import os


# Carregar variáveis do arquivo .env
load_dotenv()

# Obter as variáveis
email = os.getenv("LOGIN_EMAIL")
senha = os.getenv("LOGIN_SENHA")
login_url = os.getenv("URL_LOGIN")
target_url = os.getenv("URL_TARGET")

if not email or not senha or not login_url or not target_url:
    raise ValueError("As variáveis de ambiente URL_LOGIN, URL_TARGET, LOGIN_EMAIL ou LOGIN_SENHA não estão definidas.")


# Dados do login
login_payload = {
    "login-email": "email",  # Substitua pelo campo correto do formulário
    "login-password": "senha"     # Substitua pelo campo correto do formulário
}

# Cabeçalhos (opcional)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}


def verificar_agendamento(session):
    # Acessar a URL desejada
    target_response = session.get(target_url, headers=headers)
    time.sleep(3)

    # Verificar se foi redirecionado
    current_url = target_response.url
    
    if current_url == target_url:
        print(f"Página acessada com sucesso: {current_url}")
        #playsound("alert.mp3")
    else:
        print(f"Não tem vaga!")
        print(f"Url atual: {current_url}")
        time.sleep(180)
        verificar_agendamento(session)


# Iniciar a sessão
def main():
    with requests.Session() as session:
        first = session.get("https://prenotami.esteri.it", headers=headers)
        time.sleep(3)
        print(f"Url: {first.url}")
        
        # Realizar o login
        #response = session.post(login_url, data=login_payload, headers=headers)
        response = session.post(login_url, data=login_payload, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"URL após login: {response.url}")
        print(f"Resposta: {response.text[:500]}")  # Exibe os primeiros 500 caracteres da resposta
        time.sleep(3)

        # Verificar se o login foi bem-sucedido
        if response.ok:
            print("Login realizado com sucesso!")
            print(f"Url acessada: {response.url}")
        else:
            print("Erro ao realizar login.")
            exit()

        verificar_agendamento(session)

def main2():
    # Configuração
    base_url = "https://prenotami.esteri.it"
    login_url = f"{base_url}/Home/Login"  # Construir a URL completa do endpoint de login
    payload = {
        "login-email": "bianor.araujo@gmail.com",  # Substitua pelo email
        "login-password": "PrenotamiGu@01",          # Substitua pela senha
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Origin": "https://prenotami.esteri.it",
    }

    # Iniciar a sessão
    with requests.Session() as session:
        try:
            first = session.get(base_url, headers=headers)
            time.sleep(3)
            print(f"Url: {first.url}")
            
            # Fazer a requisição POST para o endpoint de login
            response = session.post(login_url, data=payload, headers=headers, timeout=10)
            
            # Verificar o status da resposta
            if response.status_code == 200:
                print("Login realizado com sucesso!")
            else:
                print(f"Falha ao realizar login. Status Code: {response.status_code}")
            
            # Testar acesso a uma página protegida após login
            protected_page = f"{base_url}/pagina-protegida"  # Substitua por uma URL válida
            protected_response = session.get(protected_page)

            # Verificar se o login persistiu
            if protected_response.url == protected_page:
                print(f"Acesso à página protegida realizado com sucesso: {protected_response.url}")
            else:
                print(f"Redirecionado para outra página: {protected_response.url}")
        except requests.exceptions.RequestException as e:
            print(f"Erro durante a requisição: {e}")

# Executar o programa
if __name__ == "__main__":
    main2()