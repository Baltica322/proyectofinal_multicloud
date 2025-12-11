from django.contrib import admin

from app.models import (
    Usuario, Gabinete, Procesador, Ram, PlacaMadre, Almacenamiento,
    TarjetaGrafica, FuentePoder, Cooler,
    Socket, TipoRAM, FormatoPlacaMadre, TipoPuerto,
    TipoConectorAlmacenamiento, Certificacion_Fuente,
    CompatibilidadGPUFuente,Cotizacion
)
# Admins principales
class GabineteAdmin(admin.ModelAdmin):
    list_display = ["fabricante", "modelo", "vidrio","mostrar_formatos_compatibles", "stock", "precio"]
    filter_horizontal = ["formatos_compatibles"]
    def mostrar_formatos_compatibles(self, obj):
            return ", ".join([formato.nombre for formato in obj.formatos_compatibles.all()])
        
    mostrar_formatos_compatibles.short_description = "Formatos Compatibles"
    
class ProcesadorAdmin(admin.ModelAdmin):
    list_display = ["fabricante", "modelo", "frecuencia", "nucleos", "hilos", "socket", "stock", "precio"]

class RamAdmin(admin.ModelAdmin):
    list_display = ["fabricante", "modelo", "frecuencia", "capacidad", "tipo_ram", "stock", "precio"]

class PlacaMadreAdmin(admin.ModelAdmin):
    list_display = ["fabricante", "modelo", "formato", "socket", "slots_ram", "puerto_gpu", "stock", "precio"]
    filter_horizontal = ["tipos_ram_compatibles", "conectores_almacenamiento"]

class TarjetaGraficaAdmin(admin.ModelAdmin):
    list_display = ["fabricante", "modelo", "vram", "puerto_requerido", "stock", "precio"]

class FuentePoderAdmin(admin.ModelAdmin):
    list_display = ["fabricante", "modelo", "potencia", "tamano", "certificacion", "stock", "precio"]

class AlmacenamientoAdmin(admin.ModelAdmin):
    list_display = ["fabricante", "modelo", "tipo_almacenamiento", "capacidad", "conector", "velocidad_lectura", "stock", "precio"]

class CoolerAdmin(admin.ModelAdmin):
    list_display = ["fabricante", "modelo", "dimensiones", "stock", "precio"]
    filter_horizontal = ["sockets_compatibles"]
    

# Admins auxiliares (opcional si los quieres mostrar o editar desde el admin)
class CompatibilidadGPUFuenteAdmin(admin.ModelAdmin):
    list_display = ["tarjeta_grafica", "fuente_poder"]

class SocketAdmin(admin.ModelAdmin):
    list_display = ["nombre"]

class TipoRAMAdmin(admin.ModelAdmin):
    list_display = ["nombre"]

class FormatoPlacaMadreAdmin(admin.ModelAdmin):
    list_display = ["nombre"]

class TipoPuertoAdmin(admin.ModelAdmin):
    list_display = ["nombre"]

class TipoConectorAlmacenamientoAdmin(admin.ModelAdmin):
    list_display = ["nombre"]

class CertificacionFuenteAdmin(admin.ModelAdmin):
    list_display = ["nombre"]

class CotizacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha']
    readonly_fields = ['fecha']    

# Registro de modelos
admin.site.register(Gabinete, GabineteAdmin)
admin.site.register(Procesador, ProcesadorAdmin)
admin.site.register(Ram, RamAdmin)
admin.site.register(PlacaMadre, PlacaMadreAdmin)
admin.site.register(TarjetaGrafica, TarjetaGraficaAdmin)
admin.site.register(FuentePoder, FuentePoderAdmin)
admin.site.register(Almacenamiento, AlmacenamientoAdmin)
admin.site.register(Cooler, CoolerAdmin)
admin.site.register(Cotizacion, CotizacionAdmin)

# Registra tablas intermedias y auxiliares
admin.site.register(CompatibilidadGPUFuente, CompatibilidadGPUFuenteAdmin)
admin.site.register(Socket, SocketAdmin)
admin.site.register(TipoRAM, TipoRAMAdmin)
admin.site.register(FormatoPlacaMadre, FormatoPlacaMadreAdmin)
admin.site.register(TipoPuerto, TipoPuertoAdmin)
admin.site.register(TipoConectorAlmacenamiento, TipoConectorAlmacenamientoAdmin)
admin.site.register(Certificacion_Fuente, CertificacionFuenteAdmin)