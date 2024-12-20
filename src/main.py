from fasthtml.common import *
from database.connection import  init_db

app, rt = fast_app(before=Beforeware(init_db))

@rt("/")
def get():
    return Titled("Website do Cleo",
        Div("Hello, World!", id="greeting"),
        Button("Change Greeting", 
               hx_post="/change-greeting", 
               hx_target="#greeting")
    )

@rt("/change-greeting")
def post():
    return Div("Hello, FastHTML!", id="greeting")

serve(reload=True)