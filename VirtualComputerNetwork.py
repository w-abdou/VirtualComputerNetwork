import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import networkx as nx
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random
import ipaddress


class NetworkSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Simulator")
        self.root.geometry("1200x800")

        # Canvas for drawing the topology
        self.canvas = tk.Canvas(self.root, bg="white", width=900, height=800, scrollregion=(0, 0, 2000, 2000))
        self.canvas.pack(side="left", fill="both", expand=True)

        # Add scrollbars for large topologies
        h_scroll = ttk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        h_scroll.pack(side="bottom", fill="x")
        v_scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        v_scroll.pack(side="right", fill="y")
        self.canvas.config(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        # Frame for control buttons
        self.control_frame = ttk.Frame(self.root, padding=10)
        self.control_frame.pack(side="right", fill="y")

        ttk.Label(self.control_frame, text="Network Simulator", font=("Arial", 16), bootstyle="info").pack(pady=10)

        # Load device icons
        self.icons = {
            "pc": ImageTk.PhotoImage(Image.open("pc.png").resize((50, 50))),
            "router": ImageTk.PhotoImage(Image.open("router.png").resize((50, 50))),
            "server": ImageTk.PhotoImage(Image.open("server.png").resize((50, 50))),
            "switch": ImageTk.PhotoImage(Image.open("switch.png").resize((50, 50))),
        }

        # Device Buttons
        ttk.Button(self.control_frame, text="Add PC", image=self.icons["pc"], compound="top",
                   command=lambda: self.set_device_type("pc"), bootstyle="outline").pack(pady=5, fill="x")
        ttk.Button(self.control_frame, text="Add Router", image=self.icons["router"], compound="top",
                   command=lambda: self.set_device_type("router"), bootstyle="outline").pack(pady=5, fill="x")
        ttk.Button(self.control_frame, text="Add Server", image=self.icons["server"], compound="top",
                   command=lambda: self.set_device_type("server"), bootstyle="outline").pack(pady=5, fill="x")
        ttk.Button(self.control_frame, text="Add Switch", image=self.icons["switch"], compound="top",
                   command=lambda: self.set_device_type("switch"), bootstyle="outline").pack(pady=5, fill="x")

        # Simulation Buttons
        ttk.Separator(self.control_frame, bootstyle="info").pack(fill="x", pady=10)
        ttk.Button(self.control_frame, text="Link Devices", command=self.link_devices, bootstyle="primary").pack(pady=5, fill="x")
        ttk.Button(self.control_frame, text="Send Packet", command=self.simulate_packet, bootstyle="success").pack(pady=5, fill="x")
        
        # Protocol Buttons
        ttk.Button(self.control_frame, text="TCP Packet", command=lambda: self.simulate_packet(protocol="TCP"), bootstyle="info").pack(pady=5, fill="x")
        ttk.Button(self.control_frame, text="UDP Packet", command=lambda: self.simulate_packet(protocol="UDP"), bootstyle="info").pack(pady=5, fill="x")
        ttk.Button(self.control_frame, text="ICMP Packet", command=lambda: self.simulate_packet(protocol="ICMP"), bootstyle="info").pack(pady=5, fill="x")

        ttk.Button(self.control_frame, text="Reset Simulation", command=self.reset_simulation, bootstyle="danger").pack(pady=20, fill="x")

        # Variables
        self.selected_device = None
        self.device_positions = {}
        self.device_names = {}
        self.device_count = 0
        self.network_topology = nx.Graph()
        self.ip_addresses = {}  
        self.arp_tables = {}  
        self.links = []  

        self.base_network = ipaddress.IPv4Network("192.168.0.0/24")
        self.current_ip_index = 1 

        # Bind canvas events
        self.canvas.bind("<Button-1>", self.add_device)
        self.canvas.bind("<Button-2>", self.show_context_menu)

    def set_device_type(self, device_type):
        """Set the type of device to add."""
        self.selected_device = device_type
        messagebox.showinfo("Device Selection", f"Selected: {device_type.capitalize()}")

    def generate_ip(self):
        """Generate the next IP address."""
        if self.current_ip_index >= self.base_network.num_addresses - 1:
            raise Exception("No more IP addresses available in this subnet.")
        ip = self.base_network[self.current_ip_index]
        self.current_ip_index += 1
        return str(ip)

    def generate_mac(self):
        """Generate a random MAC address."""
        mac = [0x00, 0x16, 0x3e,
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0xff),
               random.randint(0x00, 0xff)]
        return ':'.join(map(lambda x: "%02x" % x, mac))

    def add_device(self, event):
        """Add a device to the canvas with an IP address."""
        if not self.selected_device:
            messagebox.showwarning("No Device Selected", "Please select a device type first.")
            return

        x, y = event.x, event.y
        device_label = f"{self.selected_device.capitalize()}{self.device_count}"
        device_name = simpledialog.askstring("Device Name", f"Enter name for {device_label}:") or device_label

        # Generate and assign an IP address
        try:
            ip_address = self.generate_ip()
            mac_address = self.generate_mac()
        except Exception as e:
            messagebox.showerror("IP Error", str(e))
            return

        # Add icon and label
        icon_id = self.canvas.create_image(x, y, image=self.icons[self.selected_device], anchor=tk.CENTER, tags=device_name)
        label_id = self.canvas.create_text(x, y + 35, text=f"{device_name}\n{ip_address}", font=("Arial", 10), tags=device_name)

        # Store device info
        self.device_positions[device_name] = (x, y)
        self.device_names[device_name] = self.selected_device
        self.ip_addresses[device_name] = ip_address
        self.network_topology.add_node(device_name, type=self.selected_device, ip=ip_address, mac=mac_address)

        # Initialize ARP table for the device
        self.arp_tables[device_name] = {}

        self.device_count += 1
        self.selected_device = None  

    def link_devices(self):
        """Link two devices together."""
        devices = list(self.device_positions.keys())
        if len(devices) < 2:
            messagebox.showwarning("Insufficient Devices", "Add at least two devices to link them.")
            return

        device1 = simpledialog.askstring("Link Devices", f"Enter first device name (Available: {', '.join(devices)}):")
        device2 = simpledialog.askstring("Link Devices", f"Enter second device name (Available: {', '.join(devices)}):")

        if device1 not in devices or device2 not in devices:
            messagebox.showerror("Device Not Found", "One or both devices do not exist.")
            return

        if device1 == device2:
            messagebox.showerror("Invalid Link", "Cannot link a device to itself.")
            return

        x1, y1 = self.device_positions[device1]
        x2, y2 = self.device_positions[device2]
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2, fill="blue")
        self.network_topology.add_edge(device1, device2)
        self.links.append((device1, device2))
        messagebox.showinfo("Link Created", f"Linked {device1} to {device2}.")

    def reset_simulation(self):
        """Reset the simulation."""
        self.canvas.delete("all")
        self.device_positions.clear()
        self.device_names.clear()
        self.ip_addresses.clear()
        self.arp_tables.clear()
        self.device_count = 0
        self.current_ip_index = 1
        self.network_topology.clear()
        self.links.clear()
        messagebox.showinfo("Reset", "Simulation has been reset.")

    def resolve_arp(self, source, destination):
        """Resolve the MAC address using ARP."""
        if destination in self.arp_tables[source]:
            return self.arp_tables[source][destination]

        messagebox.showinfo("ARP Request", f"{source} is sending ARP request for {destination}.")
        destination_mac = self.network_topology.nodes[destination].get("mac")
        self.arp_tables[source][destination] = destination_mac
        self.arp_tables[destination][source] = self.network_topology.nodes[source].get("mac")
        messagebox.showinfo("ARP Reply", f"{destination} replied with MAC address {destination_mac}.")
        return destination_mac

    def simulate_packet(self, protocol="Generic"):
        """Simulate packet delivery between two devices."""
        devices = list(self.device_positions.keys())
        if len(devices) < 2:
            messagebox.showwarning("Insufficient Devices", "Add at least two devices to simulate a packet.")
            return

        source = simpledialog.askstring("Send Packet", f"Enter source device (Available: {', '.join(devices)}):")
        destination = simpledialog.askstring("Send Packet", f"Enter destination device (Available: {', '.join(devices)}):")

        if source not in devices or destination not in devices:
            messagebox.showerror("Device Not Found", "One or both devices do not exist.")
            return

        if nx.has_path(self.network_topology, source, destination):
            path = nx.shortest_path(self.network_topology, source, destination)
            self.resolve_arp(source, destination)  
            messagebox.showinfo("Packet Delivery", f"{protocol} Packet delivered successfully via path: {' -> '.join(path)}")
        else:
            messagebox.showerror("No Route", "No route exists between the devices.")


    def show_context_menu(self, event):
        """Show a context menu on right-click."""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="View Details", command=lambda: self.view_device_details(event.x, event.y))
        menu.add_command(label="Remove Device", command=lambda: self.remove_device(event.x, event.y))
        menu.post(event.x_root, event.y_root)

if __name__ == "__main__":
    root = ttk.Window(themename="darkly") 
    app = NetworkSimulator(root)
    root.mainloop()
