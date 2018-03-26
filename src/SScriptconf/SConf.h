#ifndef _SCONF_h
#define _SCONF_h

#include <cstdint>
#include <cstdlib>
#include <stdio.h>
#include <string.h>
#include <SScript.h>

#define FUNCTION_LEFT_PARSE_RIGHT_PARSE \
   int32_t *leftValue = sScript->parseIndex(++sScript->element); \
   int32_t *rightValue = sScript->parseIndex(++sScript->element);

#define FUNCTION_LEFT_PARSE_RIGHT_NOPARSE \
   int32_t *leftValue = sScript->parseIndex(++sScript->element); \
   int32_t *rightValue = ++sScript->element;

#define FUNCTION_LEFT_NOPARSE_RIGHT_PARSE \
   int32_t *leftValue = ++sScript->element; \
   int32_t *rightValue = sScript->parseIndex(++sScript->element);

#define FUNCTION_LEFT_PARSE \
   int32_t *leftValue = sScript->parseIndex(++sScript->element);

#define FUNCTION_LEFT_NOPARSE \
   int32_t *leftValue = ++sScript->element;

#define FUNCTION_ONE_PARSE \
   sScript->parseIndex(++sScript->element);

#define FUNCTION_ONE_NOPARSE \
   ++sScript->element;

#define FUNCTION_END \
   ++sScript->element;


#endif
