## Guía de Contribución para APEXIS Core

¡Gracias por tu interés en colaborar con el ecosistema APEXIS! Para mantener los estándares de calidad de software empresarial y la precisión científica de los cálculos de ingeniería eléctrica, todas las contribuciones deben seguir las pautas detalladas en este documento.

## 🏛️ Principios de Arquitectura y Diseño
Para evitar el acoplamiento y asegurar el mantenimiento a largo plazo, el núcleo de APEXIS se rige estrictamente por:

1. Arquitectura Hexagonal (Ports & Adapters): La lógica matemática de las normativas nacionales e internacionales debe vivir aislada dentro de su propio adaptador bajo src/apexis/standards/. El motor central (engine.py) solo interactúa mediante interfaces abstractas fijadas en interfaces/.
2. Optimización Estricta de Memoria: Todas las clases del dominio, adaptadores e interfaces deben declarar de forma obligatoria el mecanismo de __slots__ para eliminar el overhead de diccionarios dinámicos internos (__dict__) de Python y maximizar la velocidad en bucles masivos.
3. Programación Funcional en Fórmulas: Las ecuaciones de la carpeta formulas/ deben ser Funciones Puras sin estado, testeables de forma aislada.

## 🔧 Configuración del Entorno de Desarrollo

1. Clona el repositorio oficial de la organización e ingresa al directorio del proyecto:

   ```bash
   git clone https://github.com/apexis-electrical/apexis-core.git
   cd apexis-core
   ```

2. Instala el paquete en modo editable junto con las herramientas de desarrollo en tu entorno de Python (se requiere >=3.10):

   ```bash
   pip install -e .
   pip install pytest pytest-cov ruff pre-commit
   ```

3. Activa de forma obligatoria los ganchos locales de control (hooks) antes de realizar cualquier commit:

   ```bash
   pre-commit install
   ```

## 🛡️ Flujo de Trabajo y Control de Calidad

## 1. Convención de Código y Estilo (Ruff)
El repositorio utiliza Ruff de forma nativa para el análisis estático y formateo. Antes de enviar cambios, tu código debe pasar la aduana de estilo configurada en el pyproject.toml (la cual ignora automáticamente mallas de test y ejemplos):

   ```bash
    ruff check . --fix
    ruff format
   ```

## 2. Suite de Pruebas Cruzadas (Pytest)
No se aceptará ninguna funcionalidad o parche que reduzca la cobertura o carezca de pruebas integradas. Cada fórmula técnica o validador debe contar con su correspondiente contraprueba matemática testigo en la carpeta tests/ utilizando la convención de nombres de rutas completa (test_src_...py):

   ```bash
    pytest -v
   ```

## 3. Mensajes de Commit (Conventional Commits)
Los commits deben seguir la estructura internacional para mantener un historial limpio y automatizar el changelog:

- feat(norma): add voltage drop tables method for nec2023 adapter
- fix(core-math): resolve types collision inside circuit validator split
- chore(ci): update pre-commit hooks to version v0.5.0

## 🚀 Proceso para Enviar un Pull Request (PR)

 1. Crea una rama descriptiva a partir de la rama de desarrollo dev (git checkout -b feat/mi-nueva-norma).
1. Desarrolla el código asegurándote de usar variables, firmas y nombres de archivos en inglés, y docstrings/comentarios analíticos en español.
2. Verifica que tu máquina apruebe los controles locales de pre-commit y toda la suite de casos de pytest.
3. Realiza el git push hacia tu fork y abre el Pull Request apuntando estrictamente a la rama dev del repositorio oficial (la rama main queda reservada exclusivamente para despliegues estables y etiquetado de producción). El workflow de GitHub Actions (CI) evaluará automáticamente tu código en Python 3.10, 3.11 y 3.12 antes de la revisión final por parte del comité de arquitectura.
