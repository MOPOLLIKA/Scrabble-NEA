from PIL import Image

# Load the image
image_path = "Scrabble_(2003)-1-1.png"
image = Image.open(image_path)

# Get image dimensions and calculate the middle point for vertical split
width, height = image.size
middle = width // 2

# Split the image vertically into two halves
left_half = image.crop((0, 0, middle, height))
right_half = image.crop((middle, 0, width, height))

# Save the two halves as separate PNG files
left_half_path = "Scrabble_rules_left_half.png"
right_half_path = "Scrabble_rules_right_half.png"
left_half.save(left_half_path)
right_half.save(right_half_path)