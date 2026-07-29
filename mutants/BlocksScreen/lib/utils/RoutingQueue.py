import queue
import threading
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


class RoutingQueue(queue.LifoQueue):
    def __init__(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁRoutingQueueǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁRoutingQueueǁ__init____mutmut_mutants'), args, kwargs, self)
    def xǁRoutingQueueǁ__init____mutmut_orig(self):
        # Create a a new LifoQueue object
        queue.LifoQueue.__init__(self)
        # Create another queue associated with the main one
        # This one will be used for resends
        self._resend_queue = queue.Queue()

        # events
        self._clear_to_move = threading.Event()
        self._clear_to_move.set()

        # Resend flag
        self._resend = False

        # Lines in queue
        self._read_lines = 0
    def xǁRoutingQueueǁ__init____mutmut_1(self):
        # Create a a new LifoQueue object
        queue.LifoQueue.__init__(None)
        # Create another queue associated with the main one
        # This one will be used for resends
        self._resend_queue = queue.Queue()

        # events
        self._clear_to_move = threading.Event()
        self._clear_to_move.set()

        # Resend flag
        self._resend = False

        # Lines in queue
        self._read_lines = 0
    def xǁRoutingQueueǁ__init____mutmut_2(self):
        # Create a a new LifoQueue object
        queue.LifoQueue.__init__(self)
        # Create another queue associated with the main one
        # This one will be used for resends
        self._resend_queue = None

        # events
        self._clear_to_move = threading.Event()
        self._clear_to_move.set()

        # Resend flag
        self._resend = False

        # Lines in queue
        self._read_lines = 0
    def xǁRoutingQueueǁ__init____mutmut_3(self):
        # Create a a new LifoQueue object
        queue.LifoQueue.__init__(self)
        # Create another queue associated with the main one
        # This one will be used for resends
        self._resend_queue = queue.Queue()

        # events
        self._clear_to_move = None
        self._clear_to_move.set()

        # Resend flag
        self._resend = False

        # Lines in queue
        self._read_lines = 0
    def xǁRoutingQueueǁ__init____mutmut_4(self):
        # Create a a new LifoQueue object
        queue.LifoQueue.__init__(self)
        # Create another queue associated with the main one
        # This one will be used for resends
        self._resend_queue = queue.Queue()

        # events
        self._clear_to_move = threading.Event()
        self._clear_to_move.set()

        # Resend flag
        self._resend = None

        # Lines in queue
        self._read_lines = 0
    def xǁRoutingQueueǁ__init____mutmut_5(self):
        # Create a a new LifoQueue object
        queue.LifoQueue.__init__(self)
        # Create another queue associated with the main one
        # This one will be used for resends
        self._resend_queue = queue.Queue()

        # events
        self._clear_to_move = threading.Event()
        self._clear_to_move.set()

        # Resend flag
        self._resend = True

        # Lines in queue
        self._read_lines = 0
    def xǁRoutingQueueǁ__init____mutmut_6(self):
        # Create a a new LifoQueue object
        queue.LifoQueue.__init__(self)
        # Create another queue associated with the main one
        # This one will be used for resends
        self._resend_queue = queue.Queue()

        # events
        self._clear_to_move = threading.Event()
        self._clear_to_move.set()

        # Resend flag
        self._resend = False

        # Lines in queue
        self._read_lines = None
    def xǁRoutingQueueǁ__init____mutmut_7(self):
        # Create a a new LifoQueue object
        queue.LifoQueue.__init__(self)
        # Create another queue associated with the main one
        # This one will be used for resends
        self._resend_queue = queue.Queue()

        # events
        self._clear_to_move = threading.Event()
        self._clear_to_move.set()

        # Resend flag
        self._resend = False

        # Lines in queue
        self._read_lines = 1
    
    xǁRoutingQueueǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRoutingQueueǁ__init____mutmut_1': xǁRoutingQueueǁ__init____mutmut_1, 
        'xǁRoutingQueueǁ__init____mutmut_2': xǁRoutingQueueǁ__init____mutmut_2, 
        'xǁRoutingQueueǁ__init____mutmut_3': xǁRoutingQueueǁ__init____mutmut_3, 
        'xǁRoutingQueueǁ__init____mutmut_4': xǁRoutingQueueǁ__init____mutmut_4, 
        'xǁRoutingQueueǁ__init____mutmut_5': xǁRoutingQueueǁ__init____mutmut_5, 
        'xǁRoutingQueueǁ__init____mutmut_6': xǁRoutingQueueǁ__init____mutmut_6, 
        'xǁRoutingQueueǁ__init____mutmut_7': xǁRoutingQueueǁ__init____mutmut_7
    }
    xǁRoutingQueueǁ__init____mutmut_orig.__name__ = 'xǁRoutingQueueǁ__init__'

    @property
    def resend(self):
        """Resend queue"""
        return self._resend

    @resend.setter
    def resend(self, new_resend):
        with self.mutex:
            self._resend = new_resend

    def block(self):
        """Blocks queue"""
        # Sets the flag to false
        self._clear_to_move.clear()

    def unblock(self):
        """Unblock queue"""
        # Sets the flag to True
        self._clear_to_move.set()

    def add_command(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        args = [command, line_number, timestamp, resend, block, timeout]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁRoutingQueueǁadd_command__mutmut_orig'), object.__getattribute__(self, 'xǁRoutingQueueǁadd_command__mutmut_mutants'), args, kwargs, self)

    def xǁRoutingQueueǁadd_command__mutmut_orig(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_1(
        self,
        command,
        line_number,
        timestamp=None,
        resend=True,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_2(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=False,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_3(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_4(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    None, block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_5(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=None, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_6(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=None
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_7(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_8(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_9(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_10(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    None, block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_11(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=None, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_12(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=None
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_13(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_14(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_15(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_16(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines = 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_17(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines -= 1
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_18(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 2
        except Exception as e:
            raise ValueError(
                "Unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_19(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                None
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_20(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "XXUnexpected error while adding a command to queue, and argument %sXX"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_21(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "unexpected error while adding a command to queue, and argument %s"
            ) from e

    def xǁRoutingQueueǁadd_command__mutmut_22(
        self,
        command,
        line_number,
        timestamp=None,
        resend=False,
        block=True,
        timeout=None,
    ):
        """
        Adds a command to the send queue if resend is False
        Adds a command to the resend queue if resend is True
        """
        self._clear_to_move.wait()
        try:
            if command is not None:
                self.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._resend_queue.put(
                    (command, line_number, timestamp), block=block, timeout=timeout
                )
                self._read_lines += 1
        except Exception as e:
            raise ValueError(
                "UNEXPECTED ERROR WHILE ADDING A COMMAND TO QUEUE, AND ARGUMENT %S"
            ) from e
    
    xǁRoutingQueueǁadd_command__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRoutingQueueǁadd_command__mutmut_1': xǁRoutingQueueǁadd_command__mutmut_1, 
        'xǁRoutingQueueǁadd_command__mutmut_2': xǁRoutingQueueǁadd_command__mutmut_2, 
        'xǁRoutingQueueǁadd_command__mutmut_3': xǁRoutingQueueǁadd_command__mutmut_3, 
        'xǁRoutingQueueǁadd_command__mutmut_4': xǁRoutingQueueǁadd_command__mutmut_4, 
        'xǁRoutingQueueǁadd_command__mutmut_5': xǁRoutingQueueǁadd_command__mutmut_5, 
        'xǁRoutingQueueǁadd_command__mutmut_6': xǁRoutingQueueǁadd_command__mutmut_6, 
        'xǁRoutingQueueǁadd_command__mutmut_7': xǁRoutingQueueǁadd_command__mutmut_7, 
        'xǁRoutingQueueǁadd_command__mutmut_8': xǁRoutingQueueǁadd_command__mutmut_8, 
        'xǁRoutingQueueǁadd_command__mutmut_9': xǁRoutingQueueǁadd_command__mutmut_9, 
        'xǁRoutingQueueǁadd_command__mutmut_10': xǁRoutingQueueǁadd_command__mutmut_10, 
        'xǁRoutingQueueǁadd_command__mutmut_11': xǁRoutingQueueǁadd_command__mutmut_11, 
        'xǁRoutingQueueǁadd_command__mutmut_12': xǁRoutingQueueǁadd_command__mutmut_12, 
        'xǁRoutingQueueǁadd_command__mutmut_13': xǁRoutingQueueǁadd_command__mutmut_13, 
        'xǁRoutingQueueǁadd_command__mutmut_14': xǁRoutingQueueǁadd_command__mutmut_14, 
        'xǁRoutingQueueǁadd_command__mutmut_15': xǁRoutingQueueǁadd_command__mutmut_15, 
        'xǁRoutingQueueǁadd_command__mutmut_16': xǁRoutingQueueǁadd_command__mutmut_16, 
        'xǁRoutingQueueǁadd_command__mutmut_17': xǁRoutingQueueǁadd_command__mutmut_17, 
        'xǁRoutingQueueǁadd_command__mutmut_18': xǁRoutingQueueǁadd_command__mutmut_18, 
        'xǁRoutingQueueǁadd_command__mutmut_19': xǁRoutingQueueǁadd_command__mutmut_19, 
        'xǁRoutingQueueǁadd_command__mutmut_20': xǁRoutingQueueǁadd_command__mutmut_20, 
        'xǁRoutingQueueǁadd_command__mutmut_21': xǁRoutingQueueǁadd_command__mutmut_21, 
        'xǁRoutingQueueǁadd_command__mutmut_22': xǁRoutingQueueǁadd_command__mutmut_22
    }
    xǁRoutingQueueǁadd_command__mutmut_orig.__name__ = 'xǁRoutingQueueǁadd_command'

    def get_command(self, block=True, timeout=None, resend=False):
        args = [block, timeout, resend]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁRoutingQueueǁget_command__mutmut_orig'), object.__getattribute__(self, 'xǁRoutingQueueǁget_command__mutmut_mutants'), args, kwargs, self)

    def xǁRoutingQueueǁget_command__mutmut_orig(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    block=block, timeout=timeout
                )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=block, timeout=timeout
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_1(self, block=False, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    block=block, timeout=timeout
                )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=block, timeout=timeout
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_2(self, block=True, timeout=None, resend=True):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    block=block, timeout=timeout
                )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=block, timeout=timeout
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_3(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = ""
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    block=block, timeout=timeout
                )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=block, timeout=timeout
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_4(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if resend:
                _command, _line_number, _timestamp = self.get(
                    block=block, timeout=timeout
                )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=block, timeout=timeout
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_5(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = None

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=block, timeout=timeout
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_6(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    block=None, timeout=timeout
                )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=block, timeout=timeout
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_7(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    block=block, timeout=None
                )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=block, timeout=timeout
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_8(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    timeout=timeout
                )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=block, timeout=timeout
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_9(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    block=block, )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=block, timeout=timeout
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_10(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    block=block, timeout=timeout
                )

            elif resend:
                _command, _line_number, _timestamp = None
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_11(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    block=block, timeout=timeout
                )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=None, timeout=timeout
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_12(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    block=block, timeout=timeout
                )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=block, timeout=None
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_13(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    block=block, timeout=timeout
                )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    timeout=timeout
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_14(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    block=block, timeout=timeout
                )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=block, )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_15(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    block=block, timeout=timeout
                )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=block, timeout=timeout
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    None
                )
            else:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from queue: {e}"
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp

    def xǁRoutingQueueǁget_command__mutmut_16(self, block=True, timeout=None, resend=False):
        """
        Gets a command depending if resend if True or False
            If resend is True then it gets the command from the resend queue.


        """
        self._clear_to_move.wait()
        try:
            _command = _line_number = _timestamp = None
            if not resend:
                _command, _line_number, _timestamp = self.get(
                    block=block, timeout=timeout
                )

            elif resend:
                _command, _line_number, _timestamp = self._resend_queue.get(
                    block=block, timeout=timeout
                )
        except queue.Empty as e:
            if resend:
                raise queue.Empty(
                    f"Unexpected error while retrieving command from resend queue: {e}"
                )
            else:
                raise queue.Empty(
                    None
                )

        finally:
            # TODO: This is incorrect, i need to return just None if an exception is raised, not a tuple with None
            return _command, _line_number, _timestamp
    
    xǁRoutingQueueǁget_command__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRoutingQueueǁget_command__mutmut_1': xǁRoutingQueueǁget_command__mutmut_1, 
        'xǁRoutingQueueǁget_command__mutmut_2': xǁRoutingQueueǁget_command__mutmut_2, 
        'xǁRoutingQueueǁget_command__mutmut_3': xǁRoutingQueueǁget_command__mutmut_3, 
        'xǁRoutingQueueǁget_command__mutmut_4': xǁRoutingQueueǁget_command__mutmut_4, 
        'xǁRoutingQueueǁget_command__mutmut_5': xǁRoutingQueueǁget_command__mutmut_5, 
        'xǁRoutingQueueǁget_command__mutmut_6': xǁRoutingQueueǁget_command__mutmut_6, 
        'xǁRoutingQueueǁget_command__mutmut_7': xǁRoutingQueueǁget_command__mutmut_7, 
        'xǁRoutingQueueǁget_command__mutmut_8': xǁRoutingQueueǁget_command__mutmut_8, 
        'xǁRoutingQueueǁget_command__mutmut_9': xǁRoutingQueueǁget_command__mutmut_9, 
        'xǁRoutingQueueǁget_command__mutmut_10': xǁRoutingQueueǁget_command__mutmut_10, 
        'xǁRoutingQueueǁget_command__mutmut_11': xǁRoutingQueueǁget_command__mutmut_11, 
        'xǁRoutingQueueǁget_command__mutmut_12': xǁRoutingQueueǁget_command__mutmut_12, 
        'xǁRoutingQueueǁget_command__mutmut_13': xǁRoutingQueueǁget_command__mutmut_13, 
        'xǁRoutingQueueǁget_command__mutmut_14': xǁRoutingQueueǁget_command__mutmut_14, 
        'xǁRoutingQueueǁget_command__mutmut_15': xǁRoutingQueueǁget_command__mutmut_15, 
        'xǁRoutingQueueǁget_command__mutmut_16': xǁRoutingQueueǁget_command__mutmut_16
    }
    xǁRoutingQueueǁget_command__mutmut_orig.__name__ = 'xǁRoutingQueueǁget_command'

    def clear_queues(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁRoutingQueueǁclear_queues__mutmut_orig'), object.__getattribute__(self, 'xǁRoutingQueueǁclear_queues__mutmut_mutants'), args, kwargs, self)

    def xǁRoutingQueueǁclear_queues__mutmut_orig(self):
        """
        Clears both the MAIN and RESEND queues

        Returns:
            True if the queues are all empty
            False if one of the queues or both of them are not emty
        """
        if self.empty():
            return

        try:
            with (
                self.mutex
            ):  # This mutex is already associated with queeus no need to declare it
                # Clear the MAIN queue and the RESEND queue
                self.queue.clear()
            with self._resend_queue.mutex:
                self._resend_queue.queue.clear()

            return True
        except Exception as e:
            raise Exception(f"Unexpected error while clearing queues, error: {e}")
        finally:
            return False

    def xǁRoutingQueueǁclear_queues__mutmut_1(self):
        """
        Clears both the MAIN and RESEND queues

        Returns:
            True if the queues are all empty
            False if one of the queues or both of them are not emty
        """
        if self.empty():
            return

        try:
            with (
                self.mutex
            ):  # This mutex is already associated with queeus no need to declare it
                # Clear the MAIN queue and the RESEND queue
                self.queue.clear()
            with self._resend_queue.mutex:
                self._resend_queue.queue.clear()

            return False
        except Exception as e:
            raise Exception(f"Unexpected error while clearing queues, error: {e}")
        finally:
            return False

    def xǁRoutingQueueǁclear_queues__mutmut_2(self):
        """
        Clears both the MAIN and RESEND queues

        Returns:
            True if the queues are all empty
            False if one of the queues or both of them are not emty
        """
        if self.empty():
            return

        try:
            with (
                self.mutex
            ):  # This mutex is already associated with queeus no need to declare it
                # Clear the MAIN queue and the RESEND queue
                self.queue.clear()
            with self._resend_queue.mutex:
                self._resend_queue.queue.clear()

            return True
        except Exception as e:
            raise Exception(None)
        finally:
            return False

    def xǁRoutingQueueǁclear_queues__mutmut_3(self):
        """
        Clears both the MAIN and RESEND queues

        Returns:
            True if the queues are all empty
            False if one of the queues or both of them are not emty
        """
        if self.empty():
            return

        try:
            with (
                self.mutex
            ):  # This mutex is already associated with queeus no need to declare it
                # Clear the MAIN queue and the RESEND queue
                self.queue.clear()
            with self._resend_queue.mutex:
                self._resend_queue.queue.clear()

            return True
        except Exception as e:
            raise Exception(f"Unexpected error while clearing queues, error: {e}")
        finally:
            return True
    
    xǁRoutingQueueǁclear_queues__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRoutingQueueǁclear_queues__mutmut_1': xǁRoutingQueueǁclear_queues__mutmut_1, 
        'xǁRoutingQueueǁclear_queues__mutmut_2': xǁRoutingQueueǁclear_queues__mutmut_2, 
        'xǁRoutingQueueǁclear_queues__mutmut_3': xǁRoutingQueueǁclear_queues__mutmut_3
    }
    xǁRoutingQueueǁclear_queues__mutmut_orig.__name__ = 'xǁRoutingQueueǁclear_queues'
