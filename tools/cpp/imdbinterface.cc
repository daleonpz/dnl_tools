#include <stdio.h>
//#include <libpq-fe.h>
#include <stdlib.h>
#include "parse.h"
#include "db_interface.h"

/*
 * TODO: 
 *      - add predefined queries ( display full table, one entry)
 *      - add data
 *      - delete data
 * */


int main(int argc, char* argv[]) {
    int             rec_count;
    int             nFields;
    int             row;
    int             col;
    int             op;
 
    DB_INPUT dbinputs;
    init_dbinputs(&dbinputs);
    parse_input(argc,argv,&dbinputs);

    DBinterface dbinterface(&dbinputs);
    free_dbinputs(&dbinputs);

    dbinterface.checkconnection();

    if( (op=dbinterface.display_menu()) < 0 ){
        puts("invalid option");
        exit(1);
    } 
/*

     res = PQexec(conn, "select * from parkour");
      sorted entries (codigo, nombre, email) 
 
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
*/
 //   ~dbinterface();
//     puts("Connection is closed!");
 
     return 0;
 }
