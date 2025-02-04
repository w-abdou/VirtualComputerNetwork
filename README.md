
# Virtual Computer Network

## Overview

The **Virtual Computer Network** is a console-based application that simulates a network of virtual computers. It allows users to create and manage a network, establish connections between computers, send messages, and analyze network behavior. The application demonstrates key concepts of networking, including topology management, data transmission, and network routing.

## Features

- **Create Virtual Computers**: Users can add virtual computers to the network.
- **Establish Connections**: Define and modify connections between computers.
- **Send Messages**: Transmit data between virtual computers.
- **Network Topology Management**: Visualize and manage the structure of the network.
- **Analyze Network Behavior**: Simulate data flow and measure network performance.
- **Error Handling & Logging**: Ensures robust message transmission with error checking and logging.

## Code Structure

The main components of the code are:

1. **Data Structures**:
    - `Computer`: Represents a virtual computer with attributes such as ID, name, and connection list.
    - `Network`: Manages the collection of computers and their connections.

2. **Functions**:
    - `addComputer()`: Adds a new virtual computer to the network.
    - `connectComputers()`: Establishes a connection between two computers.
    - `sendMessage()`: Sends a message from one computer to another.
    - `displayNetwork()`: Shows the current network topology.
    - `analyzeNetwork()`: Evaluates network efficiency and connection reliability.

## How to Use

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/w-abdou/VirtualComputerNetwork.git
   cd VirtualComputerNetwork
   ```

2. **Compile the Program**  
   Use a C compiler (e.g., GCC) to compile the source code:
   ```bash
   gcc VirtualComputerNetwork.c -o VirtualComputerNetwork
   ```

3. **Run the Program**  
   Execute the compiled binary:
   ```bash
   ./VirtualComputerNetwork
   ```

4. **Main Menu**  
   The program starts with a main menu where users can:
   - Add computers to the network.
   - Connect computers.
   - Send messages between computers.
   - Display the network topology.
   - Analyze network behavior.

## Example Usage

1. **Create Computers**  
   - Add multiple computers to the virtual network.
   
2. **Establish Connections**  
   - Define network connections between computers.
   
3. **Send Messages**  
   - Transmit messages between connected computers and observe routing behavior.
   
4. **Analyze Network**  
   - Evaluate the network structure and performance metrics.

## Notes

- Ensure valid inputs to avoid unexpected behavior.
- The program currently uses a predefined set of network configurations.

## Future Enhancements

- Implement real-time packet tracking.
- Support for dynamic routing algorithms.
- Introduce graphical visualization for better user interaction.
- Enhance network security features.

