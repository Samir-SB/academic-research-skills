import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg
import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
from collections import Counter

# Create a directory to save the images
# os.makedirs('plot', exist_ok=True)

plt.ion()


# Function to create a video from the saved images
def create_video(image_folder, output_video, fps=10):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort()  # Sort images by episode number

    # Read the first image to get the size
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Define the video codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    video.release()
    print(f"Video saved as {output_video}")
    
    # Remove the images after creating the video
    for image in images:
        os.remove(os.path.join(image_folder, image))
    print(f"Removed {len(images)} images from {image_folder}")


def plot_bar_from_counter(data):
    """
    Plot a bar chart from a dictionary or Counter.

    Parameters:
    data: Mapping from category to frequency.
    """
    sorted_keys = sorted(data.keys())
    sorted_values = [data[k] for k in sorted_keys]

    plt.figure(figsize=(10, 5))
    plt.bar(sorted_keys, sorted_values, color='skyblue', edgecolor='black')
    plt.xlabel('Actions')
    plt.ylabel('Frequency')
    plt.title('Frequency Distribution')
    plt.xticks(sorted_keys)
    plt.tight_layout()
    plt.savefig('bar_chart.png')
    plt.close()


def plot_stacked_actions(total_data, valid_data):
    """
    Plot a stacked bar chart showing valid and invalid actions.

    Parameters:
    total_data: Dictionary/Counter of total counts per action.
    valid_data: Dictionary/Counter of valid counts per action.
    """
    total_counter = Counter(total_data)
    valid_counter = Counter(valid_data)
    sorted_keys = sorted(total_counter.keys())

    valid_vals = [valid_counter.get(k, 0) for k in sorted_keys]
    invalid_vals = [total_counter[k] - valid_counter.get(k, 0) for k in sorted_keys]

    plt.figure(figsize=(10, 5))
    plt.bar(sorted_keys, valid_vals, label='Valid Actions', color='#4CAF50', edgecolor='black')
    plt.bar(
        sorted_keys,
        invalid_vals,
        bottom=valid_vals,
        label='Invalid Actions',
        color='#F44336',
        edgecolor='black',
    )

    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.title('Total Actions: Valid vs Invalid')
    plt.xticks(sorted_keys)
    plt.legend()
    plt.tight_layout()
    plt.savefig('plot/stacked_bar_chart.png')
    plt.close()


def plot_training_metrics(actor_losses, critic_losses, entropy_losses, episode, valid, reward, annotations_title, parameters_dict):
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'Training Metrics - Episode {episode}')
    
     # Plot Reward
    # axs[0, 0].plot(rewards, label='Reward', color='yellow')
    axs[0, 0].plot(valid, label='Valid actions', color='green')
    axs[0, 0].plot(reward, label='Reward Percentages', color='red')
    axs[0, 0].set_title('Reward')
    axs[0, 0].set_xlabel('Episode')
    axs[0, 0].set_ylabel('Reward')
    axs[0, 0].legend()

    # Plot Actor Loss
    axs[0, 1].plot(actor_losses, label='Actor Loss', color='red')
    axs[0, 1].set_title('Actor Loss')
    axs[0, 1].set_xlabel('Step')
    axs[0, 1].set_ylabel('Loss')
    axs[0, 1].legend()
    
    # Plot Entropy Loss
    axs[1, 0].plot(entropy_losses, label='Entropy Loss', color='green')
    axs[1, 0].set_title('Entropy Loss')
    axs[1, 0].set_xlabel('Step')
    axs[1, 0].set_ylabel('Loss')
    axs[1, 0].legend()

    # Plot Critic Loss
    axs[1, 1].plot(critic_losses, label='Critic Loss', color='magenta')    
    axs[1, 1].set_title('Critic Loss')
    axs[1, 1].set_xlabel('Step')
    axs[1, 1].set_ylabel('Loss')
    axs[1, 1].legend()

    # Add text annotations for lr, gamma, and n_step
    text_str = set_annotations_text(annotations_title, parameters_dict)
    fig.text(0.08, 0.60, text_str, fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout()
    
    # Save the figure as an image
    plt.savefig(f'plot/episode_a2c.png')
    # Uncomment the following line to enable the generate video function
    # plt.savefig(f'training_plots/episode_{episode:04d}.png')
    
    plt.close(fig)  # Explicitly close the figure to release resources
    
def set_annotations_text(title, parameters_dict):
    text_str = f'{title}\n'
    for key, value in parameters_dict.items():
        if key in ['device', 'random_seed', 'model_dir', 'num_episodes']:
            continue
        text_str += f'{key}: {value}\n'
        
    return text_str

def plot_metrics(rewards, accuracies, losses, title="DQN Training Metrics"):
    """
    Plots rewards, accuracies, and losses in one figure, even if their lengths differ.

    Parameters:
    - rewards (list or numpy array): List of reward values over time.
    - accuracies (list or numpy array): List of accuracy values over time.
    - losses (list or numpy array): List of loss values over time.
    - title (str): Title of the plot.
    """
    
    # Create a figure and a set of subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    
    # Plot rewards
    ax1.plot(range(len(rewards)), rewards, label='Reward', color='blue')
    ax1.set_title('Reward over Time')
    ax1.set_xlabel('Steps')
    ax1.set_ylabel('Reward')
    ax1.legend()
    
    # Plot accuracies
    ax2.plot(range(len(accuracies)), accuracies, label='Accuracy', color='green')
    ax2.set_title('Accuracy over Time')
    ax2.set_xlabel('Steps')
    ax2.set_ylabel('Accuracy')
    ax2.legend()
    
    # Plot losses
    ax3.plot(range(len(losses)), losses, label='Loss', color='red')
    ax3.set_title('Loss over Time')
    ax3.set_xlabel('Steps')
    ax3.set_ylabel('Loss')
    ax3.legend()
    
    # Adjust layout
    plt.tight_layout()
    plt.suptitle(title, y=1.02, fontsize=14)

    # Save figure
    plt.savefig('plot/dqn.png')
    
    # Show the plot
    # plt.show()

if __name__ == "__main__":

    # # After training, create a video from the saved images
    create_video('training_plots', 'training_progress.mp4', fps=5)
