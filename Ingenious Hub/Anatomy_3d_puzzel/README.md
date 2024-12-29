# 3D Anatomy Organs Puzzle Game - Pelvis

This project involves creating a 3D anatomy puzzle game where users can interact with different parts of the pelvis organ, rotate, flip, and manually piece the organ back together. The pelvis is cut into several parts, randomized in 3D space, and the user must align them correctly, much like a 3D Tetris game.

## Features

- **Pelvis Organ Selection**: The group is working on the pelvis organ for this puzzle.
- **3D Pelvis Model**: A high-quality 3D model of the pelvis is used, with cuts made into 5 to 8 parts for the puzzle.
- **Interactive Game**: The puzzle game allows the user to rotate, flip, and align the pelvis parts manually to form the complete organ.
- **Randomized Parts**: The parts of the pelvis are randomized in 3D space, and their orientations are also randomized.
- **Game Controls**: The game allows players to use keyboard shortcuts to manipulate the pieces and reassemble the pelvis.

## Tools and Technologies

- **Blender**: Used for creating and cutting the 3D pelvis model into separate parts. Ensure the organ is a surface model, not a volume model.
- **Unity**: Used for game development. Unity handles the 3D environment, user interaction, and game logic.
- **C#**: The primary programming language for the Unity game development.
  
## Steps to Follow

### 1. Organ Selection
The group has selected the **pelvis** organ for the puzzle game.

### 2. Obtain 3D Model
Obtain a high-quality 3D model of the pelvis. Use **Blender** to visualize and ensure that the pelvis is in surface model form.

### 3. Cutting the Pelvis
In Blender, cut the pelvis into 5 to 8 parts. These cuts can either be based on the pelvis’s natural sub-components or through geometric cuts. These parts will later be used as puzzle pieces.

### 4. Game Development
Develop the 3D puzzle game in **Unity** with the following features:

- **Randomization**: Randomly position and orient the pelvis puzzle pieces in the 3D space when the game starts.
- **Interaction**: Allow users to flip and rotate the parts using keyboard shortcuts (similar to Tetris).
- **Manual Assembly**: The user can manually move and position the pieces to form the whole pelvis.

### 5. Game Controls
Provide the user with intuitive controls:

- Use keyboard shortcuts to rotate and flip each part (e.g., arrow keys for rotation, spacebar for flipping).
- Allow the user to manually move the parts closer to their correct positions by clicking and dragging.

## Requirements

- **Unity**: Download and install Unity (any version compatible with the 3D game development needs).
- **Blender**: To create and cut the pelvis into parts.
- **3D Model Files**: Ensure that the 3D models are in formats compatible with Unity (e.g., .fbx or .obj).

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/3d-anatomy-puzzle.git
    cd 3d-anatomy-puzzle
    ```

2. Open the project in Unity.

3. Import your 3D pelvis model into Unity by copying the model files (e.g., `.fbx`) into the `Assets` folder.

4. Develop the game logic and implement the interactions (rotations, flips, and manual assembly).

## Usage

To start the game:

1. Open the Unity project.
2. Press the `Play` button in Unity to start the game.
3. Select the pelvis puzzle from the UI, and interact with the pieces using the provided controls.

## Contributing

If you would like to contribute to this project, feel free to:

- Fork the repository.
- Submit issues for bugs or feature requests.
- Create pull requests for any improvements or fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This README now clearly states that the project is focused on the pelvis organ for the anatomy puzzle game.
