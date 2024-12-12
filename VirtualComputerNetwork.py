import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import networkx as nx
import time

class NetworkSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Simulator")
        self.root.geometry("1200x800")

        # Canvas for drawing the topology
        self.canvas = tk.Canvas(self.root, bg="white", width=900, height=800)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Frame for control buttons
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side="right", fill="y", padx=10, pady=10)

        tk.Label(self.control_frame, text="Network Simulator", font=("Arial", 16)).pack(pady=10)

        # Load device icons
        self.icons = {
            "pc": ImageTk.PhotoImage(Image.open("pc.png").resize((50, 50))),
            "router": ImageTk.PhotoImage(Image.open("router.png").resize((50, 50))),
            "server": ImageTk.PhotoImage(Image.open("server.png").resize((50, 50))),
            "switch": ImageTk.PhotoImage(Image.open("switch.png").resize((50, 50))),
        }

        # Device Buttons
        tk.Button(self.control_frame, text="Add PC", image=self.icons["pc"], compound="top",
                  command=lambda: self.set_device_type("pc")).pack(pady=5)
        tk.Button(self.control_frame, text="Add Router", image=self.icons["router"], compound="top",
                  command=lambda: self.set_device_type("router")).pack(pady=5)
        tk.Button(self.control_frame, text="Add Server", image=self.icons["server"], compound="top",
                  command=lambda: self.set_device_type("server")).pack(pady=5)
        tk.Button(self.control_frame, text="Add Switch", image=self.icons["switch"], compound="top",
                  command=lambda: self.set_device_type("switch")).pack(pady=5)

        # Action Buttons
        tk.Button(self.control_frame, text="Link Devices", command=self.link_devices).pack(pady=10)
        tk.Button(self.control_frame, text="Ping (ICMP)", command=self.simulate_icmp).pack(pady=5)
        tk.Button(self.control_frame, text="ARP Request", command=self.simulate_arp).pack(pady=5)
        tk.Button(self.control_frame, text="TCP", command=self.simulate_tcp).pack(pady=5)
        tk.Button(self.control_frame, text="UDP", command=self.simulate_udp).pack(pady=5)
        tk.Button(self.control_frame, text="Reset Simulation", command=self.reset_simulation).pack(pady=20)

        # Variables
        self.selected_device = None
        self.device_positions = {}
        self.device_names = {}
        self.device_count = 0
        self.network_topology = nx.Graph()

        # Bind canvas click events
        self.canvas.bind("<Button-1>", self.add_device)

        # ARP Table
        self.arp_table = {}

    def set_device_type(self, device_type):
        """Set the type of device to add."""
        self.selected_device = device_type
        messagebox.showinfo("Device Selection", f"Selected: {device_type.capitalize()}")

    def add_device(self, event):
        """Add a device to the canvas."""
        if not self.selected_device:
            messagebox.showwarning("No Device Selected", "Please select a device type first.")
            return

        x, y = event.x, event.y
        device_label = f"{self.selected_device.capitalize()}{self.device_count}"
        device_name = simpledialog.askstring("Device Name", f"Enter name for {device_label}:") or device_label

        # Add icon and label
        self.canvas.create_image(x, y, image=self.icons[self.selected_device], anchor=tk.CENTER)
        self.canvas.create_text(x, y + 35, text=device_name, font=("Arial", 10))

        # Store device info
        self.device_positions[device_name] = (x, y)
        self.device_names[device_name] = self.selected_device
        self.network_topology.add_node(device_name, type=self.selected_device)

        self.device_count += 1
        self.selected_device = None  # Reset selection

    def link_devices(self):
        """Link two devices in the topology."""
        device1 = simpledialog.askstring("Link Devices", "Enter name of the first device:")
        device2 = simpledialog.askstring("Link Devices", "Enter name of the second device:")

        if device1 in self.device_positions and device2 in self.device_positions:
            x1, y1 = self.device_positions[device1]
            x2, y2 = self.device_positions[device2]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
            self.network_topology.add_edge(device1, device2)
            messagebox.showinfo("Linking", f"Linked {device1} and {device2}.")
        else:
            messagebox.showwarning("Invalid Devices", "One or both devices not found.")

    def simulate_icmp(self):
        """Simulate ICMP ping between two devices."""
        source = simpledialog.askstring("ICMP Ping", "Enter source device:")
        destination = simpledialog.askstring("ICMP Ping", "Enter destination device:")

        if self.network_topology.has_edge(source, destination):
            messagebox.showinfo("ICMP", f"Pinging {destination} from {source}: Success!")
        else:
            messagebox.showwarning("ICMP", f"Ping failed: {source} and {destination} are not connected.")

    def simulate_arp(self):
        """Simulate ARP request."""
        ip_address = simpledialog.askstring("ARP Request", "Enter IP address to resolve:")
        if ip_address in self.arp_table:
            mac_address = self.arp_table[ip_address]
            messagebox.showinfo("ARP", f"ARP Response: {ip_address} is at {mac_address}")
        else:
            messagebox.showinfo("ARP", f"ARP Request: Who has {ip_address}?")

    def simulate_tcp(self):
        """Simulate TCP connection."""
        source = simpledialog.askstring("TCP", "Enter source device:")
        destination = simpledialog.askstring("TCP", "Enter destination device:")
        data = simpledialog.askstring("TCP", "Enter data to send:")

        if self.network_topology.has_edge(source, destination):
            messagebox.showinfo("TCP", f"Connection established between {source} and {destination}. Data sent: {data}")
        else:
            messagebox.showwarning("TCP", "Connection failed. Devices are not connected.")

    def simulate_udp(self):
        """Simulate UDP data transfer."""
        source = simpledialog.askstring("UDP", "Enter source device:")
        destination = simpledialog.askstring("UDP", "Enter destination device:")
        data = simpledialog.askstring("UDP", "Enter data to send:")

        if self.network_topology.has_edge(source, destination):
            messagebox.showinfo("UDP", f"Data sent from {source} to {destination}: {data}")
        else:
            messagebox.showwarning("UDP", "Data transfer failed. Devices are not connected.")

    def reset_simulation(self):
        """Reset the simulation."""
        self.canvas.delete("all")
        self.device_positions.clear()
        self.device_names.clear()
        self.device_count = 0
        self.network_topology.clear()
        messagebox.showinfo("Reset", "Simulation has been reset.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkSimulator(root)
    root.mainloop()