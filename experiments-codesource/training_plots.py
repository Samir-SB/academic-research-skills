import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg
import matplotlib.pyplot as plt
import os
import cv2
import numpy as np

# Create a directory to save the images
os.makedirs('plot', exist_ok=True)

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


def plot_training_metrics(actor_losses, critic_losses, entropy_losses, episode, valid, best, annotations_title, parameters_dict):
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'Training Metrics - Episode {episode}')
    
     # Plot Reward
    # axs[0, 0].plot(rewards, label='Reward', color='yellow')
    axs[0, 0].plot(valid, label='Valid', color='green')
    axs[0, 0].plot(best, label='Best', color='red')
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
        text_str += f'{key}: {value}\n'
        
    return text_str

def create_bar_chart(actions_chosen, N, episode=1):    
    # Count the occurrences of each action
    action_counts = np.bincount(actions_chosen, minlength=N)

    # Calculate the percentage of each action
    action_percentages = (action_counts / len(actions_chosen)) * 100    
    
    # Create a bar chart
    actions = range(N)
    bars = plt.bar(actions, action_percentages, tick_label=[f'Action {i}' for i in actions])

    # Add percentage labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # x-position of the label
            height,                             # y-position of the label
            f'{height:.1f}%',                   # label text
            ha='center',                        # horizontal alignment
            va='bottom'                         # vertical alignment
        )

    plt.xlabel('Actions')
    plt.ylabel('Percentage')
    plt.title(f'Percentage of Selection for Each Action - {episode}')
    plt.savefig('actions.png')
    # plt.show()
    plt.close()

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