package interfaces

import "time"

type Notifier struct {
	Id      uint      
	Title   string    
	Message string    
	Hour    time.Time 
}

type Notifications []Notifier
