def calculate_intra_region_data_cost(amount):
    gb = 1024
    cost_per_gb = 0.01
    total_data = amount * gb

    return (total_data * cost_per_gb) + (total_data * cost_per_gb)

def calculate_outbound_data_cost(to, amount):
    gb = 1024
    amount = amount * gb
    cost = 0
    first_10_tb = 10240
    next_40_tb = 40960
    next_100_tb = 102400
    gb_150 = 153600

    if to == 'internet':
        if amount <= first_10_tb:
            cost += amount * 0.09
            return cost
        else:
            cost += first_10_tb * 0.09

        if first_10_tb < amount <= next_40_tb:
            cost += (amount - first_10_tb) * 0.085
            print(abs((next_40_tb - (amount - first_10_tb))))
            return cost
        else:
            cost += next_40_tb * 0.085

        if next_40_tb < amount <= next_100_tb:
            cost += abs((next_100_tb - (amount + next_40_tb + first_10_tb))) * 0.07
            return cost

        if next_100_tb < amount <= gb_150:
            cost += abs(amount - (next_40_tb + first_10_tb)) * 0.07

        if amount > gb_150:
            cost += next_100_tb * 0.07
            cost += abs(amount - (first_10_tb + next_40_tb + next_100_tb)) * 0.05
            x = abs(amount - (first_10_tb + next_40_tb + next_100_tb))

    if to == 'other regions':
        cost += amount * 0.02

    return cost
