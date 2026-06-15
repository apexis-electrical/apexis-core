[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://pypi.org)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-BSD-green)](https://github.com/apexis-electrical/apexis-core/blob/main/LICENSE)
[![CI](https://github.com/apexis-electrical/apexis-core/actions/workflows/ci.yml/badge.svg)](https://github.com)
[![Lint](https://img.shields.io/badge/lint-ruff-informational)](https://github.com/apexis-electrical/apexis-core/actions)


# APEXIS Core

**APEXIS Core** es un motor de cálculo y dimensionamiento iterativo de alta velocidad y nivel corporativo para ingeniería eléctrica. Diseñado bajo los principios de **Arquitectura Hexagonal** y optimizado a nivel de microsegundos de CPU mediante el bloqueo de mallas físicas (`__slots__`), permite automatizar las inecuaciones técnicas de normativas internacionales de forma totalmente agnóstica y escalable.

El núcleo matemático actual incluye soporte nativo y blindado para la reglamentación argentina **AEA 90364-7-771** (Viviendas, Oficinas y Locales Comerciales).

## 🚀 Características Principales

- **Rendimiento Extremo**: Estructuras del dominio sin overhead de memoria RAM (`0.10s` para el procesamiento y reporte de proyectos residenciales completos).
- **Pipeline de Plugins (`Exporters`)**: Sistema de complementos en serie para exportar memorias técnicas en paralelo (`.md`, y futuras expansiones a `.pdf` y `.docx`).
- **Validación de Frontera (`Aduana Normativa`)**: Intercepta e impide el procesamiento de datos ilegales o fuera de rangos de tabla antes del cálculo.
- **Resolución Automática de Tramos**: Las entidades de entrada asimilan vectores secuenciales de distancias sumándolos de forma matemática exacta.
- **Triple Anillo de Seguridad**: Calidad garantizada mediante configuraciones estrictas en `pyproject.toml`, mallas locales de `pre-commit` y workflows automatizados en GitHub Actions (CI).

## 📦 Instalación

### Desde el Repositorio Oficial de GitHub (Recomendado para Desarrollo)
Puedes instalar el núcleo de APEXIS descargando e integrando la última versión del código fuente directamente desde el sistema de control de versiones de GitHub en tu entorno virtual:

```bash
pip install git+https://github.com/apexis-electrical/apexis-core.git
```

### Desde el Repositorio de PyPI (Distribución Comercial)
Una vez liberadas las versiones de producción estables, también podrás instalar la librería de forma tradicional:
```bash
pip install apexis-core
```

## ⚡ Ejemplo Rápido de Uso

A continuación se muestra cómo instanciar el motor y dimensionar de forma automática un circuito terminal utilizando la fachada pública del namespace raíz:

```python
from apexis import APEXISEngine, ElectricalStandardEnum, MarkdownReportExporter

# 1. Definir los criterios globales de diseño (CRITERIA)
global_criteria = {
    "cos_phi": 0.90,
    "ampacity_margin": 1.00,
    "standard_section": "771"  # Ámbito general/oficinas s/ AEA 90364
}

# 2. Inicializar el circuito (C-01: Iluminación con tramos acumulados)
circuits_input = [
    {
        "tag": "C-01",
        "origin": "TPBT",
        "destination": "IUG en Planta Baja",
        "purpose": {
            "type": "lighting",
            "subtype": "iug",
        },
        "electrical": {
            "phase_type": "1PH",
            "voltage_v": 220.0,
            "parallels": 1,
            "length_m": [15.03, 3.82, 1.67, 1.71, 0.2, 0.78, 2.50, 4.32],
            "load": {
                "value": 2.2,
                "unit": "kVA",
            },
        },
        "installation": {
            "installation_method": "B1-2x",  # Cu PVC en cañería embutida
            "material": "Cu",
            "insulation": "PVC",
            "installation_temp_c": 40.0,
            "grouped_circuits": 1,
        },
        "short_circuit": {
            "mode": "skip",
            "Icc_kA": 4.5,
            "time_s": 0.5,
        },
        "cable": {
            "voltage_drop_method": "GDC",
            "mode": "auto",
            "section_mm2": None,
        },
    }
]

# 3. Inicializar el motor orquestador
engine = APEXISEngine(
    standard=ElectricalStandardEnum.AEA_90364.value,
    criteria=global_criteria
)

# 4. Procesar el lote de circuitos
results_table = engine.calculate_circuits(circuits_input)

# 5. Exportar los resultados de la memoria técnica en lote mediante plugins
exporters_pipeline = [MarkdownReportExporter()]
engine.export_results(
    results_table=results_table,
    plugins=exporters_pipeline,
    output_path_base="outputs/memoria_tecnica"
)
```

## 🏛️ Coherencia Física y Normativa (AEA 90364)

El motor ejecuta de forma estricta el lazo iterativo de inecuaciones dictadas por la ley eléctrica:
1.  **Criterio Térmico (Sobrecarga)**: $I_B \le I_n \le I_Z$ (Aplica factores climáticos $f_t$ y de agrupamiento $f_g$).
2.  **Criterio de Caída de Tensión ($\Delta U_{\%}$)**: Método de Gradiente de Caída (GDC s/ 771.19.7.c) calculando el lazo completo sin factores duplicados. Descarta secciones comerciales hasta clavar el límite legal (3.0% para iluminación/tomas, 5.0% para fuerza motriz).
3.  **Solicitación de Cortocircuito**: Verificación adiabática transitoria de energía pasante ($I^2t \le k^2S^2$).

## 📄 Licencia

Este proyecto está bajo la Licencia **BSD de 3 Cláusulas (Modified BSD License)**. Consulta el archivo [LICENSE](LICENSE) para obtener más detalles.
