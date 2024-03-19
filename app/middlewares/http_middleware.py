from fastapi.datastructures import URL
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time


class HTTP_Middleware(BaseHTTPMiddleware):
    """
    HTTP Middleware to add custom headers to the response
    1. When request from htmx with http header "Hx-Request", then set request.state.hx_request = True
    in order to serve pure html
    otherwise, set request.state.hx_request = False to serve for htmx component ton run
    standalone with another js and css(Layout will handle this)
    2. Put process time information into Header: X-Process-Time
    3. Root Path will be used to serve static files in standalone mode
    """
    def __init__(self, app, root_path:str):
        super().__init__(app)
        self.root_path = root_path
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        if "Hx-Request" in request.headers:
            # add hx_request to state so JINJA2 use this to add css and js files
            request.state.hx_request = True
            current_url = URL(request.headers["Hx-Current-Url"] if "Hx-Current-Url" in request.headers else request.url.path)
            request.state.current_url = current_url.path.replace('//','/')
            request.state.current_query = current_url.query
        else:
            request.state.hx_request = False
            request.state.current_url = request.url.path
        
        # Add current app to state
        request.state.current_app =f"/{request.state.current_url.lstrip('/').split('/')[0]}"
        request.state.current_path = request.state.current_url.replace(request.state.current_app,'')
        # When local dev mode, set this to serve js and other static files
        request.state.root_path=self.root_path
        # Call the next middleware or route handler
        response = await call_next(request)
        # Modify the response headers
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response