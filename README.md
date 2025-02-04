
# Virtual Computer Network

## Overview

The **Virtual Computer Network** is a desktop application developed in **Java** that simulates a network of virtual computers. It features both a **Graphical User Interface (GUI)** and a command-line mode, allowing users to create and manage a virtual network, establish connections between computers, send messages, and analyze network performance.

## Features

- **Graphical User Interface (GUI)**: An interactive interface for managing the virtual network.
- **Create Virtual Computers**: Users can add and manage virtual computers.
- **Establish Connections**: Define and modify connections between computers.
- **Send Messages**: Transmit data between virtual computers.
- **Network Visualization**: Graphically view and manage the network topology.
- **Analyze Network Behavior**: Simulate data transmission and evaluate network efficiency.
- **Error Handling & Logging**: Ensures reliable communication between nodes.

## Code Structure

The main components of the code include:

### 1. **Core Classes**
- `Computer`: Represents a virtual computer with attributes such as ID, name, and connection list.
- `Network`: Manages the collection of computers and their connections.
- `NetworkManager`: Handles network functionalities such as adding computers, connecting them, and sending messages.

### 2. **Graphical User Interface (GUI)**
- `MainFrame`: The main application window.
- `NetworkPanel`: A panel to visualize the network topology.
- `ControlPanel`: Allows users to add computers, establish connections, and send messages.
- `MessagePanel`: Displays message logs and network activity.

## How to Use

### 1. Clone the Repository:
```bash
git clone https://github.com/w-abdou/VirtualComputerNetwork.git
cd VirtualComputerNetwork
```

### 2. Compile and Run the Application:

#### **For GUI Mode**:
```bash
javac *.java
java MainFrame
```

#### **For Console Mode**:
```bash
javac *.java
java VirtualComputerNetwork
```

### 3. Application Workflow:

#### **GUI Mode:**
1. **Launch the Application**: The main window will open.
2. **Add Computers**: Use the interface to create new computers.
3. **Establish Connections**: Connect computers to form a network.
4. **Send Messages**: Select two connected computers and send messages.
5. **View Network Topology**: The network is displayed visually.
6. **Analyze Network Performance**: View connection logs and error reports.

#### **Console Mode:**
1. Select an option from the main menu:
   - Add a computer
   - Connect computers
   - Send messages
   - Display network topology
2. Follow the prompts to enter details.
3. View network updates in the console output.


## Notes

- Ensure **JavaFX** is installed if the application uses JavaFX for the GUI.
- If using **Swing**, no additional dependencies are required.


