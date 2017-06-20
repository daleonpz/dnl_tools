#include "headers/parser.h"
#include "headers/video_selector.h"

#include <sys/types.h>
#include <dirent.h>

#define FALSE 0
#define TRUE !FALSE

static int valid_format(char *file){
    char *ptr;
    ptr = rindex(file, '.');
    if ((ptr != NULL) &&
             ((strcmp(ptr, ".MOV") == 0) ||
             (strcmp(ptr, ".mp4") == 0) ||
             (strcmp(ptr, ".MP4") == 0) || 
             (strcmp(ptr, ".mpeg") == 0) ||
             (strcmp(ptr, ".avi") ==0  ))
       )
	 return (TRUE);
    else
	 return(FALSE);
}

static int file_select(struct dirent *entry){

    if ((strcmp(entry->d_name, ".")== 0) ||
            (strcmp(entry->d_name, "..") == 0)
            )
	 return FALSE;

    return ( valid_format(entry->d_name) );
     
}

int main( int argc, char **argv){
    
    struct vplayer vPlayer;

    // TODO: post about passing arg by value, trolling my pointer
    parse_input(argc, argv, &vPlayer);
    printf("Input file/folder %s\n", vPlayer.file); 

    /*
    DIR *dp;
    struct dirent *ep;
    
    dp = opendir (vPlayer.file);
    if (dp != NULL) {
        while (ep = readdir (dp)){
            if (ep->d_type == DT_REG)
                puts (ep->d_name);
        }
        (void) closedir (dp);
    }
    else
        perror ("Couldn't open the directory");
*/
    struct dirent **eps;
    int n;

    puts("************");
    n = scandir (vPlayer.file, &eps, file_select, alphasort);
    if (n >= 0) {
      int cnt;
      for (cnt = 0; cnt < n; ++cnt)
              puts (eps[cnt]->d_name);
    }
    else    
        if ( valid_format(vPlayer.file ) )
                puts(vPlayer.file);
        else
            fprintf(stderr,"No valid file format or couldn't open the directory\n");

/*
    vplayer_init(&vPlayer);

    play_video(argv[1], &vPlayer);

    vplayer_quit(&vPlayer);
*/
}
