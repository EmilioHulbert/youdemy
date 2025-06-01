#!/bin/bash

sudo apt-get  install -y devilspie
mkdir -p ~/.devilspie

echo '
(if (contains (window_class) "Code")
	(begin
		(spawn_async (str "xprop -id " (window_xid) " -f _KDE_NET_WM_BLUR_BEHIND_REGION 32c -set _KDE_NET_WM_BLUR_BEHIND_REGION 0 "))
		(spawn_async (str "xprop -id " (window_xid) " -f _NET_WM_WINDOW_OPACITY 32c -set _NET_WM_WINDOW_OPACITY 0xD8000000"))
	)
)
' > ~/.devilspie/vscode_transparent.ds

#https://www.binaryhexconverter.com/decimal-to-hex-converter
# percentage * 255 / 100 , then take number and put in url above
# take 2 chars and add then after 0x
