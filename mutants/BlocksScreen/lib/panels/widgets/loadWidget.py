from PyQt6 import QtCore, QtGui, QtWidgets
import enum
import os
from configfile import BlocksScreenConfig, get_configparser
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


class LoadingOverlayWidget(QtWidgets.QLabel):
    """
    A full-overlay widget to display a loading animation (GIF or spinning arc).
    """

    class AnimationGIF(enum.Enum):
        """Animation type"""

        DEFAULT = None
        PLACEHOLDER = "placeholder"

    def __init__(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        args = [parent, initial_anim_type]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁLoadingOverlayWidgetǁ__init____mutmut_orig(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_1(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(None)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_2(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = None
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_3(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 1
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_4(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = None
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_5(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 91.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_6(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = None
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_7(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = False
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_8(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = None
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_9(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 6.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_10(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = None
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_11(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 151.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_12(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = None

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_13(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 3.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_14(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = None
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_15(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = ""

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_16(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type != LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_17(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = None
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_18(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "XX~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gifXX"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_19(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/blocksscreen/blocksscreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_20(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BLOCKSSCREEN/BLOCKSSCREEN/LIB/UI/RESOURCES/INTRO_BLOCKS.GIF"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_21(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = None

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_22(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = None
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_23(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = None
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_24(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    None,
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_25(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(None),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_26(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = None
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_27(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = None

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_28(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT or animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_29(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_30(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = None

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_31(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(None)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_32(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = None

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_33(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(None)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_34(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(None)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_35(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(None)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_36(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(False)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_37(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = None
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_38(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = None
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_39(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(None)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_40(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(None)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_41(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_42(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(None)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_43(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(17)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_44(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText(None)
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_45(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("XXLoading...XX")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_46(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("loading...")
        self.repaint()

    def xǁLoadingOverlayWidgetǁ__init____mutmut_47(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("LOADING...")
        self.repaint()
    
    xǁLoadingOverlayWidgetǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁLoadingOverlayWidgetǁ__init____mutmut_1': xǁLoadingOverlayWidgetǁ__init____mutmut_1, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_2': xǁLoadingOverlayWidgetǁ__init____mutmut_2, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_3': xǁLoadingOverlayWidgetǁ__init____mutmut_3, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_4': xǁLoadingOverlayWidgetǁ__init____mutmut_4, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_5': xǁLoadingOverlayWidgetǁ__init____mutmut_5, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_6': xǁLoadingOverlayWidgetǁ__init____mutmut_6, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_7': xǁLoadingOverlayWidgetǁ__init____mutmut_7, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_8': xǁLoadingOverlayWidgetǁ__init____mutmut_8, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_9': xǁLoadingOverlayWidgetǁ__init____mutmut_9, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_10': xǁLoadingOverlayWidgetǁ__init____mutmut_10, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_11': xǁLoadingOverlayWidgetǁ__init____mutmut_11, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_12': xǁLoadingOverlayWidgetǁ__init____mutmut_12, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_13': xǁLoadingOverlayWidgetǁ__init____mutmut_13, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_14': xǁLoadingOverlayWidgetǁ__init____mutmut_14, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_15': xǁLoadingOverlayWidgetǁ__init____mutmut_15, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_16': xǁLoadingOverlayWidgetǁ__init____mutmut_16, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_17': xǁLoadingOverlayWidgetǁ__init____mutmut_17, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_18': xǁLoadingOverlayWidgetǁ__init____mutmut_18, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_19': xǁLoadingOverlayWidgetǁ__init____mutmut_19, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_20': xǁLoadingOverlayWidgetǁ__init____mutmut_20, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_21': xǁLoadingOverlayWidgetǁ__init____mutmut_21, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_22': xǁLoadingOverlayWidgetǁ__init____mutmut_22, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_23': xǁLoadingOverlayWidgetǁ__init____mutmut_23, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_24': xǁLoadingOverlayWidgetǁ__init____mutmut_24, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_25': xǁLoadingOverlayWidgetǁ__init____mutmut_25, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_26': xǁLoadingOverlayWidgetǁ__init____mutmut_26, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_27': xǁLoadingOverlayWidgetǁ__init____mutmut_27, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_28': xǁLoadingOverlayWidgetǁ__init____mutmut_28, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_29': xǁLoadingOverlayWidgetǁ__init____mutmut_29, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_30': xǁLoadingOverlayWidgetǁ__init____mutmut_30, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_31': xǁLoadingOverlayWidgetǁ__init____mutmut_31, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_32': xǁLoadingOverlayWidgetǁ__init____mutmut_32, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_33': xǁLoadingOverlayWidgetǁ__init____mutmut_33, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_34': xǁLoadingOverlayWidgetǁ__init____mutmut_34, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_35': xǁLoadingOverlayWidgetǁ__init____mutmut_35, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_36': xǁLoadingOverlayWidgetǁ__init____mutmut_36, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_37': xǁLoadingOverlayWidgetǁ__init____mutmut_37, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_38': xǁLoadingOverlayWidgetǁ__init____mutmut_38, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_39': xǁLoadingOverlayWidgetǁ__init____mutmut_39, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_40': xǁLoadingOverlayWidgetǁ__init____mutmut_40, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_41': xǁLoadingOverlayWidgetǁ__init____mutmut_41, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_42': xǁLoadingOverlayWidgetǁ__init____mutmut_42, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_43': xǁLoadingOverlayWidgetǁ__init____mutmut_43, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_44': xǁLoadingOverlayWidgetǁ__init____mutmut_44, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_45': xǁLoadingOverlayWidgetǁ__init____mutmut_45, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_46': xǁLoadingOverlayWidgetǁ__init____mutmut_46, 
        'xǁLoadingOverlayWidgetǁ__init____mutmut_47': xǁLoadingOverlayWidgetǁ__init____mutmut_47
    }
    xǁLoadingOverlayWidgetǁ__init____mutmut_orig.__name__ = 'xǁLoadingOverlayWidgetǁ__init__'

    def set_animation_path(self, path: str) -> None:
        args = [path]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁset_animation_path__mutmut_orig'), object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁset_animation_path__mutmut_mutants'), args, kwargs, self)

    def xǁLoadingOverlayWidgetǁset_animation_path__mutmut_orig(self, path: str) -> None:
        """Set widget animation path"""
        abs_animation_path = os.path.expanduser(path)
        if os.path.isfile(abs_animation_path):
            self.movie = QtGui.QMovie(abs_animation_path)
            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
                self.anim_type = LoadingOverlayWidget.AnimationGIF.PLACEHOLDER
                if self.timer.isActive():
                    self.timer.stop()

    def xǁLoadingOverlayWidgetǁset_animation_path__mutmut_1(self, path: str) -> None:
        """Set widget animation path"""
        abs_animation_path = None
        if os.path.isfile(abs_animation_path):
            self.movie = QtGui.QMovie(abs_animation_path)
            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
                self.anim_type = LoadingOverlayWidget.AnimationGIF.PLACEHOLDER
                if self.timer.isActive():
                    self.timer.stop()

    def xǁLoadingOverlayWidgetǁset_animation_path__mutmut_2(self, path: str) -> None:
        """Set widget animation path"""
        abs_animation_path = os.path.expanduser(None)
        if os.path.isfile(abs_animation_path):
            self.movie = QtGui.QMovie(abs_animation_path)
            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
                self.anim_type = LoadingOverlayWidget.AnimationGIF.PLACEHOLDER
                if self.timer.isActive():
                    self.timer.stop()

    def xǁLoadingOverlayWidgetǁset_animation_path__mutmut_3(self, path: str) -> None:
        """Set widget animation path"""
        abs_animation_path = os.path.expanduser(path)
        if os.path.isfile(None):
            self.movie = QtGui.QMovie(abs_animation_path)
            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
                self.anim_type = LoadingOverlayWidget.AnimationGIF.PLACEHOLDER
                if self.timer.isActive():
                    self.timer.stop()

    def xǁLoadingOverlayWidgetǁset_animation_path__mutmut_4(self, path: str) -> None:
        """Set widget animation path"""
        abs_animation_path = os.path.expanduser(path)
        if os.path.isfile(abs_animation_path):
            self.movie = None
            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
                self.anim_type = LoadingOverlayWidget.AnimationGIF.PLACEHOLDER
                if self.timer.isActive():
                    self.timer.stop()

    def xǁLoadingOverlayWidgetǁset_animation_path__mutmut_5(self, path: str) -> None:
        """Set widget animation path"""
        abs_animation_path = os.path.expanduser(path)
        if os.path.isfile(abs_animation_path):
            self.movie = QtGui.QMovie(None)
            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
                self.anim_type = LoadingOverlayWidget.AnimationGIF.PLACEHOLDER
                if self.timer.isActive():
                    self.timer.stop()

    def xǁLoadingOverlayWidgetǁset_animation_path__mutmut_6(self, path: str) -> None:
        """Set widget animation path"""
        abs_animation_path = os.path.expanduser(path)
        if os.path.isfile(abs_animation_path):
            self.movie = QtGui.QMovie(abs_animation_path)
            if self.movie.isValid():
                self.gifshow.setMovie(None)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
                self.anim_type = LoadingOverlayWidget.AnimationGIF.PLACEHOLDER
                if self.timer.isActive():
                    self.timer.stop()

    def xǁLoadingOverlayWidgetǁset_animation_path__mutmut_7(self, path: str) -> None:
        """Set widget animation path"""
        abs_animation_path = os.path.expanduser(path)
        if os.path.isfile(abs_animation_path):
            self.movie = QtGui.QMovie(abs_animation_path)
            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(None)
                self.movie.start()
                self.gifshow.show()
                self.anim_type = LoadingOverlayWidget.AnimationGIF.PLACEHOLDER
                if self.timer.isActive():
                    self.timer.stop()

    def xǁLoadingOverlayWidgetǁset_animation_path__mutmut_8(self, path: str) -> None:
        """Set widget animation path"""
        abs_animation_path = os.path.expanduser(path)
        if os.path.isfile(abs_animation_path):
            self.movie = QtGui.QMovie(abs_animation_path)
            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(False)
                self.movie.start()
                self.gifshow.show()
                self.anim_type = LoadingOverlayWidget.AnimationGIF.PLACEHOLDER
                if self.timer.isActive():
                    self.timer.stop()

    def xǁLoadingOverlayWidgetǁset_animation_path__mutmut_9(self, path: str) -> None:
        """Set widget animation path"""
        abs_animation_path = os.path.expanduser(path)
        if os.path.isfile(abs_animation_path):
            self.movie = QtGui.QMovie(abs_animation_path)
            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
                self.anim_type = None
                if self.timer.isActive():
                    self.timer.stop()
    
    xǁLoadingOverlayWidgetǁset_animation_path__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁLoadingOverlayWidgetǁset_animation_path__mutmut_1': xǁLoadingOverlayWidgetǁset_animation_path__mutmut_1, 
        'xǁLoadingOverlayWidgetǁset_animation_path__mutmut_2': xǁLoadingOverlayWidgetǁset_animation_path__mutmut_2, 
        'xǁLoadingOverlayWidgetǁset_animation_path__mutmut_3': xǁLoadingOverlayWidgetǁset_animation_path__mutmut_3, 
        'xǁLoadingOverlayWidgetǁset_animation_path__mutmut_4': xǁLoadingOverlayWidgetǁset_animation_path__mutmut_4, 
        'xǁLoadingOverlayWidgetǁset_animation_path__mutmut_5': xǁLoadingOverlayWidgetǁset_animation_path__mutmut_5, 
        'xǁLoadingOverlayWidgetǁset_animation_path__mutmut_6': xǁLoadingOverlayWidgetǁset_animation_path__mutmut_6, 
        'xǁLoadingOverlayWidgetǁset_animation_path__mutmut_7': xǁLoadingOverlayWidgetǁset_animation_path__mutmut_7, 
        'xǁLoadingOverlayWidgetǁset_animation_path__mutmut_8': xǁLoadingOverlayWidgetǁset_animation_path__mutmut_8, 
        'xǁLoadingOverlayWidgetǁset_animation_path__mutmut_9': xǁLoadingOverlayWidgetǁset_animation_path__mutmut_9
    }
    xǁLoadingOverlayWidgetǁset_animation_path__mutmut_orig.__name__ = 'xǁLoadingOverlayWidgetǁset_animation_path'

    def set_status_message(self, message: str) -> None:
        args = [message]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁset_status_message__mutmut_orig'), object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁset_status_message__mutmut_mutants'), args, kwargs, self)

    def xǁLoadingOverlayWidgetǁset_status_message__mutmut_orig(self, message: str) -> None:
        """Set widget message"""
        self.label.setText(message)

    def xǁLoadingOverlayWidgetǁset_status_message__mutmut_1(self, message: str) -> None:
        """Set widget message"""
        self.label.setText(None)
    
    xǁLoadingOverlayWidgetǁset_status_message__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁLoadingOverlayWidgetǁset_status_message__mutmut_1': xǁLoadingOverlayWidgetǁset_status_message__mutmut_1
    }
    xǁLoadingOverlayWidgetǁset_status_message__mutmut_orig.__name__ = 'xǁLoadingOverlayWidgetǁset_status_message'

    def close(self) -> bool:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁclose__mutmut_orig'), object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁclose__mutmut_mutants'), args, kwargs, self)

    def xǁLoadingOverlayWidgetǁclose__mutmut_orig(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = 0
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(self, "movie")
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_1(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText(None)
        self._angle = 0
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(self, "movie")
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_2(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("XXLoading...XX")
        self._angle = 0
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(self, "movie")
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_3(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("loading...")
        self._angle = 0
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(self, "movie")
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_4(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("LOADING...")
        self._angle = 0
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(self, "movie")
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_5(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = None
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(self, "movie")
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_6(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = 1
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(self, "movie")
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_7(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = 0
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(self, "movie") or self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_8(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = 0
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT or hasattr(self, "movie")
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_9(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = 0
        if (
            self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(self, "movie")
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_10(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = 0
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(None, "movie")
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_11(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = 0
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(self, None)
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_12(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = 0
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr("movie")
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_13(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = 0
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(self, )
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_14(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = 0
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(self, "XXmovieXX")
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()

    def xǁLoadingOverlayWidgetǁclose__mutmut_15(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = 0
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(self, "MOVIE")
            and self.movie.isValid()
        ):
            self.movie.stop()
        return super().close()
    
    xǁLoadingOverlayWidgetǁclose__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁLoadingOverlayWidgetǁclose__mutmut_1': xǁLoadingOverlayWidgetǁclose__mutmut_1, 
        'xǁLoadingOverlayWidgetǁclose__mutmut_2': xǁLoadingOverlayWidgetǁclose__mutmut_2, 
        'xǁLoadingOverlayWidgetǁclose__mutmut_3': xǁLoadingOverlayWidgetǁclose__mutmut_3, 
        'xǁLoadingOverlayWidgetǁclose__mutmut_4': xǁLoadingOverlayWidgetǁclose__mutmut_4, 
        'xǁLoadingOverlayWidgetǁclose__mutmut_5': xǁLoadingOverlayWidgetǁclose__mutmut_5, 
        'xǁLoadingOverlayWidgetǁclose__mutmut_6': xǁLoadingOverlayWidgetǁclose__mutmut_6, 
        'xǁLoadingOverlayWidgetǁclose__mutmut_7': xǁLoadingOverlayWidgetǁclose__mutmut_7, 
        'xǁLoadingOverlayWidgetǁclose__mutmut_8': xǁLoadingOverlayWidgetǁclose__mutmut_8, 
        'xǁLoadingOverlayWidgetǁclose__mutmut_9': xǁLoadingOverlayWidgetǁclose__mutmut_9, 
        'xǁLoadingOverlayWidgetǁclose__mutmut_10': xǁLoadingOverlayWidgetǁclose__mutmut_10, 
        'xǁLoadingOverlayWidgetǁclose__mutmut_11': xǁLoadingOverlayWidgetǁclose__mutmut_11, 
        'xǁLoadingOverlayWidgetǁclose__mutmut_12': xǁLoadingOverlayWidgetǁclose__mutmut_12, 
        'xǁLoadingOverlayWidgetǁclose__mutmut_13': xǁLoadingOverlayWidgetǁclose__mutmut_13, 
        'xǁLoadingOverlayWidgetǁclose__mutmut_14': xǁLoadingOverlayWidgetǁclose__mutmut_14, 
        'xǁLoadingOverlayWidgetǁclose__mutmut_15': xǁLoadingOverlayWidgetǁclose__mutmut_15
    }
    xǁLoadingOverlayWidgetǁclose__mutmut_orig.__name__ = 'xǁLoadingOverlayWidgetǁclose'

    def _update_animation(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_orig'), object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_mutants'), args, kwargs, self)

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_orig(self) -> None:
        self._angle = (self._angle + 5) % 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_1(self) -> None:
        self._angle = None
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_2(self) -> None:
        self._angle = (self._angle + 5) / 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_3(self) -> None:
        self._angle = (self._angle - 5) % 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_4(self) -> None:
        self._angle = (self._angle + 6) % 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_5(self) -> None:
        self._angle = (self._angle + 5) % 361
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_6(self) -> None:
        self._angle = (self._angle + 5) % 360
        if self._is_span_growing:
            self._span_angle = self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_7(self) -> None:
        self._angle = (self._angle + 5) % 360
        if self._is_span_growing:
            self._span_angle -= self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_8(self) -> None:
        self._angle = (self._angle + 5) % 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle > self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_9(self) -> None:
        self._angle = (self._angle + 5) % 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = None
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_10(self) -> None:
        self._angle = (self._angle + 5) % 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = None
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_11(self) -> None:
        self._angle = (self._angle + 5) % 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = True
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_12(self) -> None:
        self._angle = (self._angle + 5) % 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle = self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_13(self) -> None:
        self._angle = (self._angle + 5) % 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle += self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_14(self) -> None:
        self._angle = (self._angle + 5) % 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle < self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_15(self) -> None:
        self._angle = (self._angle + 5) % 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = None
                self._is_span_growing = True
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_16(self) -> None:
        self._angle = (self._angle + 5) % 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = None
        self.update()

    def xǁLoadingOverlayWidgetǁ_update_animation__mutmut_17(self) -> None:
        self._angle = (self._angle + 5) % 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = False
        self.update()
    
    xǁLoadingOverlayWidgetǁ_update_animation__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_1': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_1, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_2': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_2, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_3': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_3, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_4': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_4, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_5': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_5, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_6': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_6, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_7': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_7, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_8': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_8, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_9': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_9, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_10': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_10, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_11': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_11, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_12': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_12, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_13': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_13, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_14': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_14, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_15': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_15, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_16': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_16, 
        'xǁLoadingOverlayWidgetǁ_update_animation__mutmut_17': xǁLoadingOverlayWidgetǁ_update_animation__mutmut_17
    }
    xǁLoadingOverlayWidgetǁ_update_animation__mutmut_orig.__name__ = 'xǁLoadingOverlayWidgetǁ_update_animation'

    def paintEvent(self, a0: QtGui.QPaintEvent | None) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_orig(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_1(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = None
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_2(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(None)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_3(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_4(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(None, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_5(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, None)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_6(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_7(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, )
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_8(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, False)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_9(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                None, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_10(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, None
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_11(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_12(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_13(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, False
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_14(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(None, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_15(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, None)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_16(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_17(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, )
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_18(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, False)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_19(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(None, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_20(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, None)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_21(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_22(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, )
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_23(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, False)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_24(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = None
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_25(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(None)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_26(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(9)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_27(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(None)
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_28(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor(None))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_29(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("XX#ffffffXX"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_30(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#FFFFFF"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_31(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(None)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_32(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(None)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_33(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = None
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_34(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() / 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_35(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 3
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_36(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = None
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_37(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(None)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_38(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() / 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_39(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 1.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_40(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = None

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_41(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 151

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_42(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(None, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_43(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, None)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_44(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_45(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, )
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_46(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(None)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_47(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = None
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_48(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(None, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_49(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, None, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_50(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, None, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_51(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, None)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_52(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_53(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_54(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_55(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, )
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_56(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size * 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_57(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(+arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_58(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 3, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_59(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size * 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_60(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, +arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_61(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 3, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_62(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = None
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_63(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(None)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_64(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle / 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_65(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 17)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_66(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(None, 0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_67(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, None, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_68(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, None)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_69(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(0, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_70(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_71(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, )

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_72(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 1, span_angle)

        super().paintEvent(a0)

    def xǁLoadingOverlayWidgetǁpaintEvent__mutmut_73(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

        super().paintEvent(None)
    
    xǁLoadingOverlayWidgetǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_1': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_1, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_2': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_2, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_3': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_3, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_4': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_4, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_5': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_5, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_6': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_6, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_7': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_7, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_8': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_8, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_9': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_9, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_10': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_10, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_11': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_11, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_12': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_12, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_13': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_13, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_14': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_14, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_15': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_15, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_16': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_16, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_17': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_17, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_18': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_18, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_19': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_19, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_20': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_20, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_21': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_21, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_22': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_22, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_23': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_23, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_24': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_24, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_25': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_25, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_26': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_26, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_27': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_27, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_28': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_28, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_29': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_29, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_30': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_30, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_31': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_31, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_32': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_32, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_33': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_33, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_34': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_34, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_35': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_35, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_36': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_36, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_37': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_37, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_38': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_38, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_39': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_39, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_40': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_40, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_41': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_41, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_42': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_42, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_43': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_43, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_44': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_44, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_45': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_45, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_46': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_46, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_47': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_47, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_48': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_48, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_49': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_49, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_50': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_50, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_51': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_51, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_52': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_52, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_53': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_53, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_54': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_54, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_55': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_55, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_56': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_56, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_57': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_57, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_58': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_58, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_59': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_59, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_60': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_60, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_61': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_61, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_62': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_62, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_63': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_63, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_64': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_64, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_65': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_65, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_66': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_66, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_67': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_67, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_68': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_68, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_69': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_69, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_70': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_70, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_71': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_71, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_72': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_72, 
        'xǁLoadingOverlayWidgetǁpaintEvent__mutmut_73': xǁLoadingOverlayWidgetǁpaintEvent__mutmut_73
    }
    xǁLoadingOverlayWidgetǁpaintEvent__mutmut_orig.__name__ = 'xǁLoadingOverlayWidgetǁpaintEvent'

    def resizeEvent(self, a0: QtGui.QResizeEvent | None) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_orig'), object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_mutants'), args, kwargs, self)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_orig(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_1(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(None)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_2(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = None
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_3(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = None
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_4(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 101
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_5(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = None
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_6(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) / 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_7(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() + label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_8(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 3
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_9(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = None
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_10(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(None)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_11(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() / 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_12(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 1.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_13(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = None
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_14(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 21
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_15(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(None, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_16(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, None, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_17(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, None, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_18(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, None)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_19(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_20(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_21(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_22(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, )
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_23(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = None
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_24(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y + margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_25(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = None

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_26(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(None, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_27(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, None)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_28(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_29(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, )

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_30(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() + margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_31(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin / 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_32(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 3, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_33(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = None
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_34(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) / 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_35(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() + size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_36(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 3
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_37(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = None

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_38(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) / 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_39(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height + size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_40(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 3

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_41(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(None, gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_42(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, None, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_43(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, None, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_44(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, None)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_45(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_y, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_46(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, size, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_47(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size)

    def xǁLoadingOverlayWidgetǁresizeEvent__mutmut_48(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, )
    
    xǁLoadingOverlayWidgetǁresizeEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_1': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_1, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_2': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_2, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_3': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_3, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_4': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_4, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_5': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_5, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_6': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_6, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_7': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_7, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_8': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_8, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_9': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_9, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_10': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_10, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_11': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_11, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_12': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_12, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_13': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_13, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_14': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_14, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_15': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_15, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_16': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_16, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_17': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_17, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_18': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_18, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_19': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_19, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_20': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_20, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_21': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_21, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_22': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_22, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_23': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_23, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_24': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_24, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_25': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_25, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_26': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_26, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_27': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_27, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_28': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_28, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_29': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_29, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_30': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_30, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_31': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_31, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_32': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_32, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_33': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_33, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_34': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_34, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_35': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_35, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_36': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_36, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_37': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_37, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_38': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_38, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_39': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_39, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_40': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_40, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_41': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_41, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_42': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_42, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_43': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_43, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_44': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_44, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_45': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_45, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_46': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_46, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_47': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_47, 
        'xǁLoadingOverlayWidgetǁresizeEvent__mutmut_48': xǁLoadingOverlayWidgetǁresizeEvent__mutmut_48
    }
    xǁLoadingOverlayWidgetǁresizeEvent__mutmut_orig.__name__ = 'xǁLoadingOverlayWidgetǁresizeEvent'

    def show(self) -> None:
        """Re-implemented method, show widget"""
        self.repaint()
        return super().show()

    def _setupUI(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_orig'), object.__getattribute__(self, 'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_mutants'), args, kwargs, self)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_orig(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_1(self) -> None:
        self.setAttribute(None, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_2(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, None)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_3(self) -> None:
        self.setAttribute(True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_4(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, )
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_5(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_6(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = None
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_7(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel(None, self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_8(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", None)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_9(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel(self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_10(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", )
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_11(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("XXXX", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_12(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName(None)
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_13(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("XXgifshowXX")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_14(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("GIFSHOW")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_15(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet(None)
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_16(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("XXbackground: transparent;XX")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_17(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("BACKGROUND: TRANSPARENT;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_18(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(None)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_19(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = None
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_20(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(None)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_21(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = None
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_22(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(None)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_23(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_24(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(None)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_25(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet(None)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_26(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("XXcolor: #ffffff; background: transparent;XX")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_27(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("COLOR: #FFFFFF; BACKGROUND: TRANSPARENT;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def xǁLoadingOverlayWidgetǁ_setupUI__mutmut_28(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(None)
    
    xǁLoadingOverlayWidgetǁ_setupUI__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_1': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_1, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_2': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_2, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_3': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_3, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_4': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_4, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_5': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_5, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_6': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_6, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_7': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_7, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_8': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_8, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_9': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_9, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_10': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_10, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_11': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_11, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_12': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_12, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_13': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_13, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_14': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_14, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_15': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_15, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_16': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_16, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_17': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_17, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_18': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_18, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_19': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_19, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_20': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_20, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_21': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_21, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_22': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_22, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_23': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_23, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_24': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_24, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_25': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_25, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_26': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_26, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_27': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_27, 
        'xǁLoadingOverlayWidgetǁ_setupUI__mutmut_28': xǁLoadingOverlayWidgetǁ_setupUI__mutmut_28
    }
    xǁLoadingOverlayWidgetǁ_setupUI__mutmut_orig.__name__ = 'xǁLoadingOverlayWidgetǁ_setupUI'
