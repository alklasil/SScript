#ifndef _SSTD_h
#define _SSTD_h

#include "SConf.h"

// basic operations
void add();
void sub();
void mul();
void div();
void set();
void set_const();
void lt();
void gt();
void eq();
void neq();
void maxXYZ();

// helpers
void executeState();
void _if();
void _abortExpressionExecution();
void _abortStateExecution();

// timer
void readTimer();
void getTime();
void timeout();

// print
void printInt();
void printInt_ln();
void printString();
void printString_ln();
void clearString();
void concatString_String();
void concatString_Int();
void concatString_Int_List();

#define SSTD_FUNCTIONS_ALL add, \
    sub, \
    div, \
    mul, \
    set, \
    set_const, \
    lt, \
    gt, \
    eq, \
    neq, \
    maxXYZ, \
    /* helpers */ \
    executeState, \
    _if, \
    _abortExpressionExecution, \
    _abortStateExecution, \
    /* timer */ \
    readTimer, \
    getTime, \
    timeout, \
    /* printclearString */ \
    printInt, \
    printInt_ln, \
    printString, \
    printString_ln, \
    clearString, \
    concatString_String, \
    concatString_Int, \
    concatString_Int_List
    /* math */

#endif
