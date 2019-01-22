try:
    from __wallaby_local import * # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    from wallaby import * # so it works on actual robot

CAMERA_CONFIG_PATH = '/home/root/Documents/KISS/Default User/ths-botball-2019/res/camera-channels/'
"""The path for the camera configuration files. This shouldn't need
to be changed if you use the provided configuration files under
`res/camera-channels`.
"""

CAMERA_CHANNEL = 0
"""The camera channel on which to check for objects. This shouldn't
need to be changed if you use the provided configuration files under
`res/camera-channels`.
"""

OBJECT_CONFIDENCE_THRESHOLD = 0.42
"""The minimum value returned by `get_object_confidence` for an
object to be recognized as "trackable".
"""

class point:
    x = None
    y = None

    @classmethod
    def from_c(cls, c_obj):
        self = cls() 
        self.x = c_obj.x 
        self.y = c_obj.y 

        return self 


class bbox:
    x = None
    y = None 
    width = None 
    height = None

    @classmethod
    def from_c(cls, c_obj):
        self = cls() 
        self.x = c_obj.ulx
        self.y = c_obj.uly
        self.width = c_obj.width
        self.height = c_obj.height

        return self 

    def center(self):
        center = point()
        center.x = self.x + (self.width / 2)
        center.y = self.y + (self.height / 2)

        return center

class camera:
    """Represents a Logitech USB camera connected to the wallaby.
    
    Usage:

        with camera(color=...) as camera:
            # code...

    NOTE: Make sure that the camera is connected to the wallaby, otherwise
    the program will `SEGFAULT`! (unfortunately this is something we can't
    control; it's coded in libwallaby)
    """

    def __enter__(self):
        """Initializes the camera in a `with` block.
        """

        camera_open() # NOTE: This will cause a SEGFAULT if the camera isn't connected!
        set_camera_config_base_path(CAMERA_CONFIG_PATH)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Called when the `with` block exits; cleans up resources.
        """

        camera_close()

    def __init__(self, color, debug=False):
        """Initializes the camera with the specified parameters.
        
        Arguments:
            color {string} -- Any color specified in `data/camera-channels`.
        """

        self.debug = debug
        self.change_color_to(color)
        
    def change_color_to(self, color):
        """Changes the camera to track objects of the specified color.
        
        Arguments:
            color {string} -- Any color specified in `data/camera-channels`.
        
        Raises:
            Exception -- If there is an error while loading the color
                         configuration file.
        """

        self.current_color = color
        
        conf_name = 'detect-' + color # DON'T include the .conf extension
        result = camera_load_config(conf_name)
        
        if self.debug:
            print 'Loaded conf name: ', conf_name, 'Result: ', result

        if result is 0:
            raise Exception('Error while loading color config file "' + conf_name + '"!')
        
    def object_is_present(self, should_update=True):
        """Returns a boolean representing whether an object was found in 
        the camera's field of view of the color `self.current_color`.
        """

        if should_update:
            camera_update()

        return get_object_count(CAMERA_CHANNEL) >= 1
    
    def current_object_bbox(self, should_update=True):
        return self.object_bbox(0, should_update)

    def object_bbox(self, obj, should_update=True):
        if should_update:
            camera_update()

        bbox_c = get_object_bbox(CAMERA_CHANNEL, obj)
        obj_bbox = bbox.from_c(bbox_c)

        if self.debug:
            print 'Bounding box of object', obj, '=', obj_bbox
        
        return obj_bbox

    def distance_to_current_object(self, obj_height_mm, should_update=True):
        return self.distance_to_object(0, obj_height_mm, should_update)

    def distance_to_object(self, obj, obj_height_mm, should_update=True):
        if should_update:
            camera_update()

        if not self.object_is_present(should_update=False): # use the current frame; don't update a second time
            raise Exception('Tried to calculate distance but no objects were present')

        obj_bbox = self.object_bbox(obj, should_update=False)
        
        # the object isn't going to fill the *entire* FOV (because then it
        # wouldn't be picked up by the camera!), so subtract a bit to account
        # for that and make the estimate more accurate
        camera_height = float(get_camera_height() - 15)
        
        distance = (camera_height * obj_height_mm) / obj_bbox.height

        if self.debug:
            print 'Distance to object', obj, '=', distance

        return distance 

    def current_object_confidence(self, should_update=True):
        return self.object_confidence(0, should_update)

    def object_confidence(self, obj, should_update=True):
        if should_update:
            camera_update()

        confidence = get_object_confidence(CAMERA_CHANNEL, obj)

        if self.debug:
            print 'Object confidence:', confidence

        return confidence

    def is_current_object_trackable(self, should_update=True):
        return self.is_object_trackable(0, should_update)

    def is_object_trackable(self, obj, should_update=True):
        """Returns a boolean representing whether an object is considered
        to be close enough to the camera to be trackable.
        
        Arguments:
            channel {int} -- The camera channel on which to track.
        
        Returns:
            bool -- Whether the object is considered trackable.
        """

        if should_update:
            camera_update()
        
        is_trackable = self.object_is_present(should_update) and self.object_confidence(obj, should_update) > OBJECT_CONFIDENCE_THRESHOLD

        if self.debug:
            print 'Object is trackable:', is_trackable

        return is_trackable
