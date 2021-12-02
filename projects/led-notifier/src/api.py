# External deps.
from datetime import datetime
from pathlib import Path
import RPi.GPIO as GPIO

LED_1_PIN = 21
LED_2_PIN = 14
LOG_FILE = Path(__file__).parent.absolute() / f'logs/log_{datetime.now().year}-{datetime.now().month}.txt'

def handler( request ):
    GPIO.setmode( GPIO.BCM )
    GPIO.setwarnings( False )
    GPIO.setup( LED_1_PIN, GPIO.OUT )
    GPIO.setup( LED_2_PIN, GPIO.OUT )
    GPIO.setwarnings( True )

    # LED 1
    led_1 = request.args.get( 'led_1', default = -1, type = int )
    led_1_source = request.args.get( 'source', default = 'unspecified', type = str )

    if led_1 == 0:
        write_log( f'LED_1 | Action: Off | Source: { led_1_source }' )
        turn_led_off( LED_1_PIN )
    elif led_1 == 1:
        write_log( f'LED_1 | Action: On | Source: { led_1_source }' )
        turn_led_on( LED_1_PIN )

    # LED 2
    led_2 = request.args.get( 'led_2', default = -1, type = int )
    led_2_source = request.args.get( 'source', default = 'unspecified', type = str )

    if led_2 == 0:
        write_log( f'LED_2 | Action: Off | Source: { led_2_source }' )
        turn_led_off( LED_2_PIN )
    elif led_2 == 1:
        write_log( f'LED_2 | Action: On | Source: { led_2_source }' )
        turn_led_on( LED_2_PIN )

def turn_led_off( pin ):
    GPIO.setwarnings( False )
    GPIO.output( pin, GPIO.LOW )
    GPIO.cleanup( pin )
    GPIO.setwarnings( True )

def turn_led_on( pin ):
    GPIO.output( pin, GPIO.HIGH )

def format_log( s ):
    t = datetime.utcnow().isoformat()
    return f'[ { t } ]: { s }\n'

def write_log( s ):
    with open( LOG_FILE, 'a+' ) as file:
        file.write( format_log( s ) )

def get_logs():
    with open( LOG_FILE, 'a+' ) as file:
        file.seek( 0 )
        lines = file.readlines()
        return( lines[ -25: ] )
