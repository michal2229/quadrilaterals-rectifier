## readme

This is a script I wrote which finds quadrilateral surface on image, 
transforms this image to make this surface rectangular 
and then crops it to this surface only. 

It works well in many cases, i.e. for extracting presentation slides 
from photos (clearly visible, bright trapezoids on dark background),  
it performs worse if there is a lot of other shapes of similar luminosity 
as main object - it needs improvements in this department.

Samples included.

### most important functions used

* **cv2.findContours()** 
* **cv2.findHomography()**
* **cv2.warpPerspective()**

### usage

* place images in *input* dir, open terminal, write *make*, execute, check *output* dir
* use by command:
```bash
python find_rect_and_transform.py <input files> <output dir>
```

### requirements

* Python 2
* OpenCV 2
* NumPy
