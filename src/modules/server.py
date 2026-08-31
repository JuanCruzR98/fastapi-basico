from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from src.routes import auth
import os

class Server:

    
    def __init__(self):
        self.app = FastAPI()
        self._middlewares()
        self._routes()
         
    def _middlewares(self):
        self.app.add_middleware(
            CORSMiddleware,allow_origins=["*","https://7blpkhfj-8000.use.devtunnels.ms","https://www.thunderclient.com"],allow_methods=["*"],allow_headers=["*"]
        )
        self.app.mount("/public",StaticFiles(directory="public"),name="public")
    
    
    def _routes(self):
        @self.app.exception_handler(404)
        async def not_found_handler(request: Request, exc):
            # Si la ruta es de API → JSON
            if request.url.path.startswith("/api"):
                return JSONResponse(
                    status_code=404,
                    content={
                        "error": "Not Found",
                        "status": 404,
                        "message": f"El servicio que responde al endpoint {request.url.path} no existe o se encuentra en construccion"
                    }
                )
        self.app.include_router(auth.router,prefix="/api")
        
        html_404 = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>404 - Página no encontrada</title>
        </head>
        <body>
            <h1>404 - Página no encontrada</h1>
            <p>La página que buscas no existe.</p>
            <a href="javascript:history.back()">Volver a la anterior</a>
        </body>
        </html>
        """
        @self.app.get("/",response_class=HTMLResponse)
        async def read_root(request:Request):
            return FileResponse(os.path.join("public", "index.html")) 
        
        @self.app.get("/{pagina}",response_class=HTMLResponse)
        async def read_root(request:Request,pagina:str):
            file_path = os.path.join("public", f"{pagina}.html")
            if os.path.exists(file_path):
                return FileResponse(file_path)
            return HTMLResponse(content=html_404,status_code=404)   
    
    def get_app(self):
        return self.app