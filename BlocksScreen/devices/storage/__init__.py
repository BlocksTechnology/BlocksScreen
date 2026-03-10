from .usb_controller import USBManager

__doc__ = """

The storage package contains a tool that monitors 
pluggable usb devices via python-sdbus library. 
While offering an automounting option.
The package is also capable of creating a symlink that 
points directly to the mounted usb drive on the gcodes
directory. 


There is still a lot of functionality missing, that may 
be added in the future, but for now it just automounts, 
creates symlinks, cleans up broken symlinks on the 
gcodes directory.


All tools related to storage devices should be contained 
in this package directory. 
"""
__version__ = "0.0.1"
__all__ = ["USBManager"]
__name__ = "storage"
