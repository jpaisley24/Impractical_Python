import sys
import random
import matplotlib.pyplot as plt
import numpy as np

def read_to_list(file_name):
    """Open a file of data in percent, convert to decimal & return a list."""
    with open(file_name) as in_file:
        lines = [float(line.strip()) for line in in_file]
        decimal = [round(line / 100, 5) for line in lines]
        return decimal

def default_input(prompt, default=None):
    """Allow use of default values in input."""
    prompt = f'{prompt} [{default}]: '
    response = input(prompt)
    if not response and default:
        return default
    else:
        return response

# load data files with original data in percent form
print("\nNote: Input data should be in percent, not decimal!\n")
try:
    bonds = read_to_list('10-yr_TBond_returns_1926-2013_pct.txt')
    stocks = read_to_list('SP500_returns_1926-2013_pct.txt')
    blend_40_50_10 = read_to_list('S-B-C_blend_1926-2013_pct.txt')
    blend_50_50 = read_to_list('S-B_blend_1926-2013_pct.txt')
    infl_rate = read_to_list('annual_infl_rate_1926-2013_pct.txt')
except IOError as e:
    print("{}. \nTerminating program.".format(e), file=sys.stderr)
    sys.exit(1)

# get user input; use dictionary for investment-type arguments
investment_type_args = {'bonds': bonds, 'stocks': stocks,
                        'sb_blend': blend_50_50, 'sbc_blend': blend_40_50_10}

# print input legend for user
print("   stocks = S&P 500")
print("    bonds = 10-yr Treasury Bond")
print(" sb_blend = 50% S&P 500/50% TBond")
print("sbc_blend = 40% S&P 500/50% TBond/10% Cash\n")
print("Press Enter to take default value shown in [brackets].\n")

# get user input
start_value = default_input("Input starting value of investments: \n", \
                            '2000000')
while not start_value.isdigit():
    start_value = input("Invalid input! Input integer only: ")

withdrawal = default_input("Input annual pre-tax withdrawal" \
                           " (today's $): \n", '80000')
while not withdrawal.isdigit():
    withdrawal = input("Invalid input! Input integer only: ")

# start_year = default_input("Starting year: \n", '1926')
# while not start_year.isdigit():
#     start_year = input("Invalid input! Input integer only: ")

def montecarlo(start_year, returns):
    """Run MCS and return investment value at end of plan and bankrupt count."""
    bankrupt_count = 0
    outcome = []
    investments = int(start_value)
    duration = 30
    end_year = int(start_year) + duration

    lifespan = [i for i in range(int(start_year), end_year)]

    # build temporary lists for each case
    lifespan_returns = []
    lifespan_infl = []
    balance = []
    for i in lifespan:
        lifespan_returns.append(returns[i % len(returns)])
        lifespan_infl.append(infl_rate[i % len(infl_rate)])
    # loop through each year of retirement for each case run
    for index, i in enumerate(lifespan_returns):
        infl = lifespan_infl[index]

        # don't adjust for inflation the first year
        if index == 0:
            withdraw_infl_adj = int(withdrawal)
        else:
            withdraw_infl_adj = int(withdraw_infl_adj * (1 + infl))

        investments -= withdraw_infl_adj
        investments = int(investments * (1 + i))
        if investments < 0:
            investments = 0
        balance.append(investments)

    outcome.append(investments)
    outcome = int(outcome[0])

    return start_year, outcome, balance

def main():
    """Call MCS and bankrupt functions and draw bar chart of results."""
    start_year_1, outcome_bonds_1, balance_bonds_1 = montecarlo(1980, investment_type_args['bonds'])
    start_year_1, outcome_stocks_1, balance_stocks_1 = montecarlo(1980, investment_type_args['stocks'])
    start_year_1, outcome_sb_blend_1, balance_sb_blend_1 = montecarlo(1980, investment_type_args['sb_blend'])
    start_year_1, outcome_sbc_blend_1, balance_sbc_blend_1 = montecarlo(1980, investment_type_args['sbc_blend'])

    start_year_2, outcome_bonds_2, balance_bonds_2 = montecarlo(1981, investment_type_args['bonds'])
    start_year_2, outcome_stocks_2, balance_stocks_2 = montecarlo(1981, investment_type_args['stocks'])
    start_year_2, outcome_sb_blend_2, balance_sb_blend_2 = montecarlo(1981, investment_type_args['sb_blend'])
    start_year_2, outcome_sbc_blend_2, balance_sbc_blend_2 = montecarlo(1981, investment_type_args['sbc_blend'])

    print("\nStarting value: ${:,}".format(int(start_value)))
    print("Annual withdrawal: ${:,}".format(int(withdrawal)))
    # print(f"Starting year: {start_year}")
    #
    # print("\nFinal outcomes: ")
    # print(f'${outcome_bonds:,} with bond investment')
    # print(f'${outcome_stocks:,} with stock investment')
    # print(f'${outcome_sb_blend:,} with sb_blend investment')
    # print(f'${outcome_sbc_blend:,} with sbc_blend investment')

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(balance_bonds_1, label='bonds')
    ax1.plot(balance_stocks_1, label='stocks')
    ax1.plot(balance_sb_blend_1, label='sb_blend')
    ax1.plot(balance_sbc_blend_1, label='sbc_blend')
    ax1.set_title(f'Account balance starting from {start_year_1}')
    ax1.set_ylim([0, 10000000])
    ax1.legend()
    ax2.plot(balance_bonds_2, label='bonds')
    ax2.plot(balance_stocks_2, label='stocks')
    ax2.plot(balance_sb_blend_2, label='sb_blend')
    ax2.plot(balance_sbc_blend_2, label='sbc_blend')
    ax2.set_title(f'Account balance starting from {start_year_2}')
    ax2.set_ylim([0, 10000000])
    ax2.legend()
    plt.show()

# run program
if __name__ == '__main__':
    main()


