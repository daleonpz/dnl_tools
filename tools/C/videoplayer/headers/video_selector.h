#ifndef _VIDEO_SELECTOR_H_
#define _VIDEO_SELECTOR_H_

#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libswscale/swscale.h>

#include <SDL.h>
#include <SDL_thread.h>

#include <stdio.h>

struct vplayer{
        int height;
        int width;
        int bitsperpixels;
        SDL_Overlay *bmp;
        SDL_Surface     *screen;
        SDL_Rect rect;
        SDL_Event event;
    };

int vplayer_init(struct vplayer *vPlayer);
int vplayer_quit(struct vplayer *vPlayer);

int play_video(char *file, struct vplayer *vPlayer);


#endif
