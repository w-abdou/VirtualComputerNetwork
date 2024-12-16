import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import networkx as nx
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class NetworkSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Simulator")
        self.root.geometry("1200x800")

        self.canvas = tk.Canvas(self.root, bg="white", width=900, height=800, scrollregion=(0, 0, 2000, 2000))
        self.canvas.pack(side="left", fill="both", expand=True)

        h_scroll = ttk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        h_scroll.pack(side="bottom", fill="x")
        v_scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        v_scroll.pack(side="right", fill="y")
        self.canvas.config(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        self.canvas.bind("<MouseWheel>", self.zoom_canvas)

        self.control_frame = ttk.Frame(self.root, padding=10)
        self.control_frame.pack(side="right", fill="y")

        ttk.Label(self.control_frame, text="Network Simulator", font=("Arial", 16), bootstyle="info").pack(pady=10)

        self.icons = {
            "pc": ImageTk.PhotoImage(Image.open("pc.png").resize((50, 50))),
            "router": ImageTk.PhotoImage(Image.open("router.png").resize((50, 50))),
            "server": ImageTk.PhotoImage(Image.open("server.png").resize((50, 50))),
            "switch": ImageTk.PhotoImage(Image.open("switch.png").resize((50, 50))),
        }

        ttk.Button(self.control_frame, text="Add PC", image=self.icons["pc"], compound="top",
                   command=lambda: self.set_device_type("pc"), bootstyle="outline").pack(pady=5, fill="x")
        ttk.Button(self.control_frame, text="Add Router", image=self.icons["router"], compound="top",
                   command=lambda: self.set_device_type("router"), bootstyle="outline").pack(pady=5, fill="x")
        ttk.Button(self.control_frame, text="Add Server", image=self.icons["server"], compound="top",
                   command=lambda: self.set_device_type("server"), bootstyle="outline").pack(pady=5, fill="x")
        ttk.Button(self.control_frame, text="Add Switch", image=self.icons["switch"], compound="top",
                   command=lambda: self.set_device_type("switch"), bootstyle="outline").pack(pady=5, fill="x")

        ttk.Button(self.control_frame, text="Link Devices", command=self.link_devices, bootstyle="primary").pack(pady=10, fill="x")
        ttk.Button(self.control_frame, text="Ping (ICMP)", command=self.simulate_icmp, bootstyle="secondary").pack(pady=5, fill="x")
        ttk.Button(self.control_frame, text="ARP Request", command=self.simulate_arp, bootstyle="secondary").pack(pady=5, fill="x")
        ttk.Button(self.control_frame, text="TCP", command=self.simulate_tcp, bootstyle="secondary").pack(pady=5, fill="x")
        ttk.Button(self.control_frame, text="UDP", command=self.simulate_udp, bootstyle="secondary").pack(pady=5, fill="x")
        ttk.Button(self.control_frame, text="Reset Simulation", command=self.reset_simulation, bootstyle="danger").pack(pady=20, fill="x")

        self.selected_device = None
        self.device_positions = {}
        self.device_names = {}
        self.device_count = 0
        self.network_topology = nx.Graph()

        self.canvas.bind("<Button-1>", self.add_device)
        self.canvas.bind("<Button-2>", self.show_context_menu)

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

        icon_id = self.canvas.create_image(x, y, image=self.icons[self.selected_device], anchor=tk.CENTER, tags=device_name)
        label_id = self.canvas.create_text(x, y + 35, text=device_name, font=("Arial", 10), tags=device_name)

        self.device_positions[device_name] = (x, y)
        self.device_names[device_name] = self.selected_device
        self.network_topology.add_node(device_name, type=self.selected_device)

        self.device_count += 1
        self.selected_device = None  

        self.canvas.tag_bind(device_name, "<B1-Motion>", lambda e: self.move_device(e, device_name))

    def move_device(self, event, device_name):
        """Allow dragging devices."""
        x, y = event.x, event.y
        self.canvas.coords(device_name, x, y)
        self.device_positions[device_name] = (x, y)

    def link_devices(self):
        """Link two devices in the topology."""
        device1 = simpledialog.askstring("Link Devices", "Enter name of the first device:")
        device2 = simpledialog.askstring("Link Devices", "Enter name of the second device:")

        if device1 in self.device_positions and device2 in self.device_positions:
            x1, y1 = self.device_positions[device1]
            x2, y2 = self.device_positions[device2]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2, tags=f"{device1}-{device2}")
            self.network_topology.add_edge(device1, device2)
            messagebox.showinfo("Linking", f"Linked {device1} and {device2}.")
        else:
            messagebox.showwarning("Invalid Devices", "One or both devices not found.")

    def show_context_menu(self, event):
        """Show a context menu on right-click."""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="View Details", command=lambda: self.view_device_details(event.x, event.y))
        menu.add_command(label="Remove Device", command=lambda: self.remove_device(event.x, event.y))
        menu.post(event.x_root, event.y_root)

    def view_device_details(self, x, y):
        """Show details of a device."""
        for device_name, (dx, dy) in self.device_positions.items():
            if abs(x - dx) < 30 and abs(y - dy) < 30:
                device_type = self.device_names[device_name]
                messagebox.showinfo("Device Details", f"Name: {device_name}\nType: {device_type}")
                return
        messagebox.showwarning("No Device", "No device found at this location.")

    def remove_device(self, x, y):
        """Remove a device from the canvas and topology."""
        for device_name, (dx, dy) in self.device_positions.items():
            if abs(x - dx) < 30 and abs(y - dy) < 30:
                self.canvas.delete(device_name)
                self.network_topology.remove_node(device_name)
                del self.device_positions[device_name]
                del self.device_names[device_name]
                messagebox.showinfo("Remove Device", f"Device {device_name} removed.")
                return

    def zoom_canvas(self, event):
        """Zoom in and out on the canvas."""
        scale = 1.1 if event.delta > 0 else 0.9
        self.canvas.scale("all", self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, scale, scale)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

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
    root = ttk.Window(themename="darkly")  
    app = NetworkSimulator(root)
    root.mainloop()
