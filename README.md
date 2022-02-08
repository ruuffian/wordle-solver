# wordle-solver

This is just a personal project to teach myself some basic python concepts. It is a very boring brute-force 
algorithm, similar to the one behind the impossible hangman game. The only optimization in terms of guessing
the word quicker is prioritizing words with unique letters in order to guess more unguessed letters, 
and prioritizing words that have letters with higher density scores.

## How to Use the Manual Script

You can start with any word but I have included two suggestions that contain multiple vowels. The script will
then prompt you for wordle output. This is a 5 letter string that gives information on what letters are in the word,
what letters arent, and what letters are in the correct position.

Here are some wordle outputs with screenshots of the wordle screen.

#### Key: b = black, y = yellow, c = correct

![bbbbb.png](assets/bbbbb.png)

`bbbbb`

![ybcbb.png](assets/ybcbb.png)

`ybcbb`

![img.png](assets/bccbb.png)

`bccbb`

Upon successfull word guess, input `ccccc` and the script will tell you how many tries it took. Feel free to pr
or submit issues!

## How to Use the Automated Input Script

This script is muhc easier to use. It will suggest a word based on the game state, but ultimately will accept any word that you give it.
All of the I/O is done on the command line, but you can watch the bot enter the words in the browser that it opens up on runtime.

## TODO

There are some BIG plans for this little project, hopefully some or all of these come to fruition.

    1. Rewrite documentation and add some argument sugar to make methods more clear + encapsulate the code better
    2. Implement argument validation for word length, unknown characters/symbols etc
    3. Improve word suggestion algorithm, ideally with more/better datapoints and normalized scores
    4. Connecting the I/O so that there is a Human mode that waits for input and Bot mode that autocompletes the puzzle
    5. Frontend display of the bot's pass at each days wordle, hosted on gitpages
    6. Bot History -basically a history of each day's wordle, with how many tries the bot took
    7. Poll Twitter to gather global data on each day's wordle, specifically the copy-paste block that wordle offers
    8. Analyze Twitter data to find regional avgs, common words etc
    9. DIsplay Twitter info on gitpage

## License

See [LICENSE.md](LICENSE.md)

## Contributing

Fork or pull or whatever, its a fun little project so I'm sure there are hundreds of changes
that can be done to make it better. I bet you could come up with something way cooler than me!
