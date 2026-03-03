# Detección de Color con Python y OpenCV usando HSV

Video: *Detección de color con Python y OpenCV usando el espacio de color HSV*
https://youtu.be/aFNDh5k3SjU?si=uio3gqQcl6rttiCB
---

# 1️⃣ ¿Qué vamos a hacer?

Vamos a:

* Detectar objetos de un color específico (amarillo).
* Hacerlo en tiempo real con la webcam.
* Usar solo:

  * Python
  * OpenCV
  * NumPy
  * Pillow
* Sin YOLO.
* Sin TensorFlow.
* Sin GPU.
* Solo CPU.

---

# 2️⃣ Idea Principal

En lugar de trabajar en RGB/BGR, trabajamos en **HSV**.

¿Por qué?

Porque en HSV:

* El **Hue (H)** representa directamente el color.
* Es mucho más intuitivo para segmentar colores.
* Separa color de brillo.

---

# 3️⃣ Intuición del Espacio HSV

Imagina un cilindro.

Tiene 3 componentes:

* H → Hue (color)
* S → Saturation (intensidad)
* V → Value (brillo)

Si lo vemos desde arriba:

Es un círculo.

A medida que giramos alrededor del círculo:

Cambia el color.

Entonces:

> Cada color ocupa un rango en el canal Hue.

---

# 4️⃣ Cómo Detectamos un Color

No podemos decir:

“Dame el amarillo exacto”.

Porque el amarillo ocupa un rango.

Entonces definimos:

```text
[Hue_min, Hue_max]
```

Y pedimos:

> Dame todos los píxeles dentro de ese intervalo.

Eso genera una máscara.

---

# 5️⃣ Estructura Básica del Código

## 📌 1. Abrir la Webcam

```python
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("frame", frame)
```

Esto solo muestra la webcam.

---

# 6️⃣ Convertir a HSV

OpenCV trabaja por defecto en BGR.

Convertimos:

```python
hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

Ahora tenemos:

* H
* S
* V

---

# 7️⃣ Definir el Color a Detectar

En el tutorial se usa amarillo:

En BGR:

```python
yellow = [0, 255, 255]
```

Se usa una función auxiliar:

```python
lower_limit, upper_limit = get_limits(color=yellow)
```

Esta función:

* Convierte el color a HSV.
* Devuelve los límites inferior y superior.
* Nos da el intervalo correcto automáticamente.

---

# 8️⃣ Crear la Máscara

Función clave:

```python
mask = cv2.inRange(hsv_image, lower_limit, upper_limit)
```

¿Qué hace?

Para cada píxel:

Si está dentro del rango → blanco (255)
Si no → negro (0)

Resultado:

Imagen binaria.

---

# 9️⃣ Visualizar la Máscara

Si no hay objeto amarillo:

Todo negro.

Si hay limón o banana:

Las zonas amarillas aparecen blancas.

Esto significa:

> Hemos segmentado el color correctamente.

---

# 🔟 Obtener la Bounding Box

Ahora queremos dibujar un rectángulo alrededor del objeto.

Primero convertimos la máscara a formato Pillow:

```python
mask_pil = Image.fromarray(mask)
```

Luego usamos:

```python
bounding_box = mask_pil.getbbox()
```

Esto devuelve:

```text
(x1, y1, x2, y2)
```

Si no hay objeto → None
Si hay objeto → coordenadas válidas.

---

# 1️⃣1️⃣ Dibujar el Rectángulo

Si la bounding box existe:

```python
cv2.rectangle(
    frame,
    (x1, y1),
    (x2, y2),
    (0, 255, 0),
    5
)
```

Resultado:

Rectángulo verde alrededor del objeto amarillo.

---

# 1️⃣2️⃣ Pipeline Completo

```text
Webcam
   ↓
Frame BGR
   ↓
Convertir a HSV
   ↓
Definir rango de color
   ↓
cv2.inRange()
   ↓
Máscara binaria
   ↓
Bounding Box
   ↓
Dibujar rectángulo
```

Todo en tiempo real.

---

# 1️⃣3️⃣ ¿Por Qué HSV y No RGB?

En RGB:

* El color está mezclado con brillo.
* Es difícil definir rangos claros.

En HSV:

* Hue = color puro.
* Más fácil definir intervalos.
* Mejor para segmentación.

---

# 1️⃣4️⃣ Ventajas del Método

✔ Muy rápido
✔ No necesita GPU
✔ No usa redes neuronales
✔ Ideal para objetos de color sólido
✔ Fácil de implementar

---

# 1️⃣5️⃣ Limitaciones

❌ No funciona bien si:

* El fondo tiene el mismo color.
* Cambian mucho las condiciones de luz.
* El objeto tiene muchos colores.

---

# 🧠 Conexión con Otros Temas

Esto conecta con:

* HSV thresholding
* Segmentación
* Histogram backprojection
* Contours
* Object tracking

Este es uno de los pipelines clásicos de visión por computadora.

---

# 🚀 Nivel Siguiente

Podemos ahora:

* Combinar HSV + contornos
* Detectar múltiples colores
* Hacer seguimiento con CamShift
* Calcular centroide
* Estimar área del objeto
* Hacer conteo de objetos por color


