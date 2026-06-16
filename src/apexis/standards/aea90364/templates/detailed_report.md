# Introducción

La presente Memoria Técnica de Cálculo tiene como objetivo definir y justificar los criterios adoptados para el dimensionamiento de conductores eléctricos de baja tensión, así como la selección y coordinación de sus dispositivos de protección.

En este documento se establecen la metodología de cálculo, los criterios normativos aplicados y las verifi­caciones necesarias para garantizar la seguridad, el correcto funcionamiento y la protección del sistema, de conformidad con la reglamentación AEA 90364. Dicha metodología se aplica a la totalidad de los circuitos de la instalación eléctrica proyectada para el tablero eléctrico indicado.

El proceso de dimensionamiento se basa en la evaluación simultánea de las condiciones de operación en régimen permanente y del comportamiento del sistema ante condiciones de falla.

Para ello, se consideran los siguientes parámetros de diseño:

- Corriente de proyecto $(I_B)$.
- Corriente admisible del conductor $(I_Z)$.
- Condiciones reales de instalación y sus respectivos factores de corrección.
- Verificación por caída de tensión.
- Verificación en condición de cortocircuito.
- Coordinación con los dispositivos de protección.

Dicho enfoque garantiza que cada circuito cumpla con los límites térmicos admisibles, los requisitos de protección y los niveles de rendimiento exigidos por la normativa vigente.

# Determinación de la corriente de proyecto

## Normalización de la potencia de carga

Las cargas eléctricas pueden expresarse en diferentes unidades, tales como $HP$, $kW$ o $kVA$, según su naturaleza o la información disponible.

A fin de unificar los criterios de cálculo, todas las potencias se convierten a potencia aparente $(S)$, expresada en kilovolt-amperes $(kVA)$. Esto permite determinar la corriente de proyecto de forma consistente, independientemente del factor de potencia.

Cuando se dispone de la potencia activa $(P)$, la conversión a potencia aparente se realiza mediante la siguiente relación:
$$S = \frac{P}{\cos\varphi}$$
Donde:

- $S$: potencia aparente [$kVA$].
- $P$: potencia activa [$kW$].
- $\cos\varphi$: factor de potencia de la carga.

Para las cargas expresadas en potencia mecánica $(HP)$, se adoptan relaciones de conversión específicas que consideran el tipo de equipo y su rendimiento.

La normalización de las cargas a potencia aparente constituye la base para la determinación de la corriente de proyecto $(I_B)$.

Ante la falta de información precisa, se aplican valores típicos de factor de potencia según el tipo de carga.

## Cálculo de la corriente de proyecto

La corriente de proyecto se determina a partir de la potencia aparente de la carga. Este criterio resulta adecuado para instalaciones industriales, comerciales o torres residenciales, donde el factor de potencia puede presentar variaciones.

Para sistemas trifásicos, el cálculo se realiza mediante la siguiente expresión:
$$I_B = \frac{S \cdot 1000}{\sqrt{3} \cdot U}$$
Para sistemas monofásicos, se aplica la relación:
$$I_B = \frac{S \cdot 1000}{U}$$
Donde:

- $I_B$: corriente de proyecto [$A$].
- $S$: potencia aparente [$kVA$].
- $U$: tensión nominal [$V$].

# Condiciones de instalación y selección del sistema de cableado

La selección del material del conductor y de su aislación se efectúa en función de las influencias externas presentes en cada sector de la instalación. Para ello, se sigue lo establecido en la reglamentación AEA 90364 respecto a la clasificación de ambientes y las condiciones de evacuación. Estas variables determinan las exigencias específicas relativas al comportamiento frente al fuego, la emisión de humos y las características dieléctricas del cable.

## Clasificación del establecimiento

Con base en la clasificación de los locales según las categorías **BA** (tipo de usuario) y **BD** (condiciones de evacuación), se adoptan los siguientes criterios:

- **Locales de pública concurrencia o de evacuación dificultosa (BD2, BD3, BD4)**: Se emplean cables con aislación y envoltura tipo LSZH (Low Smoke Zero Halogen). Estos materiales se caracterizan por su baja emisión de humos y la ausencia de gases corrosivos o tóxicos en caso de incendio. Estos conductores responden a las normas IRAM 62266 (multipolares) e IRAM 62267 (unipolares).

- **Locales con presencia de personas con capacidades reducidas (BA2, BA3)**: Se seleccionan soluciones constructivas que priorizan materiales no propagantes del incendio y de baja toxicidad, en concordancia con las exigencias de seguridad reforzada.

- **Locales de uso general (BA1, BD1)**: Se permite la utilización de conductores con aislación de PVC no propagante de la llama, según las normas IRAM NM 247-3 para conductores en cañerías, o cables con envoltura según la norma IRAM 2178 para otros métodos de instalación.

## Métodos de instalación y selección de canalizaciones

Considerando la clasificación del local, se establece el método de instalación, que condiciona la capacidad de disipación térmica del conductor y, por lo tanto, el valor de la corriente admisible que se toma como base para el dimensionamiento. Para el cálculo, se consideran los siguientes métodos de referencia:

- **Método A1:** Conductores unipolares en cañería o conductos embutidos en una pared térmicamente aislante.
- **Método A2:** Cable multipolar en cañería o conductos embutido en una pared térmicamente aislante.
- **Método B1:** Conductores unipolares en cañería o conductos embutida en mampostería o colocada a la vista sobre pared.
- **Método B2:** Cable multipolar en cañería o conductos embutida en mampostería o colocada a la vista sobre pared.
- **Método C:** Cable multipolar o cables unipolares en contacto, tendidos en una sola capa sobre pared, piso o bandeja no perforada (de fondo sólido).
- **Método D1:** Cables instalados dentro de caños o conductos enterrados en el suelo.
- **Método D2:** Cables instalados directamente enterrados en el suelo.
- **Método E:** Cable multipolar instalado en aire libre (separado de la superficie), generalmente sobre bandeja perforada o bandeja tipo escalera.
- **Método F:** Cables unipolares en contacto entre sí, instalados en aire libre, generalmente sobre bandeja perforada o bandeja tipo escalera.
- **Método G:** Cables unipolares instalados en aire libre (generalmente sobre bandeja perforada o bandeja tipo escalera) y separados entre sí por una distancia mínima equivalente a un diámetro del conductor.

La identificación precisa del método de instalación resulta determinante para definir la sección del conductor y aplicar los factores de corrección correspondientes.

## Selección del material de aislación y tipo del conductor

Una vez que se identifica la clasificación del local y se establece el método de instalación, se selecciona el material de aislación del conductor, el cual incide de manera directa en su capacidad de conducción de corriente y en su comportamiento térmico. Para el diseño, se consideran las siguientes opciones:

- **Aislación de PVC**: Este material se utiliza en instalaciones de uso general donde las exigencias térmicas son moderadas, ya que posee una temperatura máxima de 70 °C en servicio continuo y de 160 °C en condiciones de cortocircuito.

- **Aislación de XLPE / EPR**: Este material se emplea en circuitos con altas exigencias térmicas o cuando se requiere una mayor capacidad de transporte de corriente para una misma sección conductora, debido a que admite una temperatura máxima de 90 °C en servicio continuo y de 250 °C en condiciones de cortocircuito.


# Selección y dimensionamiento del conductor

El dimensionamiento del conductor se efectúa mediante un proceso iterativo, partiendo de una selección inicial en condiciones normalizadas y verificando posteriormente su validez en función de las condiciones reales de instalación.

## Selección de la sección del conductor por corriente admisible

La corriente admisible del conductor $(I_Z)$ se obtiene a partir de las tablas normalizadas de la reglamentación AEA 90364. Este valor se determina en función del tipo de cable seleccionado, el método de instalación adoptado, la sección del conductor y los materiales constitutivos tanto del alma conductora como del aislante.

De manera específica, se aplican los siguientes criterios:

- Para conductores aislados en cañerías, se adoptan los valores correspondientes a la **Tabla 771.16.I** (y concordantes de la Sección 770).
- Para cables multipolares instalados en aire o bandejas, se emplean los valores de la **Tabla 771.16.III**.
- Para cables enterrados, se consideran la **Tabla 771.16.V** y la **Tabla 771.16.VI**.
- Para líneas aéreas preensambladas, se utilizan los valores de la **Tabla 771.16.VIII**.

Estos valores corresponden a condiciones de referencia normalizadas. Por lo tanto, constituyen la corriente admisible base del conductor antes de aplicar los factores de corrección por condiciones reales de instalación.

La sección del conductor se selecciona de manera que el valor obtenido de las tablas resulte adecuado para alimentar la carga prevista. Posteriormente, dicho valor se ajusta con los factores de corrección correspondientes. Los valores adoptados deben ser verificados en cada caso particular según la versión vigente de la reglamentación aplicable.

## Factores de corrección por condiciones de instalación

La capacidad de conducción de corriente de los conductores se encuentra condicionada por su capacidad de disipación térmica, la cual varía según las condiciones reales de instalación. A fin de contemplar estas variables, se aplican factores de corrección que ajustan la corriente admisible de referencia mediante la siguiente expresión:
$$I_{Z,corregida} = I_{tabla} \cdot f_{flex} \cdot f_t \cdot f_g \cdot f_s \cdot f_p \cdot f_{sim} \cdot n_{paralelos}$$
Donde:

- $I_{Z,corregida}$: Corriente admisible corregida.
- $I_{tabla}$: Corriente admisible de referencia para un único conductor, obtenida de las tablas normativas correspondientes.
- $f_{flex}$: Factor de reducción aplicable a conductores flexibles (Clase 5).
- $f_t$: Factor de corrección por temperatura ambiente (aire) o del terreno.
- $f_g$: Factor de corrección por agrupamiento de circuitos o conductos.
- $f_s$: Factor de corrección por resistividad térmica del suelo (para canalizaciones enterradas o cables directamente enterrados).
- $f_p$: Factor de corrección por profundidad de instalación (para canalizaciones enterradas o cables directamente enterrados).
- $f_{sim}$: Factor de reducción por asimetría en la distribución de corriente para conductores en paralelo.
- $n_{paralelos}$: Número de conductores en paralelo por fase.

La correcta aplicación de estos coeficientes resulta fundamental para garantizar que los conductores no superen su temperatura máxima de diseño durante la operación en régimen permanente. Cabe destacar que el factor de corrección por método de instalación ya se encuentra intrínsecamente incorporado en los valores de corriente obtenidos de las tablas normativas.

Al emplear conductores en paralelo por fase, la sección transversal equivalente del circuito se determina mediante la sumatoria de las secciones individuales de cada conductor:
$$ S_{eq} = n_{paralelos} \cdot S $$
Donde:

* $S_{eq}$: Sección transversal equivalente por fase del circuito.
* $S$: Sección transversal nominal de un único conductor.

Esta consideración se aplica tanto para la determinación de la capacidad de conducción de corriente total como para la verificación por caída de tensión.

## Determinación de la sección por corriente admisible corregida

El criterio fundamental de dimensionamiento térmico establece que la corriente admisible corregida del conductor debe ser igual o superior a la corriente de proyecto del circuito. Esta condición asegura que la temperatura operativa del aislamiento se mantenga estrictamente dentro de los límites de diseño admisibles en régimen permanente, evitando la degradación prematura de los materiales.

Para dar cumplimiento a esta exigencia, la sección comercial del conductor se determina mediante la verificación de la siguiente inecuación:
$$I_B \leq I_{Z,corregida}$$
Donde:

- $I_{Z,corregida}$: corriente admisible del conductor con los factores de corrección aplicados [$A$].
- $I_B$: corriente de proyecto o de diseño [$A$].

En caso de que la sección inicialmente propuesta no satisfaga esta condición de carga, se procede a seleccionar la sección comercial inmediata superior, recalculando su capacidad térmica hasta lograr la validación del circuito.

# Coordinación entre el conductor y la protección

Una vez seleccionada la sección del conductor y determinada su capacidad de conducción corregida, se procede a la selección y verificación del dispositivo de protección asociado. Para garantizar una protección eficaz contra sobrecargas, se deben cumplir de forma simultánea las siguientes condiciones normativas:

## Condición de corriente nominal

$$I_B \leq I_n \leq I_{Z,corregida}$$

## Condición de funcionamiento de la protección

$$I_2 \leq (I_{Z,corregida} \cdot 1.45)$$
Donde:

- $I_B$: corriente de proyecto o de diseño [$A$].
- $I_n$: corriente nominal del dispositivo de protección [$A$].
- $I_{Z,corregida}$: corriente admisible del conductor con los factores de corrección aplicados [$A$].
- $I_2 = 1{,}45 \cdot I_n$: corriente convencional de actuación del dispositivo de protección [$A$].

En el caso de utilizar interruptores automáticos termomagnéticos fabricados bajo la norma IEC 60898, el cumplimiento de la primera relación $(I_n \leq I_{Z,corregida})$ garantiza de forma implícita la verificación de la condición de sobrecarga, debido a las características técnicas propias de estos dispositivos.

El estricto cumplimiento de estas condiciones asegura que el conductor no opere bajo regímenes de sobrecarga permanentes y que el dispositivo de protección actúe oportunamente, antes de que los cables alcancen temperaturas que pongan en riesgo la integridad de la instalación.

## Selección y características de los dispositivos de protección

La protección de los conductores se realiza mediante dispositivos automáticos que aseguran la desconexión ante condiciones de sobrecarga y cortocircuito, preservando la integridad de toda la instalación.

Para que esta protección sea efectiva, cada dispositivo debe poseer una capacidad de ruptura o poder de corte $(P_{dc})$ adecuado a la corriente de cortocircuito máxima presunta $(I_k'')$ en su punto de instalación, cumpliendo con la siguiente condición:
$$P_{dc} \geq I_k''$$
La selección de la tecnología de protección depende de la corriente de proyecto, de las características de la carga y del nivel de cortocircuito.

### Interruptores automáticos en miniatura (MCB / PIA)

Estos dispositivos constituyen la tecnología estándar para la protección de circuitos terminales y seccionales en instalaciones residenciales, comerciales y de oficinas. Su aplicación se rige por los siguientes criterios:

* **Normativa de fabricación:** Deben cumplir con la norma **IEC 60898-1** (o IRAM 2169). Poseen características de disparo térmico y magnético fijas y un poder de corte (capacidad de ruptura) normalizado no ajustable.

* **Límites de corriente:**

  * En instalaciones bajo el alcance de la **Sección 770** (viviendas unifamiliares de hasta 63 A), el calibre máximo permitido para cualquier dispositivo del tablero es de **63 A**.
  * En instalaciones bajo la **Sección 771** (viviendas de mayor potencia, oficinas y locales), se admite el empleo de estos dispositivos con una corriente asignada de hasta **125 A** en tableros destinados a ser operados por personal no calificado (BA1), de acuerdo con la norma **IEC 61439-3**

#### Curvas de disparo

La curva de respuesta define el umbral de disparo magnético para proteger ante cortocircuitos sin provocar desconexiones intempestivas durante los arranques normales de las cargas:

- **Curva B**: Presenta un disparo magnético entre 3 y 5 veces la corriente nominal $(I_n)$. Se utiliza en circuitos con cargas puramente resistivas o en líneas de gran longitud donde la corriente de cortocircuito mínima resulta baja.
- **Curva C**: Presenta un disparo magnético entre 5 y 10 veces $I_n$. Constituye la curva estándar para usos generales, sistemas de iluminación y motores de baja potencia.
- **Curva D**: Presenta un disparo magnético entre 10 y 20 veces $I_n$. Se reserva para circuitos con altas corrientes de inserción, tales como transformadores o grandes motores.

### Interruptores automáticos de caja moldeada (MCCB / IA)

Se recurre a esta tecnología cuando las corrientes de proyecto o diseño exceden los límites de capacidad de los dispositivos modulares (típicamente > 63 A en instalaciones s/770 o > 125 A en tableros s/771), o cuando la corriente de cortocircuito presunta (Ik′′​) en el punto de instalación supera la capacidad de ruptura $(Pdc​$) de los interruptores tipo MCB.

* **Normativa de fabricación:** Estos dispositivos se rigen por la norma **IEC 60947-2**.

#### Unidades de actuación

A diferencia de los dispositivos modulares, los de caja moldeada se clasifican según la tecnología de su relé de protección:

- **Termomagnéticos (fijos o ajustables)**: Utilizan un bimetal para la protección contra sobrecargas y una bobina para los cortocircuitos. Son los más comunes en alimentadores seccionales y permiten regular los umbrales para coordinar con la capacidad del cable.

- **Electrónicos (microprocesados)**: Emplean transformadores de corriente internos y un microprocesador para evaluar la señal. Ofrecen una precisión superior, no se ven afectados por la temperatura ambiente del tablero y admiten ajustes complejos como el retardo de tiempo en cortocircuito.

#### Categorías de selectividad

En la memoria técnica se consideran las categorías de selectividad, ya que determinan la capacidad del interruptor para coordinar con protecciones instaladas aguas abajo:

- **Categoría A**: Interruptores que carecen de un retardo intencional ante cortocircuitos. Operan generalmente como limitadores de corriente y se ubican en los niveles finales de la distribución para proteger conductores de menor sección.

- **Categoría B**: Interruptores diseñados con un retardo de tiempo intencional ante cortocircuitos (tiempo de breve duración). Se especifican en las cabeceras de grandes instalaciones para asegurar que una falla en un circuito terminal sea despejada de forma local, evitando el apagón total del inmueble.

#### Condición crítica de dimensionamiento

- De acuerdo con la reglamentación **AEA 90364-7-771 (cláusula 771.19.3.d)**, cuando estos interruptores poseen órganos de disparo ajustables y se instalan en **viviendas u oficinas** (donde no hay presencia permanente de personal calificado BA4 o BA5), la sección de los conductores debe dimensionarse considerando el **valor más alto de regulación posible** del relé, independientemente del ajuste que se elija para la operación.

- Esta medida garantiza que el cable permanezca protegido ante sobrecargas incluso si un usuario no calificado modifica el ajuste del interruptor a su valor máximo en el futuro.

### Interruptores diferenciales (RCCB / ID)

Los dispositivos diferenciales constituyen el medio **obligatorio** en esquemas de conexión a tierra tipo TT para la protección contra contactos indirectos (por corte automático de la alimentación), actuando asimismo como protección complementaria contra contactos directos.

* **Normativa:** Deben responder a las normas **IEC 61008** (o IRAM 2301) o **IEC 61009** (para interruptores combinados con termomagnética).
* **Capacidad de Ruptura y Coordinación:** Dado que su capacidad de ruptura propia es limitada (típicamente 500 A o $10 \cdot I_n$​), deben estar protegidos obligatoriamente contra cortocircuitos por un dispositivo de protección contra sobrecorrientes (fusible o MCB) aguas arriba o aguas abajo, según las tablas de coordinación del fabricante.
* **Corte Omnipolar:** En instalaciones monofásicas, el interruptor diferencial debe ser **bipolar (2P)**, y en instalaciones trifásicas, **tetrapolar (4P)**, asegurando el seccionamiento simultáneo del neutro y todas las fases.

#### Criterios de selección de la sensibilidad

La sensibilidad se determina según el objetivo de seguridad, asegurando que ante una falla la tensión de contacto no supere los **24 V** en locales secos, húmedos o mojados:

* **Alta sensibilidad $(\leq 30 mA)$**: De uso obligatorio en todos los circuitos terminales de viviendas, oficinas y locales (IUG, TUG, TUE, ACU, etc.) para garantizar la protección de las personas. Su actuación debe ser **instantánea (sin retardo)**.
* **Sensibilidad media $(\leq 300 mA)$**: Se aplica en circuitos seccionales o alimentadores para proteger contra riesgos de incendio (corrientes de fuga de 300 a 500 mA pueden iniciar siniestros) y para asegurar la selectividad diferencial vertical.


#### Clasificación según el tipo de onda

Se selecciona la tecnología capaz de detectar fallas con componentes de corriente continua generadas por equipos electrónicos:

* **Clase AC (estándar):** Exclusivo para corrientes de falla alternas sinusoidales. Adecuado para cargas resistivas o inductivas simples sin electrónica de potencia asociada.
* **Clase A (superinmunizados / pulsantes):** Detectan corrientes sinusoidales y pulsantes con componentes de CC. Su empleo es obligatorio en circuitos de **recarga de vehículos eléctricos (Modos 2 y 3)** según AEA 90364-7-722, y altamente recomendado en circuitos con balastos electrónicos, variadores o luminarias LED para evitar disparos intempestivos o el bloqueo del dispositivo.
* **Clase B (universal):** Detectan corrientes de falla de CA, pulsantes y de CC alisada. Requeridos en estaciones de carga de vehículos eléctricos de alta potencia o donde el fabricante del equipo de potencia lo especifique.

#### Selectividad mediante diferenciales tipo S (Selectivos)

En instalaciones con múltiples niveles de protección, se emplean dispositivos **tipo S** en los niveles superiores (cabeceras de tableros seccionales o principales). Estos presentan un retardo de tiempo intencional y deben estar identificados en su frente con el símbolo [S]. La selectividad se logra cuando el diferencial de cabecera es de **tipo S** y posee una sensibilidad al menos **3 veces superior** al diferencial situado aguas abajo.

# Verificaciones del Dimensionamiento

## Verificación de caída de tensión

Una vez cumplidas las condiciones térmicas y de protección, se debe verificar que la caída de tensión en cada circuito se mantenga dentro de los límites reglamentarios. Esto garantiza el correcto funcionamiento de los equipos alimentados.

Para realizar esta validación, se pueden utilizar dos metodologías según el nivel de precisión requerido y el tipo de conductor: el método simplificado por GDC o el método completo por impedancia.

### Método simplificado por Gradiente de Caída (GDC)

Es el método aproximado propuesto por la norma AEA 90364.7.771. Utiliza un coeficiente tabulado denominado GDC unitario que incorpora la resistividad del material y el tipo de sistema (monofásico o trifásico), permitiendo calcular la caída de tensión en función de la sección transversal del conductor mediante la siguiente expresión:
$$\Delta V = \frac{GDC_{\text{unitario}} \cdot I \cdot L}{S}$$
Donde:

- $\Delta V$: caída de tensión absoluta [$V$].
- $GDC_{\text{unitario}}$: gradiente de caída de tensión unitario obtenido de las tablas de la norma, según el material del conductor y tipo de circuito [$\text{V} \cdot \text{mm}^2 / (\text{A} \cdot \text{m})$].
- $I$: corriente de proyecto o de empleo del circuito [$A$].
- $L$: longitud lineal del circuito (distancia simple entre origen y carga) [$m$].
- $S$: sección transversal del conductor [$\text{mm}^2$].

### Método completo de impedancia

Este método se emplea cuando se requiere un mayor nivel de precisión, especialmente en cables de grandes secciones (típicamente mayores a $70 \text{mm}^2)$ o circuitos con un factor de potencia bajo, situaciones donde la reactancia inductiva $(X)$ adquiere un peso significativo frente a la resistencia óhmica $(R)$.

La caída de tensión se calcula considerando la impedancia total del lazo, mediante las siguientes ecuaciones:

- Sistema trifásico:
$$\Delta V\% = (\frac{\sqrt{3} \cdot I \cdot L \cdot (R \cdot \cos\varphi + X \cdot \sin\varphi)}{U}) \cdot 100$$
- Sistema monofásico:
$$\Delta V\% = (\frac{2 \cdot I \cdot L \cdot (R \cdot \cos\varphi + X \cdot \sin\varphi)}{U}) \cdot 100$$
Donde:

- $R$: resistencia efectiva del conductor a la temperatura de servicio (ej. 70 °C para PVC o 90 °C para XLPE) [$\Omega/\text{m}$].
- $X$: reactancia inductiva lineal del cable [$\Omega/\text{m}$].
- $\cos\varphi$: factor de potencia de la carga.
- $\sin\varphi$: factor de reactancia de la carga $(\sqrt{1 - \cos^2\varphi})$.
- $I$: corriente del circuito [$A$].
- $L$: longitud del circuito expresada en metros [$m$].

En concordancia con las exigencias normativas, se adoptan como límites máximos permitidos los siguientes valores:

- Circuitos de tableros: $\leq 1\%$
- Circuitos de iluminación y tomacorrientes: $\leq 3\%$
- Circuitos de fuerza motriz (motores): $\leq 5\%$

## Verificación frente a condiciones de cortocircuito

Ante la ocurrencia de un cortocircuito, los conductores deben poseer la capacidad de soportar los esfuerzos térmicos generados durante el tiempo que demande la actuación del dispositivo de protección. La corriente de cortocircuito presunta en cada punto de la instalación se determina en función de las impedancias del sistema de alimentación, de los propios conductores y de los elementos de maniobra intermedios. Estos valores pueden obtenerse mediante la aplicación de la norma AEA 90909 o a través de los datos provistos por la empresa distribuidora de energía.

Dicha corriente presunta se utiliza para validar el poder de corte de las protecciones, coordinar los dispositivos y realizar la verificación térmica del conductor mediante la aplicación de la siguiente condición:
$$I^2 \cdot t \leq k^2 \cdot S^2$$
Donde:

- $k$: constante característica que depende del material conductor y del tipo de aislación.
- $S$: sección del conductor [$\text{mm}^2$].
- $I$: corriente de cortocircuito eficaz presunta [$A$].
- $t$: tiempo de despeje o apertura de la protección [$s$].

El cumplimiento de esta relación garantiza que la energía térmica integrada $(I^2 \cdot t)$ asociada a la falla sea inferior a la capacidad térmica del cable, impidiendo daños permanentes en el alma conductora o en la aislación del circuito.

La verificación puede ser omitida en ciertos casos de diseño cuando el criterio de cortocircuito no resulta gobernante o no se dispone de datos de corriente de falla, manteniendo su carácter de validación complementaria.

## Criterio de recálculo y dimensionamiento definitivo

En caso de que alguna de las verificaciones anteriores (térmica en régimen permanente, coordinación con la protección, límite de caída de tensión o solicitación por cortocircuito) no se cumpla de forma satisfactoria, se deberá seleccionar una sección de conductor superior. Ante este cambio, se deberán ejecutar nuevamente todos los cálculos y comprobaciones del circuito de manera iterativa. Este proceso se repetirá hasta asegurar que la sección final adoptada responda de forma segura y simultánea a la totalidad de las exigencias normativas y de funcionamiento establecidas.

# Dimensionamiento del conductor de protección (PE)

El conductor de protección (PE) se dimensiona de manera directa en función de la sección de los conductores de fase del circuito asociado. Para ello, se siguen los criterios de proporcionalidad establecidos en la reglamentación AEA 90364:

- Para secciones de fase menores o iguales a $16\text{mm}^2$: $S_{PE} = S$
- Para secciones de fase mayores a $16\text{mm}^2$ y menores o iguales a $35\text{mm}^2$: $S_{PE} = 16\text{mm}^2$
- Para secciones de fase mayores a $35\text{mm}^2$: $S_{PE} = \frac{S}{2}$

Donde:

- $S$: sección del conductor de fase [$\text{mm}^2$].
- $S_{PE}$: sección del conductor de protección [$\text{mm}^2$].
- $\frac{S}{2}$: El valor resultante debe ser ajustado a la sección comercial normalizada más próxima, adoptándose un valor igual o superior o el inmediato inferior cuando resulte más representativo según disponibilidad comercial.

La aplicación de este criterio asegura una baja impedancia en el lazo de falla, garantizando la adecuada conducción de las corrientes de defecto a tierra y la correcta actuación de las protecciones.

# Secciones mínimas

Independientemente de los valores que surjan de los cálculos, el diseño final debe respetar estrictamente las secciones mínimas absolutas dictadas por la normativa vigente para cada tipo de aplicación:

- Circuitos terminales de iluminación: $\geq 1,5$ mm²
- Circuitos terminales de tomacorrientes (usos generales): $\geq 2,5$ mm²
- Circuitos terminales de tomacorrientes (usos especiales): $\geq 4$ mm²
- Circuitos terminales de tomacorrientes (uso cvaa/hvac): $\geq 4$ mm²

Estas secciones mínimas resguardan la resistencia mecánica de los conductores durante las tareas de cableado y aseguran un estándar mínimo de seguridad en la instalación.

# Consideraciones normativas adicionales

Los conductores utilizados en instalaciones eléctricas fijas deberán cumplir con las tensiones nominales mínimas establecidas por la reglamentación vigente, siendo en general no inferiores a 450/750 V.

Asimismo, en circuitos de muy baja tensión (MBTS), se deberán mantener separaciones físicas respecto de circuitos de mayor tensión, salvo en aquellos casos en que los conductores posean una aislación adecuada para la máxima tensión presente en la canalización.

Estas condiciones forman parte de los criterios generales de diseño de la instalación y no afectan de forma directa el dimensionamiento térmico de los conductores, pero resultan de cumplimiento obligatorio según la reglamentación aplicable.

# Resultados del dimensionamiento

A continuación se presentan los resultados del cálculo de dimensionamiento de conductores y selección de protecciones para los distintos circuitos de la instalación, obtenidos a partir de los criterios expuestos en los apartados anteriores.

{{RESULTS_TABLE}}

::: {custom-style="caption"}
Tabla de Resultados del Dimensionamiento y Verificación de los Circuitos
:::

Los resultados obtenidos cumplen con los criterios de dimensionamiento implementados, conforme a los lineamientos de la reglamentación AEA 90364, garantizando condiciones adecuadas de seguridad, funcionamiento y protección de los conductores.

# Referencias técnicas

La presente memoria técnica y los criterios adoptados se fundamentan en la reglamentación vigente de la Asociación Electrotécnica Argentina y normas internacionales aplicables:

- **AEA 90364-4-41 / 4-43:** Protección contra choques eléctricos y sobrecorrientes.
- **AEA 90364-7-770:** Reglas particulares para instalaciones en inmuebles.
- **AEA 90364-7-771:** Determinación de secciones, métodos de instalación y protección.
- **AEA 90909:** Cálculo de corrientes de cortocircuito en sistemas trifásicos.
- **IEC 60898-1:** Interruptores automáticos para instalaciones de uso doméstico y similar.
- **IEC 60947-2:** Interruptores automáticos de baja tensión para uso industrial.
- **IEC 61008-1 / 61009:** Interruptores diferenciales.
- **IRAM NM 247-3 / IRAM 2178-1:** Conductores eléctricos aislados.
- **IRAM 4504:** Representación gráfica de planos y documentación técnica.
