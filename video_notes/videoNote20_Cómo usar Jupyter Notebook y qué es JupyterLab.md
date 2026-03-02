# Cómo usar Jupyter Notebook y qué es JupyterLab

Video: *Cómo usar JUPYTER NOTEBOOK 📝 qué es JUPYTERLAB*
YouTube: [https://www.youtube.com/watch?v=CwbMaSkKDZg](https://www.youtube.com/watch?v=CwbMaSkKDZg)

---

# 🧠 ¿Qué es un Notebook?

Un Notebook es:

> Una aplicación web para crear y compartir código.

Características clave:

* Se ejecuta en el navegador
* Usa **celdas**
* Permite mezclar:

  * Código
  * Texto
  * Tablas
  * Gráficos
  * Imágenes
  * Resultados

Es ideal para:

* Ciencia de datos
* Prototipos
* Análisis exploratorio
* Reportes reproducibles

---

# 📌 ¿Para qué sirven los Notebooks?

Ventajas principales:

1. Ejecutas código por partes (celda por celda)
2. Ves resultados inmediatamente
3. Puedes guardar tablas y gráficos dentro del documento
4. Son fáciles de compartir

Es como tener:

📓 Cuaderno + Python + Visualización todo junto.

---

# 🔍 Diferencia: Jupyter Notebook vs JupyterLab

## 📝 Jupyter Notebook

Es el documento individual donde trabajas.

## 🧪 JupyterLab

Es la interfaz avanzada que permite:

* Abrir varios notebooks
* Manejar archivos
* Ver carpetas
* Apagar kernels
* Trabajar tipo IDE

JupyterLab = entorno completo
Notebook = archivo individual

---

# 🧠 ¿Qué es un Kernel?

Cuando abres un notebook:

* Se crea un espacio en memoria
* Se activa un kernel (motor de ejecución)

En JupyterLab puedes:

* Ver kernels activos
* Apagarlos (shutdown)
* Liberar memoria

Muy importante si trabajas con datos grandes.

---

# 🧱 Lo más importante: LAS CELDAS

Todo en Jupyter gira alrededor de celdas.

Tipos principales:

1. Código
2. Markdown

---

# 💻 Celdas de Código

Ejemplo simple:

```python
1 + 1
```

Resultado aparece debajo.

También puedes:

* Crear variables
* Imprimir valores
* Hacer cálculos
* Crear tablas
* Hacer gráficos

Ejemplo:

```python
x = "nombre"
print(x)
```

---

# 📊 Mostrar Tablas

Ejemplo conceptual usando pandas:

```python
import pandas as pd

df = pd.DataFrame(...)
df
```

La tabla se muestra formateada automáticamente.

---

# 📈 Crear Gráficos

Puedes generar gráficos directamente en el notebook.

Ejemplo conceptual:

```python
import matplotlib.pyplot as plt
plt.plot(...)
plt.show()
```

El gráfico aparece debajo de la celda.

---

# 🖼 Agregar Imágenes

En celda Markdown:

```markdown
![texto](url_de_imagen)
```

También puedes insertar imágenes locales.

---

# ✍️ Celdas Markdown

Sirven para:

* Títulos
* Subtítulos
* Explicaciones
* Conclusiones
* Listas

---

# 🧾 Títulos

```markdown
# Título
## Subtítulo
### Sección
```

---

# 📌 Bullet Points

```markdown
- Primera conclusión
- Segunda conclusión
- Tercera conclusión
```

---

# 🏗 Estructura Recomendada de un Notebook

Una estructura básica profesional sería:

```markdown
# Título del Análisis

## Introducción

## Importación de Librerías

## Carga de Datos

## Análisis

## Visualización

## Conclusiones
```

Luego intercalas:

* Código
* Resultados
* Explicación

Esto es muy importante para tu portafolio.

---

# 💾 Guardar Notebook

* Ctrl + S
* Icono de disquete

Archivo se guarda como:

```id="nb3fw1"
archivo.ipynb
```

---

# 📤 Cómo Compartir un Notebook

Hay dos formas principales:

---

## 1️⃣ Compartir como .ipynb

Ventajas:

* Otra persona puede ejecutarlo
* Puede modificar código

Desventaja:

* Necesita tener Python + Jupyter instalado

---

## 2️⃣ Exportar como HTML

En menú:

File → Export Notebook as → HTML

Ventajas:

* No necesita instalar nada
* Solo lectura
* Perfecto para mostrar análisis

Desventaja:

* No se puede ejecutar código

---

# 🧠 .ipynb vs .html

| Formato | Ejecutable | Requiere Python | Editable |
| ------- | ---------- | --------------- | -------- |
| .ipynb  | Sí         | Sí              | Sí       |
| .html   | No         | No              | No       |

---

# 🎯 Esto es CLAVE para Portafolio

Para entrevistas:

* Subes .ipynb a GitHub
* Subes versión HTML para reclutadores
* O lo conviertes a PDF

Esto te da:

📊 Presentación profesional
📚 Estructura clara
💻 Código reproducible

---

# 🧠 Resumen Mental

Notebook = Documento ejecutable
JupyterLab = Entorno para manejar notebooks
Celda código = lógica
Celda markdown = explicación
Kernel = memoria + ejecución

---

# 🚀 Cómo Esto Se Conecta Con Tu Stack

Ahora tu flujo completo es:

Conda →
Crear entorno →
JupyterLab o VS Code →
Notebook estructurado →
Análisis →
Exportar a HTML →
Compartir

---
