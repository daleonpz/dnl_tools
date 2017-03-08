#include "db_interface.h"

// Constructor 
DBinterface::DBinterface(DB_INPUT* inputs){
    char *connparse;
    connparse = (char*) calloc(MAX_LENGTH, sizeof(char));

    printf(connparse,
            "dbname=%s host=%s user=%s password=%s",
            inputs->dbname,
            inputs->dbhost,
            inputs->dbuser,
            inputs->dbpassword);

    conn = PQconnectdb(connparse);
    free(connparse);
/*
    if (PQstatus(conn) == CONNECTION_BAD) {
        fprintf(stderr, "Connection to database failed: %s",
                PQerrorMessage(conn));
        PQfinish(conn);
        exit(1);
     }
     else 
         puts("Connection is established!");
*/
 
}

// Destructor
DBinterface::~DBinterface(){
    PQfinish(conn);
    puts("Connection is closed!");

}

int DBinterface::display_menu() const{

    int option;

    cout << "What do you want to do?" << endl;
    cout << "(1) retrieve data" << endl;
    cout << "(2) update data" << endl;
    cout << "(3) delete data" << endl;

    cin >> option;

    if ((option < 1 ) || (option > 3) ){
        return -1;
    }

    return option;
}


