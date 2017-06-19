#include "headers/parser.h"
#include "headers/video_selector.h"


int main( int argc, char **argv){
    
    struct vplayer vPlayer;

    // TODO: post about passing arg by value, trolling my pointer
    parse_input(argc, argv, &vPlayer);
    printf("file %s\n", vPlayer.file); 
/*
    vplayer_init(&vPlayer);

    play_video(argv[1], &vPlayer);

    vplayer_quit(&vPlayer);
*/
}
