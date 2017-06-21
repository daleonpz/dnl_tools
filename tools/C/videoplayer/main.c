#include "headers/parser.h"
#include "headers/video_selector.h"

/* ------------------------------------------- */
/*   TODO                                   
      - be able to close the sdl windows
      - after watching ask whether you would like to delete or keep the file
 */
/* ------------------------------------------- */



#include <sys/types.h>
#include <dirent.h>

#define FALSE 0
#define TRUE !FALSE

#define MAX_FILE_LENGTH 100

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
    vplayer_init(&vPlayer);

    struct dirent **eps;
    int n;

    n = scandir (vPlayer.file, &eps, file_select, alphasort);
    if (n >= 0) {
      int cnt;
//       size_t pathlen = strlen(vPlayer.file);
      char *fullpath = (char *)malloc(MAX_FILE_LENGTH);

      for (cnt = 0; cnt < n; ++cnt){
//               char *fullpath = malloc(pathlen + strlen(eps[cnt]->d_name) + 2);
              sprintf(fullpath,"%s%s", vPlayer.file, eps[cnt]->d_name);
              puts(fullpath);
              play_video(fullpath, &vPlayer);
//               free(fullpath);
      }
      free(fullpath);
    }
    else    
        if ( valid_format(vPlayer.file ) ){
                puts(vPlayer.file);
                play_video(vPlayer.file, &vPlayer);
        }       
        else
            fprintf(stderr,"No valid file format or couldn't open the directory\n");

    vplayer_quit(&vPlayer);
}
