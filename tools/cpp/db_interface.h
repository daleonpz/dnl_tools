#ifndef _DB_INTERFACE_H_
#define _DB_INTERFACE_H_ 

#include <iostream>
#include <string>
#include <libpq-fe.h>
#include "parse.h"

using namespace std;

/* ------------------------------------------- */
/*            DB INTERFACE                     */
/* ------------------------------------------- */

class DBinterface {
    private:
        PGconn *conn;
        PGresult *res;
    public:
        DBinterface(DB_INPUT*);
        ~DBinterface();

        int display_menu() const;

};
#endif
