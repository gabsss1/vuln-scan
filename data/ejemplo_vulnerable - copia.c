#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void funcion_vulnerable(char *input) {
    char buffer[50];
    
    // Vulnerabilidad de desbordamiento de buffer (buffer overflow)
    strcpy(buffer, input);
    
    printf("Has introducido: %s\n", buffer);
}

void funcion_secreta() {
    printf("¡Has explotado la vulnerabilidad!\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Uso: %s <entrada>\n", argv[0]);
        return 1;
    }
    
    // Vulnerabilidad de formato en printf (format string vulnerability)
    printf(argv[1]);
    
    // Llamada a una función vulnerable
    funcion_vulnerable(argv[1]);
    
    return 0;
}
