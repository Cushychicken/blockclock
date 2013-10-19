from soco import SoCo, SonosDiscovery
from time import strftime, localtime

class BlockClock:
    def __init__(self):
        # Time variables
        self._then = ''
        
        # Player variables        
        self._ZONE_IPS = []

        disc = SonosDiscovery()
        self.household = {}
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
        for ip in self._ZONE_IPS:
            device = SoCo(ip)
            device.play()
        return True

    def pause(self):
        for ip in self._ZONE_IPS:
            device = SoCo(ip)
            device.pause()
        return True

    def volume_up(self):
        for ip in self._ZONE_IPS:
            device = SoCo(ip)
            vol = int(device.volume())
            if vol < 100:
                device.volume(vol+1)
                return True
            elif vol == 100:
                return True

    def volume_down(self):
        for ip in self._ZONE_IPS:
            device = SoCo(ip)
            vol = int(device.volume())
            if vol > 0:
                device.volume(vol-1)
                return True
            elif vol == 100:
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

            	
