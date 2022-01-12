package interfaces

type NotifierConfig struct {
	Id      uint   `json:"id"`
	Title   string `json:"title"`
	Message string `json:"message"`
	Hour    string `json:"hour"`
}

type Config struct {
	Path     string           `json:"path"`
	Database string           `json:"database"`
	User     string           `json:"user"`
	Password string           `json:"password"`
	Host     string           `json:"localhost"`
	Notifier []NotifierConfig `json:"notifier"`
}