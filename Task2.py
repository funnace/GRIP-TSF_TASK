#Color Identification In Images
#Author: Yash Bisht

import cv2
import pandas as pd

img_path = r'C:\ML\CVision\im.jpg'
img = cv2.imread(img_path)

# Resize image to fit the screen
screen_width = 800
screen_height = 600
img = cv2.resize(img, (screen_width, screen_height))

# declaring global variables (are used later on)
clicked = False
r = g = b = x_pos = y_pos = 0
prev_text = ""  # Store previous output text

# Reading csv file with pandas and giving names to each column
csv_path = r'C:\ML\CVision\colors.csv'
index = ["name", "hex_24_bit", "red_8_bit", "green_8_bit", "blue_8_bit", "hue_degrees", "hsl_s", "hsl_l_hsv_s_hsv_v"]
csv = pd.read_csv(csv_path, names=index, header=None)

# Handling non-numeric values in the RGB columns
csv[['red_8_bit', 'green_8_bit', 'blue_8_bit']] = csv[['red_8_bit', 'green_8_bit', 'blue_8_bit']].apply(pd.to_numeric, errors='coerce')
csv = csv.dropna(subset=['red_8_bit', 'green_8_bit', 'blue_8_bit'])

# function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    min_distance = 10000
    cname = ""  # Default value for cname

    for _, row in csv.iterrows():
        r_val, g_val, b_val = row["red_8_bit"], row["green_8_bit"], row["blue_8_bit"]
        distance = abs(R - r_val) + abs(G - g_val) + abs(B - b_val)

        if distance <= min_distance:
            min_distance = distance
            cname = row["name"]

    return cname

# function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    global b, g, r, x_pos, y_pos, clicked

    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    img_copy = img.copy()  # Create a copy of the image to avoid overlapping text

    if clicked:
        # Creating text string to display (Color name and RGB values)
        color_name = get_color_name(r, g, b)
        text = f"{color_name} R={r} G={g} B={b}"

        # Clear the previous output
        img_copy = cv2.rectangle(img_copy, (20, 20), (screen_width - 20, 60), (0, 0, 0), -1)

        # Display the text with background color
        bg_color = (b, g, r)
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        cv2.rectangle(img_copy, (50, 30 - text_size[1]), (50 + text_size[0], 30), bg_color, -1)
        cv2.putText(img_copy, text, (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        prev_text = text  # Update previous output
        clicked = False

    # Display the previous output
    if prev_text:
        bg_color = (0, 0, 0)
        text_size, _ = cv2.getTextSize(prev_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        cv2.rectangle(img_copy, (50, 30 - text_size[1]), (50 + text_size[0], 30), bg_color, -1)
        cv2.putText(img_copy, prev_text, (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("image", img_copy)

    # Check if the window is closed
    if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
        break

    # Wait for 'esc' key to be pressed
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
