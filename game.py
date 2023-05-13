
class GameExcpetion(Exception):
    pass


class GameState:
    def __init__(self, x=7, y=6, win_condition=4, player_num=2):
        if not x or not y:
            raise ValueError(f'invalid size {x}x{y}')
        if win_condition > y:
            raise ValueError(f'invalid win conditon')
        if player_num < 1:
            raise ValueError(f'invalid players number')

        self.x = x
        self.y = y
        self.win_condition = win_condition
        self.player_num = player_num

        self.ground = [[None] * self.x for i in range(self.y)]
        self.players = list(range(self.player_num))
        self.current_player = 0
        self.winner = None

    def __repr__(self):
        return '\n'.join(
            '|'.join(
                self._show_cell(cell) for cell in row
            )
            for row in self.ground
        )

    def _show_cell(self, cell):
        if cell is None:
            return ' '
        return str(cell)

    def get_current_player(self):
        return self.current_player

    def _switch_player(self):
        next_player = self.current_player + 1
        if next_player >= len(self.players):
            self.current_player = 0
        else:
            self.current_player = next_player

    def make_throw(self, player: bool, x):
        self._check_not_full()
        if self.winner is not None:
            raise RuntimeError(f'{self.winner} already won')
        if player not in self.players:
            raise RuntimeError(f'{player} not exists')
        if player != self.get_current_player():
            raise RuntimeError(f'{player} is not current player')
        if x >= self.x or x < 0:
            raise GameExcpetion('invalid column')

        free_cell_y = self._get_free_cell(x)
        if free_cell_y is None:
            raise GameExcpetion('column is busy')
        self.ground[free_cell_y][x] = player
        if self._check_win(x):
            self.winner = player
            return self.winner
        self._switch_player()

    def _check_not_full(self):
        if not any(cell is None for row in self.ground for cell in row):
            raise GameExcpetion('ground is full')

    def _get_win_cords(self):
        yield from self._get_vertical_cords()
        yield from self._get_horizontal_cords()
        yield from self._get_diagonal_cords()

    def _get_vertical_cords(self):
        for y in range(self.y):
            yield [(y, x) for x in range(self.x)]

    def _get_horizontal_cords(self):
        for x in range(self.x):
            yield [(y, x) for y in range(self.y)]

    def _get_diagonal_cords(self):
        for x in range(self.x):
            cords = [(y, x + y) for y in range(self.y)]
            if len(cords) <= self.win_condition:
                yield cords

        for y in range(self.y):
            cords = [(y + x, x) for y in range(self.x)]
            if len(cords) <= self.win_condition:
                yield cords

    def _check_win(self, x):
        for cords in self._get_win_cords():
            last_player = None
            counter = 0
            for y, x in cords:
                cell = self.ground[y][x]
                if last_player is None or last_player != cell:
                    last_player = cell
                    counter = 1
                else:
                    counter += 1
                    if counter >= self.win_condition:
                        return True

    def _get_free_cell(self, x: int):
        for y in range(self.y):
            cell = self.ground[y][x]
            if cell is not None:
                if not y:
                    return
                return y - 1
        return y


class UI:
    def __init__(self, game_state: GameState):
        self.game_state = game_state

    def run(self):
        while 1:
            print(self.game_state)

            current_player = self.game_state.get_current_player()

            throw_cmd = input(f'player {current_player} throw:')

            if throw_cmd == 'q':
                print('goodbye')
                break
            try:
                throw_x = int(throw_cmd)
            except ValueError:
                print('throw value must be integer')
                continue
            try:
                winner = self.game_state.make_throw(current_player, throw_x)
                if winner is not None:
                    print(f'player {winner} win!')
                    return
            except GameExcpetion as e:
                print(f'error: {e}')
                continue


def main():
    game_state = GameState()
    ui = UI(game_state)
    ui.run()


if __name__ == '__main__':
    main()
