# Vector pointing from the curve control point to the head tip
dx = head_x - vertices[1][0]
dy = head_y - vertices[1][1]
magnitude = (dx**2 + dy**2)**0.5

# Push text 20 units out along that exact edge vector line
offset_x = (dx / magnitude) * 0.05
offset_y = (dy / magnitude) * 0.05