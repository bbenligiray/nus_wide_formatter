# NUS-WIDE Formatter

A tool to download (to be implemented, right now it uses offline data) and format NUS-WIDE dataset

It outputs a .h5 file that contains the following:

* data_types: 'train' and 'val'
* cats: names of the 81 categories
(replace x with any data type)
* x_images: flattened images (not preprocessed in any way)
* x_shapes: shapes of the images, to reshape the flattened images
* x_names: file names of the images
* x_label: a one-hot integer vector of labels

### My NUS WIDE stats:

Train
Total: 161789
Missing: 28638
Unlabeled: 66916
Remaining: 66235

Test
Total: 107859
Missing: 18924
Unlabeled: 44305
Remaining: 44630