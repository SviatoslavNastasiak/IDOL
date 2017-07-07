#include <stdio.h>
#include <stdlib.h>
#include "c_module.h"

const char * ReadDataFromFile(const char * fileName)
{
    FILE * file_hndl = fopen(fileName, "r");

    char *fcontent = NULL;
    int fsize = 0;

    if(file_hndl) {
        fseek(file_hndl, 0, SEEK_END);
        fsize = ftell(file_hndl);
        rewind(file_hndl);

        fcontent = (char*) malloc(sizeof(char) * fsize);
        fread(fcontent, 1, fsize, file_hndl);
    }

    fclose(file_hndl);

    return fcontent;
}
