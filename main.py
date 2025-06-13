#from twilio.rest import Client
import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
load_dotenv()
# Configuration

EMAIL_USER = 'ovitormora@gmail.com'
EMAIL_SENHA = os.getenv('EMAIL_SENHA')
IMAP_SERVIDOR = 'imap.gmail.com'
REMETENTE_BUSCA = 'mmartins.vitor2@gmail.com'


def conect_n_read_mail():
    try:
        # conection with IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVIDOR)
        mail.login(EMAIL_USER,EMAIL_SENHA)
        mail.select('inbox')

        # search for sender mails
        status, mensagens = mail.search(None, f'(FROM "{REMETENTE_BUSCA}")')
        email_ids = mensagens[0].split()

        if not email_ids:
            print("Nenhum e-mail encontrado do remetente especificado")
            return
        
        # Get last mail
        ultimo_email_id = email_ids[-1]
        status, dados = mail.fetch(ultimo_email_id, '(RFC822)')

        # content decoder
        raw_email = dados[0][-1]
        msg = email.message_from_bytes(raw_email)

        if msg.is_multipart():
            for parte in msg.walk():
                tipo = parte.get_content_type()
                if tipo == "text/plain":
                    corpo = parte.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()
        
        '''
        # Assunto
        assunto, encoding = decode_header(msg["Subject"])[0]
        if isinstance(assunto, bytes):
            assunto = assunto.decode(encoding if encoding else "utf-8")

        # remetente
        remetente = msg.get("From")

        # corpo do email
        if msg.is_multipart():
            for parte in msg.walk():
                tipo = parte.get_content_type()
                if tipo == "text/plain":
                    corpo = parte.get_payload(decode=True).decode()
                    break

        else:
            corpo = msg.get_payload(decode=True).decode()

        # teste
        print("✅ E-mail encontrado:")
        print("Assunto:", assunto)
        print("Remetente:", remetente)
        print("\nConteúdo:\n", corpo[:500])  # imprime só os 500 primeiros caracteres

        mail.logout()
'''
        mail.logout()
    except Exception as e:
        print("Erro encontrado: ", e)

# executar o teste

conect_n_read_mail()
