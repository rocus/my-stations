  
This repository describes a plugin for streamtuner-ng.

(see https://github.com/IronWolve/StreamTuner-ng)

The plugin makes a directory on your computer visable in streamtuner-ng. This directory is supposed to contain playable radio stations contained in pls files (or other containers). Because streamtuner-ng can only handle structures for 2 levels, your directory should be 1 or 2 levels deep. (the next level is not visable). But this limitation is obviously better than programs that let you play pls files in just one container. For example your streamtuner-ng's favorites (and locals) are just one level. See one other repository of me that "syncs" your "favorites" with a directory on your PC.

There is only one thing to set in the plugin and that is the ROOT string. You must set that to the root of your radio stations tree. The next time you start streamtuner-ng you see that root in the "my own stations" plugin.

The files in the radio tree (supposedly pls and m3u) are directly fed to the internal mpv player.

If you rightclick (in streamtuner-ng) on the channel ("my own stations") a filemanager will be started at the ROOT directory. When you change something with this filemanager the change does not immediately shows, you have to do a reload for that.
