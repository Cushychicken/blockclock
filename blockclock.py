import logging
import sys
from soco import SoCo, SonosDiscovery
from time import strftime, localtime

class BlockClock:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
	self.logger = logging.getLogger(__name__)
	fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	
	logfile = logging.FileHandler('hello.log')
	logfile.setLevel(logging.DEBUG)
	formatter = logging.Formatter(fmt)
	logfile.setFormatter(formatter)
	self.logger.addHandler(logfile)

	stderr_handle = logging.StreamHandler(sys.stdout)
        stderr_handle.setLevel(logging.INFO)
	formatter = logging.Formatter(fmt)
	logfile.setFormatter(formatter)
	self.logger.addHandler(stderr_handle)
       
        self.logger.info('Starting log...')
 
	# Time variables
	self._then = ''
        
        # Player variables        
        self._ZONE_IPS = []

	self.logger.info('Searching for zones...')
        disc = SonosDiscovery()

        self.household = {}

        self.logger.info('Building household tree...')
	for ip in disc.get_speaker_ips():
            device = SoCo(ip)
            try:
                zone = device.get_speaker_info()['zone_name']
                if zone != None:
	            if self.household.has_key(zone):
                        self.household[zone].append(ip)
                    else:
                        self.household[zone] = []
                        self.household[zone].append(ip)
            except ValueError:
                msg = 'Zone with no name at '+ip+', possibly a bridge'
		self.logger.error(msg)
                continue
            
    def setup(self):
        if len(self.household.keys()) == 0:
           print 'No households found. Exiting.'
           return False

        print 'Which zone would you like to associate your Sonos Clock with?'
        print
        for zone in self.household.keys():
            print zone
            
        zone = raw_input('Enter selection:')
        if self.household.has_key(zone):
            print 'Your Sonos Clock is now associated with zone', zone, '.'
            self._ZONE_IPS = self.household[zone]
            return True
        else:
            print zone, 'is not a valid selection.'
            self.setup()

    def play(self):
        self.logger.info('Playing zones...')
        for ip in self._ZONE_IPS:
            device = SoCo(ip)
	    self.logger.debug('Playing zone at %s', ip)
	    if not device.play():
                self.logger.error('Unable to play zone at %s', ip)
		return False
	self.logger.info('All zones playing.')
        return True

    def pause(self):
        self.logger.info('Pausing zones...')
        for ip in self._ZONE_IPS:
            device = SoCo(ip)
            self.logger.debug('Pausing zone at %s', ip)
	    if not device.pause():
                self.logger.error('Unable to pause zone at %s', ip)
		return False
	self.logger.info('All zones paused.')
        return True

    def volume_up(self):
        self.logger.info('Raising volume...')
        for ip in self._ZONE_IPS:
            device = SoCo(ip)
            vol = int(device.volume())
            if vol < 100:
		self.logger.debug('Setting volume to %d', vol+1)
                if not device.volume(vol+1):
                    self.logger.error('Could not set volume at %s.', ip)
                    return False
		else:
		    self.logger.info('Raised volume.')
		    return True
            elif vol == 100:
		self.logger.info('Volume at max, could not raise.')
                return True

    def volume_down(self):
	self.logger.info('Lowering volume...')
        for ip in self._ZONE_IPS:
            device = SoCo(ip)
            vol = int(device.volume())
            if vol > 0:
		self.logger.debug('Setting volume to %d', vol-1)
                if not device.volume(vol-1):
                    self.logger.error('Could not set volume at %s.', ip)
                    return False
		else:
		    self.logger.error('Lowered volume.')
		    return True
            elif vol == 100:
		self.logger.info('Volume at min, could not lower.')
                return True


    def clock(self):
        now = strftime("%I:%M", localtime())
        if now != self._then:
            self._then = now
            self.update_face()
        else:
            self._then = now

    def update_face(self):
        # right now this is a placeholder for I2C push
	print self._then
    
    def run(self):
        while True:
            self.clock()
            # wait for command; execute

if __name__ == '__main__':
    clock = BlockClock()
    if clock.setup():
        clock.run()
    else:
        quit()

            	
