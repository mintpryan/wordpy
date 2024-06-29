import linecache
import random
from rich.console import Console

SQUARED_EMOJIS = {'A': '🄰', 'B': '🄱', 'C': '🄲', 'D': '🄳', 'E': '🄴', 'F': '🄵', 'G': '🄶', 'H': '🄷', 'I': '🄸', 'J': '🄹', 'K': '🄺', 'L': '🄻','M': '🄼', 'N': '🄽', 'O': '🄾', 'P': '🄿', 'Q': '🅀', 'R': '🅁', 'S': '🅂', 'T': '🅃', 'U': '🅄', 'V': '🅅', 'W': '🅆', 'X': '🅇', 'Y': '🅈', 'Z': '🅉'}

line_count: int = 0
with open('words.csv', 'r') as file:
    line_count = sum(1 for line in file)

console: Console = Console()

"""The class is used for validating user input."""
class UserInput():
    def __init__(self) -> None:
        pass

    @staticmethod
    def input_int(message: str) -> int:
        int_value = None
        while type(int_value) != int:
            try:
                int_value = int(input(message))
            except ValueError:
                print("🚧 Enter correct value. 🚧")
        return int_value

    @staticmethod
    def input_alphabic(num_of_letters: int, message: str) -> str:
        try:
            word: str = input(message)
            if len(word) != num_of_letters or not word.isalpha():
                raise Exception

            return word
        except Exception:
            print(f"🚧 Make sure to enter the word correctly (only {num_of_letters} letters). 🚧")
            return None


class Game():

    def __init__(self) -> None:
        self.history: list = []


    """This method print user's attempts in the game"""
    def game_history(self) -> None:
        print("\nYour game history:")
        for i, item in enumerate(self.history):
            print(
                f'{i+1}.', " ".join([SQUARED_EMOJIS.get(char.upper()) for char in item]))
            

    """This method start the game"""
    def run(self) -> None:
        print("--------- 🅆 🄾 🅁 🄳 🄿 🅈 ---------\n")
        console.print(
            "In the game, you need to guess a 5-letter word within a limited number of attempts.\nRules:\n[red]🅆[/red] - The letter is absent in the word.\n[yellow]🄸[/yellow] - The letter is in the guessed word, but not in its correct position.\n[green]🄽[/green] - The letter is in the word and in the correct position, you guessed correctly.")

        max_attempts: int = UserInput.input_int("Enter number of attempts: ")
        line_num: int = random.randint(0, line_count)
        guess_word: str = linecache.getline('words.csv', line_num).strip()

        print("Let's start!")
        user_word: str = UserInput.input_alphabic(5, "Enter the word: ")
        self.history.append(user_word)
        tries_num: int = 1

        if user_word and user_word.lower() == guess_word:
            print("You won on the first try! 🥳")
            self.game_history()
            return
        else:
            while tries_num < max_attempts:
                if user_word and user_word.lower() == guess_word:
                    break
                elif user_word:
                    colors: list = ['', '', '', '', '']
                    temp: str = ""
                    for i, item in enumerate(user_word):
                        l_item: str = item.lower()
                        if l_item == guess_word[i]:
                            colors[i] = 'green'
                            temp += l_item
                    for i, item in enumerate(user_word):
                        l_item: str = item.lower()
                        if l_item in guess_word and guess_word.count(l_item) > temp.count(l_item):
                            colors[i] = 'yellow'
                            temp += l_item
                        elif not colors[i]:
                            colors[i] = 'red'
                    colored_text: str = ' '.join(f"[{colors[i % len(colors)]}]{
                        SQUARED_EMOJIS.get(char.upper())}[/{colors[i % len(colors)]}]" for i, char in enumerate(user_word))
                    console.print(colored_text)
                    tries_num += 1
                    
                user_word: str = UserInput.input_alphabic(
                    5, "Enter the word: ")
                self.history.append(user_word)
            print()
            if user_word and user_word.lower() != guess_word and tries_num >= max_attempts:
                print("You're lose 😞")
                print("The word - ", " ".join([SQUARED_EMOJIS.get(char.upper()) for char in guess_word]))
            if user_word and user_word.lower() == guess_word and tries_num <= max_attempts:
                print("You win! 🥳")
            self.game_history()


def main() -> None:
    game: Game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        print("\nGoodbye! 🌟")
        exit(0)


if __name__ == "__main__":
    main()
