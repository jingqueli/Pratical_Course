#include<stdio.h>
#include<stdint.h>


#define ROUND 32
#define ROL(x,n) ((x<<n)|(x>>(32-n)))
#define GET_UINT32_BE(n,b,i)                            \
{                                                       \
    (n) = ( (uint32_t) (b)[(i)    ] << 24 )             \
        | ( (uint32_t) (b)[(i) + 1] << 16 )             \
        | ( (uint32_t) (b)[(i) + 2] <<  8 )             \
        | ( (uint32_t) (b)[(i) + 3]       );            \
}

#define PUT_UINT32_BE(n,b,i)                            \
{                                                       \
    (b)[(i)    ] = (unsigned char) ( (n) >> 24 )&0x000000ff;        \
    (b)[(i) + 1] = (unsigned char) ( (n) >> 16 )&0x000000ff;        \
    (b)[(i) + 2] = (unsigned char) ( (n) >>  8 )&0x000000ff;        \
    (b)[(i) + 3] = (unsigned char) ( (n)       )&0x000000ff;        \
}

typedef struct {
    unsigned char key[16];
    uint32_t rk[ROUND];
} sm4_context;


extern const uint32_t FK[];

extern const uint32_t CK[];

extern const uint8_t sbox[];

uint32_t t(uint32_t x);

uint32_t T(uint32_t x);

uint32_t T_(uint32_t x);

void sm4_setkey(sm4_context* ctx, const unsigned char key[16]);

void sm4_encrypt(sm4_context* ctx, size_t length, unsigned char* input, unsigned char* output);


