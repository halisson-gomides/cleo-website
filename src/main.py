from fasthtml import common as fh
from database.connection import init_db

page_title="CAT Serviços de Energia Solar"

def inject_title(req, sess):
    req.injects = [fh.Title(page_title), *req.injects]

app, rt = fh.fast_app(
    before=[fh.Beforeware(init_db), inject_title], 
    static_path="src/static",
    hdrs=(
        # Add Tailwind CSS
        fh.Script(src="https://cdn.tailwindcss.com"),
    ),        
    live=True)


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
                            fh.Input(type='text', cls='w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500')
                        ),
                        fh.Div(
                            fh.Label('Telefone', cls='block text-gray-50 mb-2'),
                            fh.Input(type='tel', pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}", cls='w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500', placeholder='(XX) XXXX-XXXX')
                        ),
                        fh.Div(
                            fh.Label('E-mail', cls='block text-gray-50 mb-2'),
                            fh.Input(type='email', cls='w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500')
                        ),
                        fh.Div(
                            fh.Label('Mensagem', cls='block text-gray-50 mb-2'),
                            fh.Textarea(rows='4', cls='w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500')
                        ),
                        fh.Button('Enviar Mensagem', cls='w-full border-0 bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700'),
                        cls='space-y-6'
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


fh.serve()