## Readme

This is some script i wrote which finds quadrilateral surface on image, 
transforms this image to make this surface rectangular 
and the crops it to this surface only. 

It works well in many cases, i.e. for extracting presentation slides 
from photos (clearly visible, bright trapezoids on dark background),  
it performs worse if there is a lot of other shapes of similar luminosity 
as main object.

Main functions used:

* **cv2.findContours()** 
* **cv2.findHomography()**
* **cv2.warpPerspective()**

