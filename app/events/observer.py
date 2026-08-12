from abc import ABC, abstractmethod

from app.events.click_event import ClickEvent


class ClickObserver(ABC):
    
    # Observer interface for URL click events.
    
    @abstractmethod
    def update(self, event: ClickEvent) -> None:
        
        # Handle a click event.
        
        pass