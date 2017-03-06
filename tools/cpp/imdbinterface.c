#include <stdio.h>
#include "libpq-fe.h"
#include <string.h> 
#include <stdlib.h>
#include <iostream>

/*
 * TODO: 
 *      - use something similar to argparser (python)
 *      - add data
 *      - delete data
 * */


#define MAX_LENGTH 200

int     main(int argc, char* argv[]) {
    PGconn          *conn;
    PGresult        *res;
    int             rec_count;
    int             row;
    int             col;
 
    char *conninput;
    conninput = (char*) calloc(MAX_LENGTH, sizeof(char));

    const char *dbuser, *dbpassword;
    dbuser = argv[1];
    dbpassword = argv[2];

    const char *dbname = "pucp";
    const char *dbhost = "localhost";

    sprintf(conninput,"dbname=%s host=%s user=%s password=%s",dbname,dbhost,dbuser,dbpassword);

    conn = PQconnectdb(conninput);
     
    free(conninput);

     if (PQstatus(conn) == CONNECTION_BAD) {
             puts("We were unable to connect to the database");
             exit(0);
     }

     res = PQexec(conn,
             "select * from parkour");
 
     if (PQresultStatus(res) != PGRES_TUPLES_OK) {
             puts("We did not get any data!");
             exit(0);
     }

     rec_count = PQntuples(res);

     printf("We received %d records.\n", rec_count);
     puts("==========================");
 
     for (row=0; row<rec_count; row++) {
             for (col=0; col<3; col++) {
                     printf("%s\t", PQgetvalue(res, row, col));
             }
             puts("");
     }
 
     puts("==========================");

     PQclear(res);

     PQfinish(conn);
 
     return 0;
 }
