import time
import serial
import serial.threaded
import threading
import logging
import re

logger=logging.getLogger(__name__)

try:
    import queue
except ImportError:
    import Queue as queue

class DutException(Exception):
    pass

class DutProtocol(serial.threaded.LineReader):
    def __init__(self):
        super(DutProtocol, self).__init__()
        self.alive = True
        self.events = queue.Queue()
        self.responses = queue.Queue()
        self._awaiting_response_for = None
        self._re_exp = None
        self._re_match_hook = None
        self._event_thread = threading.Thread(target=self._run_event)
        self._event_thread.name = 'report.events'
        self._event_thread.daemon = True
        self._event_thread.start()
        self.lock = threading.Lock()
        pass

    def connection_made(self, transport):
        logger.debug("dut protocol connection made")
        super(DutProtocol, self).connection_made(transport)
        self.transport.serial.rts = False
        time.sleep(0.3)
        self.transport.serial.reset_input_buffer()
        pass

    def _run_event(self):
        while self.alive:
            try:
                self._process_event(self.events.get())
            except:
                logging.exception('_run_events queue')

    def _process_event(self, event):
        ''' event handle '''
        print("EVENT: {}".format(event))

    def _process_resp(self, line):
        ''' line response handle '''
        print("RESP: {}".format(line))
        if self._re_exp:
            m = re.search(self._re_exp, line)
            if m:
                if self._re_match_hook and self._re_match_hook(line, self._re_match_args):
                    self._command_wait_fin()

    def handle_line(self, line):
        if self._awaiting_response_for == None:
            self.events.put(line)
        else:
            self.responses.put(line)

    def _command_wait_fin(self):
        self._awaiting_response_for = None

    def Command(self, cmd, resp=None, wait_sec=5):
        """ request exec, and wait for response """
        with self.lock:
            self._awaiting_response_for = cmd
            self.write_line(cmd)
            lines = []
            waits = wait_sec
            while waits > 0 and self._awaiting_response_for:
                try:
                    line = self.responses.get(timeout=1)
                    self._process_resp(line)
                    if resp != None and line == resp:
                        lines.append(line)
                        return
                    else:
                        lines.append(line)
                    waits = wait_sec
                except queue.Empty:
                    waits = waits - 1
            self._awaiting_response_for = None
            return lines

    def ReSetExp(self, regexp="", cb=None, args=[]):
        self._re_exp = regexp
        self._re_match_hook = cb
        self._re_match_args = args
        pass

    def ReClear(self):
        self._re_exp = None
        self._re_match_hook = None
        pass

    def Init(self):
        logger.debug("super cal proto init")

    def Stop(self):
        self.alive = False
        self.events.put(None)
        self.responses.put(None)

    def Reset(self):
        logger.debug("reset")
        self.Command("reset")