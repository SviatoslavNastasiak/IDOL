%module getter
%{
#define SWIG_FILE_WITH_INIT
#include"getter.h"
%}

const char * get_msg(const char * file);
