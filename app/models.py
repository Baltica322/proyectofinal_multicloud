from django.db import models
from django.contrib.auth.models import User

# Tablas auxiliares
class Usuario(models.Model):
    nombre=models.CharField(max_length=20)
    correo=models.EmailField()
    contraseña=models.CharField(max_length=20)

class Socket(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return self.nombre

class TipoRAM(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.nombre}"

class FormatoPlacaMadre(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return self.nombre

class TipoPuerto(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return self.nombre

class TipoConectorAlmacenamiento(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return self.nombre

class Certificacion_Fuente(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return self.nombre

class Gabinete(models.Model):
    fabricante = models.CharField(max_length=20, null=True, blank=True)
    modelo = models.CharField(max_length=20,null=True, blank=True)
    vidrio = models.CharField(max_length=20)
    formatos_compatibles = models.ManyToManyField(FormatoPlacaMadre)
    stock = models.IntegerField(null=True, blank=True)
    precio = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.fabricante} {self.modelo}"

class Procesador(models.Model):
    fabricante = models.CharField(max_length=8, null=True, blank=True)
    modelo = models.CharField(max_length=20,null=True, blank=True)
    frecuencia = models.CharField(max_length=20)
    nucleos = models.IntegerField()
    hilos = models.IntegerField()
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE)
    stock = models.IntegerField(null=True, blank=True)
    precio = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.fabricante} {self.modelo}"
    

class Ram(models.Model):
    fabricante = models.CharField(max_length=20, null=True, blank=True)
    modelo = models.CharField(max_length=20,null=True, blank=True)
    frecuencia = models.CharField(max_length=20)
    capacidad = models.CharField(max_length=10)
    tipo_ram = models.ForeignKey(TipoRAM, on_delete=models.CASCADE)
    stock = models.IntegerField(null=True, blank=True)
    precio = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.fabricante} {self.modelo}"

class PlacaMadre(models.Model):
    fabricante = models.CharField(max_length=20, null=True, blank=True)
    modelo = models.CharField(max_length=20,null=True, blank=True)
    formato = models.ForeignKey(FormatoPlacaMadre, on_delete=models.CASCADE,null=True, blank=True)
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE,null=True, blank=True)
    slots_ram = models.IntegerField(null=True, blank=True)
    tipos_ram_compatibles = models.ManyToManyField(TipoRAM)
    conectores_almacenamiento = models.ManyToManyField(TipoConectorAlmacenamiento)
    puerto_gpu = models.ForeignKey(TipoPuerto, on_delete=models.CASCADE,null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    precio = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.fabricante} {self.modelo} {self.tipos_ram_compatibles}"

class Almacenamiento(models.Model):
    fabricante = models.CharField(max_length=20, null=True, blank=True)
    modelo = models.CharField(max_length=20,null=True, blank=True)
    tipo_almacenamiento = models.CharField(max_length=20)
    capacidad = models.CharField(max_length=20)
    conector = models.ForeignKey(TipoConectorAlmacenamiento, on_delete=models.CASCADE)
    velocidad_lectura = models.CharField(max_length=20)
    stock = models.IntegerField(null=True, blank=True)
    precio = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.fabricante} {self.modelo}"

class TarjetaGrafica(models.Model):
    fabricante = models.CharField(max_length=20, null=True, blank=True)
    modelo = models.CharField(max_length=20,null=True, blank=True)
    vram = models.CharField(max_length=20)
    puerto_requerido = models.ForeignKey(TipoPuerto, on_delete=models.CASCADE)
    stock = models.IntegerField(null=True, blank=True)
    precio = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"{self.fabricante} {self.modelo}"

class FuentePoder(models.Model):
    fabricante = models.CharField(max_length=20, null=True, blank=True)
    modelo = models.CharField(max_length=20,null=True, blank=True)
    potencia = models.CharField(max_length=20)
    tamano = models.CharField(max_length=20)
    certificacion = models.ForeignKey(Certificacion_Fuente, on_delete=models.CASCADE)
    stock = models.IntegerField(null=True, blank=True)
    precio = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.fabricante} {self.modelo}"

class CompatibilidadGPUFuente(models.Model):
    tarjeta_grafica = models.ForeignKey(TarjetaGrafica, on_delete=models.CASCADE)
    fuente_poder = models.ForeignKey(FuentePoder, on_delete=models.CASCADE)

class Cooler(models.Model):
    fabricante = models.CharField(max_length=20, null=True, blank=True)
    modelo = models.CharField(max_length=20,null=True, blank=True)
    dimensiones = models.CharField(max_length=20)
    sockets_compatibles = models.ManyToManyField(Socket)
    stock = models.IntegerField(null=True, blank=True)
    precio = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.fabricante} {self.modelo}"

class Cotizacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=50, help_text="Nombre para identificar esta cotización")
    fecha = models.DateTimeField(auto_now_add=True)

    procesador = models.ForeignKey(Procesador, on_delete=models.SET_NULL, null=True, blank=True)
    placa_madre = models.ForeignKey(PlacaMadre, on_delete=models.SET_NULL, null=True, blank=True)
    ram = models.ForeignKey(Ram, on_delete=models.SET_NULL, null=True, blank=True)
    tarjeta_grafica = models.ForeignKey(TarjetaGrafica, on_delete=models.SET_NULL, null=True, blank=True)
    almacenamiento = models.ForeignKey(Almacenamiento, on_delete=models.SET_NULL, null=True, blank=True)
    fuente_poder = models.ForeignKey(FuentePoder, on_delete=models.SET_NULL, null=True, blank=True)
    gabinete = models.ForeignKey(Gabinete, on_delete=models.SET_NULL, null=True, blank=True)
    cooler = models.ForeignKey(Cooler, on_delete=models.SET_NULL, null=True, blank=True)

    
    def __str__(self):
        return f'Cotización #{self.id} - {self.usuario.username}'

    # Opcional: total calculado
    def calcular_precio_total(self):
        componentes = [
            self.procesador,
            self.placa_madre,
            self.ram,
            self.tarjeta_grafica,
            self.almacenamiento,
            self.fuente_poder,
            self.gabinete,
            self.cooler,
        ]
        return sum(c.precio for c in componentes if c and c.precio)

    def __str__(self):
        return f"Cotización de {self.usuario.first_name} {self.usuario.last_name}"





    