# HINT: Use Image ID as foreign key
SEMANTICS_FILE = 'test.txt'
AVA_FILE = 'AVA 2.0.txt'

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
max_tags = None

# Append 0s wherever necessary

# Create new string

# Open 'AVA 2.0'

# Semantic Tag IDs goes before challenge ID (Index -1)

# Store again (Follow AVA 1.0 format)