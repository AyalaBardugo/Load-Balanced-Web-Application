"""Application route handlers"""
from flask import request, make_response, jsonify, Response
from datetime import datetime, timedelta, timezone
import socket
from database import Database
import logging 

class RouteManager:
    """Handle application routes and requests"""
    
    def __init__(self, app) -> None:
        """Initialize route manager
        Args:
            app: Flask application instance
        """
        self.app = app
        self.db = Database()
        self.setup_routes()

    def setup_routes(self) -> None:
        """Configure application routes"""
        @self.app.route('/')
        def home():
            return self.handle_home()

        @self.app.route('/showcount')
        def show_count():
            return self.handle_show_count()

    def get_current_counter(self) -> int:
        """Get current counter value
        Returns:
            int: Current counter value or -1 on error
        """
        try:
            result = self.db.fetch_query("SELECT counter_value FROM global_counter")
            return result[0]['counter_value']
        except Exception as e:
            logging.error(f"Error fetching counter: {e}")
            return -1

    def increment_counter(self) -> int:
        """Increment global counter by 1
        Returns:
            int: New counter value or -1 on error
        """
        try:
            self.db.execute_query(
                "UPDATE global_counter SET counter_value = counter_value + 1"
            )
            return self.get_current_counter()
        except Exception as e:
            logging.error(f"Error updating counter: {e}")
            return -1

    def log_access(self, client_ip: str, internal_ip: str, access_time: datetime) -> None:
        """Log access details to database
        Args:
            client_ip: Client IP address
            internal_ip: Server internal IP
            access_time: Access timestamp
        """
        try:
            self.db.execute_query(
                """INSERT INTO access_log 
                (client_ip, internal_ip, access_time) 
                VALUES (%s, %s, %s)""",
                (client_ip, internal_ip, access_time)
            )
        except Exception as e:
            logging.error(f"Error logging access: {e}")

    def create_sticky_cookie(self, response, internal_ip: str) -> None:
        """Add sticky session cookie to response"""
        expires = datetime.now(timezone.utc) + timedelta(minutes=5)
        expires_str = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
        cookie_value = f'server_ip={internal_ip}; Expires={expires_str}; Path=/; HttpOnly'
        
        logging.info(f"Setting new cookie: {cookie_value}")
        logging.info(f"Cookie expiration time: {expires_str}")
        
        response.headers['Set-Cookie'] = cookie_value


    def create_response_with_cookie(self, internal_ip: str) -> Response:
        """Create response with sticky session cookie if needed"""
        # internal_ip = socket.gethostbyname(socket.gethostname())
        response = make_response(f"Server Internal IP: {internal_ip}")
        
        logging.info(f"Request cookies: {request.cookies}")
        logging.info(f"Current container IP: {internal_ip}")
        
        if 'server_ip' not in request.cookies:
            logging.info("No existing cookie found - creating new cookie")
            self.create_sticky_cookie(response, internal_ip)
        else:
            logging.info(f"Existing cookie found - server_ip: {request.cookies.get('server_ip')}")
            
        return response

    def handle_home(self) -> Response:
        """Handle root path '/'"""
        client_ip = request.remote_addr
        internal_ip = socket.gethostbyname(socket.gethostname())
        current_time = datetime.now(timezone.utc)
        
        logging.info("=== New Request ===")
        logging.info(f"Time: {current_time}")
        logging.info(f"Client IP: {client_ip}")
        logging.info(f"Container Internal IP: {internal_ip}")
        logging.info(f"Request Headers: {dict(request.headers)}")

        self.increment_counter()
        self.log_access(client_ip, internal_ip, current_time)
        return self.create_response_with_cookie(internal_ip)


    def handle_show_count(self)-> Response:
        """Handle '/showcount' path
        Returns:
            Response: JSON with current counter value
        """
        current_counter = self.get_current_counter()
        return jsonify({"global_counter": current_counter})