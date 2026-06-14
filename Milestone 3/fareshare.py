#!/usr/bin/env python3
"""
FareShare Ride-Sharing System - Complete Application
Database Systems Project - Milestone 3
Namal University, Mianwali

FEATURES:
- Rider books ride → Request sent to drivers
- Drivers receive notifications and can accept/reject
- Real-time ride tracking with animation
- SOS emergency alerts
- Rating system
- Admin dashboard for driver verification
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import mysql.connector
from mysql.connector import Error
import uuid
import datetime
from datetime import datetime as dt
import random
import time
import threading
class Colors:
    PRIMARY = "#6366F1"
    PRIMARY_DARK = "#4F46E5"
    PRIMARY_LIGHT = "#818CF8"
    PRIMARY_GLOW = "#A5B4FC"
    SECONDARY = "#F59E0B"
    SECONDARY_DARK = "#D97706"
    SUCCESS = "#10B981"
    SUCCESS_DARK = "#059669"
    ERROR = "#EF4444"
    ERROR_DARK = "#DC2626"
    WARNING = "#F59E0B"
    INFO = "#3B82F6"
    INFO_DARK = "#2563EB"
    WHITE = "#FFFFFF"
    BLACK = "#111827"
    GRAY_50 = "#F9FAFB"
    GRAY_100 = "#F3F4F6"
    GRAY_200 = "#E5E7EB"
    GRAY_300 = "#D1D5DB"
    GRAY_400 = "#9CA3AF"
    GRAY_500 = "#6B7280"
    GRAY_600 = "#4B5563"
    GRAY_700 = "#374151"
    GRAY_800 = "#1F2937"
    DARK_BG = "#0F172A"
    DARK_SURFACE = "#1E293B"
    DARK_HOVER = "#334155"
    CARD_SHADOW = "#E0E7FF"
    ACCENT_BLUE = "#06B6D4"
    ACCENT_PURPLE = "#8B5CF6"
    ACCENT_GREEN = "#34D399"

class Fonts:
    TITLE = ("Segoe UI", 32, "bold")
    HEADING = ("Segoe UI", 24, "bold")
    SUBHEADING = ("Segoe UI", 18, "bold")
    NORMAL = ("Segoe UI", 11)
    NORMAL_BOLD = ("Segoe UI", 11, "bold")
    SMALL = ("Segoe UI", 9)
    SMALL_BOLD = ("Segoe UI", 9, "bold")
    BUTTON = ("Segoe UI", 12, "bold")
    MONO = ("Consolas", 10)

class ModernButton(tk.Button):
    def __init__(self, parent, text, command, bg_color=Colors.PRIMARY,
                 hover_color=Colors.PRIMARY_DARK, text_color=Colors.WHITE,
                 icon="", width=200, height=40):
        display_text = f"{icon}  {text}" if icon else text
        padx_val, pady_val = (8, 6) if width <= 120 else (24, 11)
        
        super().__init__(
            parent, text=display_text, command=command, bg=bg_color, fg=text_color,
            font=Fonts.BUTTON if width > 120 else Fonts.NORMAL, relief=tk.FLAT,
            cursor="hand2", padx=padx_val, pady=pady_val, activebackground=hover_color,
            activeforeground=text_color, borderwidth=0
        )
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.bind("<Enter>", lambda e: self.configure(bg=self.hover_color))
        self.bind("<Leave>", lambda e: self.configure(bg=self.bg_color))

class ModernCard(tk.Frame):
    def __init__(self, parent, title=None, **kwargs):
        super().__init__(parent, bg=Colors.WHITE, relief=tk.RAISED, bd=1, **kwargs)
        if title:
            title_frame = tk.Frame(self, bg=Colors.WHITE)
            title_frame.pack(fill=tk.X, padx=20, pady=(15, 5))
            tk.Frame(title_frame, bg=Colors.PRIMARY, width=4, height=20).pack(side=tk.LEFT, padx=(0, 10))
            tk.Label(title_frame, text=title, font=Fonts.SUBHEADING, bg=Colors.WHITE, fg=Colors.GRAY_800).pack(side=tk.LEFT)
        self.content = tk.Frame(self, bg=Colors.WHITE)
        self.content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

class ModernEntry(tk.Frame):
    def __init__(self, parent, label_text="", placeholder="", **kwargs):
        super().__init__(parent, bg=Colors.WHITE)
        if label_text:
            tk.Label(self, text=label_text, font=Fonts.SMALL, fg=Colors.GRAY_600, bg=Colors.WHITE, anchor=tk.W).pack(fill=tk.X, padx=12, pady=(8, 0))
        self.entry = tk.Entry(self, font=Fonts.NORMAL, bd=1, relief=tk.SOLID, bg=Colors.WHITE, fg=Colors.GRAY_800, **kwargs)
        self.entry.pack(fill=tk.X, padx=12, pady=(5, 8))
        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.bind("<FocusIn>", lambda e: self._clear_placeholder(placeholder))
            self.entry.bind("<FocusOut>", lambda e: self._restore_placeholder(placeholder))
    
    def _clear_placeholder(self, placeholder):
        if self.entry.get() == placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=Colors.GRAY_800)
    
    def _restore_placeholder(self, placeholder):
        if not self.entry.get():
            self.entry.insert(0, placeholder)
            self.entry.config(fg=Colors.GRAY_400)
    
    def get(self):
        return self.entry.get()
    
    def set(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

class ModernDropdown(tk.Frame):
    def __init__(self, parent, label_text="", options=None, default=None):
        super().__init__(parent, bg=Colors.WHITE)
        if label_text:
            tk.Label(self, text=label_text, font=Fonts.SMALL, fg=Colors.GRAY_600, bg=Colors.WHITE, anchor=tk.W).pack(fill=tk.X, padx=12, pady=(8, 0))
        self.var = tk.StringVar(value=default if default else (options[0] if options else ""))
        self.dropdown = ttk.Combobox(self, textvariable=self.var, values=options, font=Fonts.NORMAL, state="readonly")
        self.dropdown.pack(fill=tk.X, padx=12, pady=(5, 8))
    
    def get(self):
        return self.var.get()

class ToastNotification(tk.Toplevel):
    def __init__(self, parent, message, type="success"):
        super().__init__(parent)
        self.overrideredirect(True)
        colors = {"success": (Colors.SUCCESS, Colors.WHITE), "error": (Colors.ERROR, Colors.WHITE),
                  "warning": (Colors.WARNING, Colors.WHITE), "info": (Colors.INFO, Colors.WHITE),
                  "ride_request": (Colors.PRIMARY, Colors.WHITE)}
        icons = {"success": "✓", "error": "✗", "warning": "⚠", "info": "ℹ", "ride_request": "🚗"}
        bg_color, text_color = colors.get(type, colors["info"])
        
        self.configure(bg=bg_color)
        frame = tk.Frame(self, bg=bg_color)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        tk.Label(frame, text=icons.get(type, "ℹ"), font=("Segoe UI", 14, "bold"), bg=bg_color, fg=text_color).pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(frame, text=message, font=Fonts.NORMAL, bg=bg_color, fg=text_color).pack(side=tk.LEFT)
        
        self.update_idletasks()
        x = parent.winfo_rootx() + parent.winfo_width() // 2 - self.winfo_width() // 2
        y = parent.winfo_rooty() + parent.winfo_height() - 80
        self.geometry(f"+{x}+{y}")
        self.after(3000, self.destroy)

class RideRequestWindow:
    
    def __init__(self, parent, ride_details, on_accept, on_reject):
        self.parent = parent
        self.ride_details = ride_details
        self.on_accept = on_accept
        self.on_reject = on_reject
        self.window = None
        
        self.show_request()
    
    def show_request(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("🚗 New Ride Request - FareShare")
        self.window.geometry("450x480")
        self.window.configure(bg=Colors.WHITE)
        self.window.transient(self.parent)
        self.window.grab_set()
        
        self.window.update_idletasks()
        x, y = (self.window.winfo_screenwidth() - 450) // 2, (self.window.winfo_screenheight() - 480) // 2
        self.window.geometry(f"+{x}+{y}")
        
        header = tk.Frame(self.window, bg=Colors.PRIMARY, height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="🚗 New Ride Request", font=Fonts.HEADING, bg=Colors.PRIMARY, fg=Colors.WHITE).pack(pady=(18, 3))
        tk.Label(header, text="A passenger needs a ride", font=Fonts.NORMAL, bg=Colors.PRIMARY, fg=Colors.PRIMARY_LIGHT).pack()
        
        details_card = ModernCard(self.window, title="📍 Trip Details")
        details_card.pack(fill=tk.X, padx=20, pady=10)
        
        info = [
            (f"👤 Rider: {self.ride_details.get('rider_name', 'A passenger')}", Fonts.NORMAL_BOLD, Colors.GRAY_800),
            (f"📍 From: {self.ride_details.get('pickup', 'Current Location')}", Fonts.NORMAL, Colors.GRAY_700),
            (f"🏁 To: {self.ride_details.get('dropoff', 'Destination')}", Fonts.NORMAL, Colors.GRAY_700),
            (f"💰 Fare: PKR {self.ride_details.get('fare', 0)}", Fonts.NORMAL_BOLD, Colors.PRIMARY)
        ]
        for text, font, color in info:
            tk.Label(details_card.content, text=text, font=font, bg=Colors.WHITE, fg=color).pack(anchor=tk.W, pady=2)
        
        earnings_card = ModernCard(self.window, title="� Your Earnings")
        earnings_card.pack(fill=tk.X, padx=20, pady=10)
        fare = self.ride_details.get('fare', 0)
        tk.Label(earnings_card.content, text=f"You will earn: PKR {fare * 0.85:.0f}", font=Fonts.NORMAL_BOLD, bg=Colors.WHITE, fg=Colors.SUCCESS).pack(anchor=tk.W, pady=2)
        tk.Label(earnings_card.content, text=f"Commission (15%): PKR {fare * 0.15:.0f}", font=Fonts.SMALL, bg=Colors.WHITE, fg=Colors.GRAY_500).pack(anchor=tk.W, pady=2)
        
        time_card = ModernCard(self.window, title="⏱️ Response Time")
        time_card.pack(fill=tk.X, padx=20, pady=10)
        self.time_label = tk.Label(time_card.content, text="You have 30 seconds to respond", font=Fonts.NORMAL, bg=Colors.WHITE, fg=Colors.WARNING)
        self.time_label.pack(pady=10)
        
        btn_frame = tk.Frame(self.window, bg=Colors.WHITE)
        btn_frame.pack(pady=15)
        ModernButton(btn_frame, text="Accept Ride", command=self.accept_ride, bg_color=Colors.SUCCESS, hover_color=Colors.SUCCESS, icon="✅", width=170, height=42).pack(side=tk.LEFT, padx=8)
        ModernButton(btn_frame, text="Decline", command=self.reject_ride, bg_color=Colors.ERROR, hover_color=Colors.ERROR, icon="❌", width=170, height=42).pack(side=tk.LEFT, padx=8)
        
        self.time_left = 30
        self.update_timer()
    
    def update_timer(self):
        if self.time_left <= 0:
            if self.window:
                self.window.destroy()
                self.on_reject()
            return
        self.time_label.config(text=f"⏰ {self.time_left} seconds remaining to accept")
        self.time_left -= 1
        self.window.after(1000, self.update_timer)
    
    def accept_ride(self):
        if self.window:
            self.window.destroy()
            self.on_accept()
    
    def reject_ride(self):
        if self.window:
            self.window.destroy()
            self.on_reject()


class RideAnimationWindow:
    def __init__(self, parent, ride_details, on_complete=None):
        self.parent = parent
        self.ride_details = ride_details
        self.on_complete = on_complete
        self.is_running = True
        self.progress = 0
        self.total_duration = 10
        self.start_time = None
        
        self.window = tk.Toplevel(parent)
        self.window.title("🚗 Ride in Progress - FareShare")
        self.window.geometry("500x600")
        self.window.configure(bg=Colors.GRAY_50)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        self.start_animation()
    
    def setup_ui(self):
        header = tk.Frame(self.window, bg=Colors.PRIMARY, height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🚗 Ride in Progress", font=Fonts.HEADING,
                bg=Colors.PRIMARY, fg=Colors.WHITE).pack(pady=(20, 5))
        tk.Label(header, text="Your driver is taking you to your destination",
                font=Fonts.NORMAL, bg=Colors.PRIMARY, fg=Colors.PRIMARY_LIGHT).pack()
        
        driver_card = ModernCard(self.window, title="👨‍✈️ Driver Information")
        driver_card.pack(fill=tk.X, padx=20, pady=10)
        
        driver_name = self.ride_details.get('driver_name', 'Your Driver')
        vehicle_type = self.ride_details.get('vehicle_type', 'Sedan')
        plate = self.ride_details.get('plate_number', 'ABC-123')
        
        tk.Label(driver_card.content, text=f"Name: {driver_name}", font=Fonts.NORMAL_BOLD,
                bg=Colors.WHITE, fg=Colors.GRAY_800).pack(anchor=tk.W, pady=2)
        tk.Label(driver_card.content, text=f"Vehicle: {vehicle_type} ({plate})", font=Fonts.NORMAL,
                bg=Colors.WHITE, fg=Colors.GRAY_600).pack(anchor=tk.W, pady=2)
        
        trip_card = ModernCard(self.window, title="📍 Trip Information")
        trip_card.pack(fill=tk.X, padx=20, pady=10)
        
        pickup = self.ride_details.get('pickup', 'Current Location')
        dropoff = self.ride_details.get('dropoff', 'Destination')
        fare = self.ride_details.get('fare', 0)
        
        tk.Label(trip_card.content, text=f"From: {pickup}", font=Fonts.NORMAL,
                bg=Colors.WHITE, fg=Colors.GRAY_700).pack(anchor=tk.W, pady=2)
        tk.Label(trip_card.content, text=f"To: {dropoff}", font=Fonts.NORMAL,
                bg=Colors.WHITE, fg=Colors.GRAY_700).pack(anchor=tk.W, pady=2)
        tk.Label(trip_card.content, text=f"Fare: PKR {fare}", font=Fonts.NORMAL_BOLD,
                bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor=tk.W, pady=2)
        
        progress_card = ModernCard(self.window, title="🔄 Trip Progress")
        progress_card.pack(fill=tk.X, padx=20, pady=10)
        
        self.progress_bar = ttk.Progressbar(progress_card.content, mode='determinate', length=400)
        self.progress_bar.pack(pady=10)
        
        self.progress_label = tk.Label(progress_card.content, text="0% Complete",
                                       font=Fonts.NORMAL_BOLD, bg=Colors.WHITE, fg=Colors.PRIMARY)
        self.progress_label.pack()
        
        info_frame = tk.Frame(progress_card.content, bg=Colors.WHITE)
        info_frame.pack(fill=tk.X, pady=10)
        
        self.eta_label = tk.Label(info_frame, text="⏱️ ETA: Calculating...",
                                  font=Fonts.NORMAL, bg=Colors.WHITE, fg=Colors.GRAY_600)
        self.eta_label.pack(side=tk.LEFT, expand=True)
        
        self.distance_label = tk.Label(info_frame, text="📏 Distance: 5.0 km",
                                       font=Fonts.NORMAL, bg=Colors.WHITE, fg=Colors.GRAY_600)
        self.distance_label.pack(side=tk.RIGHT, expand=True)
        
        canvas_frame = ModernCard(self.window, title="🗺️ Route Map")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame.content, height=150, bg=Colors.GRAY_100, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        style = ttk.Style()
        style.configure("TProgressbar", thickness=15, background=Colors.PRIMARY)
    
    def draw_road(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10:
            w = 400
        road_y = h // 2
        self.canvas.create_line(20, road_y, w - 20, road_y, fill=Colors.GRAY_400, width=6, capstyle=tk.ROUND)
        self.canvas.create_line(20, road_y, w - 20, road_y, fill=Colors.GRAY_300, width=2, dash=(10, 5), capstyle=tk.ROUND)
        self.canvas.create_oval(10, road_y - 8, 26, road_y + 8, fill=Colors.SUCCESS, outline="")
        self.canvas.create_text(18, road_y - 12, text="🚩", font=("Segoe UI", 12))
        self.canvas.create_oval(w - 36, road_y - 8, w - 20, road_y + 8, fill=Colors.ERROR, outline="")
        self.canvas.create_text(w - 28, road_y - 12, text="🏁", font=("Segoe UI", 12))
        car_x = 20 + (w - 40) * (self.progress / 100)
        self.canvas.create_text(car_x, road_y, text="🚗", font=("Segoe UI", 24))
    
    def start_animation(self):
        self.start_time = time.time()
        self.update_animation()
    
    def update_animation(self):
        if not self.is_running:
            return
        elapsed = time.time() - self.start_time
        self.progress = min(100, (elapsed / self.total_duration) * 100)
        self.progress_bar['value'] = self.progress
        self.progress_label.config(text=f"{int(self.progress)}% Complete")
        remaining = max(0, self.total_duration - elapsed)
        eta_seconds = int(remaining)
        eta_minutes = eta_seconds // 60
        eta_secs = eta_seconds % 60
        if eta_minutes > 0:
            eta_text = f"⏱️ ETA: {eta_minutes} min {eta_secs} sec"
        else:
            eta_text = f"⏱️ ETA: {eta_secs} seconds"
        self.eta_label.config(text=eta_text)
        distance_remaining = 5.0 * (1 - self.progress / 100)
        self.distance_label.config(text=f"📏 Distance: {distance_remaining:.1f} km")
        self.draw_road()
        if self.progress >= 100:
            self.complete_ride()
        else:
            self.window.after(100, self.update_animation)
    
    def complete_ride(self):
        self.is_running = False
        self.window.destroy()
        messagebox.showinfo("Ride Completed", 
                           f"🎉 You have reached your destination!\n\nTotal Fare: PKR {self.ride_details.get('fare', 0)}\nPlease pay in cash to the driver.\n\nThank you for riding with FareShare!")
        if self.on_complete:
            self.on_complete()
    
    def cancel_ride(self):
        if messagebox.askyesno("Cancel Ride", "Are you sure you want to cancel this ride?"):
            self.is_running = False
            self.window.destroy()
            messagebox.showinfo("Ride Cancelled", "Your ride has been cancelled.")


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.pending_requests = {}
    
    def _execute_safe(self, query, params=None, fetch=True):
        try:
            self.cursor.execute(query, params) if params else self.cursor.execute(query)
            return self.cursor.fetchall() if fetch else self.cursor.rowcount
        except Error as e:
            if not fetch:
                self.connection.rollback()
            raise Exception(f"Query failed: {e}")  # Store pending ride requests for drivers
        
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost', database='fareshare_db', user='root',
                password='Dbh83067', autocommit=False
            )
            self.cursor = self.connection.cursor(dictionary=True)
            return True
        except Error as e:
            print(f"Database error: {e}")
            return False
    
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=None):
        return self._execute_safe(query, params, fetch=True)
    
    def execute_update(self, query, params=None):
        try:
            result = self._execute_safe(query, params, fetch=False)
            self.connection.commit()
            return result
        except Exception as e:
            raise e
    
    def call_procedure(self, procedure_name, params=None):
        try:
            if params:
                self.cursor.callproc(procedure_name, params)
            else:
                self.cursor.callproc(procedure_name)
            results = []
            for result in self.cursor.stored_results():
                results.extend(result.fetchall())
            self.connection.commit()
            return results
        except Error as e:
            self.connection.rollback()
            raise Exception(f"Procedure failed: {e}")
    
    def login_user(self, phone_number, user_role):
        query = "SELECT user_id, full_name, user_role, created_at, phone_number FROM User WHERE phone_number = %s AND user_role = %s"
        results = self.execute_query(query, (phone_number, user_role))
        if results:
            return {'success': True, 'user': results[0]}
        return {'success': False, 'message': 'Invalid credentials'}
    
    def check_phone_exists(self, phone_number):
        query = "SELECT COUNT(*) as count FROM User WHERE phone_number = %s"
        result = self.execute_query(query, (phone_number,))
        return result[0]['count'] > 0 if result else False
    
    def register_rider(self, phone_number, full_name):
        user_id = str(uuid.uuid4())
        try:
            self.call_procedure('sp_register_rider', (user_id, phone_number, full_name, None))
            return {'success': True, 'user_id': user_id}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def register_driver(self, phone_number, full_name, cnic, license_num,
                       vehicle_id, plate_number, vehicle_type, model):
        user_id = str(uuid.uuid4())
        try:
            self.call_procedure('sp_register_driver',
                               (user_id, phone_number, full_name, cnic, 
                                license_num, vehicle_id, plate_number, 
                                vehicle_type, model))
            return {'success': True, 'user_id': user_id}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_available_drivers(self, vehicle_type=None):
        query = """
            SELECT u.user_id, u.full_name, d.rating_average, 
                   v.vehicle_id, v.vehicle_type, v.plate_number, v.model
            FROM Driver d
            JOIN User u ON d.user_id = u.user_id
            JOIN Vehicle v ON d.user_id = v.driver_id
            WHERE d.is_online = TRUE AND d.is_verified = TRUE
        """
        if vehicle_type and vehicle_type != "All":
            query += f" AND v.vehicle_type = '{vehicle_type}'"
        query += " LIMIT 20"
        return self.execute_query(query)
    
    def calculate_fare(self, vehicle_type, distance_km=5, duration_min=10):
        pricing = {
            "Bike": {"base": 30, "per_km": 8, "per_min": 2},
            "Rickshaw": {"base": 50, "per_km": 12, "per_min": 3},
            "Mini": {"base": 80, "per_km": 18, "per_min": 4},
            "Sedan": {"base": 120, "per_km": 25, "per_min": 5}
        }
        p = pricing.get(vehicle_type, pricing["Sedan"])
        fare = p["base"] + (distance_km * p["per_km"]) + (duration_min * p["per_min"])
        return round(fare, 0)
    
    def create_ride_request(self, rider_id, driver_id, vehicle_id, is_shared, 
                            total_fare, pickup, dropoff, rider_name):
        """Create a ride request (pending approval)"""
        ride_id = str(uuid.uuid4())
        request = {
            'ride_id': ride_id,
            'rider_id': rider_id,
            'driver_id': driver_id,
            'vehicle_id': vehicle_id,
            'is_shared': is_shared,
            'total_fare': total_fare,
            'pickup': pickup,
            'dropoff': dropoff,
            'rider_name': rider_name,
            'status': 'pending'
        }
        
        if driver_id not in self.pending_requests:
            self.pending_requests[driver_id] = []
        self.pending_requests[driver_id].append(request)
        
        return {'success': True, 'ride_id': ride_id, 'request': request}
    
    def get_pending_requests_for_driver(self, driver_id):
        """Get pending ride requests for a specific driver"""
        return self.pending_requests.get(driver_id, [])
    
    def accept_ride_request(self, driver_id, ride_id):
        """Driver accepts a ride request"""
        requests = self.pending_requests.get(driver_id, [])
        for req in requests:
            if req['ride_id'] == ride_id and req['status'] == 'pending':
                req['status'] = 'accepted'
                
                if req['rider_id'] == 'fake_rider' or req['vehicle_id'] == 'fake_vehicle':
                    return {'success': True, 'participant_id': 'fake_participant', 'request': req}
                
                participant_id = str(uuid.uuid4())
                payment_id = str(uuid.uuid4())
                
                try:
                    self.call_procedure('sp_book_ride',
                                       (ride_id, driver_id, req['vehicle_id'], req['is_shared'],
                                        req['total_fare'], participant_id, req['rider_id'],
                                        32.5833, 71.5417, 32.5950, 71.5550, payment_id))
                    return {'success': True, 'participant_id': participant_id, 'request': req}
                except Exception as e:
                    return {'success': False, 'message': str(e)}
        return {'success': False, 'message': 'Request not found'}
    
    def reject_ride_request(self, driver_id, ride_id):
        """Driver rejects a ride request"""
        requests = self.pending_requests.get(driver_id, [])
        for req in requests:
            if req['ride_id'] == ride_id:
                req['status'] = 'rejected'
                return {'success': True}
        return {'success': False}
    
    def update_ride_status(self, ride_id, status):
        try:
            query = "UPDATE Ride SET status = %s WHERE ride_id = %s"
            self.execute_update(query, (status, ride_id))
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def complete_ride(self, ride_id, participant_id):
        try:
            self.call_procedure('sp_complete_ride', (ride_id, participant_id))
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_rider_rides(self, rider_id):
        query = """
            SELECT r.ride_id, r.status, r.total_fare, r.created_at,
                   u.full_name as driver_name, r.is_shared,
                   rp.segment_fare, p.is_received, v.vehicle_type, v.plate_number
            FROM Ride r
            JOIN RideParticipant rp ON r.ride_id = rp.ride_id
            LEFT JOIN Driver d ON r.driver_id = d.user_id
            LEFT JOIN User u ON d.user_id = u.user_id
            LEFT JOIN Payment p ON rp.participant_id = p.participant_id
            LEFT JOIN Vehicle v ON r.vehicle_id = v.vehicle_id
            WHERE rp.rider_id = %s
            ORDER BY r.created_at DESC LIMIT 20
        """
        return self.execute_query(query, (rider_id,))
    
    def get_driver_rides(self, driver_id):
        query = """
            SELECT r.ride_id, r.status, r.total_fare, r.created_at,
                   COUNT(rp.participant_id) as passenger_count
            FROM Ride r
            LEFT JOIN RideParticipant rp ON r.ride_id = rp.ride_id
            WHERE r.driver_id = %s
            GROUP BY r.ride_id
            ORDER BY r.created_at DESC LIMIT 20
        """
        return self.execute_query(query, (driver_id,))
    
    def get_driver_earnings(self, driver_id):
        query = """
            SELECT 
                COUNT(*) as total_rides,
                COALESCE(SUM(total_fare), 0) as gross_earnings,
                COALESCE(SUM(total_fare * 0.85), 0) as net_earnings,
                COALESCE(SUM(total_fare * 0.15), 0) as commission
            FROM Ride
            WHERE driver_id = %s AND status = 'Completed'
        """
        return self.execute_query(query, (driver_id,))
    
    def get_ride_by_id(self, ride_id):
        query = """
            SELECT r.*, u.full_name as driver_name, v.vehicle_type, v.plate_number
            FROM Ride r
            LEFT JOIN Driver d ON r.driver_id = d.user_id
            LEFT JOIN User u ON d.user_id = u.user_id
            LEFT JOIN Vehicle v ON r.vehicle_id = v.vehicle_id
            WHERE r.ride_id = %s
        """
        result = self.execute_query(query, (ride_id,))
        return result[0] if result else None
    
    def submit_rating(self, ride_id, rater_user_id, rated_user_id, score, comment):
        rating_id = str(uuid.uuid4())
        try:
            self.call_procedure('sp_submit_rating',
                               (rating_id, ride_id, rater_user_id, 
                                rated_user_id, score, comment))
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_emergency_contacts(self, user_id):
        query = "SELECT contact_id, contact_name, phone_number, relationship FROM EmergencyContact WHERE user_id = %s LIMIT 3"
        return self.execute_query(query, (user_id,))
    
    def add_emergency_contact(self, user_id, name, phone, relationship):
        contact_id = str(uuid.uuid4())
        query = "INSERT INTO EmergencyContact (contact_id, user_id, contact_name, phone_number, relationship) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.execute_update(query, (contact_id, user_id, name, phone, relationship))
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def delete_emergency_contact(self, contact_id):
        query = "DELETE FROM EmergencyContact WHERE contact_id = %s"
        try:
            self.execute_update(query, (contact_id,))
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def trigger_sos(self, ride_id, triggered_by, lat, lng):
        alert_id = str(uuid.uuid4())
        try:
            self.call_procedure('sp_trigger_sos', (alert_id, ride_id, triggered_by, lat, lng))
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def update_driver_status(self, driver_id, is_online):
        try:
            query = "UPDATE Driver SET is_online = %s WHERE user_id = %s"
            self.execute_update(query, (is_online, driver_id))
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_system_stats(self):
        query = """
            SELECT 
                (SELECT COUNT(*) FROM User WHERE user_role = 'Rider') as total_riders,
                (SELECT COUNT(*) FROM User WHERE user_role = 'Driver') as total_drivers,
                (SELECT COUNT(*) FROM Ride WHERE status IN ('Accepted', 'InProgress', 'Requested')) as active_rides,
                (SELECT COUNT(*) FROM Ride WHERE status = 'Completed') as completed_rides,
                (SELECT COALESCE(SUM(total_fare), 0) FROM Ride WHERE status = 'Completed') as total_revenue,
                (SELECT COALESCE(AVG(score), 0) FROM Rating) as avg_rating,
                (SELECT COUNT(*) FROM DriverVerification WHERE verification_status = 'Pending') as pending_verifications
        """
        return self.execute_query(query)
    
    def get_all_users(self, search_term=None):
        query = "SELECT user_id, full_name, phone_number, user_role, created_at FROM User"
        if search_term:
            query += " WHERE full_name LIKE %s OR phone_number LIKE %s LIMIT 50"
            params = (f"%{search_term}%", f"%{search_term}%")
            return self.execute_query(query, params)
        query += " LIMIT 50"
        return self.execute_query(query)
    
    def get_pending_verifications(self):
        query = """
            SELECT dv.verification_id, u.full_name as driver_name, u.phone_number,
                   d.cnic_number, d.license_number, dv.verified_at, d.user_id as driver_id
            FROM DriverVerification dv
            JOIN Driver d ON dv.driver_id = d.user_id
            JOIN User u ON d.user_id = u.user_id
            WHERE dv.verification_status = 'Pending'
            ORDER BY dv.verified_at DESC
        """
        return self.execute_query(query)
    
    def verify_driver(self, verification_id, driver_id, admin_id, status, comments):
        try:
            query = """
                UPDATE DriverVerification 
                SET verification_status = %s, 
                    admin_id = %s, 
                    comments = %s,
                    verified_at = NOW()
                WHERE verification_id = %s
            """
            self.execute_update(query, (status, admin_id, comments, verification_id))
            
            if status == 'Approved':
                query2 = "UPDATE Driver SET is_verified = TRUE WHERE user_id = %s"
                self.execute_update(query2, (driver_id,))
            elif status == 'Rejected':
                query2 = "UPDATE Driver SET is_verified = FALSE WHERE user_id = %s"
                self.execute_update(query2, (driver_id,))
            
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_active_rides(self):
        query = """
            SELECT r.ride_id, r.status, r.total_fare, u.full_name as driver_name, r.is_shared,
                   COUNT(rp.participant_id) as passenger_count
            FROM Ride r
            LEFT JOIN Driver d ON r.driver_id = d.user_id
            LEFT JOIN User u ON d.user_id = u.user_id
            LEFT JOIN RideParticipant rp ON r.ride_id = rp.ride_id
            WHERE r.status IN ('Accepted', 'InProgress', 'Requested')
            GROUP BY r.ride_id
        """
        return self.execute_query(query)


class RiderDashboard:
    def __init__(self, parent, db, user, logout_callback):
        self.parent = parent
        self.db = db
        self.user = user
        self.logout_callback = logout_callback
        self.selected_driver = None
        self.current_ride_id = None
        self.current_participant_id = None
        self.waiting_for_response = False
        self.waiting_window = None
        
        for widget in parent.winfo_children():
            widget.destroy()
        
        self.setup_ui()
        self.load_ride_history()
        self.load_emergency_contacts()
    
    def setup_ui(self):
        sidebar = tk.Frame(self.parent, bg=Colors.DARK_BG, width=280)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        tk.Label(sidebar, text="🚗 FareShare", font=("Segoe UI", 20, "bold"),
                bg=Colors.DARK_BG, fg=Colors.WHITE).pack(pady=25)
        
        avatar_frame = tk.Frame(sidebar, bg=Colors.DARK_SURFACE, height=100)
        avatar_frame.pack(fill=tk.X, padx=20, pady=20)
        avatar_frame.pack_propagate(False)
        
        tk.Label(avatar_frame, text="👤", font=("Segoe UI", 36),
                bg=Colors.DARK_SURFACE, fg=Colors.PRIMARY_LIGHT).pack(pady=10)
        tk.Label(avatar_frame, text=self.user['full_name'][:20], font=Fonts.NORMAL_BOLD,
                bg=Colors.DARK_SURFACE, fg=Colors.WHITE).pack()
        tk.Label(avatar_frame, text=self.user['phone_number'], font=Fonts.SMALL,
                bg=Colors.DARK_SURFACE, fg=Colors.GRAY_400).pack()
        
        nav_items = [("🚗", "Book a Ride", self.show_book), ("📋", "My Rides", self.show_rides),
                     ("🆘", "Emergency", self.show_emergency), ("👤", "Profile", self.show_profile)]
        
        for icon, text, cmd in nav_items:
            btn = tk.Button(sidebar, text=f"  {icon}  {text}", command=cmd,
                           bg=Colors.DARK_BG, fg=Colors.GRAY_300, font=Fonts.NORMAL,
                           relief=tk.FLAT, anchor=tk.W, padx=20, pady=12,
                           activebackground=Colors.DARK_HOVER, activeforeground=Colors.WHITE,
                           cursor="hand2")
            btn.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Frame(sidebar, bg=Colors.DARK_BG, height=20).pack(expand=True)
        logout_btn = tk.Button(sidebar, text="🚪  Logout", command=self.logout,
                              bg=Colors.DARK_SURFACE, fg=Colors.ERROR, font=Fonts.NORMAL,
                              relief=tk.FLAT, padx=20, pady=12, cursor="hand2")
        logout_btn.pack(fill=tk.X, padx=20, pady=20)
        
        self.main = tk.Frame(self.parent, bg=Colors.GRAY_50)
        self.main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        header = tk.Frame(self.main, bg=Colors.WHITE, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="Rider Dashboard", font=("Segoe UI", 16, "bold"),
                bg=Colors.WHITE, fg=Colors.GRAY_800).pack(side=tk.LEFT, padx=20)
        
        self.content = tk.Frame(self.main, bg=Colors.GRAY_50)
        self.content.pack(fill=tk.BOTH, expand=True)
        self.show_book()
    
    def show_toast(self, message, type="success"):
        ToastNotification(self.parent, message, type)
    
    def show_book(self):
        for w in self.content.winfo_children():
            w.destroy()
        self.selected_driver = None

        banner = tk.Frame(self.content, bg=Colors.PRIMARY, height=80)
        banner.pack(fill=tk.X)
        banner.pack_propagate(False)
        bl = tk.Frame(banner, bg=Colors.PRIMARY)
        bl.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=10)
        tk.Label(bl, text=f"👋  Hello, {self.user['full_name'].split()[0]}!",
                 font=("Segoe UI", 18, "bold"), bg=Colors.PRIMARY, fg=Colors.WHITE).pack(anchor=tk.W)
        tk.Label(bl, text="Where are you going today?",
                 font=("Segoe UI", 9), bg=Colors.PRIMARY, fg=Colors.PRIMARY_GLOW).pack(anchor=tk.W)
        badge = tk.Frame(banner, bg=Colors.PRIMARY_DARK, padx=12, pady=7)
        badge.pack(side=tk.RIGHT, padx=15, pady=18)
        tk.Label(badge, text="🚀  FareShare", font=("Segoe UI", 9, "bold"),
                 bg=Colors.PRIMARY_DARK, fg=Colors.PRIMARY_GLOW).pack()

        cols = tk.Frame(self.content, bg=Colors.GRAY_200)
        cols.pack(fill=tk.BOTH, expand=True)

        right = tk.Frame(cols, bg=Colors.WHITE)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(1, 0))
        rh = tk.Frame(right, bg=Colors.WHITE)
        rh.pack(fill=tk.X, padx=15, pady=(12, 0))
        ra = tk.Frame(rh, bg=Colors.ACCENT_PURPLE, width=4, height=18)
        ra.pack(side=tk.LEFT); ra.pack_propagate(False)
        tk.Label(rh, text="  Available Drivers", font=("Segoe UI", 13, "bold"),
                 bg=Colors.WHITE, fg=Colors.GRAY_800).pack(side=tk.LEFT)
        rbtn = tk.Button(rh, text="⟳ Refresh", command=self.load_drivers,
                         bg=Colors.GRAY_100, fg=Colors.GRAY_600, font=("Segoe UI", 9),
                         relief=tk.FLAT, cursor="hand2", padx=8, pady=3)
        rbtn.pack(side=tk.RIGHT)
        rbtn.bind("<Enter>", lambda e: rbtn.config(bg=Colors.PRIMARY, fg=Colors.WHITE))
        rbtn.bind("<Leave>", lambda e: rbtn.config(bg=Colors.GRAY_100, fg=Colors.GRAY_600))
        tk.Label(right, text="Click a driver card to select",
                 font=("Segoe UI", 8), bg=Colors.WHITE, fg=Colors.GRAY_400).pack(
                 anchor=tk.W, padx=15, pady=(2, 5))
        dcv = tk.Canvas(right, bg=Colors.WHITE, highlightthickness=0)
        dsb = ttk.Scrollbar(right, orient="vertical", command=dcv.yview)
        self.drivers_frame = tk.Frame(dcv, bg=Colors.WHITE)
        self.drivers_frame.bind("<Configure>",
            lambda e: dcv.configure(scrollregion=dcv.bbox("all")))
        dcv_win = dcv.create_window((0, 0), window=self.drivers_frame, anchor="nw")
        dcv.configure(yscrollcommand=dsb.set)
        dsb.pack(side=tk.RIGHT, fill=tk.Y)
        dcv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0), pady=(0, 8))
        dcv.bind("<Configure>", lambda e: dcv.itemconfig(dcv_win, width=e.width))

        left = tk.Frame(cols, bg=Colors.WHITE)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 1))

        lh = tk.Frame(left, bg=Colors.WHITE)
        lh.pack(fill=tk.X, padx=15, pady=(12, 0))
        la = tk.Frame(lh, bg=Colors.PRIMARY, width=4, height=18)
        la.pack(side=tk.LEFT); la.pack_propagate(False)
        tk.Label(lh, text="  Book Your Ride", font=("Segoe UI", 13, "bold"),
                 bg=Colors.WHITE, fg=Colors.GRAY_800).pack(side=tk.LEFT)

        ff = tk.Frame(left, bg=Colors.WHITE)
        ff.pack(fill=tk.X, padx=15, pady=(8, 0))

        self._make_icon_entry(ff, "📍", "Pickup Location", "Current Location", is_pickup=True)
        self._make_icon_entry(ff, "🏁", "Drop-off Destination", "Enter destination", is_pickup=False)

        tk.Label(ff, text="Select Vehicle Type", font=("Segoe UI", 9, "bold"),
                 bg=Colors.WHITE, fg=Colors.GRAY_600).pack(anchor=tk.W, pady=(4, 4))
        self.vehicle_var = tk.StringVar(value="Sedan")
        self._vtype_buttons = {}
        self.shared_var = tk.BooleanVar(value=False)
        vtf = tk.Frame(ff, bg=Colors.WHITE)
        vtf.pack(fill=tk.X, pady=(0, 8))
        for vic, vt in [("🏍️", "Bike"), ("🛺", "Rickshaw"), ("🚗", "Mini"), ("🚙", "Sedan")]:
            b = tk.Button(vtf, text=f"{vic} {vt}", font=("Segoe UI", 9, "bold"),
                          relief=tk.FLAT, cursor="hand2", padx=10, pady=6, bd=0,
                          bg=Colors.GRAY_100, fg=Colors.GRAY_600)
            b.pack(side=tk.LEFT, padx=(0, 6))
            self._vtype_buttons[vt] = b
            b.config(command=lambda v=vt: self._select_vehicle(v))

        sr = tk.Frame(ff, bg=Colors.GRAY_50, padx=8, pady=6)
        sr.pack(fill=tk.X, pady=(0, 8))
        tk.Checkbutton(sr, text="🔗  Enable Fare Sharing",
                       variable=self.shared_var, bg=Colors.GRAY_50, fg=Colors.GRAY_700,
                       font=("Segoe UI", 9), selectcolor=Colors.PRIMARY_LIGHT,
                       activebackground=Colors.GRAY_50, cursor="hand2",
                       command=self.update_fare).pack(side=tk.LEFT)
        tk.Label(sr, text="Save up to 50%", font=("Segoe UI", 8, "bold"),
                 bg=Colors.GRAY_50, fg=Colors.SUCCESS).pack(side=tk.LEFT, padx=(6, 0))

        fb = tk.Frame(ff, bg=Colors.PRIMARY_GLOW, padx=2, pady=2)
        fb.pack(fill=tk.X, pady=(0, 8))
        fc = tk.Frame(fb, bg=Colors.PRIMARY)
        fc.pack(fill=tk.BOTH)
        tk.Label(fc, text="✦  Estimated Fare", font=("Segoe UI", 8, "bold"),
                 bg=Colors.PRIMARY, fg=Colors.PRIMARY_GLOW).pack(pady=(8, 0))
        self.fare_label = tk.Label(fc, text="PKR 0", font=("Segoe UI", 26, "bold"),
                                   bg=Colors.PRIMARY, fg=Colors.WHITE)
        self.fare_label.pack()
        tk.Label(fc, text="Inclusive of all charges", font=("Segoe UI", 7),
                 bg=Colors.PRIMARY, fg=Colors.PRIMARY_GLOW).pack(pady=(0, 8))

        self.book_btn = tk.Button(
            ff, text="🚗   Book Ride Now",
            command=self.send_ride_request,
            bg=Colors.GRAY_300, fg=Colors.GRAY_500,
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT, cursor="hand2",
            pady=12, bd=0,
            activebackground=Colors.SUCCESS_DARK,
            activeforeground=Colors.WHITE,
            state=tk.DISABLED
        )
        self.book_btn.pack(fill=tk.X, pady=(0, 4))
        self.book_btn.bind("<Enter>", self._book_btn_enter)
        self.book_btn.bind("<Leave>", self._book_btn_leave)
        self.book_sub = tk.Label(ff,
            text="← Select a driver on the right first",
            font=("Segoe UI", 8),
            bg=Colors.WHITE, fg=Colors.GRAY_400
        )
        self.book_sub.pack(anchor=tk.W, pady=(0, 8))

        self.load_drivers()
        self.update_fare()


    def _select_vehicle(self, vehicle_type):
        self.vehicle_var.set(vehicle_type)
        for vt, btn in self._vtype_buttons.items():
            if vt == vehicle_type:
                btn.config(bg=Colors.PRIMARY, fg=Colors.WHITE)
            else:
                btn.config(bg=Colors.GRAY_100, fg=Colors.GRAY_600)
        if hasattr(self, 'fare_label') and hasattr(self, 'shared_var') and hasattr(self, 'drivers_frame'):
            self.update_fare_and_drivers()

    def _make_icon_entry(self, parent, icon, label, placeholder, is_pickup):
        outer = tk.Frame(parent, bg=Colors.GRAY_100, padx=2, pady=2)
        outer.pack(fill=tk.X, pady=(0, 12))
        inner = tk.Frame(outer, bg=Colors.WHITE)
        inner.pack(fill=tk.BOTH)
        tk.Label(inner, text=label,
                 font=("Segoe UI", 8),
                 bg=Colors.WHITE, fg=Colors.GRAY_500).pack(anchor=tk.W, padx=10, pady=(6, 0))
        row = tk.Frame(inner, bg=Colors.WHITE)
        row.pack(fill=tk.X, padx=8, pady=(2, 8))
        tk.Label(row, text=icon, font=("Segoe UI", 14),
                 bg=Colors.WHITE).pack(side=tk.LEFT, padx=(0, 6))
        entry = tk.Entry(row, font=("Segoe UI", 11),
                         relief=tk.FLAT, bg=Colors.WHITE,
                         fg=Colors.GRAY_400, bd=0)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entry.insert(0, placeholder)

        def on_focus_in(e, ent=entry, ph=placeholder):
            if ent.get() == ph:
                ent.delete(0, tk.END)
                ent.config(fg=Colors.GRAY_800)
            outer.config(bg=Colors.PRIMARY)

        def on_focus_out(e, ent=entry, ph=placeholder):
            if not ent.get():
                ent.insert(0, ph)
                ent.config(fg=Colors.GRAY_400)
            outer.config(bg=Colors.GRAY_100)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        if is_pickup:
            self.pickup_entry = type('E', (), {'get': lambda s=entry: entry.get(), 'entry': entry})()
        else:
            self.dropoff_entry = type('E', (), {'get': lambda s=entry: entry.get(), 'entry': entry})()

    def _book_btn_enter(self, e):
        if self.book_btn.cget('state') != tk.DISABLED:
            self.book_btn.config(bg=Colors.SUCCESS_DARK)

    def _book_btn_leave(self, e):
        if self.book_btn.cget('state') != tk.DISABLED:
            self.book_btn.config(bg=Colors.SUCCESS)
    
    def update_fare(self):
        fare = self.db.calculate_fare(self.vehicle_var.get(), 5, 10)
        if self.shared_var.get():
            fare = fare // 2
        self.fare_label.config(text=f"PKR {fare}")
        return fare
    
    def update_fare_and_drivers(self):
        self.update_fare()
        self.load_drivers()
    
    def load_drivers(self):
        for w in self.drivers_frame.winfo_children():
            w.destroy()
        self._driver_cards = {}
        self.selected_driver_id = None

        drivers = self.db.get_available_drivers(self.vehicle_var.get())
        if not drivers:
            empty = tk.Frame(self.drivers_frame, bg=Colors.WHITE)
            empty.pack(expand=True, fill=tk.BOTH, pady=40)
            tk.Label(empty, text="🚫", font=("Segoe UI", 36),
                     bg=Colors.WHITE, fg=Colors.GRAY_300).pack()
            tk.Label(empty,
                     text="No drivers available right now",
                     font=("Segoe UI", 11, "bold"),
                     bg=Colors.WHITE, fg=Colors.GRAY_500).pack(pady=(6, 2))
            tk.Label(empty,
                     text="Try a different vehicle type or refresh",
                     font=("Segoe UI", 9),
                     bg=Colors.WHITE, fg=Colors.GRAY_400).pack()
            return

        vehicle_icons = {"Bike": "🏍️", "Rickshaw": "🛺", "Mini": "🚗", "Sedan": "🚙"}

        for driver in drivers:
            uid = driver['user_id']
            icon = vehicle_icons.get(driver['vehicle_type'], "🚗")
            rating = driver.get('rating_average', 5.0) or 5.0

            border = tk.Frame(self.drivers_frame, bg=Colors.GRAY_200, padx=2, pady=2)
            border.pack(fill=tk.X, pady=5, padx=4)

            card = tk.Frame(border, bg=Colors.WHITE, cursor="hand2")
            card.pack(fill=tk.BOTH)

            top_row = tk.Frame(card, bg=Colors.WHITE)
            top_row.pack(fill=tk.X, padx=14, pady=(12, 4))

            avatar = tk.Label(top_row, text=icon,
                              font=("Segoe UI", 20),
                              bg=Colors.PRIMARY_LIGHT,
                              fg=Colors.WHITE,
                              width=3)
            avatar.pack(side=tk.LEFT)

            info_col = tk.Frame(top_row, bg=Colors.WHITE)
            info_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            name_lbl = tk.Label(info_col,
                                text=driver['full_name'],
                                font=("Segoe UI", 11, "bold"),
                                bg=Colors.WHITE, fg=Colors.GRAY_800,
                                anchor=tk.W)
            name_lbl.pack(anchor=tk.W)
            tk.Label(info_col,
                     text=f"{driver['vehicle_type']}  •  {driver['plate_number']}",
                     font=("Segoe UI", 9),
                     bg=Colors.WHITE, fg=Colors.GRAY_500,
                     anchor=tk.W).pack(anchor=tk.W)

            rating_frame = tk.Frame(top_row, bg=Colors.SECONDARY, padx=8, pady=4)
            rating_frame.pack(side=tk.RIGHT)
            tk.Label(rating_frame,
                     text=f"⭐ {rating:.1f}",
                     font=("Segoe UI", 9, "bold"),
                     bg=Colors.SECONDARY, fg=Colors.WHITE).pack()

            tk.Frame(card, bg=Colors.GRAY_100, height=1).pack(fill=tk.X, padx=14)
            model_row = tk.Frame(card, bg=Colors.WHITE)
            model_row.pack(fill=tk.X, padx=14, pady=(6, 10))
            model_text = driver.get('model', '') or ''
            tk.Label(model_row,
                     text=f"🚘  {model_text}" if model_text else "🚘  Vehicle",
                     font=("Segoe UI", 8),
                     bg=Colors.WHITE, fg=Colors.GRAY_400).pack(side=tk.LEFT)
            online_dot = tk.Label(model_row,
                                  text="● Online",
                                  font=("Segoe UI", 8, "bold"),
                                  bg=Colors.WHITE, fg=Colors.SUCCESS)
            online_dot.pack(side=tk.RIGHT)

            self._driver_cards[uid] = {'border': border, 'card': card, 'driver': driver}

            for widget in [card, top_row, info_col, name_lbl, model_row, avatar]:
                widget.bind("<Button-1>", lambda e, d=driver: self.select_driver(d))
                widget.bind("<Enter>", lambda e, b=border, c=card: self._driver_hover_enter(b, c))
                widget.bind("<Leave>", lambda e, b=border, c=card, uid2=uid: self._driver_hover_leave(b, c, uid2))
            border.bind("<Button-1>", lambda e, d=driver: self.select_driver(d))
    
    def _driver_hover_enter(self, border, card):
        border.config(bg=Colors.PRIMARY_LIGHT)
        card.config(bg=Colors.CARD_SHADOW)
        for child in card.winfo_children():
            try:
                child.config(bg=Colors.CARD_SHADOW)
            except Exception:
                pass

    def _driver_hover_leave(self, border, card, uid):
        if getattr(self, 'selected_driver', None) and self.selected_driver.get('user_id') == uid:
            border.config(bg=Colors.PRIMARY)
            card.config(bg=Colors.CARD_SHADOW)
        else:
            border.config(bg=Colors.GRAY_200)
            card.config(bg=Colors.WHITE)
            for child in card.winfo_children():
                try:
                    child.config(bg=Colors.WHITE)
                except Exception:
                    pass

    def select_driver(self, driver):
        uid = driver['user_id']
        for k, info in self._driver_cards.items():
            info['border'].config(bg=Colors.GRAY_200)
            info['card'].config(bg=Colors.WHITE)

        if uid in self._driver_cards:
            self._driver_cards[uid]['border'].config(bg=Colors.PRIMARY)
            self._driver_cards[uid]['card'].config(bg=Colors.CARD_SHADOW)

        self.selected_driver = driver
        self.book_btn.config(
            state=tk.NORMAL,
            bg=Colors.SUCCESS,
            text=f"🚗   Book Ride with {driver['full_name'].split()[0]}"
        )
        self.book_sub.config(
            text=f"✓ {driver['full_name']} selected  •  {driver['vehicle_type']} {driver['plate_number']}",
            fg=Colors.SUCCESS
        )
        self.show_toast(f"Driver {driver['full_name']} selected!", "info")
    
    def send_ride_request(self):
        if not self.dropoff_entry.get():
            self.show_toast("Please enter a dropoff location", "warning")
            return
        if not self.selected_driver:
            self.show_toast("Please select a driver first", "warning")
            return
        
        fare = self.update_fare()
        pickup = self.pickup_entry.get() or "Current Location"
        dropoff = self.dropoff_entry.get()
        
        result = self.db.create_ride_request(
            self.user['user_id'], self.selected_driver['user_id'],
            self.selected_driver['vehicle_id'], self.shared_var.get(),
            fare, pickup, dropoff, self.user['full_name']
        )
        
        if result['success']:
            self.current_ride_id = result['ride_id']
            self.show_toast(f"Ride request sent to {self.selected_driver['full_name']}!", "ride_request")
            
            self.show_waiting_for_driver()
            
            self.wait_for_driver_response()
    
    def show_waiting_for_driver(self):
        self.waiting_window = tk.Toplevel(self.parent)
        self.waiting_window.title("Waiting for Driver")
        self.waiting_window.geometry("400x300")
        self.waiting_window.configure(bg=Colors.WHITE)
        self.waiting_window.transient(self.parent)
        self.waiting_window.grab_set()
        
        self.waiting_window.update_idletasks()
        x = (self.waiting_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.waiting_window.winfo_screenheight() // 2) - (300 // 2)
        self.waiting_window.geometry(f"+{x}+{y}")
        
        tk.Label(self.waiting_window, text="⏳", font=("Segoe UI", 48),
                bg=Colors.WHITE, fg=Colors.PRIMARY).pack(pady=20)
        tk.Label(self.waiting_window, text="Waiting for Driver Response", font=Fonts.HEADING,
                bg=Colors.WHITE, fg=Colors.GRAY_800).pack()
        tk.Label(self.waiting_window, text=f"Request sent to {self.selected_driver['full_name']}",
                font=Fonts.NORMAL, bg=Colors.WHITE, fg=Colors.GRAY_600).pack(pady=5)
        
        self.waiting_label = tk.Label(self.waiting_window, text="Driver will respond shortly...",
                                     font=Fonts.NORMAL, bg=Colors.WHITE, fg=Colors.WARNING)
        self.waiting_label.pack(pady=20)
        
        self.animation_dots = 0
        self.animate_waiting()
        
        cancel_btn = tk.Button(self.waiting_window, text="Cancel Request", command=self.cancel_request,
                              bg=Colors.ERROR, fg=Colors.WHITE, font=Fonts.NORMAL,
                              relief=tk.FLAT, padx=20, pady=10, cursor="hand2")
        cancel_btn.pack(pady=20)
    
    def animate_waiting(self):
        if self.waiting_window and self.waiting_window.winfo_exists():
            dots = "." * (self.animation_dots + 1)
            self.waiting_label.config(text=f"Waiting for response{dots}")
            self.animation_dots = (self.animation_dots + 1) % 3
            self.waiting_window.after(500, self.animate_waiting)
    
    def wait_for_driver_response(self):
        def check_response():
            if self.waiting_window and self.waiting_window.winfo_exists():
                response_time = random.randint(5, 10)
                self.waiting_window.after(response_time * 1000, self.simulate_driver_response)
        
        threading.Thread(target=check_response, daemon=True).start()
    
    def simulate_driver_response(self):
        if self.waiting_window and self.waiting_window.winfo_exists():
            if random.random() < 0.85:  # 85% chance of acceptance for better demo experience
                self.driver_accepted()
            else:
                self.driver_rejected()
    
    def driver_accepted(self):
        if self.waiting_window:
            self.waiting_window.destroy()
            self.waiting_window = None
        
        self.show_toast(f"🎉 Driver {self.selected_driver['full_name']} accepted your request!", "success")
        
        result = self.db.accept_ride_request(
            self.selected_driver['user_id'], self.current_ride_id
        )
        if result.get('success'):
            self.current_participant_id = result.get('participant_id')
        else:
            self.db.update_ride_status(self.current_ride_id, 'Accepted')
        
        ride_details = {
            'driver_name': self.selected_driver['full_name'],
            'vehicle_type': self.selected_driver['vehicle_type'],
            'plate_number': self.selected_driver['plate_number'],
            'pickup': self.pickup_entry.get() or "Current Location",
            'dropoff': self.dropoff_entry.get(),
            'fare': self.update_fare()
        }
        
        RideAnimationWindow(self.parent, ride_details, self.on_ride_complete)
        self.load_ride_history()
    
    def driver_rejected(self):
        if self.waiting_window:
            self.waiting_window.destroy()
            self.waiting_window = None
        
        self.show_toast(f"Driver {self.selected_driver['full_name']} declined your request. Please try another driver.", "warning")
        self.book_btn.config(state=tk.NORMAL)
        self.book_btn.config(text=f"📨 Send Request to {self.selected_driver['full_name'].split()[0]}")
    
    def cancel_request(self):
        if self.waiting_window:
            self.waiting_window.destroy()
            self.waiting_window = None
        self.show_toast("Ride request cancelled", "info")
        self.book_btn.config(state=tk.NORMAL)
    
    def on_ride_complete(self):
        if self.current_ride_id:
            result = self.db.complete_ride(
                self.current_ride_id,
                self.current_participant_id or ''
            )
            if result.get('success'):
                self.show_toast("🎉 Ride completed! Thank you for riding with FareShare!", "success")
            else:
                self.db.update_ride_status(self.current_ride_id, 'Completed')
                self.show_toast("Ride completed! Check My Rides for details.", "success")
            self.current_ride_id = None
            self.current_participant_id = None
            self.selected_driver = None
            self.load_ride_history()
    
    def show_rides(self):
        for w in self.content.winfo_children():
            w.destroy()
        card = ModernCard(self.content, title="My Ride History")
        card.pack(fill=tk.BOTH, expand=True)
        columns = ("Date", "Driver", "Vehicle", "Fare", "Status", "Payment")
        tree_frame = tk.Frame(card.content, bg=Colors.WHITE)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ride_tree = tree
        self.load_ride_history()
        btn_frame = tk.Frame(card.content, bg=Colors.WHITE)
        btn_frame.pack(pady=10)
        ModernButton(btn_frame, text="⭐ Rate Driver", command=self.rate_ride,
                    bg_color=Colors.SECONDARY, hover_color=Colors.SECONDARY, width=150, height=35).pack(side=tk.LEFT, padx=5)
    
    def load_ride_history(self):
        if hasattr(self, 'ride_tree'):
            for item in self.ride_tree.get_children():
                self.ride_tree.delete(item)
            rides = self.db.get_rider_rides(self.user['user_id'])
            for ride in rides:
                status_icons = {"Completed": "✅", "Cancelled": "❌", "Requested": "⏳", "Accepted": "🚗", "InProgress": "🔄"}
                status = f"{status_icons.get(ride['status'], '')} {ride['status']}"
                payment = "✅ Paid" if ride.get('is_received') else "⏳ Pending"
                fare = ride.get('segment_fare', ride.get('total_fare', 0))
                date = ride['created_at'].strftime("%Y-%m-%d %H:%M") if ride['created_at'] else "N/A"
                vehicle = f"{ride.get('vehicle_type', 'N/A')}"
                self.ride_tree.insert("", tk.END, values=(date, ride.get('driver_name', 'N/A')[:15],
                                                         vehicle, f"PKR {fare}", status, payment))
    
    def rate_ride(self):
        selected = self.ride_tree.selection()
        if not selected:
            self.show_toast("Please select a ride to rate", "warning")
            return
        item = self.ride_tree.item(selected[0])
        if "Completed" not in item['values'][4]:
            self.show_toast("Only completed rides can be rated", "warning")
            return
        rides = self.db.get_rider_rides(self.user['user_id'])
        idx = self.ride_tree.index(selected[0])
        if idx < len(rides):
            ride = rides[idx]
            ride_detail = self.db.get_ride_by_id(ride['ride_id'])
            if ride_detail and ride_detail.get('driver_id'):
                self.show_rating_dialog(ride['ride_id'], ride_detail['driver_id'])
    
    def show_rating_dialog(self, ride_id, driver_id):
        dialog = tk.Toplevel(self.parent)
        dialog.title("Rate Your Ride")
        dialog.geometry("450x400")
        dialog.configure(bg=Colors.WHITE)
        dialog.transient(self.parent)
        dialog.grab_set()
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"+{x}+{y}")
        tk.Label(dialog, text="Rate Your Driver", font=Fonts.HEADING,
                bg=Colors.WHITE, fg=Colors.GRAY_800).pack(pady=20)
        rating_var = tk.IntVar(value=5)
        star_frame = tk.Frame(dialog, bg=Colors.WHITE)
        star_frame.pack(pady=10)
        def set_rating(value):
            rating_var.set(value)
            for i, star in enumerate(star_buttons, 1):
                star.config(text="★" if i <= value else "☆")
        star_buttons = []
        for i in range(1, 6):
            star = tk.Button(star_frame, text="☆", font=("Segoe UI", 32),
                            bg=Colors.WHITE, fg=Colors.SECONDARY, relief=tk.FLAT,
                            cursor="hand2", command=lambda x=i: set_rating(x))
            star.pack(side=tk.LEFT, padx=5)
            star_buttons.append(star)
        set_rating(5)
        tk.Label(dialog, text="Your Feedback (Optional)", font=Fonts.NORMAL,
                bg=Colors.WHITE, fg=Colors.GRAY_700).pack(anchor=tk.W, padx=30, pady=(20, 5))
        comment_text = tk.Text(dialog, height=4, width=40, font=Fonts.NORMAL, relief=tk.SOLID, bd=1)
        comment_text.pack(padx=30, pady=5)
        def submit():
            result = self.db.submit_rating(ride_id, self.user['user_id'], driver_id,
                                          rating_var.get(), comment_text.get("1.0", tk.END).strip())
            if result['success']:
                self.show_toast("Thank you for your feedback! ⭐", "success")
                dialog.destroy()
            else:
                self.show_toast(result['message'], "error")
        ModernButton(dialog, text="Submit Rating", command=submit,
                    bg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_DARK, width=200, height=40).pack(pady=20)
    
    def show_emergency(self):
        for w in self.content.winfo_children():
            w.destroy()
        sos_card = ModernCard(self.content, title="🚨 Emergency SOS")
        sos_card.pack(fill=tk.X, pady=(0, 20))
        sos_desc = tk.Label(sos_card.content, 
                           text="Press the button below in case of emergency.\nYour emergency contacts and admin will be notified immediately.",
                           font=Fonts.NORMAL, bg=Colors.WHITE, fg=Colors.GRAY_600, justify=tk.CENTER)
        sos_desc.pack(pady=(0, 15))
        sos_btn = tk.Button(sos_card.content, text="SOS", command=self.trigger_sos,
                           bg=Colors.ERROR, fg=Colors.WHITE, font=("Segoe UI", 32, "bold"),
                           padx=40, pady=15, relief=tk.RAISED, cursor="hand2")
        sos_btn.pack(pady=10)
        tk.Label(sos_card.content, text="⚠️ Only use in real emergencies",
                font=Fonts.SMALL, fg=Colors.GRAY_400, bg=Colors.WHITE).pack()
        contacts_card = ModernCard(self.content, title="Emergency Contacts")
        contacts_card.pack(fill=tk.BOTH, expand=True)
        self.contacts_frame = tk.Frame(contacts_card.content, bg=Colors.WHITE)
        self.contacts_frame.pack(fill=tk.BOTH, expand=True)
        add_btn = tk.Button(contacts_card.content, text="+ Add Emergency Contact", command=self.add_contact,
                           bg=Colors.INFO, fg=Colors.WHITE, font=Fonts.NORMAL,
                           relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
        add_btn.pack(pady=(10, 0))
        self.load_emergency_contacts()
    
    def load_emergency_contacts(self):
        for w in self.contacts_frame.winfo_children():
            w.destroy()
        contacts = self.db.get_emergency_contacts(self.user['user_id'])
        if not contacts:
            empty_label = tk.Label(self.contacts_frame, text="No emergency contacts added.\nAdd contacts to receive SOS alerts.",
                                  font=Fonts.NORMAL, bg=Colors.WHITE, fg=Colors.GRAY_500, justify=tk.CENTER)
            empty_label.pack(expand=True, pady=30)
            return
        for contact in contacts:
            contact_card = tk.Frame(self.contacts_frame, bg=Colors.GRAY_50, relief=tk.RAISED, bd=1)
            contact_card.pack(fill=tk.X, pady=5)
            info_frame = tk.Frame(contact_card, bg=Colors.GRAY_50)
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15, pady=10)
            tk.Label(info_frame, text=f"👤 {contact['contact_name']}", font=Fonts.NORMAL_BOLD,
                    bg=Colors.GRAY_50, fg=Colors.GRAY_800).pack(anchor=tk.W)
            tk.Label(info_frame, text=f"📞 {contact['phone_number']}", font=Fonts.SMALL,
                    bg=Colors.GRAY_50, fg=Colors.GRAY_500).pack(anchor=tk.W)
            tk.Label(info_frame, text=f"💑 {contact['relationship'] or 'Contact'}", font=Fonts.SMALL,
                    bg=Colors.GRAY_50, fg=Colors.GRAY_500).pack(anchor=tk.W)
            delete_btn = tk.Button(contact_card, text="🗑️", 
                                  command=lambda cid=contact['contact_id']: self.delete_contact(cid),
                                  bg=Colors.ERROR, fg=Colors.WHITE, font=Fonts.SMALL,
                                  relief=tk.FLAT, padx=10, pady=5, cursor="hand2")
            delete_btn.pack(side=tk.RIGHT, padx=15)
    
    def delete_contact(self, contact_id):
        if messagebox.askyesno("Confirm", "Remove this emergency contact?"):
            result = self.db.delete_emergency_contact(contact_id)
            if result['success']:
                self.show_toast("Contact removed", "success")
                self.load_emergency_contacts()
            else:
                self.show_toast(result['message'], "error")
    
    def add_contact(self):
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add Emergency Contact")
        dialog.geometry("450x400")
        dialog.configure(bg=Colors.WHITE)
        dialog.transient(self.parent)
        dialog.grab_set()
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"+{x}+{y}")
        tk.Label(dialog, text="Add Emergency Contact", font=Fonts.HEADING,
                bg=Colors.WHITE, fg=Colors.GRAY_800).pack(pady=20)
        form = tk.Frame(dialog, bg=Colors.WHITE, padx=30)
        form.pack(fill=tk.BOTH, expand=True)
        name_entry = self._create_dialog_entry(form, "Contact Name")
        phone_entry = self._create_dialog_entry(form, "Phone Number")
        rel_entry = self._create_dialog_entry(form, "Relationship (e.g., Father, Mother)")
        def save():
            result = self.db.add_emergency_contact(self.user['user_id'], name_entry.get(),
                                                   phone_entry.get(), rel_entry.get())
            if result['success']:
                self.show_toast("Emergency contact added!", "success")
                dialog.destroy()
                self.load_emergency_contacts()
            else:
                self.show_toast(result['message'], "error")
        ModernButton(form, text="Save Contact", command=save,
                    bg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_DARK, width=200, height=40).pack(pady=20)
    
    def _create_dialog_entry(self, parent, label_text):
        frame = tk.Frame(parent, bg=Colors.WHITE)
        frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(frame, text=label_text, font=Fonts.NORMAL,
                bg=Colors.WHITE, fg=Colors.GRAY_700, anchor=tk.W).pack(anchor=tk.W)
        entry = tk.Entry(frame, font=Fonts.NORMAL, bd=1, relief=tk.SOLID)
        entry.pack(fill=tk.X, pady=(5, 0))
        return entry
    
    def trigger_sos(self):
        if messagebox.askyesno("SOS Alert", "⚠️ EMERGENCY ⚠️\n\nAre you sure you want to trigger SOS?\nEmergency contacts and admin will be notified immediately.\n\nOnly use in real emergencies!", icon='warning'):
            ride_id = self.current_ride_id if self.current_ride_id else "unknown"
            result = self.db.trigger_sos(ride_id, self.user['user_id'], 32.5833, 71.5417)
            if result['success']:
                self.show_toast("SOS alert sent! Emergency contacts notified.", "success")
            else:
                self.show_toast(result['message'], "error")
    
    def show_profile(self):
        for w in self.content.winfo_children():
            w.destroy()
        card = ModernCard(self.content, title="Profile Information")
        card.pack(fill=tk.BOTH, expand=True)
        avatar_frame = tk.Frame(card.content, bg=Colors.GRAY_100, width=120, height=120)
        avatar_frame.pack(pady=20)
        avatar_frame.pack_propagate(False)
        tk.Label(avatar_frame, text="👤", font=("Segoe UI", 48),
                bg=Colors.GRAY_100, fg=Colors.GRAY_500).pack(expand=True)
        info_frame = tk.Frame(card.content, bg=Colors.WHITE)
        info_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)
        info_items = [("Full Name", self.user['full_name']), ("Phone Number", self.user['phone_number']),
                     ("User ID", self.user['user_id'][:8] + "..."),
                     ("Member Since", self.user['created_at'].strftime('%B %d, %Y') if self.user['created_at'] else 'N/A')]
        for label, value in info_items:
            row = tk.Frame(info_frame, bg=Colors.WHITE)
            row.pack(fill=tk.X, pady=8)
            tk.Label(row, text=f"{label}:", font=Fonts.NORMAL_BOLD,
                    bg=Colors.WHITE, fg=Colors.GRAY_600, width=15, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row, text=value, font=Fonts.NORMAL,
                    bg=Colors.WHITE, fg=Colors.GRAY_800, anchor=tk.W).pack(side=tk.LEFT, padx=(10, 0))
    
    def logout(self):
        self.logout_callback()


class DriverDashboard:
    def __init__(self, parent, db, user, logout_callback):
        self.parent = parent
        self.db = db
        self.user = user
        self.logout_callback = logout_callback
        self.is_online = False
        
        for widget in parent.winfo_children():
            widget.destroy()
        self.setup_ui()
    
    def setup_ui(self):
        sidebar = tk.Frame(self.parent, bg=Colors.DARK_BG, width=280)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="🚗 FareShare", font=("Segoe UI", 20, "bold"),
                bg=Colors.DARK_BG, fg=Colors.WHITE).pack(pady=25)
        avatar_frame = tk.Frame(sidebar, bg=Colors.DARK_SURFACE, height=100)
        avatar_frame.pack(fill=tk.X, padx=20, pady=20)
        avatar_frame.pack_propagate(False)
        tk.Label(avatar_frame, text="👨‍✈️", font=("Segoe UI", 36),
                bg=Colors.DARK_SURFACE, fg=Colors.PRIMARY_LIGHT).pack(pady=10)
        tk.Label(avatar_frame, text=self.user['full_name'][:20], font=Fonts.NORMAL_BOLD,
                bg=Colors.DARK_SURFACE, fg=Colors.WHITE).pack()
        nav_items = [("🚗", "Ride Requests", self.show_requests), ("📋", "My Rides", self.show_rides),
                     ("💰", "Earnings", self.show_earnings), ("👤", "Profile", self.show_profile)]
        for icon, text, cmd in nav_items:
            btn = tk.Button(sidebar, text=f"  {icon}  {text}", command=cmd,
                           bg=Colors.DARK_BG, fg=Colors.GRAY_300, font=Fonts.NORMAL,
                           relief=tk.FLAT, anchor=tk.W, padx=20, pady=12,
                           activebackground=Colors.DARK_HOVER, activeforeground=Colors.WHITE,
                           cursor="hand2")
            btn.pack(fill=tk.X, padx=15, pady=5)
        tk.Frame(sidebar, bg=Colors.DARK_BG, height=20).pack(expand=True)
        logout_btn = tk.Button(sidebar, text="🚪  Logout", command=self.logout,
                              bg=Colors.DARK_SURFACE, fg=Colors.ERROR, font=Fonts.NORMAL,
                              relief=tk.FLAT, padx=20, pady=12, cursor="hand2")
        logout_btn.pack(fill=tk.X, padx=20, pady=20)
        
        self.main = tk.Frame(self.parent, bg=Colors.GRAY_50)
        self.main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        header = tk.Frame(self.main, bg=Colors.WHITE, height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="Driver Dashboard", font=Fonts.HEADING,
                bg=Colors.WHITE, fg=Colors.GRAY_800).pack(side=tk.LEFT, padx=30)
        self.status_btn = tk.Button(header, text="🔴 Go Online", command=self.toggle_status,
                                   bg=Colors.ERROR, fg=Colors.WHITE, font=Fonts.NORMAL_BOLD,
                                   relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        self.status_btn.pack(side=tk.RIGHT, padx=20)
        
        self.content = tk.Frame(self.main, bg=Colors.GRAY_50)
        self.content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        self.show_requests()
    
    def show_toast(self, message, type="success"):
        ToastNotification(self.parent, message, type)
    
    def show_requests(self):
        for w in self.content.winfo_children():
            w.destroy()
        card = ModernCard(self.content, title="Incoming Ride Requests")
        card.pack(fill=tk.BOTH, expand=True)
        
        info_frame = tk.Frame(card.content, bg=Colors.GRAY_100, height=60)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        info_frame.pack_propagate(False)
        
        info_content = tk.Frame(info_frame, bg=Colors.GRAY_100)
        info_content.pack(expand=True, pady=5)
        
        tk.Label(info_content, text="📢 Incoming ride requests will appear below", 
                font=("Segoe UI", 9, "bold"), bg=Colors.GRAY_100, fg=Colors.GRAY_700).pack()
        tk.Label(info_content, text="Select a request and click Accept/Decline buttons, or click 'Simulate Request' for demo",
                font=Fonts.SMALL, bg=Colors.GRAY_100, fg=Colors.GRAY_600).pack()
        
        columns = ("Rider", "Pickup", "Dropoff", "Fare", "Status")
        tree_frame = tk.Frame(card.content, bg=Colors.WHITE)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.requests_tree = tree
        
        btn_frame = tk.Frame(card.content, bg=Colors.WHITE)
        btn_frame.pack(pady=10)
        
        ModernButton(btn_frame, text="✅ Accept", command=self.accept_selected_request,
                    bg_color=Colors.SUCCESS, hover_color=Colors.SUCCESS_DARK, width=120, height=32).pack(side=tk.LEFT, padx=3)
        
        ModernButton(btn_frame, text="❌ Decline", command=self.decline_selected_request,
                    bg_color=Colors.ERROR, hover_color=Colors.ERROR_DARK, width=120, height=32).pack(side=tk.LEFT, padx=3)
        
        ModernButton(btn_frame, text="🔄 Refresh", command=self.check_for_requests,
                    bg_color=Colors.INFO, hover_color=Colors.INFO, width=120, height=32).pack(side=tk.LEFT, padx=3)
        
        ModernButton(btn_frame, text="🎮 Simulate", command=self.simulate_ride_request,
                    bg_color=Colors.SECONDARY, hover_color=Colors.SECONDARY, width=120, height=32).pack(side=tk.LEFT, padx=3)
        
        self.load_requests()
    
    def check_for_requests(self):
        self.load_requests()
        self.show_toast(f"Checked for requests. {len(self.db.get_pending_requests_for_driver(self.user['user_id']))} pending.", "info")
    
    def load_requests(self):
        for item in self.requests_tree.get_children():
            self.requests_tree.delete(item)
        
        pending_requests = self.db.get_pending_requests_for_driver(self.user['user_id'])
        for req in pending_requests:
            if req['status'] == 'pending':
                status = "⏳ Pending"
                self.requests_tree.insert("", tk.END, values=(
                    req['rider_name'][:15],
                    req['pickup'][:20],
                    req['dropoff'][:20],
                    f"PKR {req['total_fare']}",
                    status
                ), tags=(req['ride_id'],))
        
        if not pending_requests:
            self.requests_tree.insert("", tk.END, values=("No requests", "", "", "", "Waiting..."))
    
    def simulate_ride_request(self):
        """Simulate a ride request from a random rider (for demo purposes)"""
        if not self.is_online:
            self.show_toast("Please go online first to receive requests", "warning")
            return
        
        fake_riders = ["Ahsan Ali", "Fatima Khan", "Omar Shah", "Zara Ahmed", "Hassan Raza"]
        fake_pickups = ["University Road", "City Center", "Railway Station", "Golf Club", "Mall Road"]
        fake_dropoffs = ["Home", "Office", "Airport", "Hospital", "Park"]
        fare = random.randint(150, 500)
        
        fake_request = {
            'ride_id': str(uuid.uuid4()),
            'rider_name': random.choice(fake_riders),
            'pickup': random.choice(fake_pickups),
            'dropoff': random.choice(fake_dropoffs),
            'total_fare': fare,
            'rider_id': 'fake_rider',  # Mark as fake
            'driver_id': self.user['user_id'],
            'vehicle_id': 'fake_vehicle',  # Mark as fake
            'is_shared': False,
            'status': 'pending'
        }
        
        if self.user['user_id'] not in self.db.pending_requests:
            self.db.pending_requests[self.user['user_id']] = []
        self.db.pending_requests[self.user['user_id']].append(fake_request)
        
        self.show_toast(f"Demo request from {fake_request['rider_name']} received!", "info")
        
        self.load_requests()
        
        self.parent.after(2000, lambda: self.show_ride_request_popup(fake_request))
    
    def show_ride_request_popup(self, request):
        def on_accept():
            self.accept_request(request['ride_id'])
        
        def on_reject():
            self.reject_request(request['ride_id'])
        
        RideRequestWindow(self.parent, request, on_accept, on_reject)
    
    def accept_request(self, ride_id):
        result = self.db.accept_ride_request(self.user['user_id'], ride_id)
        if result['success']:
            rider_name = result['request'].get('rider_name', 'Passenger')
            is_simulated = result['request'].get('rider_id') == 'fake_rider'
            
            if is_simulated:
                self.show_toast(f"Demo ride accepted from {rider_name}! (Simulation mode)", "success")
            else:
                self.show_toast(f"Ride accepted! Pick up {rider_name}", "success")
            
            self.load_requests()
            if not is_simulated:
                self.show_rides()
        else:
            self.show_toast(result.get('message', 'Failed to accept request'), "error")
    
    def reject_request(self, ride_id):
        self.db.reject_ride_request(self.user['user_id'], ride_id)
        self.show_toast("Ride request declined", "info")
        self.load_requests()
    
    def accept_selected_request(self):
        """Accept the selected request from the table"""
        if not self.is_online:
            self.show_toast("Please go online first to accept requests", "warning")
            return
        
        selected = self.requests_tree.selection()
        if not selected:
            self.show_toast("Please select a ride request from the table", "warning")
            return
        
        try:
            item = self.requests_tree.item(selected[0])
            tags = item.get('tags', ())
            
            if not tags or len(tags) == 0:
                self.show_toast("Invalid selection. Please try again.", "error")
                return
            
            ride_id = tags[0]
            
            pending_requests = self.db.get_pending_requests_for_driver(self.user['user_id'])
            selected_request = None
            for req in pending_requests:
                if req['ride_id'] == ride_id and req['status'] == 'pending':
                    selected_request = req
                    break
            
            if not selected_request:
                self.show_toast("Request no longer available", "error")
                self.load_requests()
                return
            
            self.accept_request(ride_id)
        except Exception as e:
            self.show_toast(f"Error accepting request: {str(e)}", "error")
            print(f"Accept error: {e}")
    
    def decline_selected_request(self):
        """Decline the selected request from the table"""
        selected = self.requests_tree.selection()
        if not selected:
            self.show_toast("Please select a ride request from the table", "warning")
            return
        
        try:
            item = self.requests_tree.item(selected[0])
            tags = item.get('tags', ())
            
            if not tags or len(tags) == 0:
                self.show_toast("Invalid selection. Please try again.", "error")
                return
            
            ride_id = tags[0]
            
            if messagebox.askyesno("Decline Request", "Are you sure you want to decline this ride request?"):
                self.reject_request(ride_id)
        except Exception as e:
            self.show_toast(f"Error declining request: {str(e)}", "error")
            print(f"Decline error: {e}")
    
    def show_rides(self):
        for w in self.content.winfo_children():
            w.destroy()
        card = ModernCard(self.content, title="My Rides")
        card.pack(fill=tk.BOTH, expand=True)
        columns = ("Date", "Passengers", "Fare", "Status")
        tree_frame = tk.Frame(card.content, bg=Colors.WHITE)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        rides = self.db.get_driver_rides(self.user['user_id'])
        for ride in rides:
            status_icons = {"Completed": "✅", "Cancelled": "❌", "Requested": "⏳", "Accepted": "🚗", "InProgress": "🔄"}
            status = f"{status_icons.get(ride['status'], '')} {ride['status']}"
            date = ride['created_at'].strftime("%Y-%m-%d %H:%M") if ride['created_at'] else "N/A"
            tree.insert("", tk.END, values=(date, ride.get('passenger_count', 1), f"PKR {ride['total_fare']}", status))
    
    def show_earnings(self):
        for w in self.content.winfo_children():
            w.destroy()
        card = ModernCard(self.content, title="Earnings Dashboard")
        card.pack(fill=tk.BOTH, expand=True)
        earnings = self.db.get_driver_earnings(self.user['user_id'])
        if earnings:
            e = earnings[0]
            summary_frame = tk.Frame(card.content, bg=Colors.WHITE)
            summary_frame.pack(fill=tk.X, pady=(0, 20))
            stats = [("Total Rides", str(e['total_rides']), "📊"), ("Gross Earnings", f"PKR {e['gross_earnings']:,.0f}", "💰"),
                     ("Commission", f"PKR {e['commission']:,.0f}", "📉"), ("Net Earnings", f"PKR {e['net_earnings']:,.0f}", "🎯")]
            for label, value, icon in stats:
                stat_card = tk.Frame(summary_frame, bg=Colors.GRAY_50, relief=tk.RAISED, bd=1)
                stat_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
                tk.Label(stat_card, text=f"{icon} {label}", font=Fonts.SMALL,
                        bg=Colors.GRAY_50, fg=Colors.GRAY_500).pack(pady=(10, 0))
                tk.Label(stat_card, text=value, font=Fonts.SUBHEADING,
                        bg=Colors.GRAY_50, fg=Colors.PRIMARY).pack(pady=10)
    
    def show_profile(self):
        for w in self.content.winfo_children():
            w.destroy()
        card = ModernCard(self.content, title="Driver Profile")
        card.pack(fill=tk.BOTH, expand=True)
        info_items = [("Full Name", self.user['full_name']), ("Phone Number", self.user['phone_number']),
                     ("User ID", self.user['user_id'][:8] + "..."), ("Status", "🟢 Online" if self.is_online else "⚪ Offline")]
        for label, value in info_items:
            row = tk.Frame(card.content, bg=Colors.WHITE)
            row.pack(fill=tk.X, pady=8, padx=20)
            tk.Label(row, text=f"{label}:", font=Fonts.NORMAL_BOLD,
                    bg=Colors.WHITE, fg=Colors.GRAY_600, width=15, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row, text=value, font=Fonts.NORMAL,
                    bg=Colors.WHITE, fg=Colors.GRAY_800).pack(side=tk.LEFT, padx=10)
    
    def toggle_status(self):
        self.is_online = not self.is_online
        result = self.db.update_driver_status(self.user['user_id'], self.is_online)
        if result['success']:
            if self.is_online:
                self.status_btn.config(text="🟢 Online", bg=Colors.SUCCESS)
                self.show_toast("You are now ONLINE and will receive ride requests", "success")
            else:
                self.status_btn.config(text="🔴 Offline", bg=Colors.ERROR)
                self.show_toast("You are now OFFLINE", "info")
        else:
            self.show_toast(result['message'], "error")
            self.is_online = not self.is_online
    
    def logout(self):
        self.db.update_driver_status(self.user['user_id'], False)
        self.logout_callback()


class AdminDashboard:
    def __init__(self, parent, db, user, logout_callback):
        self.parent = parent
        self.db = db
        self.user = user
        self.logout_callback = logout_callback
        
        for widget in parent.winfo_children():
            widget.destroy()
        self.setup_ui()
    
    def setup_ui(self):
        sidebar = tk.Frame(self.parent, bg=Colors.DARK_BG, width=280)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="🚗 FareShare", font=("Segoe UI", 20, "bold"),
                bg=Colors.DARK_BG, fg=Colors.WHITE).pack(pady=25)
        tk.Label(sidebar, text="Admin Panel", font=Fonts.SMALL,
                bg=Colors.DARK_BG, fg=Colors.GRAY_400).pack()
        nav_items = [("👥", "Verifications", self.show_verifications), ("👤", "Users", self.show_users),
                     ("🚗", "Rides", self.show_rides), ("📊", "Reports", self.show_reports)]
        for icon, text, cmd in nav_items:
            btn = tk.Button(sidebar, text=f"  {icon}  {text}", command=cmd,
                           bg=Colors.DARK_BG, fg=Colors.GRAY_300, font=Fonts.NORMAL,
                           relief=tk.FLAT, anchor=tk.W, padx=20, pady=12,
                           activebackground=Colors.DARK_HOVER, activeforeground=Colors.WHITE,
                           cursor="hand2")
            btn.pack(fill=tk.X, padx=15, pady=5)
        tk.Frame(sidebar, bg=Colors.DARK_BG, height=20).pack(expand=True)
        logout_btn = tk.Button(sidebar, text="🚪  Logout", command=self.logout,
                              bg=Colors.DARK_SURFACE, fg=Colors.ERROR, font=Fonts.NORMAL,
                              relief=tk.FLAT, padx=20, pady=12, cursor="hand2")
        logout_btn.pack(fill=tk.X, padx=20, pady=20)
        
        self.main = tk.Frame(self.parent, bg=Colors.GRAY_50)
        self.main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        header = tk.Frame(self.main, bg=Colors.WHITE, height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="Admin Dashboard", font=Fonts.HEADING,
                bg=Colors.WHITE, fg=Colors.GRAY_800).pack(side=tk.LEFT, padx=30)
        tk.Label(header, text=f"👑 {self.user['full_name']}", font=Fonts.NORMAL,
                bg=Colors.WHITE, fg=Colors.GRAY_600).pack(side=tk.RIGHT, padx=20)
        
        stats_frame = tk.Frame(self.main, bg=Colors.GRAY_50)
        stats_frame.pack(fill=tk.X, padx=30, pady=20)
        stats = self.db.get_system_stats()
        if stats:
            s = stats[0]
            stats_data = [("Riders", s['total_riders'], "👥"), ("Drivers", s['total_drivers'], "👨‍✈️"),
                         ("Active Rides", s['active_rides'], "🚗"), ("Completed", s['completed_rides'], "✅"),
                         ("Revenue", f"PKR {s['total_revenue']:,.0f}", "💰"), ("Pending", s['pending_verifications'], "⏳")]
            for label, value, icon in stats_data:
                card = tk.Frame(stats_frame, bg=Colors.WHITE, relief=tk.RAISED, bd=1)
                card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
                tk.Label(card, text=f"{icon} {label}", font=Fonts.SMALL,
                        bg=Colors.WHITE, fg=Colors.GRAY_500).pack(pady=(8, 0))
                tk.Label(card, text=str(value), font=Fonts.SUBHEADING,
                        bg=Colors.WHITE, fg=Colors.PRIMARY).pack(pady=8)
        
        self.content = tk.Frame(self.main, bg=Colors.GRAY_50)
        self.content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        self.show_verifications()
    
    def show_verifications(self):
        for w in self.content.winfo_children():
            w.destroy()
        card = ModernCard(self.content, title="Driver Verifications")
        card.pack(fill=tk.BOTH, expand=True)
        columns = ("Driver", "Phone", "CNIC", "License")
        tree_frame = tk.Frame(card.content, bg=Colors.WHITE)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        verifications = self.db.get_pending_verifications()
        for v in verifications:
            tree.insert("", tk.END, values=(v['driver_name'], v['phone_number'],
                                           v['cnic_number'], v['license_number']),
                       tags=(v['verification_id'], v['driver_id']))
        btn_frame = tk.Frame(card.content, bg=Colors.WHITE)
        btn_frame.pack(pady=10)
        ModernButton(btn_frame, text="Approve", command=self.approve_driver,
                    bg_color=Colors.SUCCESS, hover_color=Colors.SUCCESS, width=120, height=35).pack(side=tk.LEFT, padx=5)
        ModernButton(btn_frame, text="Reject", command=self.reject_driver,
                    bg_color=Colors.ERROR, hover_color=Colors.ERROR, width=120, height=35).pack(side=tk.LEFT, padx=5)
        self.verify_tree = tree
    
    def approve_driver(self):
        selected = self.verify_tree.selection()
        if not selected:
            self.show_toast("Please select a driver to approve", "warning")
            return
        item = self.verify_tree.item(selected[0])
        tags = item['tags']
        if len(tags) >= 2:
            result = self.db.verify_driver(tags[0], tags[1], self.user['user_id'],
                                          'Approved', "Documents verified by admin")
            if result['success']:
                self.show_toast("Driver approved successfully", "success")
                self.show_verifications()
            else:
                self.show_toast(result['message'], "error")
    
    def reject_driver(self):
        selected = self.verify_tree.selection()
        if not selected:
            self.show_toast("Please select a driver to reject", "warning")
            return
        reason = simpledialog.askstring("Rejection Reason", "Enter reason for rejection:")
        if reason:
            item = self.verify_tree.item(selected[0])
            tags = item['tags']
            if len(tags) >= 2:
                result = self.db.verify_driver(tags[0], tags[1], self.user['user_id'],
                                              'Rejected', reason)
                if result['success']:
                    self.show_toast("Driver rejected", "warning")
                    self.show_verifications()
                else:
                    self.show_toast(result['message'], "error")
    
    def show_users(self):
        for w in self.content.winfo_children():
            w.destroy()
        card = ModernCard(self.content, title="User Management")
        card.pack(fill=tk.BOTH, expand=True)
        search_frame = tk.Frame(card.content, bg=Colors.WHITE)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(search_frame, text="Search:", font=Fonts.NORMAL,
                bg=Colors.WHITE).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=Fonts.NORMAL, width=30, relief=tk.SOLID, bd=1)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        search_btn = tk.Button(search_frame, text="🔍 Search", command=self.search_users,
                              bg=Colors.INFO, fg=Colors.WHITE, font=Fonts.SMALL,
                              relief=tk.FLAT, padx=10, pady=5, cursor="hand2")
        search_btn.pack(side=tk.LEFT, padx=5)
        refresh_btn = tk.Button(search_frame, text="🔄 Show All", command=self.load_all_users,
                               bg=Colors.PRIMARY, fg=Colors.WHITE, font=Fonts.SMALL,
                               relief=tk.FLAT, padx=10, pady=5, cursor="hand2")
        refresh_btn.pack(side=tk.LEFT, padx=5)
        columns = ("Name", "Phone", "Role", "Joined")
        tree_frame = tk.Frame(card.content, bg=Colors.WHITE)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.users_tree = tree
        self.load_all_users()
    
    def load_all_users(self):
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        users = self.db.get_all_users()
        for user in users:
            date = user['created_at'].strftime("%Y-%m-%d") if user['created_at'] else "N/A"
            self.users_tree.insert("", tk.END, values=(user['full_name'][:25], user['phone_number'],
                                                      user['user_role'], date))
    
    def search_users(self):
        search_term = self.search_entry.get()
        if not search_term:
            self.load_all_users()
            return
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        users = self.db.get_all_users(search_term)
        for user in users:
            date = user['created_at'].strftime("%Y-%m-%d") if user['created_at'] else "N/A"
            self.users_tree.insert("", tk.END, values=(user['full_name'][:25], user['phone_number'],
                                                      user['user_role'], date))
    
    def show_rides(self):
        for w in self.content.winfo_children():
            w.destroy()
        card = ModernCard(self.content, title="Ride Monitoring")
        card.pack(fill=tk.BOTH, expand=True)
        columns = ("Driver", "Passengers", "Fare", "Status", "Shared")
        tree_frame = tk.Frame(card.content, bg=Colors.WHITE)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        rides = self.db.get_active_rides()
        for ride in rides:
            status_icons = {"Requested": "⏳", "Accepted": "🚗", "InProgress": "🔄"}
            status = f"{status_icons.get(ride['status'], '')} {ride['status']}"
            tree.insert("", tk.END, values=(ride.get('driver_name', 'N/A')[:20], ride.get('passenger_count', 1),
                                           f"PKR {ride['total_fare']}", status, "Yes" if ride.get('is_shared') else "No"))
        refresh_btn = ModernButton(card.content, text="🔄 Refresh", command=self.show_rides,
                                  bg_color=Colors.INFO, hover_color=Colors.INFO, width=150, height=35)
        refresh_btn.pack(pady=10)
    
    def show_reports(self):
        for w in self.content.winfo_children():
            w.destroy()
        card = ModernCard(self.content, title="System Reports")
        card.pack(fill=tk.BOTH, expand=True)
        stats = self.db.get_system_stats()
        if stats:
            s = stats[0]
            report_text = f"""
╔══════════════════════════════════════════════════════════════╗
║                    FARESHARE SYSTEM REPORT                   ║
╠══════════════════════════════════════════════════════════════╣
║ Generated: {dt.now().strftime('%Y-%m-%d %H:%M:%S')}
║ Generated By: {self.user['full_name']}
╠══════════════════════════════════════════════════════════════╣
║                        SYSTEM OVERVIEW                       ║
╠══════════════════════════════════════════════════════════════╣
║ Total Riders:        {str(s['total_riders']).ljust(45)}║
║ Total Drivers:       {str(s['total_drivers']).ljust(45)}║
║ Active Rides:        {str(s['active_rides']).ljust(45)}║
║ Completed Rides:     {str(s['completed_rides']).ljust(45)}║
║ Total Revenue:       PKR {s['total_revenue']:,.0f}
║ Average Rating:      {s['avg_rating']:.2f} / 5.00
║ Pending Verifications: {str(s['pending_verifications']).ljust(42)}║
╠══════════════════════════════════════════════════════════════╣
║                     END OF REPORT                            ║
╚══════════════════════════════════════════════════════════════╝
"""
            report_widget = scrolledtext.ScrolledText(card.content, font=Fonts.MONO, wrap=tk.NONE, height=20)
            report_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            report_widget.insert("1.0", report_text)
            report_widget.configure(state=tk.DISABLED)
    
    def show_toast(self, message, type="success"):
        ToastNotification(self.parent, message, type)
    
    def logout(self):
        self.logout_callback()


class FareShareApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FareShare - Premium Ride Sharing")
        self.root.geometry("1280x800")
        self.root.minsize(1100, 700)
        self.root.configure(bg=Colors.GRAY_50)
        
        self.db = DatabaseManager()
        if not self.db.connect():
            self.show_db_error()
            return
        
        self.current_user = None
        self.setup_login_ui()
    
    def show_toast(self, message, type="success"):
        ToastNotification(self.root, message, type)
    
    def show_db_error(self):
        error_window = tk.Toplevel(self.root)
        error_window.title("Database Error")
        error_window.geometry("500x350")
        error_window.configure(bg=Colors.WHITE)
        error_window.transient(self.root)
        error_window.grab_set()
        error_window.update_idletasks()
        x = (error_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (error_window.winfo_screenheight() // 2) - (350 // 2)
        error_window.geometry(f"+{x}+{y}")
        error_frame = tk.Frame(error_window, bg=Colors.WHITE)
        error_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        tk.Label(error_frame, text="⚠️", font=("Segoe UI", 64),
                bg=Colors.WHITE, fg=Colors.ERROR).pack()
        tk.Label(error_frame, text="Database Connection Failed", font=Fonts.HEADING,
                bg=Colors.WHITE, fg=Colors.ERROR).pack(pady=(10, 20))
        message_text = """Please ensure:\n• MySQL server is running\n• Database 'fareshare_db' exists\n• Credentials are correct in the code"""
        tk.Label(error_frame, text=message_text, font=Fonts.NORMAL,
                bg=Colors.WHITE, fg=Colors.GRAY_600, justify=tk.CENTER).pack()
        ModernButton(error_frame, text="Exit Application", command=self.root.destroy,
                    bg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_DARK, width=200, height=40).pack(pady=30)
    
    def setup_login_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        main_container = tk.Frame(self.root, bg=Colors.GRAY_50)
        main_container.pack(fill=tk.BOTH, expand=True)
        left_frame = tk.Frame(main_container, bg=Colors.PRIMARY, width=500)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_frame.pack_propagate(False)
        hero_frame = tk.Frame(left_frame, bg=Colors.PRIMARY)
        hero_frame.pack(expand=True, padx=40, pady=60)
        logo_frame = tk.Frame(hero_frame, bg=Colors.PRIMARY)
        logo_frame.pack(anchor=tk.W, pady=(0, 30))
        tk.Label(logo_frame, text="🚗", font=("Segoe UI", 48),
                bg=Colors.PRIMARY, fg=Colors.WHITE).pack(side=tk.LEFT)
        tk.Label(logo_frame, text="FareShare", font=("Segoe UI", 36, "bold"),
                bg=Colors.PRIMARY, fg=Colors.WHITE).pack(side=tk.LEFT, padx=(10, 0))
        tk.Label(hero_frame, text="Share the Ride,\nShare the Fare", 
                font=("Segoe UI", 28, "bold"), bg=Colors.PRIMARY, fg=Colors.PRIMARY_LIGHT, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 40))
        features = [("✓", "Safe & Verified Drivers"), ("💰", "Share Fares & Save Money"),
                    ("🆘", "24/7 Emergency Support"), ("📍", "Real-time GPS Tracking")]
        for icon, text in features:
            feature_frame = tk.Frame(hero_frame, bg=Colors.PRIMARY)
            feature_frame.pack(anchor=tk.W, pady=8)
            tk.Label(feature_frame, text=icon, font=("Segoe UI", 16),
                    bg=Colors.PRIMARY, fg=Colors.WHITE).pack(side=tk.LEFT)
            tk.Label(feature_frame, text=text, font=Fonts.NORMAL_BOLD,
                    bg=Colors.PRIMARY, fg=Colors.WHITE).pack(side=tk.LEFT, padx=(10, 0))
        right_frame = tk.Frame(main_container, bg=Colors.WHITE)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        scroll_container = tk.Frame(right_frame, bg=Colors.WHITE)
        scroll_container.pack(expand=True, fill=tk.BOTH, padx=60, pady=60)
        welcome_frame = tk.Frame(scroll_container, bg=Colors.WHITE)
        welcome_frame.pack(fill=tk.X, pady=(0, 30))
        tk.Label(welcome_frame, text="Welcome Back", font=Fonts.TITLE,
                bg=Colors.WHITE, fg=Colors.GRAY_800).pack(anchor=tk.W)
        tk.Label(welcome_frame, text="Sign in to continue your journey", 
                font=Fonts.NORMAL, bg=Colors.WHITE, fg=Colors.GRAY_500).pack(anchor=tk.W, pady=(5, 0))
        self.phone_entry = ModernEntry(scroll_container, "Phone Number", placeholder="+923XXXXXXXXX")
        self.phone_entry.pack(fill=tk.X, pady=(0, 20))
        role_label = tk.Label(scroll_container, text="Login As", font=Fonts.NORMAL,
                             bg=Colors.WHITE, fg=Colors.GRAY_600, anchor=tk.W)
        role_label.pack(anchor=tk.W, pady=(0, 5))
        self.role_dropdown = ModernDropdown(scroll_container, "", options=["Rider", "Driver", "Admin"], default="Rider")
        self.role_dropdown.pack(fill=tk.X, pady=(0, 25))
        demo_card = tk.Frame(scroll_container, bg=Colors.GRAY_50, relief=tk.FLAT)
        demo_card.pack(fill=tk.X, pady=(0, 25))
        tk.Label(demo_card, text="💡 Demo Accounts", font=Fonts.SMALL_BOLD,
                bg=Colors.GRAY_50, fg=Colors.GRAY_600).pack(anchor=tk.W, padx=15, pady=(10, 5))
        demo_text = """Rider: +923001234501\nDriver: +923011234501\nAdmin: +923021234501"""
        tk.Label(demo_card, text=demo_text, font=Fonts.SMALL,
                bg=Colors.GRAY_50, fg=Colors.GRAY_500, justify=tk.LEFT).pack(anchor=tk.W, padx=15, pady=(0, 10))
        login_btn = ModernButton(scroll_container, text="Sign In", command=self.login,
                                bg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_DARK, icon="→", width=350, height=45)
        login_btn.pack(pady=(0, 15))
        register_frame = tk.Frame(scroll_container, bg=Colors.WHITE)
        register_frame.pack()
        tk.Label(register_frame, text="New to FareShare? ", font=Fonts.NORMAL,
                bg=Colors.WHITE, fg=Colors.GRAY_600).pack(side=tk.LEFT)
        register_link = tk.Label(register_frame, text="Create Account", font=Fonts.NORMAL_BOLD,
                                 fg=Colors.PRIMARY, bg=Colors.WHITE, cursor="hand2")
        register_link.pack(side=tk.LEFT)
        register_link.bind("<Button-1>", lambda e: self.show_registration())
    
    def login(self):
        phone = self.phone_entry.get().strip()
        role = self.role_dropdown.get()
        if not phone:
            self.show_toast("Please enter phone number", "warning")
            return
        result = self.db.login_user(phone, role)
        if result['success']:
            self.current_user = result['user']
            self.show_toast(f"Welcome back, {self.current_user['full_name']}!", "success")
            self.show_dashboard()
        else:
            self.show_toast("Invalid phone number or role mismatch", "error")
    
    def show_registration(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Create Account - FareShare")
        reg_window.geometry("600x700")
        reg_window.configure(bg=Colors.WHITE)
        reg_window.transient(self.root)
        reg_window.grab_set()
        
        reg_window.update_idletasks()
        x = (reg_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (reg_window.winfo_screenheight() // 2) - (700 // 2)
        reg_window.geometry(f"+{x}+{y}")
        
        header = tk.Frame(reg_window, bg=Colors.PRIMARY, height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Create Account", font=Fonts.HEADING,
                bg=Colors.PRIMARY, fg=Colors.WHITE).pack(pady=(25, 5))
        tk.Label(header, text="Join FareShare and start saving", font=Fonts.NORMAL,
                bg=Colors.PRIMARY, fg=Colors.PRIMARY_LIGHT).pack()
        
        scroll_canvas = tk.Canvas(reg_window, bg=Colors.WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(reg_window, orient="vertical", command=scroll_canvas.yview)
        scrollable_frame = tk.Frame(scroll_canvas, bg=Colors.WHITE)
        
        scrollable_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))
        scroll_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        
        scroll_canvas.pack(side="left", fill="both", expand=True, padx=30, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        form = scrollable_frame
        
        role_card = tk.Frame(form, bg=Colors.GRAY_50, relief=tk.FLAT)
        role_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(role_card, text="I want to join as", font=Fonts.NORMAL_BOLD,
                bg=Colors.GRAY_50, fg=Colors.GRAY_700).pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        reg_role_var = tk.StringVar(value="Rider")
        role_frame = tk.Frame(role_card, bg=Colors.GRAY_50)
        role_frame.pack(padx=15, pady=(0, 10))
        
        def on_role_change():
            if reg_role_var.get() == "Driver":
                driver_fields.pack(fill=tk.X, pady=(10, 0))
            else:
                driver_fields.pack_forget()
        
        rider_btn = tk.Radiobutton(role_frame, text="🚗 Rider", variable=reg_role_var,
                                   value="Rider", bg=Colors.GRAY_50, font=Fonts.NORMAL,
                                   selectcolor=Colors.GRAY_50, command=on_role_change)
        rider_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        driver_btn = tk.Radiobutton(role_frame, text="🚙 Driver", variable=reg_role_var,
                                    value="Driver", bg=Colors.GRAY_50, font=Fonts.NORMAL,
                                    selectcolor=Colors.GRAY_50, command=on_role_change)
        driver_btn.pack(side=tk.LEFT)
        
        name_entry = ModernEntry(form, "Full Name", placeholder="Enter your full name")
        name_entry.pack(fill=tk.X, pady=(0, 15))
        
        phone_entry = ModernEntry(form, "Phone Number", placeholder="+923XXXXXXXXX")
        phone_entry.pack(fill=tk.X, pady=(0, 15))
        
        driver_fields = tk.Frame(form, bg=Colors.WHITE)
        
        driver_info_card = tk.Frame(driver_fields, bg=Colors.GRAY_50, relief=tk.FLAT)
        driver_info_card.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(driver_info_card, text="Driver Information", font=Fonts.NORMAL_BOLD,
                bg=Colors.GRAY_50, fg=Colors.GRAY_700).pack(anchor=tk.W, padx=15, pady=(10, 5))
        tk.Label(driver_info_card, text="Please have your documents ready", font=Fonts.SMALL,
                bg=Colors.GRAY_50, fg=Colors.GRAY_500).pack(anchor=tk.W, padx=15, pady=(0, 10))
        
        cnic_entry = ModernEntry(driver_fields, "CNIC Number", placeholder="xxxxx-xxxxxxx-x")
        cnic_entry.pack(fill=tk.X, pady=(0, 10))
        license_entry = ModernEntry(driver_fields, "License Number", placeholder="Enter license number")
        license_entry.pack(fill=tk.X, pady=(0, 10))
        
        vehicle_info_card = tk.Frame(driver_fields, bg=Colors.GRAY_50, relief=tk.FLAT)
        vehicle_info_card.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(vehicle_info_card, text="Vehicle Information", font=Fonts.NORMAL_BOLD,
                bg=Colors.GRAY_50, fg=Colors.GRAY_700).pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        vehicle_id_entry = ModernEntry(driver_fields, "Vehicle ID", placeholder="Unique vehicle identifier")
        vehicle_id_entry.pack(fill=tk.X, pady=(0, 10))
        plate_entry = ModernEntry(driver_fields, "Plate Number", placeholder="ABC-123")
        plate_entry.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(driver_fields, text="Vehicle Type", font=Fonts.NORMAL,
                bg=Colors.WHITE, fg=Colors.GRAY_600).pack(anchor=tk.W, pady=(0, 5))
        
        vehicle_type_var = tk.StringVar(value="Sedan")
        vtype_frame = tk.Frame(driver_fields, bg=Colors.WHITE)
        vtype_frame.pack(fill=tk.X, pady=(0, 10))
        
        vehicle_types = [("🏍️ Bike", "Bike"), ("🛺 Rickshaw", "Rickshaw"),
                        ("🚗 Mini", "Mini"), ("🚙 Sedan", "Sedan")]
        
        for display, value in vehicle_types:
            rb = tk.Radiobutton(vtype_frame, text=display, variable=vehicle_type_var,
                               value=value, bg=Colors.WHITE, font=Fonts.SMALL,
                               selectcolor=Colors.WHITE)
            rb.pack(side=tk.LEFT, padx=(0, 15))
        
        model_entry = ModernEntry(driver_fields, "Vehicle Model", placeholder="e.g., Toyota Corolla 2020")
        model_entry.pack(fill=tk.X, pady=(0, 10))
        
        terms_var = tk.BooleanVar(value=False)
        terms_frame = tk.Frame(form, bg=Colors.WHITE)
        terms_frame.pack(fill=tk.X, pady=(20, 10))
        
        terms_cb = tk.Checkbutton(terms_frame, variable=terms_var, bg=Colors.WHITE,
                                  font=Fonts.SMALL, selectcolor=Colors.WHITE)
        terms_cb.pack(side=tk.LEFT)
        
        terms_label = tk.Label(terms_frame,
                              text="I agree to the Terms of Service and Privacy Policy",
                              font=Fonts.SMALL, bg=Colors.WHITE, fg=Colors.GRAY_600,
                              cursor="hand2")
        terms_label.pack(side=tk.LEFT, padx=(5, 0))
        
        def do_register():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            role = reg_role_var.get()
            
            if not name or not phone:
                self.show_toast("Please fill all required fields", "warning")
                return
            
            if not terms_var.get():
                self.show_toast("Please accept the Terms of Service", "warning")
                return
            
            if self.db.check_phone_exists(phone):
                self.show_toast("Phone number already registered", "error")
                return
            
            if role == "Rider":
                result = self.db.register_rider(phone, name)
            else:
                cnic = cnic_entry.get().strip()
                license_num = license_entry.get().strip()
                vehicle_id = vehicle_id_entry.get().strip()
                plate = plate_entry.get().strip()
                vehicle_type = vehicle_type_var.get()
                model = model_entry.get().strip()
                
                if not all([cnic, license_num, vehicle_id, plate]):
                    self.show_toast("Please fill all driver fields", "warning")
                    return
                
                result = self.db.register_driver(phone, name, cnic, license_num,
                                                vehicle_id, plate, vehicle_type, model)
            
            if result['success']:
                self.show_toast("Registration successful! Please login.", "success")
                reg_window.destroy()
            else:
                self.show_toast(result['message'], "error")
        
        create_btn = ModernButton(form, text="Create Account", command=do_register,
                                 bg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_DARK,
                                 icon="✨", width=300, height=45)
        create_btn.pack(pady=20)
        
        back_btn = tk.Button(form, text="← Back to Login", command=reg_window.destroy,
                            bg=Colors.WHITE, fg=Colors.GRAY_500, font=Fonts.NORMAL,
                            relief=tk.FLAT, cursor="hand2")
        back_btn.pack(pady=(0, 10))
        
        tk.Frame(form, height=20, bg=Colors.WHITE).pack()
    
    def show_dashboard(self):
        role = self.current_user['user_role']
        if role == "Rider":
            RiderDashboard(self.root, self.db, self.current_user, self.logout)
        elif role == "Driver":
            DriverDashboard(self.root, self.db, self.current_user, self.logout)
        elif role == "Admin":
            AdminDashboard(self.root, self.db, self.current_user, self.logout)
    
    def logout(self):
        self.current_user = None
        self.setup_login_ui()
        self.show_toast("Logged out successfully", "info")
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    print("=" * 60)
    print("FareShare Ride-Sharing System")
    print("   Complete Application with Ride Requests")
    print("   Database Systems Project - Milestone 3")
    print("   Namal University, Mianwali")
    print("=" * 60)
    print("\nFeatures:")
    print("  - Rider sends ride request to selected driver")
    print("  - Driver receives popup notification (5-10 sec delay for demo)")
    print("  - Driver can accept or decline the request")
    print("  - Ride animation with ETA and distance tracking")
    print("  - Emergency SOS alerts")
    print("  - Rating system for completed rides")
    print("  - Admin dashboard for driver verification")
    print("=" * 60)
    print("\nDemo Instructions:")
    print("1. Login as Rider (+923001234501)")
    print("2. Select a driver and book a ride")
    print("3. Login as Driver (+923011234501) in another window")
    print("4. Driver must be ONLINE to receive requests")
    print("5. Driver can simulate requests or wait for real ones")
    print("=" * 60)
    
    app = FareShareApp()
    app.run()