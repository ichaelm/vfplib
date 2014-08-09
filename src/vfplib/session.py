'''
Created on Jun 4, 2014

@author: mschaffe
'''

import io
import time
import urllib2

from PIL import Image

# delay between POST commands (multiply by 2 for delay per input operation)
DEFAULT_COMMAND_DELAY = 0.05
# delay between screen captures (multiply by 2 for delay per screen capture operation)
DEFAULT_SCREENCAP_DELAY = .2

class Session(object):
    """Represents a Virtual Front Panel session.

    Automatically establishes the connection on initialization, throws exceptions on failure.
    """
    # Stores session number as self.sessionid
    # Stores IP address as self.address
    def __init__(self, address):
        """Establishes connection to device at given IP address, or throws exceptions on failure."""
        assert isinstance(address, str)
        # param address = string containing ip address of the device.
        # goal: store self.address, and use it to initialize a session and store the session number
        self._address = address
        try:
            response = urllib2.urlopen('http://' + self._address + '/ajax_proc', 'function=9').readline()
            if '\x00' not in response:  # This string appears to indicate that the connection is new. If not new, creates a new one.
                response = urllib2.urlopen('http://' + self._address + '/ajax_proc', 'function=9').readline()
        except urllib2.URLError:
            # error communicating with server
            raise
        except urllib2.HTTPError:
            # server responded with error message, such as 404
            raise
        self._sessionid = int(response.partition('=')[2].partition('$')[0])  # parses response of the form 'session=XXX$symbols'
        self.screencap_delay = DEFAULT_SCREENCAP_DELAY
        self.command_delay = DEFAULT_COMMAND_DELAY

    @property
    def address(self):
        """Stores the IP address of the device"""
        return self._address

    @property
    def sessionid(self):
        """Stores the ID number of the current session"""
        return self._sessionid

    def reset(self):
        """Re-establishes connection using the stored IP address, or throws exceptions on failure."""
        try:
            response = urllib2.urlopen('http://' + self._address + '/ajax_proc', 'function=9').readline()
            if '\x00' not in response:  # This string appears to indicate that the connection is new. If not new, creates a new one.
                response = urllib2.urlopen('http://' + self._address + '/ajax_proc', 'function=9').readline()
        except urllib2.URLError:
            # error communicating with server
            raise
        except urllib2.HTTPError:
            # server responded with error message, such as 404
            raise
        self._sessionid = int(response.partition('=')[2].partition('$')[0])  # parses response of the form 'session=XXX$symbols'

    def screencap(self):
        """Performs screen capture, including all dummy requests and delays to ensure the screen returned is what was shown at the time this function was called.

        Returns a PIL image object
        """
        _ = urllib2.urlopen('http://' + self._address + '/images/fp.png?' + str(self._sessionid))
        time.sleep(self.screencap_delay)
        # _ = urllib2.urlopen('http://' + self._address + '/images/fp.png?' + str(self._sessionid))
        # time.sleep(self.screencap_delay)
        data = urllib2.urlopen('http://' + self._address + '/images/fp.png?' + str(self._sessionid))
        image_file = io.BytesIO(data.read())
        im = Image.open(image_file)
        while im.size[0] < 20:
            time.sleep(self.screencap_delay)
            data = urllib2.urlopen('http://' + self._address + '/images/fp.png?' + str(self._sessionid))
            image_file = io.BytesIO(data.read())
            im = Image.open(image_file)
        return im

    def click(self, x, y):
        """Sends command to click at (x,y)"""
        urllib2.urlopen('http://' + self._address + '/ajax_proc', 'function=2&x1=' + str(x) + '&y1=' + str(y) + '&session=' + str(self._sessionid))
        time.sleep(self.command_delay)
        urllib2.urlopen('http://' + self._address + '/ajax_proc', 'function=3&x1=' + str(x) + '&y1=' + str(y) + '&x2=' + str(x) + '&y2=' + str(y) + '&session=' + str(self._sessionid))
        time.sleep(self.command_delay)

    def drag(self, x1, y1, x2, y2):
        """Sends command to drag screen from (x1,y1) to (x2,y2)."""
        # Does not work
        urllib2.urlopen('http://' + self._address + '/ajax_proc', 'function=2&x1=' + str(x1) + '&y1=' + str(y1) + '&session=' + str(self._sessionid))
        time.sleep(self.command_delay)
        urllib2.urlopen('http://' + self._address + '/ajax_proc', 'function=4&x1=' + str(x1) + '&y1=' + str(y1) + '&x2=' + str(x2) + '&y2=' + str(y2) + '&session=' + str(self._sessionid))
        # TODO: missing dir parameter in second command
        time.sleep(self.command_delay)

    def press(self, buttonnumber):
        """Sends command to press the physical button with the given number."""
        urllib2.urlopen('http://' + self._address + '/ajax_proc', 'function=7&button=' + str(buttonnumber) + '&session=' + str(self._sessionid))
        time.sleep(self.command_delay)
        urllib2.urlopen('http://' + self._address + '/ajax_proc', 'function=8&button=' + str(buttonnumber) + '&session=' + str(self._sessionid))
        time.sleep(self.command_delay)

    def __hash__(self):
        return hash((self._address, self._sessionid))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self._address, self._sessionid) == (other._address, other._sessionid)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'VFP session #' + str(self._sessionid) + ' at ' + self._address

