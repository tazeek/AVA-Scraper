# HINT: Use Image ID as foreign key
SEMANTICS_FILE = 'test.txt'
AVA_FILE = 'dummy.txt'

# Load 'AVA 2.0 Image Semantics.txt' Dummy: test.txt
# Store as follows: 'Image ID: [Tags]'
image_semantics_dict = {}

# Split lines after Index 0 (Index 0 is id, rest are semantic tag ids)
with open(SEMANTICS_FILE) as file:
	for line in file:
		data = line.split()
		
		# Get key (id) and value (tags)
		image_id = data[0]
		image_tags = data[1:]
		image_semantics_dict[image_id] = image_tags

# Find the maximum number of tags
max_tags = 0

for key, value in image_semantics_dict.items():
	
	if max_tags < len(value):
		max_tags = len(value)

# Append 0s wherever necessary
for key, value in image_semantics_dict.items():

	if len(value) < max_tags:
		concat_val = max_tags - len(value)
		value += list('0' * concat_val)

		image_semantics_dict[key] = value

# Open 'AVA 2.0.txt' Dummy: dummy.txt
image_data_dict = {}

with open(AVA_FILE) as file:
	for line in file:
		data = line.split()

		# Get key (id) and value (index number + ratings + challenge id)
		image_id = data[1]
		value = [data[0]] + data[2:]
		image_data_dict[image_id] = value

# Semantic Tag IDs goes before challenge ID (Index -1)
ava_image_data = []

for key, value in image_semantics_dict.items():
	semantic_data = value
	image_data = image_data_dict[key]

	new_string = [image_data[0], key] + image_data[1:-1] + semantic_data + [image_data[-1]]
	ava_image_data.append(' '.join(new_string))

# Store again (Follow AVA 1.0 format)
with open(AVA_FILE, 'w') as file:
	for data in ava_image_data:
		file.write(data + '\n')