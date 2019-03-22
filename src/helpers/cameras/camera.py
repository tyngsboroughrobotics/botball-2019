try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from geometry import bbox

CAMERA_CHANNEL = 0
"""The camera channel on which to check for objects. This shouldn't
need to be changed if you use the provided configuration files under
`res/camera-channels`.
"""

OBJECT_CONFIDENCE_THRESHOLD = 0.42
"""The minimum value returned by `get_object_confidence` for an
object to be recognized as "trackable".
"""

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

        w.camera_open() # NOTE: This will cause a SEGFAULT if the camera isn't connected!
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Called when the `with` block exits; cleans up resources.
        """

        w.camera_close()

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
        result = w.camera_load_config(conf_name)
        
        if self.debug:
            print 'Loaded conf name: ', conf_name, 'Result: ', result

        if result is 0:
            raise Exception('Error while loading color config file "' + conf_name + '"!')

        # allow the camera to get its bearings by updating the feed for a bit
        for _ in range(20):
            w.camera_update()
        
    def object_is_present(self, should_update=True):
        """Returns a boolean representing whether an object was found in 
        the camera's field of view of the color `self.current_color`.
        """

        if should_update:
            w.camera_update()

        return w.get_object_count(CAMERA_CHANNEL) >= 1
    
    def current_object_bbox(self, should_update=True):
        return self.object_bbox(0, should_update)

    def object_bbox(self, obj, should_update=True):
        if should_update:
            w.camera_update()

        if not self.object_is_present(should_update=False):
            raise Exception('Tried to get object bbox but no objects are present')

        bbox_c = w.get_object_bbox(CAMERA_CHANNEL, obj)
        obj_bbox = bbox.from_c(bbox_c)

        if self.debug:
            print 'Bounding box of object', obj, '=', obj_bbox
        
        return obj_bbox

    def distance_to_current_object(self, obj_height_mm, should_update=True):
        return self.distance_to_object(0, obj_height_mm, should_update)

    def distance_to_object(self, obj, obj_height_mm, should_update=True):
        if should_update:
            w.camera_update()

        if not self.object_is_present(should_update=False):
            raise Exception('Tried to get distance to object but no objects are present')

        obj_bbox = self.object_bbox(obj, should_update=False)
        
        # the object isn't going to fill the *entire* FOV (because then it
        # wouldn't be picked up by the camera!), so subtract a bit to account
        # for that and make the estimate more accurate
        camera_height = float(w.get_camera_height() - 15)
        
        distance = (camera_height * obj_height_mm) / obj_bbox.height

        if self.debug:
            print 'Distance to object', obj, '=', distance

        return distance 

    def current_object_confidence(self, should_update=True):
        return self.object_confidence(0, should_update)

    def object_confidence(self, obj, should_update=True):
        if should_update:
            w.camera_update()

        if not self.object_is_present(should_update=False):
            raise Exception('Tried to get object confidence but no objects are present')

        confidence = w.get_object_confidence(CAMERA_CHANNEL, obj)

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
            w.camera_update()
        
        is_trackable = self.object_is_present(should_update) and self.object_confidence(obj, should_update=False) > OBJECT_CONFIDENCE_THRESHOLD

        if self.debug:
            print 'Object is trackable:', is_trackable

        return is_trackable
