#include <string.h>
#include <stdio.h>
#include <iostream>
#include <windows.h>
#include "sm3.h"
#include <stdint.h>
# include <immintrin.h>
#include <chrono>
using namespace std;

void IV0_assignment(sm3_context* ctx) {
    ctx->iplen = 0;
    ctx->state[0] = 0x7380166F,ctx->state[1] = 0x4914B2B9;
    ctx->state[2] = 0x172442D7,ctx->state[3] = 0xDA8A0600;
    ctx->state[4] = 0xA96F30BC,ctx->state[5] = 0x163138AA;
    ctx->state[6] = 0xE38DEE4D,ctx->state[7] = 0xB0FB0E4E;
}//初始IV赋值


void sm3_process(sm3_context* ctx, uint8_t data[64]) {
    int j;
    unsigned long SS1, SS2, TT1, TT2, W1[68], W2[64];
    unsigned long A, B, C, D, E, F, G, H;
    unsigned long T[64];
    __m128i X, K, R;
    __m128i M = _mm_setr_epi32(0, 0, 0, 0xffffffff);
    __m128i V = _mm_setr_epi8(3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12);
#ifdef _DEBUG
    int i;
#endif

    for (j = 0; j < 16; j++) {
        T[j] = 0x79CC4519;
    }
    for (j = 16; j < 64; j++) {
        T[j] = 0x7A879D8A;
    }

    for (j = 0; j < 16; j += 4) {
        X = _mm_loadu_si128((__m128i*)(data + j * 4));
        X = _mm_shuffle_epi8(X, V);
        _mm_storeu_si128((__m128i*)(W1 + j), X);
    }

//FF函数，GG函数
#define FF0(x,y,z) ( (x) ^ (y) ^ (z))
#define FF1(x,y,z) (((x) & (y)) | ( (x) & (z)) | ( (y) & (z)))

#define GG0(x,y,z) ( (x) ^ (y) ^ (z))
#define GG1(x,y,z) (((x) & (y)) | ( (~(x)) & (z)) )


#define SHL(x,n) (((x) & 0xFFFFFFFF) << (n))
#define ROTL(x,n) (SHL((x),n) | ((x) >> (32 - n)))

#define P0(x) ((x) ^  ROTL((x),9) ^ ROTL((x),17))
#define P1(x) ((x) ^  ROTL((x),15) ^ ROTL((x),23))

# define _mm_rotl_epi32(X,i) _mm_xor_si128(_mm_slli_epi32((X),(i)), _mm_srli_epi32((X),32-(i)))
    //消息扩展
    for (j = 16; j < 68; j += 4) {
        /* X = (W1[j - 3], W1[j - 2], W1[j - 1], 0) */
        X = _mm_loadu_si128((__m128i*)(W1 + j - 3));
        X = _mm_andnot_si128(M, X);

        X = _mm_rotl_epi32(X, 15);
        K = _mm_loadu_si128((__m128i*)(W1 + j - 9));
        X = _mm_xor_si128(X, K);
        K = _mm_loadu_si128((__m128i*)(W1 + j - 16));
        X = _mm_xor_si128(X, K);

        /* P1() */
        K = _mm_rotl_epi32(X, 8);
        K = _mm_xor_si128(K, X);
        K = _mm_rotl_epi32(K, 15);
        X = _mm_xor_si128(X, K);

        K = _mm_loadu_si128((__m128i*)(W1 + j - 13));
        K = _mm_rotl_epi32(K, 7);
        X = _mm_xor_si128(X, K);
        K = _mm_loadu_si128((__m128i*)(W1 + j - 6));
        X = _mm_xor_si128(X, K);

        /* W1[j + 3] ^= P1(ROL32(W1[j + 1], 15)) */
        R = _mm_shuffle_epi32(X, 0);
        R = _mm_and_si128(R, M);
        K = _mm_rotl_epi32(R, 15);
        K = _mm_xor_si128(K, R);
        K = _mm_rotl_epi32(K, 9);
        R = _mm_xor_si128(R, K);
        R = _mm_rotl_epi32(R, 6);
        X = _mm_xor_si128(X, R);

        _mm_storeu_si128((__m128i*)(W1 + j), X);
    }
    /* W2 = W1[j] ^ W1[j+4] */
    for (int j = 0; j < 64; j += 4) {
        X = _mm_loadu_si128((__m128i*)(W1 + j));
        K = _mm_loadu_si128((__m128i*)(W1 + j + 4));
        X = _mm_xor_si128(X, K);
        _mm_storeu_si128((__m128i*)(W2 + j), X);
    }

    //迭代压缩
    A = ctx->state[0];
    B = ctx->state[1];
    C = ctx->state[2];
    D = ctx->state[3];
    E = ctx->state[4];
    F = ctx->state[5];
    G = ctx->state[6];
    H = ctx->state[7];

    //压缩函数
    for (j = 0; j < 16; j++) {
        SS1 = ROTL((ROTL(A, 12) + E + ROTL(T[j], j)), 7);
        SS2 = SS1 ^ ROTL(A, 12);
        TT1 = FF0(A, B, C) + D + SS2 + W2[j];
        TT2 = GG0(E, F, G) + H + SS1 + W1[j];
        D = C;
        C = ROTL(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = ROTL(F, 19);
        F = E;
        E = P0(TT2);
/*#ifdef _DEBUG
        printf("%02d %08x %08x %08x %08x %08x %08x %08x %08x\n", j, A, B, C, D, E, F, G, H);
#endif*/

    }

    for (j = 16; j < 64; j++) {
        SS1 = ROTL((ROTL(A, 12) + E + ROTL(T[j], j)), 7);
        SS2 = SS1 ^ ROTL(A, 12);
        TT1 = FF1(A, B, C) + D + SS2 + W2[j];
        TT2 = GG1(E, F, G) + H + SS1 + W1[j];
        D = C;
        C = ROTL(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = ROTL(F, 19);
        F = E;
        E = P0(TT2);
/*#ifdef _DEBUG
        printf("%02d %08x %08x %08x %08x %08x %08x %08x %08x\n", j, A, B, C, D, E, F, G, H);
#endif*/

    }

    ctx->state[0] ^= A;
    ctx->state[1] ^= B;
    ctx->state[2] ^= C;
    ctx->state[3] ^= D;
    ctx->state[4] ^= E;
    ctx->state[5] ^= F;
    ctx->state[6] ^= G;
    ctx->state[7] ^= H;
#ifdef _DEBUG
#endif
}


/*
 * SM3 process buffer
 */
void sm3_update(sm3_context* ctx, unsigned char* input, int iplen_t) {
    /*
     * iplen_t 待填充data的长度
     * input 待填充的data
     */
    int fill;
    unsigned long left;

    if (iplen_t <= 0)
        return;

    left = ctx->iplen & 0x3F;       
    fill = 64 - left;               

    ctx->iplen += iplen_t;             

    if (left && iplen_t >= fill) {
        memcpy((void*)(ctx->buffer + left), (void*)input, fill);     // 补全当前分块到64字节
        sm3_process(ctx, ctx->buffer);                              
        input += fill;                                              // 填入下一个分块的第一个表项位置更新
        iplen_t -= fill;                                            
        left = 0;                                                   
    }

    while (iplen_t >= 64) {
        sm3_process(ctx, input);
        input += 64;
        iplen_t -= 64;
    }// 若待填充data长度不小于64bit则将64bit填入一个块并进行操作

    if (iplen_t > 0) {
        memcpy((void*)(ctx->buffer + left), (void*)input, iplen_t);
    }//带填充消息写入buffer
}

static unsigned char sm3_padding[64] =
{
        0x80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
};//用1分割后，在消息和消息长度的中间全部填充0

/*
 * SM3 final digest
 */
 /* unsigned char b[i] = unsigned long n 的i  -  i+8位 */
#ifndef UN_PUT
#define UN_PUT(n,b,i)                             \
{                                                       \
    (b)[i    ] = (unsigned char) ( (n) >> 24 );       \
    (b)[i + 1] = (unsigned char) ( (n) >> 16 );       \
    (b)[i + 2] = (unsigned char) ( (n) >>  8 );       \
    (b)[i + 3] = (unsigned char) ( (n)       );       \
}
#endif
void sm3_finish(sm3_context* ctx, unsigned char output[32]) {
    unsigned long last, padn;
    unsigned long high, low;
    unsigned char msglen[8];        // 消息长度

    high = (ctx->iplen >> 29);
    low = (ctx->iplen << 3);

    UN_PUT(high, msglen, 0);
    UN_PUT(low, msglen, 4);

    last = ctx->iplen & 0x3F;     // 每64字节一个分组
    padn = (last < 56) ? (56 - last) : (120 - last);            

    sm3_update(ctx, (unsigned char*)sm3_padding, padn);         //填充全0
    sm3_update(ctx, msglen, 8);                                 // 最后填充8字节的消息长度

    UN_PUT(ctx->state[0], output, 0 );UN_PUT(ctx->state[1], output, 4);
    UN_PUT(ctx->state[2], output, 8 );UN_PUT(ctx->state[3], output, 12);
    UN_PUT(ctx->state[4], output, 16);UN_PUT(ctx->state[5], output, 20);
    UN_PUT(ctx->state[6], output, 24);UN_PUT(ctx->state[7], output, 28);
}

int main(int argc, char* argv[])
{
    auto* input = (unsigned char*)"O my Luve is like a red, red rose,That is newly sprung in June";   // input
    int iplen = 3;                   // input length
    unsigned char output[32];       // output
    int i;
    //auto start = std::chrono::high_resolution_clock::now();
    sm3_context ctx;
    //auto start = std::chrono::high_resolution_clock::now();
    cout << "Message:" << endl;
    cout << input << endl;
    auto start = std::chrono::high_resolution_clock::now();
    IV0_assignment(&ctx);
    sm3_update(&ctx, input, iplen);
    sm3_finish(&ctx, output);
    //auto end = std::chrono::high_resolution_clock::now();
    memset(&ctx, 0, sizeof(sm3_context));
    auto end = std::chrono::high_resolution_clock::now();
    cout << "Hash:" << endl;
    for (i = 0; i < 32; i++)
    {
        printf("%02x", output[i]);
        if (((i + 1) % 4) == 0) printf(" ");
    }
    printf("\n");
    //auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

    std::cout << "Time taken: " << duration << " microseconds" << std::endl;

}
