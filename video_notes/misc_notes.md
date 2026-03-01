
Position estimation of an object with YOLO using RealSense

24,794 vistas  31 ago 2021
This is a tutorial of how to estimate position of an object in the real world using RealSense camera.

The program is here
https://drive.google.com/drive/folders/1-FxgYAKfAFJofLZS13B6m7ihtzJrZ4Sz

This program was tested with
python 3.6.8
tensorflow-gpu 1.14.0
keras 2.1.5
h5py 2.9.0
numpy 1.17.2
opencv-contrib-python  4.2.0.34


- - - 
Object 6D pose estimation with MegaPose
Online 6D object pose tracking. This approach uses MegaPose as estimator, given the 3D CAD model of the object.

Here is the extracted text from the images:

---

**Comment 1:**

@tomwon5451 
Very cool. But why don't you use FoundationPose?
It should be more powerful.

---

**Comment 2:**

Hola Afonso, por lo que veo en tu canal consigues usar MegaPose6D con éxito y por ello te muestro mis respetos.

A nosotros nos está costando mucho, llevamos un mes entre MegaPose y VISP y no hay manera que funcione.

Megapose no nos renderiza la textura.

Tienes alguna recomendación al respecto ?
Estamos en una situación un poco desesperada.

Muchas gracias de antemano.

Cordialmente,
Xuban

---

**Reply:**

Yes, I was able to run MegaPose6D with ViSP library!
I recommend you to strictly follow all the instructions explained here:
[https://visp-doc.inria.fr/doxygen/visp-daily/tutorial-tracking-megapose.html](https://visp-doc.inria.fr/doxygen/visp-daily/tutorial-tracking-megapose.html)

Given your mentioned problem, you have to ensure that firstly (before anything else) you have a folder with the 3D CAD model of your object.
In this folder, you should have 3 files:
1- model.obj
2- model.mtl
3- texture.jpg

You can find my example of this folder here:
[https://github.com/afonsocastro/visp/tree/master/tutorial/tracking/dnn/data/models/wood_block](https://github.com/afonsocastro/visp/tree/master/tutorial/tracking/dnn/data/models/wood_block)

Personally, I used Blender to create the 3D CAD model of my object. The texture you can either get from real images of your object or you can download some close texture sample to your real object. In my case, since I used a wood block, I just download a very similar wood type texture from here:
[https://www.blenderkit.com/asset-gallery?query=category_subtree:wood+order:-created+is_free:true](https://www.blenderkit.com/asset-gallery?query=category_subtree:wood+order:-created+is_free:true)

Only after you have completed this step (creating a folder containing your object model), you can start setting up ViSP and MegaPose.

Hope this will help you!
If you have further questions, don't hesitate to reach me :)

- - -

