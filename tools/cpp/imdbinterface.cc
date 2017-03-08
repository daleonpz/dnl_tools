#include <stdio.h>
#include <libpq-fe.h>
#include <string.h> 
#include <stdlib.h>
#include <iostream>
#include "parse.h"

/*
 * TODO: 
 *      - ask for possible actions to perform ( add, delete, display)
 *      - add predefined queries ( display full table, one entry)
 *      - add data
 *      - delete data
 * */


static void exit_nicely(PGconn *conn)
{
    PQfinish(conn);
    exit(1);
}


int main(int argc, char* argv[]) {
    PGconn          *conn;
    PGresult        *res;
    int             rec_count;
    int             nFields;
    int             row;
    int             col;
 
    DB_INPUT dbinputs;

    init_dbinputs(&dbinputs);

    char *connparse;
    connparse = (char*) calloc(MAX_LENGTH, sizeof(char));

    parse_input(argc,argv,&dbinputs);
   
    sprintf(connparse,
            "dbname=%s host=%s user=%s password=%s",
            dbinputs.dbname,
            dbinputs.dbhost,
            dbinputs.dbuser,
            dbinputs.dbpassword);

    conn = PQconnectdb(connparse);
     
    free_dbinputs(&dbinputs);
    free(connparse);

     if (PQstatus(conn) == CONNECTION_BAD) {
        fprintf(stderr, "Connection to database failed: %s",
                PQerrorMessage(conn));
        exit_nicely(conn);
     }
     else 
         puts("Connection is established!");

     res = PQexec(conn, "select * from parkour");
     /* sorted entries (codigo, nombre, email)*/
 
     if (PQresultStatus(res) != PGRES_TUPLES_OK) {
        fprintf(stderr, "FETCH ALL failed: %s", PQerrorMessage(conn));
        PQclear(res);
        exit_nicely(conn);
     }

     rec_count = PQntuples(res);
     nFields = PQnfields(res);

     printf("We received %d records.\n", rec_count);
     puts("==========================");
 
     for (row=0; row<rec_count; row++) {
             for (col=0; col<nFields; col++) {
                     printf("%s\t", PQgetvalue(res, row, col));
             }
             puts("");
     }
 
     puts("==========================");

     PQclear(res);

     PQfinish(conn);

     puts("Connection is closed!");
 
     return 0;
 }
