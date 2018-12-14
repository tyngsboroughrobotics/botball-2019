import walla as w
from ctypes import c_int
w = w.w

RES_LOW = 0
RES_MED = 1
RES_HIG = 2
RES_NAT = 3


class point2(Structure):
    _fields_ = [("x", c_int),
                ("y", c_int)]


def camera_open(res=RES_LOW):
    """
    @summary: opens the camera at the specified resolution
    @param res: the desired resolution; one of RES_LOW, RES_MED, RES_HIG, RES_NAT
    @type res: number
    """

    w.camera_open_at_res(c_int(res))


def camera_close():
    """
    @summary: closes the camera
    """

    w.camera_close()


def camera_open_device(number, res=RES_LOW):
    """
    @summary: opens the camera specified with the number(if multiple cameras are plugged in)
    @param number: the number of the camera to open
    @type number: number
    @param res: the desired resolution; one of RES_LOW, RES_MED, RES_HIG, RES_NAT
    @type res: number
    """

    w.camera_open_device(number, res)


def camera_load_config(filename):
    """
    @summary: loads a different camera configuration file
    @param filename: the name of the configuration file
    @type filename: string
    @return: 1 if the configuration was loaded, 0 otherwise
    @rtype: bool
    """

    w.camera_load_config(filename)


def set_camera_width(width):
    """
    @summary: sets the width of the camera
    @param width: the desired width
    @type width: number
    """

    w.set_camera_width(width)


def set_camera_height(height):
    """
    @summary: sets the height of the camera
    @param height: the desired height
    @type height: number
    """

    w.set_camera_height(height)


def get_camera_width():
    """
    @summary: gets the width of the camera
    @return: the width
    @rtype: number
    """

    return w.get_camera_width()


def get_camera_height():
    """
    @summary: gets the height of the camera
    @return: the height
    @rtype: number
    """

    return w.set_camera_height()


def camera_update():
    """
    @summary: updates the camera to process the current image
    @return: 1 if the camera could be updated, 0 otherwise
    @rtype: bool
    """

    return w.camera_update()


def get_camera_pixel(x, y):
    """
    @summary: returns the color values for the specified pixel
    @param x: the x coordinate of the pixel
    @type x: number
    @param y: the y coordinate of the pixel
    @type y: number
    @return: the pixel
    @rtype: object in the format { 'r': 0, 'g': 0, 'b': 0 }
    """

    pos = point2(x, y)
    pixel = w.get_camera_pixel(pos)
    retObj = {}
    retObj['r'] = pixel.r
    retObj['g'] = pixel.g
    retObj['b'] = pixel.b
    return retObj


def get_channel_count():
    """
    @summary: gets the amount of camera channels
    @return: the amount of channels
    @rtype: number
    """

    return w.get_channel_count()


def check_channel(number):
    """
    @summary: checks if a channel exists
    @param number: the number of the channel
    @type number: number
    @return: 1 if the channel exists, 0 otherwise
    @rtype: bool
    """

    return w.check_channel(number)


def check_channel_and_object(channel, obj):
    """
    @summary: checks if a channel exists and contains a specific object
    @param channel: the number of the channel
    @type channel: number
    @param obj: the number of the object
    @type obj: number
    @return: 1 if the channel and the object exists, 0 otherwise
    @rtype: bool
    """

    return w.check_channel_and_object(channel, obj)


def get_object_count(channel):
    """
    @summary: gets the amount of objects in a channel
    @param channel: the number of the channel
    @type channel: number
    @return: the number of objects
    @rtype: number
    """

    return w.get_object_count(channel)


def get_object_confidence(channel, obj):
    """
    @summary: gets the confidence for an object
    @param channel: the number of the channel
    @type channel: number
    @param obj: the number of the object
    @type obj: number
    @return: the confidence
    @rtype: number
    """

    return w.get_object_confidence(channel, obj)


def get_qr_data(channel, obj):
    """
    @summary: gets the information written on a qr code
    @param channel: the number of the channel
    @type channel: number
    @param obj: the number of the object
    @type obj: number
    @return: the text on the code
    @rtype: string
    """

    return w.get_object_data(channel, obj)


def get_qr_num(channel, obj):
    """
    @summary: gets the information written on a qr code as a number
    @param channel: the number of the channel
    @type channel: number
    @param obj: the number of the object
    @type obj: number
    @return: the information on the code
    @rtype: number
    """

    return w.get_code_num(channel, obj)


def get_qr_len(channel, obj):
    """
    @summary: gets the length of the information written on a qr code
    @param channel: the number of the channel
    @type channel: number
    @param obj: the number of the object
    @type obj: number
    @return: the length of the text on the code
    @rtype: number
    """

    return w.get_object_data_length(channel, obj)


def get_object_area(channel, obj):
    """
    @summary: gets the area of an object
    @param channel: the number of the channel
    @type channel: number
    @param obj: the number of the object
    @type obj: number
    @return: the area of the object
    @rtype: number
    """

    return w.get_object_area(channel, obj)


def get_object_bbox(channel, obj):
    """
    @summary: gets the bounding box of an object
    @param channel: the number of the channel
    @type channel: number
    @param obj: the number of the object
    @type obj: number
    @return: the bounding box
    @rtype: object in the format { 'x': 0, 'y': 0, 'width': 0, 'height': 0 }
    """

    rect = w.get_object_bbox(channel, obj)
    retObj = {}
    retObj["x"] = rect.ulx
    retObj["y"] = rect.uly
    retObj["width"] = rect.width
    retObj["height"] = rect.height


def get_object_centroid(channel, obj):
    """
    @summary: returns the center of mass of an object
    @param channel: the number of the channel
    @type channel: number
    @param obj: the number of the object
    @type obj: number
    @return: the center
    @rtype: object in the format { 'x': 0, 'y': 0 }
    """

    point = w.get_object_centroid(channel, obj)
    retObj = {}
    retObj['x'] = point.x
    retObj['y'] = point.y
    return retObj


def get_object_center(channel, obj):
    """
    @summary: returns the center of an object
    @param channel: the number of the channel
    @type channel: number
    @param obj: the number of the object
    @type obj: number
    @return: the center
    @rtype: object in the format { 'x': 0, 'y': 0 }
    """

    point = w.get_object_center(channel, obj)
    retObj = {}
    retObj['x'] = point.x
    retObj['y'] = point.y
    return retObj


def set_camera_config_base_path(path):
    """
    @summary: sets the camera configuration base path
    @param path: the path
    @type path: string
    """

    w.set_camera_config_base_path(path)
