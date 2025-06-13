from twilio.rest import Client
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
REMETENTE_BUSCA = 'contato@thenewscc.com.br'
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
WHATSAPP_DESTINO = os.getenv('WHATSAPP_DESTINO')


def enviar_whatsapp(mensagem):
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        message = client.messages.create(
            body=mensagem,
            from_='whatsapp:+14155238886',  # Número do sandbox Twilio
            to=WHATSAPP_DESTINO
        )
        print(f'✅ Mensagem enviada com SID: {message.sid}')
    except Exception as e:
        print("❌ Erro ao enviar WhatsApp:", e)


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

        corpo = None
        if msg.is_multipart():
            for parte in msg.walk():
                if parte.get_content_type() == "text/plain":
                    corpo = parte.get_payload(decode=True).decode()
                    break
        else:
            corpo = msg.get_payload(decode=True).decode()

        mail.logout()

        if corpo:
            print("✅ Conteúdo recebido do e-mail:")
            print(corpo[:500])
            enviar_whatsapp(corpo)
        else:
            print("⚠️ E-mail não tinha conteúdo 'text/plain'.")

    except Exception as e:
        print("Erro encontrado: ", e)

# executar o teste

conect_n_read_mail()
