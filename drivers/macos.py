import Quartz
def mover_mouse(dx, dy):
  
    current = Quartz.CGEventGetLocation(
        Quartz.CGEventCreate(None)
    )
    new_x = current.x + dx
    new_y = current.y + dy
    event = Quartz.CGEventCreateMouseEvent(
        None,
        Quartz.kCGEventMouseMoved,
        (new_x, new_y),
        Quartz.kCGMouseButtonLeft
    )
    Quartz.CGEventPost(
        Quartz.kCGHIDEventTap,
        event
    )