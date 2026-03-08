# rfidfyi — Python RFID API Client Demo
Output demo.gif

Set FontSize 20
Set Width 1000
Set Height 560
Set Shell "zsh"
Set Theme "Catppuccin Mocha"
Set TypingSpeed 30ms
Set Padding 24

Type "uv run --with rfidfyi python3"
Enter
Sleep 2s

Type "from rfidfyi import RFIDFYI"
Enter
Sleep 1s

Type "client = RFIDFYI()"
Enter
Sleep 1s

Type "# Search RFID tags"
Enter
Sleep 0.5s

Type "client.search('monza')"
Enter
Sleep 2.5s

Type "# Look up an RFID tag"
Enter
Sleep 0.5s

Type "client.tag('monza-r6')"
Enter
Sleep 3s

Type "exit()"
Enter
Sleep 1s
