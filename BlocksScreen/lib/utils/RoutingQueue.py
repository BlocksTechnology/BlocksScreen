import queue
import threading


class RoutingQueue(queue.LifoQueue):
    def __init__(self):
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

    @property
    def resend(self):
        return self._resend

    @resend.setter
    def resend(self, new_resend):
        with self.mutex:
            self._resend = new_resend

    def block(self):
        # Sets the flag to false
        self._clear_to_move.clear()

    def unblock(self):
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

    def get_command(self, block=True, timeout=None, resend=False):
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

    def clear_queues(self):
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
