# 3d-bounding-box-visualization
I share a code to visualize 3d bounding boxes. In specific, this code generates discrete points alone the 3d bounding boxes and save these points as a .txt file. Then we can use the software `CloudCompare` to visualize the 3d bounding box that the code generated. A visualization example is shown below.
![](https://github.com/Prominem/3d-bounding-box-visualization/blob/master/3dbboxes.png)
# Usage
This code is run with Python. A demo can be conducted by running `vis_main.py`. Then open the generated files in the `vis` folder with `CloudCompare`. In particular, the bounding box parameters should be formated as shape (n, 8)--n indicates the number of bounding boxes and digit 8 indicates center coordinates, box size, rotation angle and class index(x,y,z,dx,dy,dx,θ,c).
