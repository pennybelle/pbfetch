RGB_REGEX = r"\$RGB\(\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*\)"
RGB_START = r"rgb\(\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*\)"
RGB_END = r"\/rgb"
FINAL_RGB_START = r"<rgb\(\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*\)\>"
COLOR_RESET = r"[38;2;\g<1>;\g<2>;\g<3>m"

DEFAULT_CONFIG = r"""
┌────────────────────────────────────────────────────────┬─────────────────────┐
│ Software:                                              │$hst                 │
│ • os     $sys                                          ├─────────────────────┤
│ • ker    $ker                                          │   <rgb(23,147,209)>       .       </rgb>   │ <comment> these lines dont match up           </comment>
│ • bios   $bio                                          │   <rgb(23,147,209)>      /#\      </rgb>   │ <comment> because of the color tags,          </comment>
│ • fs     $fsm                                          │   <rgb(23,147,209)>     /###\     </rgb>   │ <comment> however the tags dont appear        </comment>
│ • term   $trm                                          │   <rgb(23,147,209)>    /p^###\    </rgb>   │ <comment> in the console output so            </comment>
│ • sh     $shl                                          │   <rgb(23,147,209)>   /##P^q##\   </rgb>   │ <comment> adjust your formatting              </comment>
│ • de     $den                                          │   <rgb(23,147,209)>  /##(   )##\  </rgb>   │ <comment> accordingly, as demonstrated.       </comment>
│ • wm     $wmn                                          │   <rgb(23,147,209)> /###P   q#,^\ </rgb>   │ <comment> it is recommended to build your     </comment>
│ • thme   $thm                                          │   <rgb(23,147,209)>/P^         ^q\</rgb>   │ <comment> structure before adding color tags. </comment>
│ • lcl    $lcl                                          │                     │
│ • tfnt   $tft                                          └─────────────────────┤
│ • fnt    $fnt                                                                │
│ • pkgs   $pac                                                                │
│ • up     $upt                                                                │
│                                                                              │
│ Hardware:                                                                    │
│ • comp   $cmp                                                                │
│ • cpu    $cpu                                                                │
│ • gpu    $gpu                                                                │
│ • mb     $mbd                                                                │
│ • ram    $mem                           <comment> inline comment </comment>  │
│ • disc   $dsc                                                                │
│ • res    $res                                                                │
│ • batt   $bat                                                                │
└──────────────────────────────────────────────────────────────────────────────┘

<comment> Comments can be left by prefixing the line with <comment>
<comment> Inline comments are also possible now! To end an inline comment, end it with </comment>

<comment> Legend:

<comment> $cmp = computer name
<comment> $usr = username@hostname
<comment> $hst = hostname
<comment> $sys = operating system
<comment> $ach = cpu architecture
<comment> $ker = kernel
<comment> $mem = ram (used/total MB)
<comment> $upt = uptime
<comment> $pac = packages (pacman, & flatpak supported)
<comment> $cpu = cpu name
<comment> $dsk = disk (used/total MB)
<comment> $shl = current shell
<comment> $wmn = window manager
<comment> $den = desktop environment
<comment> $fsm = filesystem
<comment> $lcl = locale
<comment> $bat = battery
<comment> $gpu = gpu name
<comment> $mbd = motherboard name
<comment> $bio = bios type (UEFI/Legacy)
<comment> $res = screen resolution (WIP)
<comment> $dat = date and time
<comment> $thm = theme
<comment> $fnt = system font
<comment> $tft = terminal font
<comment> $trm = terminal name

<comment> Warnings:

<comment> - Make sure there's enough whitespace between a
<comment> keyword tag and any non-whitespace following it
<comment> to fill in the stat data
<comment> - Whitespace is only removed from the END of the
<comment> final line (so comments dont cause weird output beahavior)
<comment> - Using escape characters can cause unpredictable behavior.
<comment> Use the <rgb()> and </rgb> tags for colors instead
<comment> - Make sure to close your <rgb()> tags with </rgb> to prevent
<comment> unpredictable behavior. If there is another line
<comment> it is recommended to use these tags at the beginning of the
<comment> next line instead of the end of a line

<comment> Plans:

<comment> - Allow color by line/character index by giving an array as an
<comment> input in the config.txt
<comment> This would allow for a more comprehensive config while also
<comment> allowing for more color customization options
<comment> - Add photos to fetch output

<comment> Known Bugs:

<comment> - Using multiple keyword tags on one line can cause
<comment> unpredictable behavior 
<comment> and may require fine tuning by the user
<comment> - RGB tags can interfere with stat prints if directly
<comment> to the right of the stat keyword
<comment> - Current comment style is too prone to false positives,
<comment> this method is flawed and will be changed later
"""

PLUG = """
                _|            _|_|              _|                _|        
      _|_|_|    _|_|_|      _|        _|_|    _|_|_|_|    _|_|_|  _|_|_|    
      _|    _|  _|    _|  _|_|_|_|  _|_|_|_|    _|      _|        _|    _|  
      _|    _|  _|    _|    _|      _|          _|      _|        _|    _|  
      _|_|_|    _|_|_|      _|        _|_|_|      _|_|    _|_|_|  _|    _|  
      _|                                                                    
      _|                                                                    
                                                                                  
              This project aims to be the most customizable fetch.          
              You can do almost anything with the config.txt.               
              It is located in $configpath
                                                                                     
              Have fun customizing! Take note of the comments in            
              the default config, as they contain valuable info.
"""
