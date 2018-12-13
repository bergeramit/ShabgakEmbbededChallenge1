# ShabgakEmbbededChallenge1

First We can see that there is a function named "save_to_flash" this function 
always saves after a "format_save" function as occured.
The format is:

```
struct for record{
uint8_t a;
uint32_t len;
uint8_t data[len]; 
}
```

Now we can create a template in 010 editor for this:

```
struct RECORD {
     UBYTE    format <fgcolor=cBlue>;
     UINT   size <fgcolor=cBlack, bgcolor=0x00FF00>;
     UBYTE data[size] <fgcolor=cWhite, bgcolor=0x0000FF>;
};

while(1)
{
 RECORD rec;
}
```
This leads us to see that the whole memory (other than a record 0x4fff) was saved thjis way.

## Getting to know the formats

### a == 1
> by looking at the function format1 -> which is called everytime we have a == 1. upon extracting its data we can see this is latitude and longtitude of places in Israel. We need to understand the right lat and log from this pile of coordinates.
### a == 0
> When looking at a = 0 we see refrence to "reset=true" - which is refered to a reset of the device. This reset saves the time and data in two longs, the last one happened in 28/10/18 in 16:17:00. We know from the riddle that the right coordinates happened at 30/10/18 1:21:00, which is exactly 1984 minutes from this reset.

# Getting the right coordinates
Most of the Information about the proccessor is from this source: https://www.instructables.com/id/Arduino-Timer-Interrupts/
We now need to understand the ISRs in the program, we can see that there is a interrupt that happends periodicaly
```
ISR(TIMER1_COMPA_vect)
```
This interrupt depends on the CPU (which we know is 16MHz) the params in the "configure1" function
```
     OCR1A = 62499;
     TCCR1B |= (1 << WGM12);
     TCCR1B |= (1 << CS12) | (1 << CS10);
     TIMSK1 |= (1 << OCIE1A);
```
Set CS10 and CS12 bits for 1024 prescaler, on 16MHz CPU and 
By the formula: 
```
(16*10^6) / (x*1024) - 1 = 62499
```
x is the ratio of seconds to cycles which is 4
this means that every 4 cycles a second is passed

> so the total number of seconds is 1984 * 60 = 119040 seconds and every cycle is 0.25 seconds.

# a == 2 and a == 
We can see the the saves happen in the "ISR(TIMER1_COMPA_vect)" but ios influences on the state of the boolean _is_triggered_.
the cycles it takes to save is different depending on the state of this var.
If a == 2 then the cycles until save is: 15 
If a == 3 then the cycles until save is: 150

We can tell that this variable is a toggle so every time we see a record that is a ==3 or a == 2 we know the cycles-to-save counter.
THe code apply this information and solved the challenge:

## Psuedo Code
every record we calculate the time it took : (cycles_for_this_record) / 4
and we substruct it from the time left,
on a == 3 or a == 2 we configure the number of cycles for each record accordingly
and when the time left is 0 we print the coordinates

>
