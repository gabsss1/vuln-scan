#include <stdio.h>
#include <string.h>

void vulnerable() {
    char buffer[10];
    gets(buffer); // ⚠️ Esta función es insegura (buffer overflow)
    printf("Input: %s\n", buffer);
}