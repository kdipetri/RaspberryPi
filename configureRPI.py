# SPI master for ETROC0 
# Raspberry Pi 2 Model B
# Jamieson Olsen 14-May-2019
# Sid Minor edits: 12-Jun-2019

import time
#import spidev
#import RPi.GPIO as GPIO

import sys
import datetime
import ConfigParser 


def testConfig(cfg):
    max_speed = cfg.get('SPI', 'max_speed_hz')  
    print(max_speed)
    
    no_cs = cfg.get('SPI', 'no_cs')
    print(no_cs)

def configureETROC(cfg):
    
    # configure the SPI peripheral
    # note: the 32 bit vector will be sent as four bytes
    # and ETROC0 doesn't have a CS (chip select) pin
    # SCLK = pin 23
    # MISO = pin 21
    # MOSI = pin 19
    
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz = 5000
    spi.bits_per_word = 8
    spi.no_cs = True
    
    # there are also a few GPIO pins we'll also need to configure:
    
    RST_pin         = 17 # pin 11 (GPIO17)
    TestModeSel_pin = 27 # pin 13 (GPIO27)
    SLOAD_pin       = 22 # pin 15 (GPIO22)
    
    GPIO.setmode(GPIO.BCM) # use GPIOxx numbers
    GPIO.setwarnings(False)
    GPIO.setup(RST_pin,GPIO.OUT)
    GPIO.setup(TestModeSel_pin,GPIO.OUT)
    GPIO.setup(SLOAD_pin,GPIO.OUT)
    
    # Specify the GPIO initial conditions here:
    
    GPIO.output(TestModeSel_pin,GPIO.LOW)
    GPIO.output(RST_pin,GPIO.LOW)
    GPIO.output(SLOAD_pin,GPIO.LOW)
    
    
    # ####################################################################
    # Specify the ETROC0 Control Bits
    
    # INTERNAL CHARGE INJECTION 
    # When driving the Qinj input this setting will determine 
    # how much charge is injected into the front end. 
    # If QV input is used this can be ignored.
    # range is 0 to 127 femto farads, default is 6
    
    QSEL = 6
    
    # enable INTERNAL or EXTERNAL charge injection circuit.
    # If LGAD is used then QEN should be 0.
    
    QEN = 1
    
    # select load capacitance, 2 bits.def: 0b00
    
    CLSel = 0b00
    
    # bias current selection, 3 bits. def: 0b111
    ## 0b111 low power
    ## 0b000 high power
    IBSel = 0b000
    
    # feedback resistor selection, 2 bits.
    ## 0 = 20k ohm (highest gain)
    ## 1 = 10k ohm
    ## 2 = 5.7k ohm
    ## 3 = 4.4k ohm (lowest gain)
    RFSel = 3
    
    # hysteresis voltage, 4 bits. 0b1111
    
    HysSel = 0b1111
    
    # power-down signal for discriminator, 1 bit.(Active High) def: 0b0 
    
    DisPD = 0b1
    
    # DAC input code, 10 bits.def: 0b011000000
    # DAC is a ten bit number range 0 to 1023 (OK to use decimal here!)
    #DAC = 186 (673mV) : P00 4-2 (batch2) starts oscillation (closed box)
    DAC = 300
    
    # power-down signal for DAC, 1 bit.def: 0b0
    
    DACPD = 1
    
    # output enable st6, 1 bit.def: 0b1 
    
    OE = 1
    
    ######################################################
    
    
    
    
    
    
    # now form the 32-bit vector to shift into the ETROC
    
    msg = 0x00000000
    
    msg = (OE << 31) + (DACPD << 30) + (DAC << 20) + (DisPD << 19) + \
    (HysSel << 15) + (RFSel << 13) + (IBSel << 10) + (CLSel << 8) + \
    (QEN << 7) + QSEL
    
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    print("32-bit vector to send = 0x%08X" % msg)
    
    # but first we have to break it up into bytes...
    
    msg3 = (msg & 0xFF000000) >> 24
    msg2 = (msg & 0x00FF0000) >> 16
    msg1 = (msg & 0x0000FF00) >> 8
    msg0 = (msg & 0x000000FF)
    
    to_send = [msg3, msg2, msg1, msg0]
    
    print("bytes to send: ", to_send ) # note this is decimal
    
    # OK now we are ready to go...
    
    # release RST, let it go high, then wait a bit...
    
    GPIO.output(RST_pin,GPIO.HIGH)
    time.sleep(0.01)
    
    
    # now send SPI data as four bytes
    
    got_back = spi.xfer(to_send)
    
    print("bytes received: ", got_back)
    
    # wait a bit then pulse SLOAD
    
    time.sleep(0.01)
    GPIO.output(SLOAD_pin,GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(SLOAD_pin,GPIO.LOW)
    
    # we're done!
    
    spi.close()
    
    # NOTE: if we cleanup() the GPIO then the RST pin goes low
    # which we probably don't want! Comment this out so
    # that the GPIO output pins retain the last value written
    # to them.
    # GPIO.cleanup()


def main():


    # Get configuration file 
    config_file = "run_default.cfg"
    if len(sys.argv) > 1 : config_file = sys.argv[1]
    
    print("Configuration File : {}".format(config_file))

    # Read in configuration  
    config = ConfigParser.ConfigParser()
    config.read(config_file)

    # Test config file reading
    testConfig(config)

    # Configure the ETROC
    #configureETROC(config)


if __name__ == "__main__":
    main()
