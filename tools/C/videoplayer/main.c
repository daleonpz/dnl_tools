#include "headers/video_selector.h"


int main( int argc,char **argv){
    
    struct vplayer vPlayer;

    vplayer_init(&vPlayer);

    play_video(argv[1], &vPlayer);

    vplayer_quit(&vPlayer);

}
