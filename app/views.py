from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from app.models import Procesador,PlacaMadre,Ram,TarjetaGrafica,Almacenamiento,Gabinete,FuentePoder,Cooler,Cotizacion,Usuario,Socket,FormatoPlacaMadre,TipoRAM,TipoConectorAlmacenamiento,TipoPuerto

def login(request):
    if request.method == "GET":
        tipo = request.session.get("tipo")
        if tipo == "user":
            return render(request, "inicio.html")
        elif tipo == "admin":
            return render(request, "inicio_admin.html")
        else:
            return render(request, "login.html")

    elif request.method == "POST":
        usuarioHTML = request.POST["username"]
        passwordHTML = request.POST["password"]

        user = authenticate(request, username=usuarioHTML, password=passwordHTML)

        if user is not None:
            auth_login(request, user)
            request.session['usuario_id'] = user.id  # 👈 Esto es clave para tu middleware

            if user.is_superuser:
                request.session["tipo"] = "admin"
                return render(request, "inicio_admin.html")
            else:
                request.session["tipo"] = "user"
                return render(request, "inicio.html")
        else:
            return render(request, "login.html", {
                "error": "Usuario y/o contraseña erróneo(s)"
            })




def logout(request):
    request.session.flush()
    return login(request)

def getUsuarios(request):
    tipo = request.session.get("tipo")
    if tipo == "admin":
        usuarios = User.objects.all()
        return render(request, "users/tabla.html", {"listaUsuarios": usuarios})
    else:
        return login(request)


def sobrenosotros(request):

    return render(request, "sobrenosotros.html")


def crearUsuario(request):
    if request.method == "GET":
        return render(request, "users/crear_usuarios.html")

    elif request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        email = request.POST.get("email", "").strip()
        nombre = request.POST.get("nombre", "").strip()
        apellido = request.POST.get("apellido", "").strip()

        # Validaciones
        if not username:
            return render(request, "users/crear_usuarios.html", {"error": "El nombre de usuario es requerido."})

        if User.objects.filter(username=username).exists():
            return render(request, "users/crear_usuarios.html", {"error": "El nombre de usuario ya existe."})

        if not password or len(password) < 8:
            return render(request, "users/crear_usuarios.html", {"error": "La contraseña debe tener al menos 8 dígitos."})

        if not email:
            return render(request, "users/crear_usuarios.html", {"error": "El correo electrónico es requerido."})

        if User.objects.filter(email=email).exists():
            return render(request, "users/crear_usuarios.html", {"error": "El correo electrónico ya se utiliza."})

        if not nombre:
            return render(request, "users/crear_usuarios.html", {"error": "El nombre es requerido."})

        if not apellido:
            return render(request, "users/crear_usuarios.html", {"error": "El apellido es requerido."})

        # Si las validaciones pasan, crear el usuario
        usuario = User.objects.create_user(username=username, password=password, email=email)
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.save()

        return redirect('login')


@login_required
def perfilusuario(request):
    cotizaciones = Cotizacion.objects.filter(usuario=request.user)
    return render(request, "users/perfilusuario.html", {
        "cotizaciones": cotizaciones
    })
    
def customizarpc(request):
    procesadores = Procesador.objects.all()
    placamadre = PlacaMadre.objects.all()
    ram = Ram.objects.all()
    tarjetagrafica = TarjetaGrafica.objects.all()
    almacenamiento = Almacenamiento.objects.all()
    gabinete = Gabinete.objects.all()
    fuentepoder = FuentePoder.objects.all()
    data = {'procesadores': procesadores,'placamadre':placamadre,'ram':ram,'tarjetagrafica':tarjetagrafica,'almacenamiento':almacenamiento,'gabinete':gabinete,'fuentepoder':fuentepoder}
    return render(request, "customizar pc/crear_cotizacion.html", data)

def placas_compatibles(request, procesador_id):
    try:
        procesador = Procesador.objects.get(id=procesador_id)
        placas = PlacaMadre.objects.filter(socket=procesador.socket)

        data = [{
            "id": p.id,
            "fabricante": p.fabricante,
            "modelo": p.modelo
        } for p in placas]

        return JsonResponse(data, safe=False)
    except Procesador.DoesNotExist:
        return JsonResponse([], safe=False)
    
def rams_compatibles(request, placa_id):
    try:
        placa = PlacaMadre.objects.get(id=placa_id)
    except PlacaMadre.DoesNotExist:
        return JsonResponse([], safe=False)

    tipos_ram = placa.tipos_ram_compatibles.all()
    rams = Ram.objects.filter(tipo_ram__in=tipos_ram)

    data = [
        {
            "id": ram.id,
            "fabricante": ram.fabricante,
            "modelo": ram.modelo,
            "tipo_memoria": ram.tipo_ram.nombre,
        }
        for ram in rams
    ]
    return JsonResponse(data, safe=False)

def gpus_compatibles(request, placa_id):
    try:
        placa = PlacaMadre.objects.get(id=placa_id)
    except PlacaMadre.DoesNotExist:
        return JsonResponse([], safe=False)

    if not placa.puerto_gpu:
        return JsonResponse([], safe=False)

    gpus = TarjetaGrafica.objects.filter(puerto_requerido=placa.puerto_gpu)

    data = [
        {
            "id": gpu.id,
            "fabricante": gpu.fabricante,
            "modelo": gpu.modelo,
            "vram": gpu.vram,
        }
        for gpu in gpus
    ]
    return JsonResponse(data, safe=False)

def almacenamientos_compatibles(request, placa_id):
    try:
        placa = PlacaMadre.objects.get(id=placa_id)
    except PlacaMadre.DoesNotExist:
        return JsonResponse([], safe=False)

    conectores = placa.conectores_almacenamiento.all()
    almacenamientos = Almacenamiento.objects.filter(conector__in=conectores)

    data = [
        {
            "id": a.id,
            "fabricante": a.fabricante,
            "modelo": a.modelo,
            "capacidad": a.capacidad,
            "tipo_almacenamiento": a.tipo_almacenamiento,
        }
        for a in almacenamientos
    ]
    return JsonResponse(data, safe=False)

def gabinetes_compatibles(request, placa_id):
    try:
        placa = PlacaMadre.objects.get(id=placa_id)
    except PlacaMadre.DoesNotExist:
        return JsonResponse([], safe=False)

    formato_placa = placa.formato
    if not formato_placa:
        return JsonResponse([], safe=False)

    gabinetes = Gabinete.objects.filter(formatos_compatibles=formato_placa)

    data = [
        {
            "id": g.id,
            "fabricante": g.fabricante,
            "modelo": g.modelo,
            "vidrio": g.vidrio,
        }
        for g in gabinetes
    ]
    return JsonResponse(data, safe=False)

def fuentes_compatibles(request, gpu_id):
    try:
        gpu = TarjetaGrafica.objects.get(id=gpu_id)
    except TarjetaGrafica.DoesNotExist:
        return JsonResponse([], safe=False)

    fuentes = gpu.fuentes_compatibles.all()

    data = [
        {
            "id": fuente.id,
            "fabricante": fuente.fabricante,
            "modelo": fuente.modelo,
            "potencia": fuente.potencia,
            "certificacion": fuente.certificacion.nombre,
        }
        for fuente in fuentes
    ]
    return JsonResponse(data, safe=False)

def coolers_compatibles(request, procesador_id):
    try:
        procesador = Procesador.objects.get(id=procesador_id)
    except Procesador.DoesNotExist:
        return JsonResponse([], safe=False)

    socket_id = procesador.socket.id
    coolers = Cooler.objects.filter(sockets_compatibles=socket_id)

    data = [
        {
            "id": cooler.id,
            "fabricante": cooler.fabricante,
            "modelo": cooler.modelo,
            "dimensiones": cooler.dimensiones,
        }
        for cooler in coolers
    ]
    return JsonResponse(data, safe=False)


def inicio(request):
    return render(request,"inicio.html")


@login_required(login_url='login')
def customizarpc(request):
    if request.method == "POST":
        Cotizacion.objects.create(
            usuario=request.user,
            nombre=request.POST.get("nombre"),  # <- Usa el valor del input
            procesador_id=request.POST.get("cpu"),
            placa_madre_id=request.POST.get("motherboard"),
            ram_id=request.POST.get("ram"),
            tarjeta_grafica_id=request.POST.get("gpu"),
            almacenamiento_id=request.POST.get("storage"),
            fuente_poder_id=request.POST.get("fuente"),
            gabinete_id=request.POST.get("gabinete"),
            cooler_id=request.POST.get("cooler"),
        )
        return redirect("inicio")  # O a donde quieras redirigir

    # Si es GET, muestra los componentes para seleccionar
    procesadores = Procesador.objects.all()
    placamadre = PlacaMadre.objects.all()
    ram = Ram.objects.all()
    tarjetagrafica = TarjetaGrafica.objects.all()
    almacenamiento = Almacenamiento.objects.all()
    gabinete = Gabinete.objects.all()
    fuentepoder = FuentePoder.objects.all()
    coolers = Cooler.objects.all()
    data = {
        'procesadores': procesadores,
        'placamadre': placamadre,
        'ram': ram,
        'gpu': tarjetagrafica,
        'storage': almacenamiento,
        'gabinete': gabinete,
        'fuente': fuentepoder,
        'cooler': coolers
    }
    return render(request, "customizar pc/crear_cotizacion.html", data)


@login_required
def eliminar_cotizacion(request, cotizacion_id):
    if request.method == "POST":
        cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id, usuario=request.user)
        cotizacion.delete()
        return redirect('perfilusuario')
    return redirect('perfilusuario')

def actualizar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk)

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        if not nombre:
            messages.error(request, "El nombre es obligatorio.")
            return redirect("actualizar_cotizacion", pk=pk)
        else:
            cotizacion.nombre = nombre
            cotizacion.procesador = Procesador.objects.filter(id=request.POST.get("procesador")).first()
            cotizacion.placa_madre = PlacaMadre.objects.filter(id=request.POST.get("placas_madre")).first()
            cotizacion.ram = Ram.objects.filter(id=request.POST.get("ram")).first()
            cotizacion.tarjeta_grafica = TarjetaGrafica.objects.filter(id=request.POST.get("gpu")).first()
            cotizacion.almacenamiento = Almacenamiento.objects.filter(id=request.POST.get("storage")).first()
            cotizacion.fuente_poder = FuentePoder.objects.filter(id=request.POST.get("fuente")).first()
            cotizacion.gabinete = Gabinete.objects.filter(id=request.POST.get("gabinete")).first()
            cotizacion.cooler = Cooler.objects.filter(id=request.POST.get("cooler")).first()
            cotizacion.save()
            messages.success(request, "Cotización actualizada correctamente.")
            return redirect("perfilusuario")

    context = {
        "cotizacion": cotizacion,
        "procesadores": Procesador.objects.all(),
        "placas_madre": PlacaMadre.objects.all(),
        "rams": Ram.objects.all(),
        "tarjetas_graficas": TarjetaGrafica.objects.all(),
        "almacenamientos": Almacenamiento.objects.all(),
        "fuentes_poder": FuentePoder.objects.all(),
        "gabinetes": Gabinete.objects.all(),
        "coolers": Cooler.objects.all(),
    }
    return render(request, "customizar pc/actualizar_cotizacion.html", context)
    
def panel_admin(request):
    cotizaciones = Cotizacion.objects.select_related('usuario').all()
    usuarios = User.objects.all()
    return render(request, 'inicio_admin.html', {
        'cotizaciones': cotizaciones,
        'usuarios': usuarios
    })



def ver_cotizaciones_y_usuarios(request):
    cotizaciones = Cotizacion.objects.all()  # O con filtro si estás limitando sin darte cuenta
    usuarios = Usuario.objects.all()  # Asegúrate que trae todos los usuarios

    context = {
        'cotizaciones': cotizaciones,
        'usuarios': usuarios,
    }
    return render(request, 'inicio_admin.html', context)


def procesador_admin(request):
    socket = Socket.objects.all()

    if request.method == "POST":
        # 1. Capturar los datos del formulario
        fabricante = request.POST.get("cpu_fabricante")
        modelo = request.POST.get("cpu_modelo")
        frecuencia = request.POST.get("cpu_frecuencia")
        nucleos = request.POST.get("cpu_nucleos")
        hilos = request.POST.get("cpu_hilos")
        socket_id = request.POST.get("cpu_socket")
        stock = request.POST.get("cpu_stock")
        precio = request.POST.get("cpu_precio")

        # 2. Validar que el socket exista
        try:
            socket_obj = Socket.objects.get(id=socket_id)
        except Socket.DoesNotExist:
            return render(request, "admin/procesador/procesador.html", {
                "socket": socket,
                "procesadores": Procesador.objects.all(),
                "error": "El socket seleccionado no existe."
            })

        # 3. Crear el procesador
        Procesador.objects.create(
            fabricante=fabricante,
            modelo=modelo,
            frecuencia=frecuencia,
            nucleos=nucleos,
            hilos=hilos,
            socket=socket_obj,
            stock=stock,
            precio=precio
        )

        # 4. Redirigir para evitar doble envío
        return redirect("adminprocesador")  # Asegúrate de tener esta URL con ese `name`

    # 5. Mostrar página con sockets y procesadores ya guardados
    return render(request, "admin/procesador/procesador.html", {
        "socket": socket,
        "procesadores": Procesador.objects.all()
    })

def buscar_procesador(request):
    resultados = []
    consulta = request.GET.get('consulta')

    if consulta:
        # Crear un campo concatenado fabricante + " " + modelo
        resultados = Procesador.objects.annotate(
            fabricante_modelo=Concat('fabricante', Value(' '), 'modelo', output_field=CharField())
        ).filter(
            fabricante_modelo__icontains=consulta
        )

    return render(request, 'admin/procesador/buscarprocesador.html', {
        'resultados': resultados,
        'consulta': consulta,
    })

def eliminar_procesador(request):
    resultados = []
    consulta = request.GET.get('consulta')

    if consulta:
        resultados = Procesador.objects.annotate(
            fabricante_modelo=Concat('fabricante', Value(' '), 'modelo', output_field=CharField())
        ).filter(
            fabricante_modelo__icontains=consulta
        )

    return render(request, 'admin/procesador/eliminarprocesador.html', {
        'resultados': resultados,
        'consulta': consulta,
    })
def eliminar_procesador_confirmado(request, pk):
    if request.method == 'POST':
        procesador = get_object_or_404(Procesador, pk=pk)
        procesador.delete()
    return redirect('eliminarprocesador')

def editar_procesador(request):
    consulta = request.GET.get('consulta')
    resultados = []
    sockets = Socket.objects.all()

    if consulta:
        resultados = Procesador.objects.annotate(
            fabricante_modelo=Concat('fabricante', Value(' '), 'modelo', output_field=CharField())
        ).filter(fabricante_modelo__icontains=consulta)

    return render(request, 'admin/procesador/editarprocesador.html', {
        'resultados': resultados,
        'consulta': consulta,
        'sockets': sockets,  # Pasamos los sockets al template
    })

def editarprocesador_confirmado(request, id):
    procesador = get_object_or_404(Procesador, id=id)

    if request.method == 'POST':
        procesador.fabricante = request.POST.get('fabricante')
        procesador.modelo = request.POST.get('modelo')
        procesador.frecuencia = request.POST.get('frecuencia')
        procesador.nucleos = request.POST.get('nucleos')
        procesador.hilos = request.POST.get('hilos')

        # ⚠️ Corregido aquí:
        socket_nombre = request.POST.get('socket')
        socket_instancia = get_object_or_404(Socket, nombre=socket_nombre)
        procesador.socket = socket_instancia

        procesador.stock = request.POST.get('stock')
        procesador.precio = request.POST.get('precio')

        procesador.save()
        # Redirige donde quieras, por ejemplo:
        return redirect('adminprocesador')  

    return render(request, 'admin/procesador/editarprocesador.html', {
        'procesador': procesador,
    })

def placamadre_admin(request):

    return render(request, "admin/placamadre/placamadre.html")



def placamadre_admin(request):
    socket = Socket.objects.all()
    formato = FormatoPlacaMadre.objects.all()
    tiporam = TipoRAM.objects.all()
    tipoconector = TipoConectorAlmacenamiento.objects.all()
    tipopuerto = TipoPuerto.objects.all()

    if request.method == "POST":
        fabricante = request.POST.get("placa_fabricante")
        modelo = request.POST.get("placa_modelo")
        formato_id = request.POST.get("placa_formato")
        socket_id = request.POST.get("placa_socket")
        slots_ram = request.POST.get("placa_slots_ram")
        tipos_ram_ids = request.POST.getlist("placa_tiporam")  # múltiples valores
        conectores_ids = request.POST.getlist("placa_conector")  # múltiples valores
        puerto_gpu_id = request.POST.get("placa_gpu")
        stock = request.POST.get("placa_stock")
        precio = request.POST.get("placa_precio")

        try:
            formato_obj = FormatoPlacaMadre.objects.get(id=formato_id)
            socket_obj = Socket.objects.get(id=socket_id)
            puerto_gpu_obj = TipoPuerto.objects.get(id=puerto_gpu_id)
        except (FormatoPlacaMadre.DoesNotExist, Socket.DoesNotExist, TipoPuerto.DoesNotExist):
            return render(request, "admin/placamadre/placamadre.html", {
                "socket": socket,
                "formato": formato,
                "tiporam": tiporam,
                "tipoconector": tipoconector,
                "tipopuerto": tipopuerto,
                "error": "Alguno de los datos no es válido."
            })

        # Crear la placa madre sin los ManyToMany
        placa = PlacaMadre.objects.create(
            fabricante=fabricante,
            modelo=modelo,
            formato=formato_obj,
            socket=socket_obj,
            slots_ram=slots_ram,
            puerto_gpu=puerto_gpu_obj,
            stock=stock,
            precio=precio
        )

        # Asignar los ManyToMany
        placa.tipos_ram_compatibles.set(tipos_ram_ids)
        placa.conectores_almacenamiento.set(conectores_ids)

        return redirect("adminplacamadre")

    return render(request, "admin/placamadre/placamadre.html", {
        "socket": socket,
        "formato": formato,
        "tiporam": tiporam,
        "tipoconector": tipoconector,
        "tipopuerto": tipopuerto,
    })

def buscar_placamadre(request):
    resultados = []
    consulta = request.GET.get('consulta')

    if consulta:
        # Crear un campo concatenado fabricante + " " + modelo
        resultados = PlacaMadre.objects.annotate(
            fabricante_modelo=Concat('fabricante', Value(' '), 'modelo', output_field=CharField())
        ).filter(
            fabricante_modelo__icontains=consulta
        )

    return render(request, 'admin/placamadre/buscarplacamadre.html', {
        'resultados': resultados,
        'consulta': consulta,
    })

def eliminar_placamadre(request):
    resultados = []
    consulta = request.GET.get('consulta')

    if consulta:
        resultados = PlacaMadre.objects.annotate(
            fabricante_modelo=Concat('fabricante', Value(' '), 'modelo', output_field=CharField())
        ).filter(
            fabricante_modelo__icontains=consulta
        )

    return render(request, 'admin/placamadre/eliminarplacamadre.html', {
        'resultados': resultados,
        'consulta': consulta,
    })

def eliminar_placamadre_confirmado(request, pk):
    if request.method == 'POST':
        placamadre = get_object_or_404(PlacaMadre, pk=pk)
        placamadre.delete()
    return redirect('eliminarplacamadre')

def editar_placamadre(request):
    consulta = request.GET.get('consulta')
    resultados = []

    if consulta:
        resultados = PlacaMadre.objects.annotate(
            fabricante_modelo=Concat('fabricante', Value(' '), 'modelo', output_field=CharField())
        ).filter(
            fabricante_modelo__icontains=consulta
        )

    return render(request, 'admin/placamadre/editarplacamadre.html', {
        'consulta': consulta,
        'resultados': resultados,
        # ✅ Estas listas deben ser pasadas para los <select>
        'formatos': FormatoPlacaMadre.objects.all(),
        'sockets': Socket.objects.all(),
        'tipos_ram': TipoRAM.objects.all(),
        'conectores': TipoConectorAlmacenamiento.objects.all(),
        'puertos': TipoPuerto.objects.all(),
    })
def editarplacamadre_confirmado(request, id):
    placamadre = get_object_or_404(PlacaMadre, id=id)

    if request.method == 'POST':
        placamadre.fabricante = request.POST.get('fabricante')
        placamadre.modelo = request.POST.get('modelo')

        # ForeignKey: Formato
        formato_id = request.POST.get('formato')
        placamadre.formato = get_object_or_404(FormatoPlacaMadre, id=formato_id)

        # ForeignKey: Socket
        socket_id = request.POST.get('socket')
        placamadre.socket = get_object_or_404(Socket, id=socket_id)

        # Campo simple
        placamadre.slots_ram = request.POST.get('slots_ram')

        # ManyToMany: TipoRAM
        tipos_ram_ids = request.POST.getlist('tipos_ram_compatibles')
        placamadre.save()  # Se necesita guardar antes de setear M2M
        placamadre.tipos_ram_compatibles.set(tipos_ram_ids)

        # ManyToMany: Conectores almacenamiento
        conectores_ids = request.POST.getlist('conectores_almacenamiento')
        placamadre.conectores_almacenamiento.set(conectores_ids)

        # ForeignKey: Puerto GPU
        puerto_gpu_id = request.POST.get('puerto_gpu')
        placamadre.puerto_gpu = get_object_or_404(TipoPuerto, id=puerto_gpu_id)

        # Stock y precio
        placamadre.stock = request.POST.get('stock')
        placamadre.precio = request.POST.get('precio')

        placamadre.save()

        return redirect('adminplacamadre')  # Cambia a tu URL destino

    return render(request, 'admin/placamadre/editarplacamadre.html', {
        'placamadre': placamadre,
    })

def tarjeta_grafica_admin(request):
    puerto = TipoPuerto.objects.all()
    tarjetas_graficas = TarjetaGrafica.objects.all()

    if request.method == "POST":
        fabricante = request.POST.get("gpu_fabricante")
        modelo = request.POST.get("gpu_modelo")
        vram = request.POST.get("gpu_vram")
        puerto_id = request.POST.get("gpu_puerto")
        stock = request.POST.get("gpu_stock")
        precio = request.POST.get("gpu_precio")

        try:
            puerto_obj = TipoPuerto.objects.get(id=puerto_id)
        except TipoPuerto.DoesNotExist:
            return render(request, "admin/tarjetagrafica/tarjetagrafica.html", {
                "puerto": puerto,
                "tarjetas_graficas": tarjetas_graficas,
                "error": "El puerto seleccionado no existe."
            })

        TarjetaGrafica.objects.create(
            fabricante=fabricante,
            modelo=modelo,
            vram=vram,
            puerto_requerido=puerto_obj,
            stock=stock,
            precio=precio
        )

        return redirect("admintarjetagrafica")

    return render(request, "admin/tarjetagrafica/tarjetagrafica.html", {
        "puerto": puerto,
        "tarjetas_graficas": tarjetas_graficas
    })

def buscar_tarjetagrafica(request):
    resultados = []
    consulta = request.GET.get('consulta')

    if consulta:
        # Crear un campo concatenado fabricante + " " + modelo
        resultados = TarjetaGrafica.objects.annotate(
            fabricante_modelo=Concat('fabricante', Value(' '), 'modelo', output_field=CharField())
        ).filter(
            fabricante_modelo__icontains=consulta
        )

    return render(request, 'admin/tarjetagrafica/buscartarjetagrafica.html', {
        'resultados': resultados,
        'consulta': consulta,
    })

def editar_tarjetagrafica(request):
    consulta = request.GET.get('consulta')
    resultados = []
    puertos = TipoPuerto.objects.all()

    if consulta:
        resultados = TarjetaGrafica.objects.annotate(
            fabricante_modelo=Concat('fabricante', Value(' '), 'modelo', output_field=CharField())
        ).filter(
            fabricante_modelo__icontains=consulta
        )

    return render(request, 'admin/tarjetagrafica/editartarjetagrafica.html', {
        'resultados': resultados,
        'consulta': consulta,
        'puertos': puertos,  # Pasamos los puertos al template
    })


def editar_tarjetagrafica_confirmado(request, id):
    gpu = get_object_or_404(TarjetaGrafica, id=id)

    if request.method == 'POST':
        gpu.fabricante = request.POST.get('fabricante')
        gpu.modelo = request.POST.get('modelo')
        gpu.vram = request.POST.get('vram')

        # ForeignKey: Puerto requerido
        puerto_id = request.POST.get('puerto')
        gpu.puerto_requerido = get_object_or_404(TipoPuerto, id=puerto_id)

        gpu.stock = request.POST.get('stock')
        gpu.precio = request.POST.get('precio')

        gpu.save()

        return redirect('admintarjetagrafica')  # Cambia al nombre correcto si tu URL es distinta

    return render(request, 'admin/tarjetagrafica/editartarjetagrafica.html', {
        'gpu': gpu,
    })

def eliminar_tarjetagrafica(request):
    resultados = []
    consulta = request.GET.get('consulta')

    if consulta:
        resultados = TarjetaGrafica.objects.annotate(
            fabricante_modelo=Concat('fabricante', Value(' '), 'modelo', output_field=CharField())
        ).filter(
            fabricante_modelo__icontains=consulta
        )

    return render(request, 'admin/tarjetagrafica/eliminartarjetagrafica.html', {
        'resultados': resultados,
        'consulta': consulta,
    })
def eliminar_tarjetagrafica_confirmado(request, pk):
    if request.method == 'POST':
        tarjeta_grafica = get_object_or_404(TarjetaGrafica, pk=pk)
        tarjeta_grafica.delete()
    return redirect('eliminartarjetagrafica')

def gabinete_admin(request):
    formatos = FormatoPlacaMadre.objects.all()

    if request.method == "POST":
        fabricante = request.POST.get("gabinete_fabricante")
        modelo = request.POST.get("gabinete_modelo")
        tipo_vidrio = request.POST.get("gabinete_vidrio")  
        formatos_ids = request.POST.getlist("gabinete_formato")  
        stock = request.POST.get("gabinete_stock")
        precio = request.POST.get("gabinete_precio")

        gabinete = Gabinete.objects.create(
            fabricante=fabricante,
            modelo=modelo,
            vidrio=tipo_vidrio,
            stock=stock,
            precio=precio
        )

        gabinete.formatos_compatibles.set(formatos_ids)  

        return redirect("admingabinete")

    return render(request, "admin/gabinete/gabinete.html", {
        "formato": formatos
    })

def buscar_gabinete(request):
    resultados = []
    consulta = request.GET.get('consulta')

    if consulta:
        # Crear un campo concatenado fabricante + " " + modelo
        resultados = Gabinete.objects.annotate(
            fabricante_modelo=Concat('fabricante', Value(' '), 'modelo', output_field=CharField())
        ).filter(
            fabricante_modelo__icontains=consulta
        )

    return render(request, 'admin/gabinete/buscargabinete.html', {
        'resultados': resultados,
        'consulta': consulta,
    })

def editar_gabinete(request):
    consulta = request.GET.get('consulta')
    resultados = []
    formatos = FormatoPlacaMadre.objects.all()

    if consulta:
        resultados = Gabinete.objects.annotate(
            fabricante_modelo=Concat('fabricante', Value(' '), 'modelo', output_field=CharField())
        ).filter(
            fabricante_modelo__icontains=consulta
        )

    return render(request, 'admin/gabinete/editargabinete.html', {
        'resultados': resultados,
        'consulta': consulta,
        'formatos': formatos,  # Pasamos los formatos al template
    })

def editar_gabinete_confirmado(request, id):
    gabinete = get_object_or_404(Gabinete, id=id)

    if request.method == 'POST':
        gabinete.fabricante = request.POST.get('fabricante')
        gabinete.modelo = request.POST.get('modelo')
        gabinete.vidrio = request.POST.get('vidrio')

        # ManyToMany: Formatos compatibles
        formatos_ids = request.POST.getlist('formatos_compatibles')
        gabinete.save()  # Se necesita guardar antes de setear M2M
        gabinete.formatos_compatibles.set(formatos_ids)

        gabinete.stock = request.POST.get('stock')
        gabinete.precio = request.POST.get('precio')

        gabinete.save()

        return redirect('admingabinete')  # Cambia a tu URL destino

    return render(request, 'admin/gabinete/editargabinete.html', {
        'gabinete': gabinete,
    })

def eliminar_gabinete(request):
    resultados = []
    consulta = request.GET.get('consulta')

    if consulta:
        resultados = Gabinete.objects.annotate(
            fabricante_modelo=Concat('fabricante', Value(' '), 'modelo', output_field=CharField())
        ).filter(
            fabricante_modelo__icontains=consulta
        )

    return render(request, 'admin/gabinete/eliminargabinete.html', {
        'resultados': resultados,
        'consulta': consulta,
    })

def eliminar_gabinete_confirmado(request, pk):
    if request.method == 'POST':
        gabinete = get_object_or_404(Gabinete, pk=pk)
        gabinete.delete()
    return redirect('eliminargabinete')  # Cambia a tu URL destino si es necesario