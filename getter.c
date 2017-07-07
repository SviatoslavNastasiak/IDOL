#include "getter.h"

const char * get_msg(const char * fileName)
{
    FILE* file;
    file = fopen(fileName, "r");
    char *buffer = NULL;
    int fsize = 0;

    if(file) {
        fseek(file, 0, SEEK_END);
        fsize = ftell(file);
        rewind(file);

        buffer = (char*) calloc(fsize, sizeof(char));
        if(1 != fread(buffer, fsize, sizeof(char), file) )
            {
                fclose(file);
                free(buffer);
                exit(1);
            }
    }
    else 
    {
        perror("cannot open a file\n");
        exit(1);
    }

    fclose(file);

    return buffer;
}

