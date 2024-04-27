import time
import serial
import serial.threaded
import threading
import logging

LOG_FMT="%(asctime)s %(module)s %(name)s %(message)s"
logging.basicConfig(format=LOG_FMT, filename="dut.log", level=logging.NOTSET)
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
        self._event_thread = threading.Thread(target=self._run_event)
        self._event_thread.name = 'report.events'
        self._event_thread.daemon = True
        self._event_thread.start()
        self.lock = threading.Lock()

    def stop(self):
        self.alive = False
        self.events.put(None)
        self.responses.put(None)

    def reset(self):
        logger.debug("reset")
        self.command("reset")

    def connection_made(self, transport):
        logger.debug("dut protocol connection made {}".format(transport))
        super(DutProtocol, self).connection_made(transport)
        self.transport.serial.rts = False
        time.sleep(0.3)
        self.transport.serial.reset_input_buffer()

    def _run_event(self):
        while self.alive:
            try:
                self.handle_event(self.events.get())
            except:
                logging.exception('_run_events queue')
                
    def handle_event(self, event):
        ''' event handle actions '''
        print("EVENT: {}".format(event))

    def handle_line(self, line):
        if self._awaiting_response_for == None:
            self.events.put(line)
        else:
            self.responses.put(line)

    def handle_resp(self, lines):
        # print(lines)
        for line in lines:
            print("RESP: {}".format(line))

    def command(self, cmd, resp=None, wait_sec=5):
        """ request exec, and wait for response """
        with self.lock:
            self._awaiting_response_for = cmd
            self.write_line(cmd)
            lines = []
            waits = wait_sec
            while waits > 0:
                try:
                    line = self.responses.get(timeout = 0.1)
                    # print("<{}>".format(line))
                    if resp != None and line == resp:
                        lines.append(line)
                        break
                    else:
                        lines.append(line)
                    waits = wait_sec
                except queue.Empty:
                    waits = waits - 1
                    break
            self._awaiting_response_for = None
            self.handle_resp(lines)
            return lines

    def cal_init(self):
        logger.debug("super cal init")

