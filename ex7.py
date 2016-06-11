######################################################################
# FILE: ex7.py
# WRITER: Idan Refaeli, idan0610, 305681132
# EXERCISE: intro2cs ex7 2014-2015
# DESCRIPTION:
# functions used for image processing
#######################################################################
from SolveLinear3 import solve_linear_3

START_INDEX = 4
NUM_OF_VERTEXES = 3
NUM_OF_RGB_VALUES = 3


def is_point_inside_triangle(point, v1, v2, v3):
    '''
    The function check if a point is inside a triangle

    :param point: tuple of floats (x, y), coordinates of the point
    :param v1: tuple of floats (x, y), coordinates of vertex 1
    :param v2: tuple of floats (x, y), coordinates of vertex 2
    :param v3: tuple of floats (x, y), coordinates of vertex 3
    :return:tuple (is_inside, results):
    is_inside: True for point inside triangle, False for not
    results: results of a, b, c from equations for checking if the point is
             inside the triangle
    '''

    # Place the coordinates of point and v1, v2, v3 inside variables:

    p_x, p_y = point

    v1_x, v1_y = v1
    v2_x, v2_y = v2
    v3_x, v3_y = v3

    # Create list of lists of coefficients for each equation,
    # and numbers for the right hand of the equations  according
    # the guidance of the Targil
    coefficients_list = [[v1_x, v2_x, v3_x], [v1_y, v2_y, v3_y], [1, 1, 1]]

    right_hand_list = [p_x, p_y, 1]

    # Get answers for a, b, c from equations, according the guidance
    results = solve_linear_3(coefficients_list, right_hand_list)
    a, b, c = results
    is_inside = False

    if 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1:
        # According to guidance, if 0 <= a, b, c <= 1, the point is inside
        # the triangle
        is_inside = True
    elif a < 0 or b < 0 or c < 0:
        # According to guidance, if a or b or c < 0, the point is outside
        # the triangle
        is_inside = False

    return (is_inside, results)


def create_triangles(list_of_points):
    '''
    The function gets a list of points, and returns a lists of triangles
    creates from joining the points

    :param list_of_points: list of tuples of floats (x, y), list of points
    :return: triangles: list of tuples of tuples of floats (x, y, z),
             list of triangles
    '''

    triangles = [] # List of triangles

    # Assume the first 4 points of the corners are exist, create the first 2
    # big triangles
    p1, p2 = list_of_points[0], list_of_points[1]
    p3, p4 = list_of_points[2], list_of_points[3]
    triangles.append((p1, p2, p3))
    triangles.append((p1, p3, p4))

    for i in range(START_INDEX, len(list_of_points)):
        # For each point after the first 4, create 3 new triangles
        current_point = list_of_points[i] #the current point

        index_of_triangle = find_triangle(current_point, triangles) #the
                            #triangle index where current_point is located

        # Delete the triangle the point is located at, but keep its vertexes
        v1, v2, v3 = triangles.pop(index_of_triangle)

        # Create 3 new triangles with v1, v2, v3 and current_point as vertexes
        new_triangle_1 = (v1, v2, current_point)
        new_triangle_2 = (v2, v3, current_point)
        new_triangle_3 = (v1, v3, current_point)

        # Add the triangles to the list to the index where the deleted
        # triangle was located
        triangles.insert(index_of_triangle, new_triangle_1)
        triangles.insert(index_of_triangle, new_triangle_2)
        triangles.insert(index_of_triangle, new_triangle_3)

    return triangles


def find_triangle(point, triangles_list):
    '''
    The function find the triangle where the point is located in
    :param point: tuple of floats (x, y), the point
    :param triangles_list: list of tuples (v1, v2, v3) of tuples (x, y) of
            floats. list of triangles
    :return: i: int, the index of triangle the point is located at
    '''

    for i in range(len(triangles_list)):
        # For every triangle, get its vertexes and check if the point is
        # located inside that triangle. if that so, return the triangle's
        # index
        v1, v2, v3 = triangles_list[i]
        results = is_point_inside_triangle(point, v1, v2, v3)
        is_found = results[0]
        if is_found:
            return i


def do_triangle_lists_match(list_of_points1, list_of_points2):
    '''
    The function check if each 2 points from 2 list of points with the same
    indexes are located on triangles with the same indexes also

    :param list_of_points1: list of tuples (x, y) of floats, list of points
    :param list_of_points2: list of tuples (x, y) of floats, list of points
    :return: True for a perfect match between points and triangles
             False for at least one couple of points located on triangles with
                   different indexes
    '''

    # Creates the lists of triangles
    triangles_list1 = create_triangles(list_of_points1)
    triangles_list2 = create_triangles(list_of_points2)

    for i in range(len(list_of_points1)):
        # For each couple of points, check if the indexes of the triangles
        # The points are located at are the same
        point_i_1 = list_of_points1[i]
        point_i_2 = list_of_points2[i]
        index_of_triangle1 = find_triangle(point_i_1, triangles_list1)
        index_of_triangle2 = find_triangle(point_i_2, triangles_list2)

        if index_of_triangle1 != index_of_triangle2:
            # If we find one couple of points that doesnt match with the
            # triangles indexes, stop the function and return False
            return False

    # No problems were found, so return True
    return True


def get_point_in_segment(p1, p2, alpha):
    '''
    The function find the point located between p1 and p2, so that if for
    example the distance between p1 and p2 is I, so v is located in distance
    alpha * I from p1, and (1-alpha) * I from p2
    :param p1: tuple (x,y) of floats, point 1
    :param p2: tuple (x,y) of floats, point 2
    :param alpha: float, 0 <= alpha <= 1
    :return: v: tuple (v_x, v_y) of floats, the point found
    '''

    # Put the coordinates in variables:
    p1_x, p1_y = p1
    p2_x, p2_y = p2

    # Calculate the coordinates of v, using the guidance from the Targil
    v_x = ((1 - alpha) * p1_x) + (alpha * p2_x)
    v_y = ((1 - alpha) * p1_y) + (alpha * p2_y)

    v = (v_x, v_y) # Create the point

    return v


def get_intermediate_triangles(source_triangles_list, target_triangles_list,
                                                                  alpha):
    '''
    The function finds the intermediate triangles located between each couple
    of triangles in source and target lists of triangles so that if for
    example the distance between triangle 1 and 2 is I, so the new triangle
    is located in distance alpha * I from source triangle, and (1-alpha) * I
    from target triangle

    :param source_triangles_list: tuple of tuples (v1, v2, v3) of tuples (x, y)
                                  of floats. The source triangles list
    :param target_triangles_list: tuple of tuples (v1, v2, v3) of tuples (x, y)
                                  of floats. The target triangles list
    :param alpha: float, 0 <= alpha <= 1
    :return: intermediate_triangles: tuple of tuples (v1, v2, v3) of tuples
            (x, y) of floats. The intermediate triangles
    '''

    intermediate_triangles = []

    for i in range(len(source_triangles_list)):
        # Take the triangles with index i from both lists of triangles
        triangle_source = source_triangles_list[i]
        triangle_target = target_triangles_list[i]

        vertexes = [0] * NUM_OF_VERTEXES  # List of vertexes
        for j in range(NUM_OF_VERTEXES):
            # Find the new vertex using get_point in segment and add to
            # vertexes list
            v_s = triangle_source[j]
            v_t = triangle_target[j]
            v = get_point_in_segment(v_s, v_t, alpha)
            vertexes[j] = v

        # Create new intermediate triangle from the vertexes and add it
        # to the intermediate_triangles list
        new_triangle = (vertexes[0], vertexes[1], vertexes[2])
        intermediate_triangles.append(new_triangle)

    return intermediate_triangles


# until here should be submitted by next week - 18.12.2014


def get_array_of_matching_points(size, triangles_list,
                                 intermediate_triangles_list):
    '''
    The function finds matches of points for every couple of points from
    triangles_list and intermediate_triangles_list

    :param size: tuple (max_x, max_y) of floats, the size of the image
    :param triangles_list: list of tuples (v1, v2, v3) of tuples (x, y) of
                           floats. List of triangles
    :param intermediate_triangles_list: list of tuples (v1, v2, v3) of tuples
                                        (x, y) of floats. List of
                                        intermediate triangles
    :return: matching_points: list of lists max_x X max _y:
             matching_points[y][x] has the mathing point (x, y) from
             triangles_list
    '''

    max_x, max_y = size
    matching_points = []  # The array of the matching points
    i = 0  # the index of the triangles from both lists of triangles, the
           # matching points are located

    for y in range(max_y):
        matching_points.append([]) # New row in image
        for x in range(max_x):
            point = (x, y)

            # In order to optimize the program, check if the current point is
            # located on the same triangle of previous point, and take its
            # coefficients from is_point_inside_triangle. Only if it's not the
            # same triangle, find the new triangle and take its coefficients
            v1_i, v2_i, v3_i = intermediate_triangles_list[i]
            is_inside, results = is_point_inside_triangle(point, v1_i, v2_i, \
                                                          v3_i)
            if not is_inside:
                # If the current point is not located on the same triangle of
                # previous point, find the new coefficients
                i = find_triangle(point, intermediate_triangles_list)
                v1_i, v2_i, v3_i = intermediate_triangles_list[i]
                is_inside, results = is_point_inside_triangle(point, v1_i, \
                                                              v2_i, v3_i)

            a, b, c = results  # The coefficients of the right triangle

            # Take the vertexes of the triangle with the same index i of
            # the triangle from intermediate_triangles_list
            v1, v2, v3 = triangles_list[i]
            v1_x, v1_y = v1
            v2_x, v2_y = v2
            v3_x, v3_y = v3

            # Find the matching point according the guidance from Targil
            new_x = a * v1_x + b * v2_x + c * v3_x
            new_y = a * v1_y + b * v2_y + c * v3_y

            # Add the found matching point to matching_points[y][x]
            matching_points[y].append((new_x, new_y))

    return matching_points


def create_intermediate_image(alpha, size, source_image, target_image,
                              source_triangles_list, target_triangles_list):
    '''
    The function creates 1 frame from the sequence of frames

    :param alpha: float, 0 <= alpha <= 1
    :param size: tuple (max_x, max_y) of floats, the size of the image
    :param source_image: image, the source image
    :param target_image: image, the target image
    :param source_triangles_list: tuple of tuples (v1, v2, v3) of tuples (x, y)
                                  of floats. The source triangles list
    :param target_triangles_list: tuple of tuples (v1, v2, v3) of tuples (x, y)
                                  of floats. The target triangles list
    :return: image: list of lists max_x X max_y:
             image[y][x] contains the pixel (R, G, B) of the current point
             on frame
    '''

    max_x, max_y = size
    image = []  # The frame the function creating right now

    # Find the intermediate triangles list using get_intermediate_triangles
    intermediate_triangles_list = get_intermediate_triangles(\
        source_triangles_list, target_triangles_list, alpha)

    # Find the matching points of each point from the intermediate triangles
    # list and source / target triangles list
    matching_points_source = get_array_of_matching_points(size, \
        source_triangles_list, intermediate_triangles_list)
    matching_points_target = get_array_of_matching_points(size, \
        target_triangles_list, intermediate_triangles_list)

    for y in range(max_y):
        image.append([]) # New row on image
        for x in range(max_x):
            # Take the matching points from matching_points_source and
            # matching_points_target of the current point
            source_match_point = matching_points_source[y][x]
            target_match_point = matching_points_target[y][x]

            source_x, source_y = source_match_point
            target_x, target_y = target_match_point

            # Take the pixels of the matching points from the source and
            # target images
            source_RGB = source_image[source_x, source_y]
            target_RGB = target_image[target_x, target_y]

            RGB_values = []  # The RGB values of the new pixel
            for i in range(NUM_OF_RGB_VALUES):
                # Find the current value of R / G / B using the guidance
                # from the Targil and add it to RGB_values
                value = int((1 - alpha) * source_RGB[i] + \
                            alpha * target_RGB[i])
                RGB_values.append(value)

            # Convert RGB_values to tuple and the new pixel to image[y][x]
            image[y].append(tuple(RGB_values))

    return image


def create_sequence_of_images(size, source_image, target_image, 
                source_triangles_list, target_triangles_list, num_frames):
    '''
    The function creates a sequence of frames, each frame using
    create_intermediate_triangles

    :param size: tuple (max_x, max_y) of floats, the size of the image
    :param source_image: image, the source image
    :param target_image: image, the target image
    :param source_triangles_list: tuple of tuples (v1, v2, v3) of tuples (x, y)
                                  of floats. The source triangles list
    :param target_triangles_list: tuple of tuples (v1, v2, v3) of tuples (x, y)
                                  of floats. The target triangles list
    :param num_frames: int, the requested number of frames
    :return: sequences_of images: list of images returned from
                                  create_intermediate_triangles
    '''

    sequence_of_images = []  # List of frames

    for i in range(num_frames):
        # For each frame, calculate the current alpha according the guidance
        # from Targil and create a new frame using create_intemediate_image
        alpha = i / (num_frames - 1)
        image = create_intermediate_image(alpha, size, source_image, \
            target_image, source_triangles_list, target_triangles_list)

        # Add the new image to sequences_of_images
        sequence_of_images.append(image)

    return sequence_of_images


# until here should be submitted by 25.12.2014