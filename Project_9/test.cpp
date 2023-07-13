#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include"define.h"
#include<cstdio>
int main()
{



    // 加密mp4文件
    FILE* fp = fopen("D:\\QQDownload\\sm4_self\\video.mp4", "rb");
    if (fp == NULL) {
        printf("Failed to open file.\n");
        return -1;
    }

    // 获取文件长度
    fseek(fp, 0, SEEK_END);
    long file_size = ftell(fp);
    rewind(fp);
    printf("file size = %ld\n", file_size);
    int padding = 16 * (file_size/16 + 1) - file_size;
    printf("%d", padding);
    // 读取文件数据
    unsigned char* buffer = (unsigned char*)malloc((file_size + padding)  * sizeof(char));
    fread(buffer, sizeof(char), file_size, fp);
    memset(buffer + file_size, padding, padding);

    // 转换成十六进制字符串并打印输出

    // 写入十六进制字符串到文件
    FILE* fp_output = fopen("output.txt", "w");
    if (fp == NULL) {
        printf("Failed to create file.\n");
        return -1;
    }

    for (int i = 0; i < file_size + padding; i++) {
        fprintf(fp_output, "%02X ", (unsigned char)buffer[i]);
    }

    fclose(fp);
    fclose(fp_output);


    unsigned char key[16] = { 0x01,0x23,0x45,0x67,0x89,0xab,0xcd,0xef,0xfe,0xdc,0xba,0x98,0x76,0x54,0x32,0x10 };
    unsigned char* cipher_mp4 = (unsigned char*)malloc((file_size + padding) * sizeof(char));
    sm4_context ctx2;
    sm4_setkey(&ctx2, key);
    printf("sizeof(buffer):%d", sizeof(&buffer));
    sm4_encrypt(&ctx2,file_size+padding,buffer, cipher_mp4);

    for(int i =0;i<10;i++){
    	printf("%02x " ,(unsigned char)cipher_mp4[i]);

    }

    FILE* fp_cipher = fopen("D:\\QQDownload\\sm4_self\\cipher.txt", "w");
    if (fp_cipher == NULL) {
        printf("Failed to create cipher file.\n");
        return -1;

    }

    for (int i = 0; i < file_size + padding; i++)
    {
        fprintf(fp_cipher, "%02x", (unsigned char)cipher_mp4[i]);

    }

    fclose(fp_cipher);


    return 0;

}
