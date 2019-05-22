
#include <avr/io.h>
#include<util/delay.h>
#include<avr/interrupt.h>
#define SET_BIT(PORT, PIN) PORT |= (1<<PIN)
#define CLR_BIT(PORT, PIN) PORT &= ~(1<<PIN)
void initADC();
uint16_t readADC(uint8_t ch);
volatile int Collision_detection = 0;
volatile int Car_Speed = 0;
int main(void)
{
    CLR_BIT(DDRD, 2);
    SET_BIT(PORTD, 2);
    SET_BIT(EICRA, ISC00);
    SET_BIT(EIMSK, INT0);
    CLR_BIT(DDRC, PC0);
    SET_BIT(DDRC, PC0);
    CLR_BIT(DDRC, PC1);
    SET_BIT(DDRC, PC1);
    SET_BIT(DDRB, 5);
    SET_BIT(DDRB, PB1);
    initADC();
    sei();
    TCCR1A|=((1<<COM1A1)|(1<<WGM11)|(1<<WGM10));
    TCCR1B|=((1<<WGM12)|(1<<CS01)|(1<<CS00));
    TCNT1=0x00;
    while(1)
    {
        Car_Speed=readADC(1);
        OCR1A= readADC(0);


     if(Collision_detection==1&&Car_Speed==0&&readADC(0)<255)
        {

                CLR_BIT(PORTB, 5);

        }

     else
     {
               SET_BIT(PORTB, 5);
                 //_delay_ms(500);

    }
    }
    return 0;
}
ISR(INT0_vect)
{
    if(!(PIND&(1<<PD2)))
       Collision_detection = 1;
    else
    Collision_detection = 0;
}
void initADC()
{
    ADMUX=(1<<REFS0);
    ADCSRA=(1<<ADEN)|(7<<ADPS0);
}
uint16_t readADC(uint8_t ch)
{
    ADMUX&=0xf8;
    ch=ch&0b00000111;
    ADMUX|=ch;

    ADCSRA|=(1<<ADSC);
    while(!(ADCSRA&(1<<ADIF)));
    ADCSRA|=(1<<ADIF);
    uint16_t TEMP=0;
    TEMP|=(ADCH<<8);
    TEMP|=(ADCL);
    return(TEMP);
}

