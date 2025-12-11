from django.shortcuts import redirect

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_urls = [
            '/login/',
            '/static/',
            '/media/',
            '/admin/',
            '/crearUsuario/',

         
        ]

        is_root = request.path == '/'

        print("=== MIDDLEWARE DEBUG ===")
        print(f"Path: {request.path}")
        print(f"Session usuario_id: {request.session.get('usuario_id')}")

        is_public = any(request.path.startswith(url) for url in public_urls) or is_root
        print(f"Is public: {is_public}")

        if not request.session.get('usuario_id') and not is_public:
            print("REDIRIGIENDO A LOGIN...")
            return redirect('login')  # O usa redirect('login') si tienes URL nombrada

        print("PERMITIENDO ACCESO...")
        return self.get_response(request)
