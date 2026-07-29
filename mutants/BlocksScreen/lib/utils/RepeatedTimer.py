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


class RepeatedTimer(threading.Thread):
    def __init__(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
        *args,
        **kwargs,
    ):
        args = [timeout, callback, name, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁRepeatedTimerǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁRepeatedTimerǁ__init____mutmut_mutants'), args, kwargs, self)
    def xǁRepeatedTimerǁ__init____mutmut_orig(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_1(
        self,
        timeout,
        callback,
        name="XXRepeatedTimerXX",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_2(
        self,
        timeout,
        callback,
        name="repeatedtimer",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_3(
        self,
        timeout,
        callback,
        name="REPEATEDTIMER",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_4(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=None)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_5(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=False)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_6(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=True)
        self.name = None
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_7(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=True)
        self.name = name
        self._timeout = None
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_8(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = None
        self._args = args
        self._kwargs = kwargs

        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_9(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = None
        self._kwargs = kwargs

        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_10(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = None

        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_11(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self.running = None
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_12(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self.running = True
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_13(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self.running = False
        self.timeoutEvent = None
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_14(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = None
        self._timer = None
        self.startTimer()
    def xǁRepeatedTimerǁ__init____mutmut_15(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
        *args,
        **kwargs,
    ):
        super().__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = ""
        self.startTimer()
    
    xǁRepeatedTimerǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRepeatedTimerǁ__init____mutmut_1': xǁRepeatedTimerǁ__init____mutmut_1, 
        'xǁRepeatedTimerǁ__init____mutmut_2': xǁRepeatedTimerǁ__init____mutmut_2, 
        'xǁRepeatedTimerǁ__init____mutmut_3': xǁRepeatedTimerǁ__init____mutmut_3, 
        'xǁRepeatedTimerǁ__init____mutmut_4': xǁRepeatedTimerǁ__init____mutmut_4, 
        'xǁRepeatedTimerǁ__init____mutmut_5': xǁRepeatedTimerǁ__init____mutmut_5, 
        'xǁRepeatedTimerǁ__init____mutmut_6': xǁRepeatedTimerǁ__init____mutmut_6, 
        'xǁRepeatedTimerǁ__init____mutmut_7': xǁRepeatedTimerǁ__init____mutmut_7, 
        'xǁRepeatedTimerǁ__init____mutmut_8': xǁRepeatedTimerǁ__init____mutmut_8, 
        'xǁRepeatedTimerǁ__init____mutmut_9': xǁRepeatedTimerǁ__init____mutmut_9, 
        'xǁRepeatedTimerǁ__init____mutmut_10': xǁRepeatedTimerǁ__init____mutmut_10, 
        'xǁRepeatedTimerǁ__init____mutmut_11': xǁRepeatedTimerǁ__init____mutmut_11, 
        'xǁRepeatedTimerǁ__init____mutmut_12': xǁRepeatedTimerǁ__init____mutmut_12, 
        'xǁRepeatedTimerǁ__init____mutmut_13': xǁRepeatedTimerǁ__init____mutmut_13, 
        'xǁRepeatedTimerǁ__init____mutmut_14': xǁRepeatedTimerǁ__init____mutmut_14, 
        'xǁRepeatedTimerǁ__init____mutmut_15': xǁRepeatedTimerǁ__init____mutmut_15
    }
    xǁRepeatedTimerǁ__init____mutmut_orig.__name__ = 'xǁRepeatedTimerǁ__init__'

    def _run(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁRepeatedTimerǁ_run__mutmut_orig'), object.__getattribute__(self, 'xǁRepeatedTimerǁ_run__mutmut_mutants'), args, kwargs, self)

    def xǁRepeatedTimerǁ_run__mutmut_orig(self):
        self.running = False
        self.startTimer()
        self.stopEvent.wait()
        if callable(self._function):
            self._function(*self._args, **self._kwargs)

    def xǁRepeatedTimerǁ_run__mutmut_1(self):
        self.running = None
        self.startTimer()
        self.stopEvent.wait()
        if callable(self._function):
            self._function(*self._args, **self._kwargs)

    def xǁRepeatedTimerǁ_run__mutmut_2(self):
        self.running = True
        self.startTimer()
        self.stopEvent.wait()
        if callable(self._function):
            self._function(*self._args, **self._kwargs)

    def xǁRepeatedTimerǁ_run__mutmut_3(self):
        self.running = False
        self.startTimer()
        self.stopEvent.wait()
        if callable(None):
            self._function(*self._args, **self._kwargs)

    def xǁRepeatedTimerǁ_run__mutmut_4(self):
        self.running = False
        self.startTimer()
        self.stopEvent.wait()
        if callable(self._function):
            self._function(**self._kwargs)

    def xǁRepeatedTimerǁ_run__mutmut_5(self):
        self.running = False
        self.startTimer()
        self.stopEvent.wait()
        if callable(self._function):
            self._function(*self._args, )
    
    xǁRepeatedTimerǁ_run__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRepeatedTimerǁ_run__mutmut_1': xǁRepeatedTimerǁ_run__mutmut_1, 
        'xǁRepeatedTimerǁ_run__mutmut_2': xǁRepeatedTimerǁ_run__mutmut_2, 
        'xǁRepeatedTimerǁ_run__mutmut_3': xǁRepeatedTimerǁ_run__mutmut_3, 
        'xǁRepeatedTimerǁ_run__mutmut_4': xǁRepeatedTimerǁ_run__mutmut_4, 
        'xǁRepeatedTimerǁ_run__mutmut_5': xǁRepeatedTimerǁ_run__mutmut_5
    }
    xǁRepeatedTimerǁ_run__mutmut_orig.__name__ = 'xǁRepeatedTimerǁ_run'

    def startTimer(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁRepeatedTimerǁstartTimer__mutmut_orig'), object.__getattribute__(self, 'xǁRepeatedTimerǁstartTimer__mutmut_mutants'), args, kwargs, self)

    def xǁRepeatedTimerǁstartTimer__mutmut_orig(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = threading.Timer(self._timeout, self._run)
                self._timer.daemon = True
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = False
            self.running = True

    def xǁRepeatedTimerǁstartTimer__mutmut_1(self):
        """Start timer"""
        if self.running is not False:
            try:
                self._timer = threading.Timer(self._timeout, self._run)
                self._timer.daemon = True
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = False
            self.running = True

    def xǁRepeatedTimerǁstartTimer__mutmut_2(self):
        """Start timer"""
        if self.running is True:
            try:
                self._timer = threading.Timer(self._timeout, self._run)
                self._timer.daemon = True
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = False
            self.running = True

    def xǁRepeatedTimerǁstartTimer__mutmut_3(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = None
                self._timer.daemon = True
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = False
            self.running = True

    def xǁRepeatedTimerǁstartTimer__mutmut_4(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = threading.Timer(None, self._run)
                self._timer.daemon = True
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = False
            self.running = True

    def xǁRepeatedTimerǁstartTimer__mutmut_5(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = threading.Timer(self._timeout, None)
                self._timer.daemon = True
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = False
            self.running = True

    def xǁRepeatedTimerǁstartTimer__mutmut_6(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = threading.Timer(self._run)
                self._timer.daemon = True
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = False
            self.running = True

    def xǁRepeatedTimerǁstartTimer__mutmut_7(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = threading.Timer(self._timeout, )
                self._timer.daemon = True
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = False
            self.running = True

    def xǁRepeatedTimerǁstartTimer__mutmut_8(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = threading.Timer(self._timeout, self._run)
                self._timer.daemon = None
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = False
            self.running = True

    def xǁRepeatedTimerǁstartTimer__mutmut_9(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = threading.Timer(self._timeout, self._run)
                self._timer.daemon = False
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = False
            self.running = True

    def xǁRepeatedTimerǁstartTimer__mutmut_10(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = threading.Timer(self._timeout, self._run)
                self._timer.daemon = True
                self._timer.start()
                if self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = False
            self.running = True

    def xǁRepeatedTimerǁstartTimer__mutmut_11(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = threading.Timer(self._timeout, self._run)
                self._timer.daemon = True
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    None
                )
            finally:
                self.running = False
            self.running = True

    def xǁRepeatedTimerǁstartTimer__mutmut_12(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = threading.Timer(self._timeout, self._run)
                self._timer.daemon = True
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = None
            self.running = True

    def xǁRepeatedTimerǁstartTimer__mutmut_13(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = threading.Timer(self._timeout, self._run)
                self._timer.daemon = True
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = True
            self.running = True

    def xǁRepeatedTimerǁstartTimer__mutmut_14(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = threading.Timer(self._timeout, self._run)
                self._timer.daemon = True
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = False
            self.running = None

    def xǁRepeatedTimerǁstartTimer__mutmut_15(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = threading.Timer(self._timeout, self._run)
                self._timer.daemon = True
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = False
            self.running = False
    
    xǁRepeatedTimerǁstartTimer__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRepeatedTimerǁstartTimer__mutmut_1': xǁRepeatedTimerǁstartTimer__mutmut_1, 
        'xǁRepeatedTimerǁstartTimer__mutmut_2': xǁRepeatedTimerǁstartTimer__mutmut_2, 
        'xǁRepeatedTimerǁstartTimer__mutmut_3': xǁRepeatedTimerǁstartTimer__mutmut_3, 
        'xǁRepeatedTimerǁstartTimer__mutmut_4': xǁRepeatedTimerǁstartTimer__mutmut_4, 
        'xǁRepeatedTimerǁstartTimer__mutmut_5': xǁRepeatedTimerǁstartTimer__mutmut_5, 
        'xǁRepeatedTimerǁstartTimer__mutmut_6': xǁRepeatedTimerǁstartTimer__mutmut_6, 
        'xǁRepeatedTimerǁstartTimer__mutmut_7': xǁRepeatedTimerǁstartTimer__mutmut_7, 
        'xǁRepeatedTimerǁstartTimer__mutmut_8': xǁRepeatedTimerǁstartTimer__mutmut_8, 
        'xǁRepeatedTimerǁstartTimer__mutmut_9': xǁRepeatedTimerǁstartTimer__mutmut_9, 
        'xǁRepeatedTimerǁstartTimer__mutmut_10': xǁRepeatedTimerǁstartTimer__mutmut_10, 
        'xǁRepeatedTimerǁstartTimer__mutmut_11': xǁRepeatedTimerǁstartTimer__mutmut_11, 
        'xǁRepeatedTimerǁstartTimer__mutmut_12': xǁRepeatedTimerǁstartTimer__mutmut_12, 
        'xǁRepeatedTimerǁstartTimer__mutmut_13': xǁRepeatedTimerǁstartTimer__mutmut_13, 
        'xǁRepeatedTimerǁstartTimer__mutmut_14': xǁRepeatedTimerǁstartTimer__mutmut_14, 
        'xǁRepeatedTimerǁstartTimer__mutmut_15': xǁRepeatedTimerǁstartTimer__mutmut_15
    }
    xǁRepeatedTimerǁstartTimer__mutmut_orig.__name__ = 'xǁRepeatedTimerǁstartTimer'

    def stopTimer(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁRepeatedTimerǁstopTimer__mutmut_orig'), object.__getattribute__(self, 'xǁRepeatedTimerǁstopTimer__mutmut_mutants'), args, kwargs, self)

    def xǁRepeatedTimerǁstopTimer__mutmut_orig(self):
        """Stop timer"""
        if self._timer is None:
            return
        if self.running:
            self._timer.cancel()
            self._timer.join()
            self._timer = None
            self.stopEvent.clear()
            self.running = False

    def xǁRepeatedTimerǁstopTimer__mutmut_1(self):
        """Stop timer"""
        if self._timer is not None:
            return
        if self.running:
            self._timer.cancel()
            self._timer.join()
            self._timer = None
            self.stopEvent.clear()
            self.running = False

    def xǁRepeatedTimerǁstopTimer__mutmut_2(self):
        """Stop timer"""
        if self._timer is None:
            return
        if self.running:
            self._timer.cancel()
            self._timer.join()
            self._timer = ""
            self.stopEvent.clear()
            self.running = False

    def xǁRepeatedTimerǁstopTimer__mutmut_3(self):
        """Stop timer"""
        if self._timer is None:
            return
        if self.running:
            self._timer.cancel()
            self._timer.join()
            self._timer = None
            self.stopEvent.clear()
            self.running = None

    def xǁRepeatedTimerǁstopTimer__mutmut_4(self):
        """Stop timer"""
        if self._timer is None:
            return
        if self.running:
            self._timer.cancel()
            self._timer.join()
            self._timer = None
            self.stopEvent.clear()
            self.running = True
    
    xǁRepeatedTimerǁstopTimer__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRepeatedTimerǁstopTimer__mutmut_1': xǁRepeatedTimerǁstopTimer__mutmut_1, 
        'xǁRepeatedTimerǁstopTimer__mutmut_2': xǁRepeatedTimerǁstopTimer__mutmut_2, 
        'xǁRepeatedTimerǁstopTimer__mutmut_3': xǁRepeatedTimerǁstopTimer__mutmut_3, 
        'xǁRepeatedTimerǁstopTimer__mutmut_4': xǁRepeatedTimerǁstopTimer__mutmut_4
    }
    xǁRepeatedTimerǁstopTimer__mutmut_orig.__name__ = 'xǁRepeatedTimerǁstopTimer'
