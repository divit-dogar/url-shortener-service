from app.events.click_event import ClickEvent
from app.events.observer import ClickObserver


class ClickEventPublisher:
    
    # Publishes click events to registered observers.

    def __init__(self):
        self._observers: list[ClickObserver] = []

    def subscribe(self, observer: ClickObserver) -> None:
        
        # Register an observer.
        
        self._observers.append(observer)

    def unsubscribe(self, observer: ClickObserver) -> None:
        
        # Remove an observer.
        
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: ClickEvent) -> None:
        
        # Notify all registered observers.
        
        for observer in self._observers:
            observer.update(event)