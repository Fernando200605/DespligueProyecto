"""
Tests simples para explicación
Este archivo contiene pruebas básicas y fáciles de entender
"""
from django.test import TestCase
from app.models import Usuario, Curso, Estudiante
from datetime import date


# ==========================
# TEST 1: Crear un usuario básico
# ==========================
class TestUsuarioBasico(TestCase):
    
    def test_crear_usuario_simple(self):
        """
        Verifica que podemos crear un usuario con datos básicos
        """
        # Crear usuario
        usuario = Usuario.objects.create_user(
            email="test@colegio.edu",
            nombre="Juan Pérez",
            password="mi_clave_segura"
        )
        
        # Verificar que se creó correctamente
        self.assertEqual(usuario.email, "test@colegio.edu")
        self.assertEqual(usuario.nombre, "Juan Pérez")
        self.assertTrue(usuario.estado)  # El usuario debe estar activo por defecto


# ==========================
# TEST 2: Verificar que el email es único
# ==========================
class TestEmailUnico(TestCase):
    
    def test_no_se_permiten_emails_duplicados(self):
        """
        Verifica que no se pueden crear dos usuarios con el mismo email
        """
        # Crear primer usuario
        Usuario.objects.create_user(
            email="test@colegio.edu",
            nombre="Usuario 1",
            password="clave123"
        )
        
        # Intentar crear segundo usuario con el mismo email debe fallar
        with self.assertRaises(Exception):
            Usuario.objects.create_user(
                email="test@colegio.edu",
                nombre="Usuario 2",
                password="clave456"
            )


# ==========================
# TEST 3: Crear un curso
# ==========================
class TestCrearCurso(TestCase):
    
    def test_crear_curso_con_docente(self):
        """
        Verifica que podemos crear un curso y asignarle un docente
        """
        # Crear usuario para el docente
        usuario_docente = Usuario.objects.create_user(
            email="docente@colegio.edu",
            nombre="Profesor García",
            password="clave_docente"
        )
        
        # Crear docente
        from app.models import docente
        profesor = docente.objects.create(
            usuario=usuario_docente,
            especialidad="Matemáticas"
        )
        
        # Crear curso
        curso = Curso.objects.create(
            grado=10,
            codigo="10A",
            capacidad=40,
            docenteid=profesor
        )
        
        # Verificar datos del curso
        self.assertEqual(curso.grado, 10)
        self.assertEqual(curso.codigo, "10A")
        self.assertEqual(curso.capacidad, 40)
        self.assertEqual(curso.docenteid.usuario.nombre, "Profesor García")


# ==========================
# TEST 4: Crear un estudiante
# ==========================
class TestCrearEstudiante(TestCase):
    
    def test_crear_estudiante_en_curso(self):
        """
        Verifica que podemos crear un estudiante y asignarlo a un curso
        """
        # Crear docente
        usuario_docente = Usuario.objects.create_user(
            email="docente@colegio.edu",
            nombre="Profesor",
            password="clave"
        )
        from app.models import docente
        profesor = docente.objects.create(
            usuario=usuario_docente,
            especialidad="Español"
        )
        
        # Crear curso
        curso = Curso.objects.create(
            grado=11,
            codigo="11B",
            capacidad=35,
            docenteid=profesor
        )
        
        # Crear usuario del estudiante
        usuario_estudiante = Usuario.objects.create_user(
            email="estudiante@colegio.edu",
            nombre="María López",
            password="clave_estudiante"
        )
        
        # Crear estudiante
        estudiante = Estudiante.objects.create(
            usuario=usuario_estudiante,
            fechaNacimiento=date(2008, 5, 15),
            estadoMatricula="Matriculado",
            cursoId=curso,
            codigo="EST001"
        )
        
        # Verificar datos del estudiante
        self.assertEqual(estudiante.usuario.nombre, "María López")
        self.assertEqual(estudiante.estadoMatricula, "Matriculado")
        self.assertEqual(estudiante.cursoId.codigo, "11B")


# ==========================
# TEST 5: Verificar contraseña encriptada
# ==========================
class TestSeguridadBasica(TestCase):
    
    def test_contraseña_no_esta_guardada_en_texto_plano(self):
        """
        Verifica que las contraseñas se guardan de forma segura (encriptadas)
        """
        usuario = Usuario.objects.create_user(
            email="test@colegio.edu",
            nombre="Usuario",
            password="mi_clave_secreta"
        )
        
        # La contraseña guardada NO debe ser igual a la original
        self.assertNotEqual(usuario.password, "mi_clave_secreta")
        
        # La contraseña debe estar encriptada (empieza con pbkdf2)
        self.assertTrue(usuario.password.startswith("pbkdf2"))


# ==========================
# TEST 6: Buscar estudiantes
# ==========================
class TestBuscarEstudiante(TestCase):
    
    def test_buscar_estudiante_por_codigo(self):
        """
        Verifica que podemos buscar un estudiante por su código
        """
        # Crear datos necesarios
        usuario_docente = Usuario.objects.create_user(
            email="docente@colegio.edu",
            nombre="Docente",
            password="clave"
        )
        from app.models import docente
        profesor = docente.objects.create(
            usuario=usuario_docente,
            especialidad="Historia"
        )
        curso = Curso.objects.create(
            grado=9,
            codigo="9A",
            capacidad=30,
            docenteid=profesor
        )
        
        usuario_estudiante = Usuario.objects.create_user(
            email="estudiante@colegio.edu",
            nombre="Pedro",
            password="clave"
        )
        
        Estudiante.objects.create(
            usuario=usuario_estudiante,
            fechaNacimiento=date(2009, 3, 10),
            estadoMatricula="Matriculado",
            cursoId=curso,
            codigo="EST002"
        )
        
        # Buscar el estudiante
        existe = Estudiante.objects.filter(codigo="EST002").exists()
        
        # Verificar que existe
        self.assertTrue(existe)


# ==========================
# TEST 7: Verificar configuración de Django
# ==========================
class TestConfiguracionDjango(TestCase):
    
    def test_django_tiene_clave_secreta_configurada(self):
        """
        Verifica que Django tiene una clave secreta configurada
        (necesaria para la seguridad de la aplicación)
        """
        from django.conf import settings
        
        # La clave secreta no debe estar vacía
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertNotEqual(settings.SECRET_KEY, "")


# ==========================
# TEST 8: Usuario inactivo
# ==========================
class TestUsuarioInactivo(TestCase):
    
    def test_se_puede_crear_usuario_inactivo(self):
        """
        Verifica que se puede crear un usuario desactivado
        """
        usuario = Usuario.objects.create_user(
            email="inactivo@colegio.edu",
            nombre="Usuario Inactivo",
            password="clave",
            estado=False  # Usuario inactivo
        )
        
        # Verificar que está inactivo
        self.assertFalse(usuario.estado)