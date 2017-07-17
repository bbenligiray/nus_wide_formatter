import os
import numpy as np
from random import shuffle
from PIL import Image

import h5py
from keras.utils.io_utils import HDF5Matrix

def visualize_serialized_dataset(dataset_path, cat_names):
	data = HDF5Matrix(dataset_path, 'data')
	labels = HDF5Matrix(dataset_path, 'labels')
	no_cats = len(cat_names)

	no_images = len(data)

	while 1:
		# get a random image
		ind = np.random.randint(0, no_images)

		# show the image
		image_data = data[ind]
		image = Image.fromarray(image_data, 'RGB')
		image.show()
		
		# print the labels
		label = labels[ind]
		print 'Categories'
		for i in range(no_cats):
			if label[i] == 1:
				print cat_names[i]

		raw_input("Press Enter to continue...")

def serialize_dataset(image_path, image_names, image_tags, output_path):

	no_images = len(image_names)
	no_cats = 81

	# create the output file
	f = h5py.File(output_path, 'w')
	data_h = f.create_dataset('data', (no_images, 224, 224, 3), dtype='uint8')
	label_h = f.create_dataset('labels', (no_images, no_cats), dtype='i') 

	for ind in range(no_images):
		# read image and preprocess
		image = Image.open(os.path.join(image_path, image_names[ind]))
		image = image.resize((224, 224), Image.BILINEAR)
		n_image = np.array(image)
		if len(n_image.shape) == 2:
			n_image = np.repeat(n_image[:, :, np.newaxis], 3, axis = 2)
		# write the image to the h5 file
		data_h[ind, :, :, :] = n_image

		label_h[ind, :] = image_tags[ind, :]

	f.close()

def create_cat_names(cat_names_path):

	with open(cat_names_path, 'r') as f:
		cat_names = f.read().splitlines()

	with open('NUS_WIDE_cats', 'w') as f:
		for cat in cat_names:
			print>>f, cat

	return cat_names

def main():

	dataset_path = ''
	image_path = os.path.join(dataset_path, 'org_images')

	cat_names = create_cat_names(os.path.join(dataset_path, 'NUS_WID_Tags', 'Concepts81.txt'))

	# visualize_serialized_dataset('NUS_WIDE_train.h5', cat_names)

	# read train annotation
	train_image_list_file = open(os.path.join(dataset_path, 'ImageList', 'TrainImagelist.txt'))
	train_tag_file = open(os.path.join(dataset_path, 'NUS_WID_Tags', 'Train_Tags81.txt'))

	train_image_names_raw = train_image_list_file.read().splitlines()
	train_tags_raw = train_tag_file.read().splitlines()

	train_image_names = []
	train_tags_list = []

	no_missing = 0
	no_total = len(train_image_names_raw)

	for ind in range(len(train_image_names_raw)):
		tags = np.fromstring(train_tags_raw[ind], dtype = int, sep = ' ')
		if not np.sum(tags) == 0:
			image_name = train_image_names_raw[ind].split('_')[1]
			try:
				image = Image.open(os.path.join(image_path, image_name))
				train_tags_list.append(tags)
				train_image_names.append(image_name)
			except:
				no_missing = no_missing + 1

	print 'Training: ' + str(no_missing) + '/' + str(no_total) + ' missing'

	combined = list(zip(train_image_names, train_tags_list))
	shuffle(combined)
	train_image_names[:], train_tags_list[:] = zip(*combined)

	train_tags = np.array(train_tags_list)

	train_image_list_file.close()
	train_tag_file.close()

	# read test annotation
	test_image_list_file = open(os.path.join(dataset_path, 'ImageList', 'TestImagelist.txt'))
	test_tag_file = open(os.path.join(dataset_path, 'NUS_WID_Tags', 'Test_Tags81.txt'))

	test_image_names_raw = test_image_list_file.read().splitlines()
	test_tags_raw = test_tag_file.read().splitlines()

	test_image_names = []
	test_tags_list = []

	no_missing = 0
	no_total = len(test_image_names_raw)

	for ind in range(len(test_image_names_raw)):
		tags = np.fromstring(test_tags_raw[ind], dtype = int, sep = ' ')
		if not np.sum(tags) == 0:
			image_name = test_image_names_raw[ind].split('_')[1]
			try:
				image = Image.open(os.path.join(image_path, image_name))
				test_tags_list.append(tags)
				test_image_names.append(image_name)
			except:
				no_missing = no_missing + 1

	print 'Test: ' + str(no_missing) + '/' + str(no_total) + ' missing'

	combined = list(zip(test_image_names, test_tags_list))
	shuffle(combined)
	test_image_names[:], test_tags_list[:] = zip(*combined)

	test_tags = np.array(test_tags_list)

	test_image_list_file.close()
	test_tag_file.close()

	no_cats = len(cat_names)
	examples = []
	for ind in range(no_cats):
		examples.append([])

	for ind_image in range(len(train_tags)):
		for ind_cat in range(no_cats):
			if train_tags[ind_image, ind_cat] == 1:
				examples[ind_cat].append(train_image_names[ind_image])

	ratio_val = 0.1
	list_val = []
	for ind_cat in range(no_cats):
		shuffle(examples[ind_cat])
		list_val += examples[ind_cat][0:int(len(examples[ind_cat]) * ratio_val)]

	list_val = list(set(list_val))

	only_train_image_names = []
	only_train_tags = np.zeros([len(train_image_names) - len(list_val), no_cats], dtype = np.int64)

	val_image_names = []
	val_tags = np.zeros([len(list_val), no_cats], dtype = np.int64)
	
	for ind_image in range(len(train_tags)):
		if train_image_names[ind_image] in list_val:
			val_tags[len(val_image_names)] = train_tags[ind_image]
			val_image_names.append(train_image_names[ind_image])
		else:
			only_train_tags[len(only_train_image_names)] = train_tags[ind_image]
			only_train_image_names.append(train_image_names[ind_image])
			
	serialize_dataset(image_path, train_image_names, train_tags, 'NUS_WIDE_trainval.h5')
	serialize_dataset(image_path, only_train_image_names, only_train_tags, 'NUS_WIDE_train.h5')
	serialize_dataset(image_path, val_image_names, val_tags, 'NUS_WIDE_val.h5')
	serialize_dataset(image_path, test_image_names, test_tags, 'NUS_WIDE_test.h5')

	visualize_serialized_dataset('NUS_WIDE_val.h5', cat_names)

if __name__ == "__main__":
    main()