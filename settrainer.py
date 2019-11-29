from card import Card
from random import randint

class SetTrainer:
    def __init__(self):
        self.cards = self.populate_cards()

    def populate_cards(self):
        """Populate the set of cards with respective shape, number, color and shade attributes."""

        for i1 in range(0, 3):
            # Set Shape variables
            if i1 == 0:
                shape = 'O'  # Oval
            elif i1 == 1:
                shape = 'S'  # Squigly
            else:
                shape = 'D'  # Diamond

            for i2 in range(0, 3):
                # Set Color Variables
                if i2 == 0:
                    color = 'R'  # Red
                elif i2 == 1:
                    color = 'G'  # Green
                else:
                    color = 'V'  # Violet

                for i3 in range(0, 3):
                    # Set Shade Variables
                    if i3 == 0:
                        shade = 'E'  # Empty
                    elif i3 == 1:
                        shade = 'H'  # Half full/Striped
                    else:
                        shade = 'F'  # Full

                    for i4 in range(0, 3):
                        # Set Number Variables
                        if i3 == 0:
                            number = '1'
                        elif i3 == 1:
                            number = '2'
                        else:
                            number = '3'

                        self.cards.append(Card(shape, color, number, shade))

    def get_cards(self, amount):
        output_cards = []

        for i in range(0, amount):
            output_cards.append(self.get_random_card())

        return output_cards

    def get_random_card(self):
        random_index = randint(0, len(self.cards) - 1)
        return self.cards[random_index]



if __name__ == "__main__":
    st = SetTrainer()

    st.populate_cards()

    print(st.generate_card().number)
