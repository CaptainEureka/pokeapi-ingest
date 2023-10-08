Set FontSize 20
Set FontFamily "VictorMono Nerd Font Mono"
Set Width 1280
Set Height 720
Set Padding 20
Set TypingSpeed 0.2
Set Theme "Catppuccin Mocha"
Set WindowBar Colorful
Set Shell zsh
Output assets/docker-build-n-run-app.gif

Type "# Running the containerised application is pretty simple"
Ctrl+C
Enter 3
Type "docker compose run -it --rm stockpile --help"
Enter
Sleep 2.5s
Type "docker compose run -it --rm stockpile ingest --pokemon-id 317"
Enter
Sleep 10s
Type "clear"
Enter
Sleep 2.5s
Type "bat output/run_*/pokemon_data.json"
Enter
Sleep 3s
Down 2
Sleep 0.5s
Down 2
Sleep 0.5s
Down 2
Sleep 0.5s
Down 2
Type "G"
Sleep 5s
Up 2
Sleep 0.5s
Up 2
Sleep 0.5s
Up 2
Sleep 0.5s
Up 2
Sleep 5s

