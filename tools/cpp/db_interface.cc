#include "db_interface.h"

/* ---------------------------------------- */ 
/*           CONSTRUCTOR                    */
/* ---------------------------------------- */ 
DBinterface::DBinterface(DB_INPUT* inputs){
    char *connparse;
    connparse = (char*) calloc(MAX_LENGTH, sizeof(char));

    sprintf(connparse,
            "dbname=%s host=%s user=%s password=%s",
            inputs->dbname,
            inputs->dbhost,
            inputs->dbuser,
            inputs->dbpassword);

    conn = PQconnectdb(connparse);
    free(connparse);
}

/* ---------------------------------------- */ 
/*            DESTRUCTOR                    */
/* ---------------------------------------- */ 
DBinterface::~DBinterface(){
    PQfinish(conn);
    puts("Connection is closed!");

}

/* ---------------------------------------- */ 
/*            M A C R O S                   */
/* ---------------------------------------- */ 

/* ---------------------------------------- */ 
/*            M E T H O D S                 */
/* ---------------------------------------- */ 
void DBinterface::checkconnection() {
    if (PQstatus(conn) == CONNECTION_BAD) {
        fprintf(stderr, "Connection to database failed: %s",
                PQerrorMessage(conn));
        exit(1);
     }
     else{
        puts("Connection is established!") ;
     }
}



int DBinterface::display_menu() {

    int option;

    cout << "What do you want to do?" << endl;
    cout << "(1) retrieve data" << endl;
    cout << "(2) update data" << endl;
    cout << "(3) delete data" << endl;

    cin >> option;

    if ((option < 1 ) || (option > 3) ){
        return 1;
    }

    switch(option){
        case 1:
            retrieve_data();
            break;

        case 2:
            break;

        case 3:
            break;
    }



    return 0;
}


void DBinterface::retrieve_data(){
    PGresult *res;
    string query;
    int ntuples;
    int nfields;
    int i,j;

    cin.ignore();
    cout << "q<< ";
    getline(cin,query);
    res = PQexec(conn, query.c_str() );

    if ( PQresultStatus(res) != PGRES_TUPLES_OK ){
        fprintf(stderr, "FETCH ALL failed: %s", PQerrorMessage(conn));
        PQclear(res);
        exit(1);
    }

    ntuples = PQntuples(res);
    nfields = PQnfields(res);

    puts("==========================");
 
    for (i=0; i<ntuples; i++) {
        for (j=0; j<nfields; j++) {
            printf("%s\t", PQgetvalue(res, i, j));
         }
        puts("");
    }
 
    puts("==========================");

    PQclear(res);
}

