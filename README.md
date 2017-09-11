# NUS-WIDE Formatter

A tool to format NUS-WIDE dataset. It outputs a .h5 file that contains the following:

* data_types: 'train' and 'val'
* cats: names of the 81 categories

(replace x with any data type)

* x_images: flattened images (not preprocessed in any way)
* x_shapes: shapes of the images, to reshape the flattened images
* x_names: file names of the images
* x_label: a one-hot integer vector of labels

Follow the instructions here to get a download link of the raw dataset:
http://lms.comp.nus.edu.sg/research/NUS-WIDE.htm