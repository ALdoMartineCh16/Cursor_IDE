#!/usr/bin/env python3
"""
Organizador de Archivos Mejorado
Versión 2.0 - Con recursividad, interfaz CLI, notificaciones y modo deshacer

Características:
- Organización recursiva en subdirectorios
- Interfaz de línea de comandos con argparse
- Manejo de archivos duplicados
- Sistema de notificaciones
- Modo deshacer para revertir cambios
- Compatible con Windows, macOS y Linux
"""

import os
import sys
import json
import shutil
import platform
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Configuración de categorías de archivos
CATEGORIAS = {
    "Imagenes": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp", ".svg", ".ico"],
    "Documentos": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
    "Musica": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
    "Archivos_Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Programas": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".app"],
    "Scripts": [".py", ".js", ".html", ".css", ".php", ".sh", ".bat", ".cmd"],
}

class OrganizadorArchivos:
    """Clase principal para organizar archivos por categorías"""

    def __init__(self, carpeta_objetivo: Path, recursivo: bool = True,
                 sobreescribir: bool = False, log_path: Optional[Path] = None):
        self.carpeta_objetivo = carpeta_objetivo
        self.recursivo = recursivo
        self.sobreescribir = sobreescribir
        self.log_path = log_path or (carpeta_objetivo / ".organizador_log.json")
        self.extension_a_categoria = self._crear_mapa_extensiones()
        self.acciones_realizadas = []  # Para el modo deshacer

    def _crear_mapa_extensiones(self) -> Dict[str, str]:
        """Crea un diccionario que mapea extensiones a categorías"""
        mapa = {}
        for categoria, extensiones in CATEGORIAS.items():
            for ext in extensiones:
                mapa[ext.lower()] = categoria
        return mapa

    def _es_carpeta_organizada(self, ruta: Path) -> bool:
        """Verifica si una carpeta parece estar ya organizada (contiene solo archivos organizados)"""
        if not ruta.is_dir():
            return False

        # Si la carpeta tiene el mismo nombre que una categoría, probablemente está organizada
        if ruta.name in CATEGORIAS.keys():
            return True

        # Verificar si contiene principalmente archivos organizados
        archivos = list(ruta.glob("*"))
        if not archivos:
            return False

        # Si contiene carpetas con nombres de categorías, probablemente está organizada
        nombres_carpetas = {f.name for f in archivos if f.is_dir()}
        return bool(nombres_carpetas & set(CATEGORIAS.keys()))

    def _obtener_archivos_a_organizar(self) -> List[Path]:
        """Obtiene la lista de archivos a organizar, evitando carpetas ya organizadas"""
        archivos = []

        if self.recursivo:
            # Buscar archivos recursivamente
            for root, dirs, files in os.walk(self.carpeta_objetivo):
                root_path = Path(root)

                # Saltar carpetas que parecen estar ya organizadas
                dirs[:] = [d for d in dirs if not self._es_carpeta_organizada(root_path / d)]

                for file in files:
                    archivo_path = root_path / file
                    # Solo incluir archivos que no estén ya en carpetas de categorías
                    if not self._esta_en_carpeta_categoria(archivo_path):
                        archivos.append(archivo_path)
        else:
            # Solo archivos en el directorio raíz
            archivos = [f for f in self.carpeta_objetivo.iterdir()
                       if f.is_file() and not self._esta_en_carpeta_categoria(f)]

        return archivos

    def _esta_en_carpeta_categoria(self, archivo: Path) -> bool:
        """Verifica si un archivo ya está en una carpeta de categoría"""
        return archivo.parent.name in CATEGORIAS.keys()

    def _manejar_archivo_duplicado(self, origen: Path, destino: Path) -> Path:
        """Maneja archivos duplicados según la configuración"""
        if not destino.exists():
            return destino

        if self.sobreescribir:
            return destino

        # Generar nombre único
        contador = 1
        stem = destino.stem
        suffix = destino.suffix
        directorio = destino.parent

        while True:
            nuevo_nombre = f"{stem}_{contador}{suffix}"
            nuevo_destino = directorio / nuevo_nombre
            if not nuevo_destino.exists():
                return nuevo_destino
            contador += 1

    def organizar_archivos(self) -> Dict[str, int]:
        """Organiza los archivos por categorías"""
        archivos = self._obtener_archivos_a_organizar()
        estadisticas = {categoria: 0 for categoria in CATEGORIAS.keys()}
        estadisticas["Otros"] = 0

        print(f"Encontrados {len(archivos)} archivos para organizar...")

        for archivo in archivos:
            ext = archivo.suffix.lower()
            categoria = self.extension_a_categoria.get(ext, "Otros")

            # Crear directorio de destino
            destino_dir = self.carpeta_objetivo / categoria
            destino_dir.mkdir(exist_ok=True)

            # Calcular ruta de destino
            destino_archivo = destino_dir / archivo.name
            destino_final = self._manejar_archivo_duplicado(archivo, destino_archivo)

            try:
                # Registrar acción para deshacer
                self.acciones_realizadas.append({
                    "tipo": "mover",
                    "origen": str(archivo),
                    "destino": str(destino_final),
                    "timestamp": datetime.now().isoformat()
                })

                # Mover archivo
                if destino_final != archivo:
                    shutil.move(str(archivo), str(destino_final))

                estadisticas[categoria] += 1
                print(f"✓ Movido: {archivo.name} → {categoria}/")

            except Exception as e:
                print(f"✗ Error moviendo {archivo.name}: {e}")

        # Guardar log de acciones
        self._guardar_log_acciones()

        return estadisticas

    def _guardar_log_acciones(self):
        """Guarda el registro de acciones realizadas para poder deshacer"""
        try:
            with open(self.log_path, 'w', encoding='utf-8') as f:
                json.dump(self.acciones_realizadas, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Advertencia: No se pudo guardar el log de acciones: {e}")

    def deshacer_ultima_organizacion(self) -> bool:
        """Deshace la última organización realizada"""
        if not self.log_path.exists():
            print("No se encontró registro de acciones para deshacer.")
            return False

        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                acciones = json.load(f)
        except Exception as e:
            print(f"Error leyendo el log de acciones: {e}")
            return False

        print("Deshaciendo última organización...")

        for accion in reversed(acciones):
            if accion["tipo"] == "mover":
                try:
                    origen = Path(accion["origen"])
                    destino = Path(accion["destino"])

                    if destino.exists():
                        # Mover de vuelta al lugar original
                        if origen.parent.exists():
                            shutil.move(str(destino), str(origen))
                            print(f"✓ Restaurado: {destino.name} → {origen.parent.name}/")
                        else:
                            # Si el directorio original no existe, restaurar al directorio raíz
                            destino_raiz = self.carpeta_objetivo / destino.name
                            shutil.move(str(destino), str(destino_raiz))
                            print(f"✓ Restaurado: {destino.name} → {self.carpeta_objetivo.name}/")

                except Exception as e:
                    print(f"✗ Error restaurando {destino.name}: {e}")

        # Limpiar carpetas vacías de categorías
        self._limpiar_carpetas_vacias()

        # Eliminar el log después de deshacer
        try:
            self.log_path.unlink()
            print("Registro de acciones eliminado.")
        except:
            pass

        return True

    def _limpiar_carpetas_vacias(self):
        """Elimina carpetas de categorías que estén vacías"""
        for categoria in CATEGORIAS.keys():
            categoria_dir = self.carpeta_objetivo / categoria
            if categoria_dir.exists() and not list(categoria_dir.iterdir()):
                try:
                    categoria_dir.rmdir()
                    print(f"Eliminada carpeta vacía: {categoria}/")
                except:
                    pass

    def mostrar_estadisticas(self, estadisticas: Dict[str, int]):
        """Muestra estadísticas de la organización"""
        print("\n" + "="*50)
        print("📊 ESTADÍSTICAS DE ORGANIZACIÓN")
        print("="*50)

        total_archivos = sum(estadisticas.values())
        print(f"Total de archivos organizados: {total_archivos}")

        if total_archivos > 0:
            print("\nArchivos por categoría:")
            for categoria, cantidad in estadisticas.items():
                if cantidad > 0:
                    porcentaje = (cantidad / total_archivos) * 100
                    print(f"  {categoria}: {cantidad} archivos ({porcentaje:.1f}%)")

        print("="*50)


def enviar_notificacion(titulo: str, mensaje: str, sistema: str = None):
    """Envía una notificación según el sistema operativo"""
    if sistema is None:
        sistema = platform.system().lower()

    try:
        if sistema == "windows":
            # Usar plyer si está disponible, sino notificación nativa
            try:
                from plyer import notification
                notification.notify(
                    title=titulo,
                    message=mensaje,
                    app_name="Organizador de Archivos",
                    timeout=10
                )
            except ImportError:
                # Notificación básica de Windows
                import subprocess
                subprocess.run([
                    "powershell", "-Command",
                    f'Add-Type -AssemblyName System.Windows.Forms; ' +
                    f'[System.Windows.Forms.MessageBox]::Show("{mensaje}", "{titulo}")'
                ], capture_output=True)

        elif sistema == "darwin":  # macOS
            try:
                import subprocess
                subprocess.run([
                    "terminal-notifier",
                    "-title", titulo,
                    "-message", mensaje,
                    "-sound", "default"
                ], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback: usar osascript
                import subprocess
                script = f'display notification "{mensaje}" with title "{titulo}"'
                subprocess.run(["osascript", "-e", script], check=True)

        elif sistema == "linux":
            try:
                import subprocess
                subprocess.run([
                    "notify-send",
                    titulo,
                    mensaje,
                    "--icon=dialog-information"
                ], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback: imprimir en consola
                print(f"\n🔔 {titulo}: {mensaje}")

        else:
            print(f"\n🔔 {titulo}: {mensaje}")

    except Exception as e:
        print(f"\n🔔 {titulo}: {mensaje}")
        print(f"Nota: Error enviando notificación nativa: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Organizador de archivos por categorías",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python organizar.py                    # Organiza la carpeta 'archivos' en el directorio actual
  python organizar.py /ruta/a/carpeta   # Organiza una carpeta específica
  python organizar.py -r -o /tmp/test   # Recursivo y sobreescribe duplicados
  python organizar.py --deshacer        # Deshace la última organización
  python organizar.py --crear-exe       # Crea ejecutable con PyInstaller (Windows)

Categorías disponibles:
""" + "\n".join(f"  - {cat}: {', '.join(exts[:3])}{'...' if len(exts) > 3 else ''}"
                for cat, exts in CATEGORIAS.items())
    )

    parser.add_argument(
        "carpeta",
        nargs="?",
        type=Path,
        default=Path(__file__).parent / "archivos",
        help="Carpeta a organizar (por defecto: carpeta 'archivos' en el directorio del script)"
    )

    parser.add_argument(
        "-r", "--recursivo",
        action="store_true",
        default=True,
        help="Organizar también subdirectorios (por defecto: activado)"
    )

    parser.add_argument(
        "-o", "--sobreescribir",
        action="store_true",
        help="Sobreescribir archivos duplicados en lugar de renombrarlos"
    )

    parser.add_argument(
        "--deshacer",
        action="store_true",
        help="Deshacer la última organización realizada"
    )

    parser.add_argument(
        "--crear-exe",
        action="store_true",
        help="Crear ejecutable independiente con PyInstaller (solo Windows)"
    )

    parser.add_argument(
        "--sin-notificaciones",
        action="store_true",
        help="Desactivar notificaciones al finalizar"
    )

    args = parser.parse_args()

    # Crear ejecutable si se solicita
    if args.crear_exe:
        crear_ejecutable()
        return

    # Verificar que la carpeta existe
    if not args.carpeta.exists():
        print(f"Error: La carpeta '{args.carpeta}' no existe.")
        sys.exit(1)

    if not args.carpeta.is_dir():
        print(f"Error: '{args.carpeta}' no es un directorio.")
        sys.exit(1)

    print(f"🎯 Organizando archivos en: {args.carpeta.absolute()}")

    # Crear instancia del organizador
    organizador = OrganizadorArchivos(
        carpeta_objetivo=args.carpeta,
        recursivo=args.recursivo,
        sobreescribir=args.sobreescribir
    )

    try:
        if args.deshacer:
            # Modo deshacer
            print("🔄 Modo deshacer activado...")
            exito = organizador.deshacer_ultima_organizacion()
            if exito:
                enviar_notificacion(
                    "Organización Deshecha",
                    f"Se restauraron los archivos en {args.carpeta.name}",
                    sistema=platform.system().lower()
                )
            else:
                enviar_notificacion(
                    "Error",
                    "No se pudo deshacer la organización",
                    sistema=platform.system().lower()
                )
        else:
            # Modo organización
            estadisticas = organizador.organizar_archivos()
            organizador.mostrar_estadisticas(estadisticas)

            if not args.sin_notificaciones:
                total = sum(estadisticas.values())
                enviar_notificacion(
                    "Organización Completada",
                    f"Se organizaron {total} archivos en {args.carpeta.name}",
                    sistema=platform.system().lower()
                )

    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
        enviar_notificacion(
            "Operación Cancelada",
            "La organización fue interrumpida",
            sistema=platform.system().lower()
        )
        sys.exit(1)

    except Exception as e:
        print(f"\nError inesperado: {e}")
        enviar_notificacion(
            "Error",
            f"Error durante la organización: {e}",
            sistema=platform.system().lower()
        )
        sys.exit(1)


def crear_ejecutable():
    """Crea un ejecutable independiente usando PyInstaller"""
    try:
        import subprocess
        import sys

        print("🔧 Creando ejecutable con PyInstaller...")

        # Instalar PyInstaller si no está disponible
        try:
            import PyInstaller
        except ImportError:
            print("Instalando PyInstaller...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

        # Crear el ejecutable
        script_path = Path(__file__).absolute()
        output_name = "Organizador_Archivos"

        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", output_name,
            "--add-data", f"{script_path};.",
            str(script_path)
        ]

        subprocess.check_call(cmd)

        exe_path = Path("dist") / f"{output_name}.exe"
        print(f"✅ Ejecutable creado: {exe_path.absolute()}")

        # Crear archivo batch para facilitar el uso
        batch_content = f'@echo off\n"{exe_path.absolute()}" %*\npause'
        batch_path = Path("Organizar_Archivos.bat")
        batch_path.write_text(batch_content, encoding='utf-8')
        print(f"✅ Archivo batch creado: {batch_path.absolute()}")

        print("\n📋 Instrucciones para automatización en Windows:")
        print("1. Presiona Win+R, escribe 'taskschd.msc' y Enter")
        print("2. Crear tarea básica → Dar nombre")
        print("3. Configurar triggers (programar cuando ejecutar)")
        print("4. En Actions: Start a program → Browse al .exe")
        print("5. En Arguments agregar la ruta de la carpeta a organizar")

    except Exception as e:
        print(f"Error creando ejecutable: {e}")
        print("Asegúrate de tener PyInstaller instalado: pip install pyinstaller")


if __name__ == "__main__":
    main()