void safe() {
    char buffer[8];
    strncpy(buffer, "abc", sizeof(buffer)-1);
    buffer[sizeof(buffer)-1] = '\0';
}