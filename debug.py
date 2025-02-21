def send_can_message(button_index):
    """Send a CAN message with the button index."""
    try:
        print(f"Opening CAN interface: {CAN_INTERFACE}")  # Debugging

        bus = can.interface.Bus(CAN_INTERFACE, bustype="socketcan")
        message = can.Message(arbitration_id=0x123, data=[button_index, 0xAA, 0xBB], is_extended_id=False)

        print(f"Sending CAN Message: {message}")  # Debugging
        bus.send(message)
        
        print(f"Message Sent Successfully!")
        display_message(f"Button {button_index} Sent")

    except Exception as e:
        print(f"CAN Error: {e}")
