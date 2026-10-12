
from cards import Deck, hand_value


class Blackjack:
    def __init__(self):
        self.chips = 100
        self._round_counter = 0
        self._settled_rounds = set()

    def _draw_card(self, deck, owner, hidden=False):
        """Draw safely and report only cards that were actually drawn."""
        card = deck.draw()

        if card is None:
            print("Deck is empty. Round cancelled; wager returned.")
            return None

        if hidden:
            print(f"{owner} receives a face-down card.")
        else:
            rank, suit = card
            print(f"{owner} draws: {rank}{suit}")

        return card

    def show(self, player, dealer, hide=True):
        shown_dealer = (
            ["??"] if hide
            else [f"{r}{s}" for r, s in dealer]
        )
        print("Dealer:", " ".join(shown_dealer))
        print(
            "Player:", " ".join(f"{r}{s}" for r, s in player),
            "=", hand_value(player)
        )

    def round(self):
        deck = Deck()

        # Initial deal: check every draw before using the card.
        player = []
        dealer = []

        for _ in range(2):
            card = self._draw_card(deck, "Player")
            if card is None:
                return "cancelled"
            player.append(card)

        card = self._draw_card(deck, "Dealer")
        if card is None:
            return "cancelled"
        dealer.append(card)

        card = self._draw_card(deck, "Dealer", hidden=True)
        if card is None:
            return "cancelled"
        dealer.append(card)

        self.show(player, dealer)

        pv = hand_value(player)
        dv = hand_value(dealer)

        # Natural blackjack: initial two-card 21.
        player_natural = pv == 21 and len(player) == 2
        dealer_natural = dv == 21 and len(dealer) == 2

        if player_natural or dealer_natural:
            self.show(player, dealer, hide=False)

            if player_natural and dealer_natural:
                print("Push. Both have blackjack.")
                return "push"
            elif player_natural:
                print("Player wins with natural blackjack!")
                return "win"
            else:
                print("Dealer wins with natural blackjack.")
                return "loss"

        # Player's turn.
        while hand_value(player) < 21:
            key = input("[h]it [s]tand [q]uit: ").strip().lower()

            if key == "q":
                print("Round cancelled. Wager returned.")
                return "cancelled"

            elif key == "s":
                break

            elif key == "h":
                card = self._draw_card(deck, "Player")
                if card is None:
                    return "cancelled"

                player.append(card)
                self.show(player, dealer)

                if hand_value(player) > 21:
                    print("Player busts. Dealer wins.")
                    self.show(player, dealer, hide=False)
                    return "loss"

            else:
                print("Invalid choice. Enter h, s, or q.")

        # Dealer draws until reaching at least 17.
        while hand_value(dealer) < 17:
            card = self._draw_card(deck, "Dealer")
            if card is None:
                return "cancelled"

            dealer.append(card)

        # Reveal hands and resolve the round.
        self.show(player, dealer, hide=False)

        pv = hand_value(player)
        dv = hand_value(dealer)

        if dv > 21:
            print("Dealer busts. Player wins!")
            return "win"
        elif pv > dv:
            print("Player wins!")
            return "win"
        elif pv < dv:
            print("Dealer wins.")
            return "loss"
        else:
            print("Push. Both hands have the same value.")
            return "push"

    def _settle_wager(self, wager, outcome, round_id):
        # Prevent duplicate settlement.
        if round_id in self._settled_rounds:
            print("Round already settled. Ignoring duplicate settlement.")
            return False

        self._settled_rounds.add(round_id)

        if outcome == "win":
            self.chips += wager
        elif outcome == "loss":
            self.chips -= wager
        elif outcome in ("push", "cancelled"):
            pass
        else:
            self._settled_rounds.remove(round_id)
            raise ValueError(f"Unknown round outcome: {outcome}")

        if outcome == "cancelled":
            print("No chips lost. Wager returned.")

        print("Bankroll:", self.chips, "chips")
        return True

    def run(self):
        print("Blackjack — starting chips:", self.chips)

        while self.chips > 0:
            # Validate the wager before starting a round.
            while True:
                raw_wager = input(
                    f"Enter wager (1-{self.chips}) or q to quit: "
                ).strip().lower()

                if raw_wager == "q":
                    print("Goodbye.")
                    return

                try:
                    wager = int(raw_wager)
                except ValueError:
                    print("Invalid wager. Enter a positive whole number.")
                    continue

                if wager <= 0:
                    print("Invalid wager. Wager must be greater than 0.")
                    continue

                if wager > self.chips:
                    print("Invalid wager. Not enough chips.")
                    continue

                break

            self._round_counter += 1
            round_id = self._round_counter

            outcome = self.round()
            self._settle_wager(wager, outcome, round_id)

            if outcome == "cancelled":
                return

            if self.chips <= 0:
                print("Game over. You have no chips left.")
                return

            # Validate the replay command as well.
            while True:
                answer = input(
                    "Play again? [y/n]: "
                ).strip().lower()

                if answer == "y":
                    break
                elif answer in ("n", "q"):
                    print("Goodbye.")
                    return
                else:
                    print("Invalid choice. Enter y or n.")


if __name__ == "__main__":
    Blackjack().run()
