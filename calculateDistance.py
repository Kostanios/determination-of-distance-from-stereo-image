# pixel_size = 2.834645


def calculate_distance(camera_delta, delta, F, matrix_size, pixel_size):
    print([camera_delta], ' ', [delta], ' ', [F], ' ', matrix_size)
    return float(camera_delta) * float(F) / (float(pixel_size) * float(delta))
