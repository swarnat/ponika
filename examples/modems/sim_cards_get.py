from examples.config import connection

for sim_card in connection.modems.sim_cards.get_config('1-1'):
    print(sim_card)
