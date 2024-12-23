from fasthtml import common as fh
from database.connection import init_db

app, rt = fh.fast_app(before=fh.Beforeware(init_db), live=True)

page_title = "Cleanto"

def render_content(page_title:str, content):
    return fh.Titled(page_title, 
        fh.Div(content, id="content", cls="bg-gray-200",)
    )

@rt("/")
def home():
    page_content = fh.Div(
        fh.Div(
            fh.H2("Bem-vindo ao meu Website!", cls="text-xl font-bold text-blue-800"),
            fh.P("Este é um exemplo de aplicação web utilizando o FastHTML.", cls="text-sm text-gray-600 mt-1"),
            fh.P("Acesse o menu para navegar pelas páginas.", cls="row-start-2 text-sm text-gray-600 mt-1"),
            cls="bg-gray-100 p-6"
        ),
        fh.Div(
            fh.Button(
                "action_text",
                cls="px-4 py-2 bg-green-400 text-white rounded hover:bg-blue-500 transition-colors"
            ),
            cls="bg-gray-100 p-6"
        )
    )
    return render_content(page_title, page_content)


fh.serve()