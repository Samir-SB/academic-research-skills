import matplotlib.pyplot as plt
from collections import deque, Counter


# ----------------------------- Actions -----------------------------------------------------

def plot_bar_from_counter(data):
    """
    Plots a bar chart from a dictionary or collections.Counter object.
    
    Parameters:
    data (dict): A dictionary or Counter object where keys are categories 
                 and values are frequencies.
    """
    # Sort keys to ensure the x-axis follows a logical order (0, 1, 2...)
    sorted_keys = sorted(data.keys())
    sorted_values = [data[k] for k in sorted_keys]

    # Create the bar plot
    plt.bar(sorted_keys, sorted_values, color='skyblue', edgecolor='black')

    # Add labels and title
    plt.xlabel('Actions')
    plt.ylabel('Frequency')
    plt.title('Frequency Distribution')

    # Ensure all keys are shown on the x-axis
    plt.xticks(sorted_keys)

    # Save and show the plot
    plt.savefig('bar_chart.png')
    plt.show()


def plot_stacked_actions(total_data, valid_data):
    """
    Plots a stacked bar chart showing valid vs invalid actions.
    
    Parameters:
    total_data (dict): Dictionary of total counts per category.
    valid_data (dict): Dictionary of valid counts per category.
    """
    # Sort keys to ensure consistent order
    sorted_keys = sorted(total_data.keys())
    
    # Calculate values
    valid_vals = [valid_data.get(k, 0) for k in sorted_keys]
    invalid_vals = [total_data[k] - valid_data.get(k, 0) for k in sorted_keys]

    # Create the stacked bars
    # Valid actions as the base
    plt.bar(sorted_keys, valid_vals, label='Valid Actions', color='#4CAF50', edgecolor='black')
    
    # Invalid actions stacked on top using 'bottom'
    plt.bar(sorted_keys, invalid_vals, bottom=valid_vals, label='Invalid Actions', color='#F44336', edgecolor='black')

    # Formatting
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.title('Total Actions: Valid vs Invalid')
    plt.xticks(sorted_keys)
    plt.legend()

    # Save and show
    plt.savefig('stacked_bar_chart.png')
    plt.show()


# -------------------------------- 


# ---------------------------------------------------------------------------
# Example usage with your data:
if __name__ == "__main__":
    # Data from your request
    total = {5: 3946, 3: 1358, 4: 1347, 1: 1141, 0: 865, 2: 373}
    valid = {5: 3367, 4: 1220, 1: 1136, 3: 982, 0: 780, 2: 373}

    # plot_bar_from_counter(total)

    plot_stacked_actions(total, valid)
