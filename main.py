from fasthtml import common as fh
from src.database.connection import init_db, get_session
from dataclasses import dataclass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


page_title="CAT Serviços de Energia Solar"

def inject_title(req, sess):
    req.injects = [fh.Title(page_title), *req.injects]

app, rt = fh.fast_app(
    before=[fh.Beforeware(init_db), inject_title], 
    static_path="src/static",
    hdrs=(
        # Add Tailwind CSS
        fh.Script(src="https://cdn.tailwindcss.com"),
        fh.Link(rel="icon", type="assets/x-icon", href="img/favicon.png"),                
    ),        
    live=True)

@dataclass
class Message:
    name: str
    phone: str
    email: str
    text: str


def validate_form(message: Message):
    import re
    pattern = r"^\(\d{2}\) 9\d{4}-\d{4}$"
    errors = []
    if len(message.name) < 3:
        errors.append("O nome deve conter ao menos 3 caracteres")
    if not re.match(pattern, message.phone):     
        errors.append("Número de telefone inválido")
    if '@' not in message.email:
        errors.append("Endereço de e-mail inválido")
    if len(message.text) < 10:
        errors.append("Escreva uma mensagem com ao menos 10 caracteres")
    return errors


async def add_message(message: Message):
    from src.database.models import Cliente  
    from sqlalchemy.exc import SQLAlchemyError

    # Usar async with para gerenciar o contexto da sessão
    async with get_session() as db_session:    
        try:        
            # Adicionar objeto
            new_message = Cliente(
                name=message.name, 
                phone=message.phone, 
                email=message.email, 
                message=message.text, 
                gender_id=1
            )
            db_session.add(new_message)
            await db_session.commit()
            return True
        except SQLAlchemyError as e:
            await db_session.rollback()
            print(f"Error: {e}")
            return False


def send_email(message: Message):
    # Configuração do servidor de e-mail
    smtp_server = os.getenv("MAIL_SERVER")
    smtp_port = os.getenv("MAIL_PORT")    
    smtp_user = os.getenv("MAIL_USERNAME")
    smtp_pass = os.getenv("MAIL_PASSWORD")
    sender_email = os.getenv("MAIL_FROM")
    receiver_email = os.getenv("MAIL_TO")

    mail_message = MIMEMultipart("alternative")
    mail_message["Subject"] = f"Nova mensagem - {page_title}"
    mail_message["From"] = sender_email
    mail_message["To"] = receiver_email

    mail_body = f"""\
    <html>
    <body>
        <div style="font-family: Arial, sans-serif; padding: 2rem; border-radius: 0.375rem; background-color: #374151; max-width: 32rem; margin: 0 auto;">
            <h2 style="color: #e4e8f0; text-align:center; font-weight:700;">Nova mensagem</h2>
            <p style="color: #e4e8f0;"><b>Nome</b>:</p>
          	<div style="font-family: Arial, sans-serif; color: #646b79; padding: 1rem; border-radius: 0.375rem; background-color: #e4e8f0; max-width: 32rem; margin: 0 auto">
              {message.name}
          </div>
            <p style="color: #e4e8f0;"><b>Telefone</b>:</p>
          <div style="font-family: Arial, sans-serif; color: #646b79; padding: 1rem; border-radius: 0.375rem; background-color: #e4e8f0; max-width: 32rem; margin: 0 auto">
              {message.phone}
          </div>
            <p style="color: #e4e8f0;"><b>E-mail</b>:</p>
          <div style="font-family: Arial, sans-serif; color: #646b79; padding: 1rem; border-radius: 0.375rem; background-color: #e4e8f0; max-width: 32rem; margin: 0 auto">
              {message.email}
          </div>
            <p style="color: #e4e8f0;"><b>Mensagem</b>:</p>
          <div style="font-family: Arial, sans-serif; color: #646b79; padding: 2rem; border-radius: 0.375rem; background-color: #e4e8f0; max-width: 32rem; margin: 0 auto">
              {message.text}
          </div>
        </div>
    </body>
    </html>
    """
    part = MIMEText(mail_body, "html")
    mail_message.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        try:
            # server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.ehlo()
            # server.esmtp_features['auth'] = 'LOGIN DIGEST-MD5 PLAIN'            
            server.login(smtp_user, smtp_pass)
            server.sendmail(
                sender_email, receiver_email, mail_message.as_string()
            )
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            return False
    return True


@rt("/")
def home():   
   return fh.Div(        
        fh.Section(
            fh.Nav(
                fh.Div(
                    fh.Div('CAT SERVIÇOS DE ENERGIA SOLAR', cls='text-2xl font-bold text-gray-700 pr-20'),
                    fh.Div(
                        fh.A('Serviços', href='#servicos', cls='text-gray-600 font-medium hover:underline'),                        
                        fh.A('Sobre', href='#sobre', cls='text-gray-600 font-medium hover:underline'),
                        fh.A('Contato', href='#contato', cls='text-gray-600 font-medium hover:underline'),
                        cls='hidden md:flex space-x-8'
                    ),
                    cls='flex items-center justify-between'
                ),
                cls='container mx-auto px-6 py-4'
            ),
            cls='bg-white shadow'
        ),
        fh.Section(
            fh.Div(
                fh.Div(
                    fh.H1('Soluções em Energia Solar', cls='text-5xl font-bold mb-6 text-slate-50'),
                    fh.P('Transforme sua empresa ou residência com energia limpa e sustentável. Reduza custos e contribua para um futuro melhor.', cls='text-xl mb-8 text-slate-50'),
                    fh.A('Solicitar Orçamento', href='#contato', cls='bg-green-600 text-white px-8 py-4 rounded-lg font-semibold hover:bg-green-700'),
                    cls='max-w-3xl'
                ),
                cls='container mx-auto px-6 py-24'
            ),
            cls='bg-slate-700'
        ),
        fh.Section(
            fh.Div(
                fh.H2('Nossos Serviços', cls='text-3xl font-bold text-center mb-16'),
                fh.Div(
                    fh.Div(
                        fh.Div(
                            fh.Img(src='img/solar_system_installation.jpg', alt='Instalação', cls='w-32 h-32 object-cover rounded-full mx-auto mb-6'),
                            cls='bg-blue-100 rounded-full w-32 h-32 flex items-center justify-center mx-auto mb-6'
                        ),
                        fh.H3('Instalação de Painéis', cls='text-xl font-semibold mb-4'),
                        fh.P('Projeto e instalação completa de sistemas fotovoltaicos para sua empresa ou residência', cls='text-gray-600'),
                        cls='text-center'
                    ),
                    fh.Div(
                        fh.Div(
                            fh.Img(src='img/solar_system_maintenance.jpg', alt='Manutenção', cls='w-32 h-32 object-cover rounded-full mx-auto mb-6'),
                            cls='bg-blue-100 rounded-full w-32 h-32 flex items-center justify-center mx-auto mb-6'
                        ),
                        fh.H3('Manutenção', cls='text-xl font-semibold mb-4'),
                        fh.P('Serviços de manutenção preventiva e corretiva para seu sistema solar', cls='text-gray-600'),
                        cls='text-center'
                    ),
                    fh.Div(
                        fh.Div(
                             fh.Img(src='img/solar_system_consultant.jpg', alt='Instalação', cls='w-32 h-32 object-cover rounded-full mx-auto mb-6'),
                            cls='bg-blue-100 rounded-full w-32 h-32 flex items-center justify-center mx-auto mb-6'
                        ),
                        fh.H3('Consultoria', cls='text-xl font-semibold mb-4'),
                        fh.P('Análise de viabilidade e dimensionamento do seu projeto solar', cls='text-gray-600'),
                        cls='text-center'
                    ),
                    cls='grid md:grid-cols-3 gap-12'
                ),
                cls='container mx-auto px-6'
            ),
            id='servicos',
            cls='py-20'
        ),
        fh.Section(
            fh.Div(                
                fh.Div(
                    fh.Div(
                        fh.Img(src='img/solar_system_who.jpg', alt='Blog Post', cls='w-full h-48 object-cover'),
                        fh.Div(
                            fh.H3('Quem Somos', cls='text-xl font-semibold mb-4'),
                            fh.P('Somos uma empresa especializada em vendas e instalações de sistema de energia solar fotovoltaico, \
                                em residências, empresas, industrias e agronegócios há mais de 5 anos em Brasília-DF e Entorno-GO, \
                                entregando soluções que atendem as necessidades de cada cliente, com eficiência, trazendo-lhes \
                                resultados com economia e sustentabilidade preservando a natureza com geração de energia limpa.', cls='text-gray-600 mb-4'),
                            
                            cls='p-6'
                        ),
                        cls='bg-slate-200 rounded-lg overflow-hidden shadow'
                    ),
                    fh.Div(
                        fh.Img(src='img/solar_system_porfolio.jpg', alt='Blog Post', cls='w-full h-48 object-cover'),
                        fh.Div(
                            fh.H3('Portfolio', cls='text-xl font-semibold mb-4'),
                            fh.P('Com um know-how de mais de 300 instalações de Sistema de Energia Fotovoltaico em Brasília-DF e Entorno-GO, \
                                utilizando os melhores produtos do mercado, painéis, inversores e outros componentes, escolhidos com rigor para \
                                assegurar o melhor desempenho,  garantindo eficiência e durabilidade', cls='text-gray-600 mb-4'),                            
                            cls='p-6'
                        ),
                        cls='bg-slate-200 rounded-lg overflow-hidden shadow'
                    ),                    
                    cls='grid md:grid-cols-2 lg:grid-cols-2 gap-8'
                ),
                cls='container mx-auto px-6'
            ),
            id='sobre',
            cls='bg-gray-100 py-20'
        ),
        fh.Section(
            fh.Div(
                fh.Div(
                    fh.H2('Entre em Contato', cls='text-3xl text-gray-50 font-bold text-center mb-8'),
                    fh.Form(
                        fh.Div(
                            fh.Label('Nome', cls='block text-gray-50 mb-2'),
                            fh.Input(type='text', name="name", maxlength="120", required=True, cls='w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500', placeholder='Nome completo')
                        ),
                        fh.Div(
                            fh.Label('Telefone', cls='block text-gray-50 mb-2'),
                            fh.Input(type='tel', name="phone", maxlength="15", required=True, cls='w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500', placeholder='(XX) XXXXX-XXXX')
                        ),
                        fh.Div(
                            fh.Label('E-mail', cls='block text-gray-50 mb-2'),
                            fh.Input(type='email', name="email", maxlength="120", required=True, cls='w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500', placeholder='E-mail válido')
                        ),
                        fh.Div(
                            fh.Label('Mensagem', cls='block text-gray-50 mb-2'),
                            fh.Textarea(rows='4', name="text", maxlength="300", required=True, cls='w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500', placeholder='Escreva sua mensagem...')
                        ),
                        fh.Button('Enviar Mensagem', id="submit_button", type="submit", cls='w-full border-0 bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700'),
                        fh.Div('Enviando...', aria_busy="true", cls="blinking htmx-indicator text-white font-bold justify-self-center", id="indicador"),
                        fh.Div(id='result', cls='hidden'),
                        cls='space-y-6',
                        method="post",
                        hx_post="/submit-message",
                        hx_disabled_elt="#submit_button", # Disable button on submit
                        hx_indicator="#indicador", # Show loading indicator                        
                        hx_on__before_request="document.getElementById('result').style.visibility = 'hidden';", # Reset form after submit                        
                        hx_target="#result",
                        hx_swap="outerHTML", # replace the entire content of the target element                                
                    ),
                    cls='max-w-lg mx-auto rounded-md p-8 bg-slate-600'
                ),                
                cls='container mx-auto px-6'
            ),
            id='contato',
            cls='py-20'
        ),
        fh.Footer(
            fh.Div(
                fh.Div(
                    fh.Div(
                        fh.H3('CT representações – Cleanto Antunes Teixeira', cls='text-xl text-gray-500 font-semibold mb-4'),
                        fh.P('Soluções profissionais em energia solar para sua empresa ou residência.', cls='text-gray-400')
                    ),
                    fh.Div(
                        fh.H3('Contato', cls='text-xl font-semibold mb-4 text-gray-500'),
                        fh.P('E-mail: cleantoat@terra.com.br', cls='text-gray-400'),
                        fh.P('Tel: (61) 98154-8307', cls='text-gray-400')
                    ),
                    fh.Div(
                        fh.H3('Endereço', cls='text-xl font-semibold mb-4 text-gray-500'),
                        fh.P('SHA CONJ. 06 CHCACARA 28 LOTE 11', cls='text-gray-400')
                    ),
                    cls='grid md:grid-cols-3 gap-8'
                ),
                cls='container mx-auto px-6'
            ),
            cls='bg-gray-800 text-white py-12'
        ),
        cls='bg-gray-50'
    )


@rt("/submit-message", methods=["POST"])
async def post(message:Message):
    errors = validate_form(message)
    if errors:
        return fh.Div(fh.H3("Erros encontrados:", cls="text-red-700 font-bold text-lg px-8"),
                      fh.Ul(*[fh.Li(error, cls="text-red-700") for error in errors], cls="px-8"),                       
                      id="result", 
                      hx_disabled_elt="this",
                      cls="bg-red-100 border border-red-400 text-red-700 p-4 rounded relative w-full")
        
    # Insert into database
    if send_email(message):
        await add_message(message)
        return fh.Div("Mensagem enviada com sucesso!", 
                      id="result",
                      hx_disabled_elt="this",
                      cls="bg-green-100 border border-green-400 text-green-700 p-4 rounded relative font-bold text-center w-full")
    else:
        return fh.Div("Erro ao enviar mensagem. Tente novamente mais tarde.",                      
                      id="result", 
                      hx_disabled_elt="this",
                      cls="bg-red-100 border border-red-400 text-red-700 p-4 rounded relative font-bold text-center w-full")


fh.serve()