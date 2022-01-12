package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"time"

	"github.com/gen2brain/beeep"

	"github.com/luisnquin/vert-cli/src/tasker/interfaces"
)

var (
	current_minute string
)

func main() {
	file, err := ioutil.ReadFile("./config.json")
	if err != nil {
		panic(err)
	}
	c := &interfaces.Config{}
	json.Unmarshal(file, &c)

	// Minutes are used to safeguard performance
	for {
		time.Sleep(time.Minute)
		current := time.Now()
		current_minute = fmt.Sprintf("%v:%v:00", current.Hour(), current.Minute())
		for _, n := range c.Notifier {
			if n.Hour == current_minute {
				err := beeep.Notify(n.Title, n.Message, "./assets/command-line.png")
				if err != nil {
					panic(err)
				}
				fmt.Println("Coincidence")
			}
		}
	}
}
